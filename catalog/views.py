from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter


class BaseView(generic.TemplateView):
	template_name = 'catalog/base.html'


class SocialAccountAdapter(DefaultAccountAdapter):
	def get_login_redirect_url(self, request):
		return reverse('base')