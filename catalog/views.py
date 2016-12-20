from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.views import generic, View
import re

from django.urls import reverse
from django.db.models import Q, Case, When, IntegerField
from django.db.models.aggregates import Count
from allauth.account.adapter import DefaultAccountAdapter
from taggit.models import Tag

from catalog.models import Location, User, Item
from catalog.forms import ItemForm


class NavbarMixin(object):
	def dispatch(self, request, *args, **kwargs):
		# Extract preserved location for authenticated users
		if not request.user.is_anonymous:
			if request.user.location is None:				
				request.user.location = Location.objects.get(id=1) # TODO
				request.user.save()

			self.location = request.user.location

		# Check session
		elif request.session.has_key('location'):
			self.location = Location.objects.get(id=int(request.session['location']))

		# Default location
		else:
			self.location = Location.objects.get(id=1) # TODO

		return super(NavbarMixin, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		return super(NavbarMixin, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(NavbarMixin, self).get_context_data(**kwargs)
		context['locations'] = Location.objects.all()
		context['location'] = self.location

		return context

	def post(self, request, *args, **kwargs):
		if request.POST.has_key('location'):
			if request.user.is_authenticated():
				request.user.location = Location.objects.get(id=request.POST['location'])
				request.user.save()

			else:
				request.session['location'] = request.POST['location']

			return HttpResponseRedirect(request.path)

		else:
			return super(NavbarMixin, self).post(request, *args, **kwargs)


class IndexView(NavbarMixin, generic.ListView):
	template_name = 'catalog/index.html'
	context_object_name = 'items'
	paginate_by = 5
	my = False

	def get_queryset(self):
		items = Item.objects.filter(user__location=self.location).filter(active=True)

		# Filter by user if necessary
		if self.my and self.request.user.is_authenticated():
			items = items.filter(user=self.request.user)

		# Find items with description or tags containing any word from the search string
		if self.request.GET.has_key('search') and len(self.request.GET['search']) > 0:
			search = map(unicode.lower, re.findall(r'(\w+)', self.request.GET['search'], re.UNICODE))
			items = items.filter(Q(tags__name__in=search) | Q(reduce(lambda x, y: x | y, [Q(description__icontains=word) for word in search]))).distinct()

		return items.order_by('-updated')

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['tags'] = Tag.objects.all().annotate(count=Count(Case(When(item__active=True, item__user__location=self.location, then=1), output_field=IntegerField(),))).order_by('-count').filter(count__gt=0)[:20]

		# Pass search GET parameters for proper pagination
		if self.request.GET.has_key('search') and len(self.request.GET['search']) > 0:
			context['search'] = "?search=" + self.request.GET['search']

		return context


class ItemView(NavbarMixin, generic.DetailView):
	model = Item
	context_object_name = 'item'
	template_name = 'catalog/item.html'


class PhoneFormatMixin(object):
	def get_initial(self):
		init = {}

		if self.request.user.phone and len(self.request.user.phone) > 0:
			init['phone'] = self.request.user.phone_formatted

		return init

class ItemCreateView(PhoneFormatMixin, NavbarMixin, generic.edit.CreateView):
	template_name = 'catalog/item_new.html'
	model = Item
	form_class = ItemForm

	def form_valid(self, form):
		item = form.save(commit=False)
		item.user = self.request.user

		if len(form.cleaned_data['phone']) > 0:
			self.request.user.phone = form.cleaned_data['phone']
			self.request.user.save()

		return super(ItemCreateView, self).form_valid(form)

	def get_success_url(self):
		return reverse('catalog:detail', kwargs={'pk': self.object.id})


class ItemUpdateView(PhoneFormatMixin, NavbarMixin, generic.edit.UpdateView):
	template_name = 'catalog/item_new.html'
	model = Item
	form_class = ItemForm
	done = False

	def get_object(self, *args, **kwargs):
		obj = super(ItemUpdateView, self).get_object(*args, **kwargs)
		if obj.user != self.request.user:
			raise PermissionDenied

		return obj

	def get(self, request, *args, **kwargs):
		self.obj = self.get_object()
		if self.done:
			self.obj.active = False
			self.obj.save()

			nxt = reverse('catalog:index') if not request.GET.has_key('next') else request.GET['next']

			return HttpResponseRedirect(nxt)

		return super(ItemUpdateView, self).get(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('catalog:detail', kwargs={'pk': self.object.id})

	def form_valid(self, form):
		if len(form.cleaned_data['phone']) > 0:
			self.request.user.phone = form.cleaned_data['phone']
			self.request.user.save()

		return super(ItemUpdateView, self).form_valid(form)


class SocialAccountAdapter(DefaultAccountAdapter):
	def get_login_redirect_url(self, request):
		return reverse('index')
