# -*- coding: utf-8 -*-

import re

from django import forms
from django.forms.models import inlineformset_factory
from django.core.validators import RegexValidator
from catalog.models import Item, Image


class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['description', 'comment', 'tags']

	description = forms.CharField(max_length=100, required=False)
	comment = forms.CharField(widget=forms.Textarea, required = False, max_length=1000)
	phone = forms.CharField(max_length=25, required = False, widget=forms.TextInput(attrs={'placeholder': '+7 (999) 999 99 99'}))

	def clean_description(self):
		description = self.cleaned_data['description']
		if len(description) == 0:
			raise forms.ValidationError(u'Не забудьте заполнить это поле')

		return description

	def clean_phone(self):
		phone = self.cleaned_data['phone']

		if len(phone) == 0:
			return phone
			
		pattern = re.compile("^(?:\+7|8|)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)$")
		r = pattern.match(phone)

		if r is None:
			raise forms.ValidationError(u'Не удается распознать номер, попробуйте так: 8 999 999 99 99')

		return reduce(lambda x, y: x + y, r.groups())

class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ['img',]


ImageFormset = inlineformset_factory(Item, Image, max_num=5, extra=5, form=ImageForm)


def tag_splitter(tag_string):
	return map(unicode.lower, re.findall('\w+', tag_string, re.UNICODE))


