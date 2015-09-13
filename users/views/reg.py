from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.utils import sorted_users, sorted_categories
from django.http import HttpResponse

def reg_list_token(request):
    pass

def reg_add_token(request):
    return render(request, 'users/reg_add_token.html', {
        'categories': sorted_categories,
    })

def reg_form(request):
    pass
