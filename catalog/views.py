from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from catalog.models import Location, User


class IndexView(generic.TemplateView):
	template_name = 'catalog/index.html'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['locations'] = Location.objects.all()

		# Extract preserved location for authenticated users
		if not self.request.user.is_anonymous and self.request.user.location is not None:
			context['location'] = self.request.user.location

		# Check session
		elif self.request.session.has_key('location'):
			context['location'] = Location.objects.get(id=int(self.request.session['location']))

		# Default location
		else:
			context['location'] = Location.objects.get(id=1) # TODO

		return context

	def post(self, request, *args, **kwargs):
		if request.POST.has_key('location'):
			if request.user.is_authenticated():
				request.user.location = Location.objects.get(id=request.POST['location'])
				request.user.save()

			else:
				request.session['location'] = request.POST['location']


		return HttpResponseRedirect(request.path)


class SocialAccountAdapter(DefaultAccountAdapter):
	def get_login_redirect_url(self, request):
		return reverse('index')