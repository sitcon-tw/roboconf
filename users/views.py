from django.shortcuts import render, redirect
import django.contrib.auth

def login(request):
	if request.user.is_authenticated():
		return redirect(reverse('index'))

	context = {}
	if 'submit' in request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth.login(request, user)
				
				# Do redirection if provided
				url = request.POST.get('next')
				url = reverse('index') if (not url) or ('//' in url) else url
				return redirect(url)
			context['error'] = 'account_disabled'
		else:
			context['error'] = 'invalid_login'

	url = request.REQUEST.get('next')
	context['redirect_url'] = url
	return render(request, 'users_login.html', context)

def logout(request):
	auth.logout(request)
	return redirect(reverse('users:login'))
