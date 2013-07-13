"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse

class IssueViewTests(TestCase):
    def test_list_view_empty(self):
        response = self.client.get(reverse('issues:list'))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, 'No issues yet')
        self.assertQuerysetEqual(response.context['issues'], [])

    def test_create_issue_view(self):
        response = self.client.get(reverse('issues:create'))
        self.assertEqual(response.status_code, 200)
