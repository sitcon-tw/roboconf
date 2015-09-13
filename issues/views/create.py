from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from issues.models import Issue, IssueHistory, Label
from issues.utils import send_mail, parse_date
from users.mentions import filter_mentions
from users.utils import sorted_users

@permission_required('issues.add_issue')
def create(request):
    errors = []

    if 'submit' in request.POST:
        issue = Issue()
        issue.title = request.POST['title']
        issue.content = request.POST['content']
        issue.creator = request.user

        due_time = request.POST.get('due_time', '').strip()
        if len(due_time):
            try:
                due_time = parse_date(due_time)
                if due_time:
                    issue.due_time = due_time
                else:
                    errors.append('date-misformed')
            except ValueError:
                errors.append('date-invalid')

        assignee = request.POST.get('assignee')
        if assignee:    # Empty value => not assigned, no need to set
            try:
                issue.assignee = User.objects.get(id=assignee)
            except User.DoesNotExist:
                assignee = None        # Just in case we're under attack...

        labels = []
        for label_id in request.POST.getlist('labels'):
            try:
                labels.append(Label.objects.get(id=label_id))
            except Label.DoesNotExist: pass

        if not errors:
            issue.save()    # Need to save before we can enforce N to N relationship
            issue.starring.add(request.user)    # Auto watch

            # Add or remove labels has history so we don't worry on history creation
            issue.labels.add(*labels)

            mentions, _ = filter_mentions(issue.content)
            if assignee:
                mentions.add(issue.assignee)
            mentions.discard(request.user)

            for user in mentions:
                issue.starring.add(user)    # Auto watch
                send_mail(request.user, user, 'mail/issue_created.html', { 'issue': issue })

            # Broadcast new issues automatically
            send_mail(request.user, settings.BROADCAST_EMAIL, 'mail/issue_created.html', { 'issue': issue })

            if assignee:
                IssueHistory.objects.create(issue=issue, user=request.user,
                                            mode=IssueHistory.ASSIGN, content=assignee)

            if due_time:
                IssueHistory.objects.create(issue=issue, user=request.user,
                                            mode=IssueHistory.SET_DUE, content=due_time)

            return redirect('issues:detail', issue.id)

    return render(request, 'issues/create.html', {
        'labels': Label.objects.all(),
        'users': sorted_users(User.objects.filter(is_active=True)),
        'errors': errors,
    })
