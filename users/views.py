from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login(request):
	if request.user.is_authenticated():
		return redirect(reverse('index'))

	context = {}
	if 'submit' in request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				
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
	logout(request)
	return redirect(reverse('users:login'))
