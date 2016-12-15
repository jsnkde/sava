from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
import re

from django.urls import reverse
from django.db.models import Q
from django.db.models.aggregates import Count
from allauth.account.adapter import DefaultAccountAdapter
from taggit.models import Tag

from catalog.models import Location, User, Item


class IndexView(generic.ListView):
	template_name = 'catalog/index.html'
	context_object_name = 'items'

	def get_location(self, request):
		# Extract preserved location for authenticated users
		if not request.user.is_anonymous and request.user.location is not None:
			self.location = request.user.location

		# Check session
		elif request.session.has_key('location'):
			self.location = Location.objects.get(id=int(request.session['location']))

		# Default location
		else:
			self.location = Location.objects.get(id=1) # TODO

	def get_queryset(self):
		self.get_location(self.request)
		
		items = Item.objects.filter(user__location=self.location)

		if self.request.GET.has_key('search') and len(self.request.GET['search']) > 0:
			search = map(unicode.lower, re.findall(r'(\w+)', self.request.GET['search'], re.UNICODE))
			items = items.filter(Q(tags__name__in=search) | Q(reduce(lambda x, y: x | y, [Q(description__icontains=word) for word in search]))).distinct()

		return items

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['locations'] = Location.objects.all()
		context['location'] = self.location
		context['tags'] = Tag.objects.filter(item__user__location=self.location).annotate(count=Count('item')).order_by('-count')

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