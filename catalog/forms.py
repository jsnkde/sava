# -*- coding: utf-8 -*-

import re

from django import forms
from django.core.validators import RegexValidator
from catalog.models import Item


class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['description', 'comment', 'tags']

	comment = forms.CharField(widget=forms.Textarea, required = False)
	phone = forms.CharField(min_length=10, max_length=25, required = False)

	def clean_phone(self):
		phone = self.cleaned_data['phone']

		if len(phone) == 0:
			return phone
			
		pattern = re.compile("^(?:\+7|8|)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)$")
		r = pattern.match(phone)

		if r is None:
			raise forms.ValidationError(u'Введите телефон в формате +7 (999) 999 99 99')

		return reduce(lambda x, y: x + y, r.groups())


def tag_splitter(tag_string):
	return map(unicode.lower, re.findall('\w+', tag_string, re.UNICODE))

