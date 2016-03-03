#!/usr/bin/env python

from django.contrib.auth.models import AnonymousUser

from notifications import views


########################################
# List
########################################

def test_list_pass_admin(rf, admin_user):
    '''
    Fixtures: (by pytest-django)

    * rf: RequestFactory
    * admin_user: Admin User

    '''

    request = rf.get('/')
    request.user = admin_user
    response = views.list(request)
    assert response.status_code == 200


def test_list_pass_user(rf):
    pass


def test_list_deny_anonymous(rf):
    request = rf.get('/')
    request.user = AnonymousUser()
    response = views.list(request)
    assert response.status_code == 302


def test_list_deny_user(rf):
    pass


########################################
# Create
########################################


def test_create_pass_admin(rf):
    pass


def test_create_pass_user(rf):
    pass


def test_create_deny_anonymous(rf):
    pass


def test_create_deny_user(rf):
    pass
