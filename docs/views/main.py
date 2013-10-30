from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

@login_required
def main(request):
	return render(request, 'docs_main.html', {})
