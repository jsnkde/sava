from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from catalog.models import Location, User, Item
from taggit.models import Tag
from django.db.models.aggregates import Count


class IndexView(generic.ListView):
	template_name = 'catalog/index.html'
	context_object_name = 'items'

	def get_queryset(self):
		print self.request.GET.getlist('tag')
		# Extract preserved location for authenticated users
		if not self.request.user.is_anonymous and self.request.user.location is not None:
			self.location = self.request.user.location

		# Check session
		elif self.request.session.has_key('location'):
			self.location = Location.objects.get(id=int(self.request.session['location']))

		# Default location
		else:
			self.location = Location.objects.get(id=1) # TODO

		items = Item.objects.filter(user__location=self.location)

		if self.request.GET.has_key('tag'):
			items = items.filter(tags__name__in=self.request.GET.getlist('tag'))

		return items

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['locations'] = Location.objects.all()
		context['location'] = self.location
		context['tags'] = Tag.objects.filter(item__user__location=self.location).annotate(count=Count('item')).order_by('-count')

		# If DB sorting is not working properly try
		# sorted(Location.objects.all(), key=operator.attrgetter('region','name'))

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