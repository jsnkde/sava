# -*- coding: utf-8 -*-

import re

from django import forms
from django.core.validators import RegexValidator
from catalog.models import Item


alphanumeric = RegexValidator(r'^[0-9]{10}$', u'Неверный формат')


class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['description', 'comment', 'tags']

	comment = forms.CharField(widget=forms.Textarea, required = False)
	phone = forms.CharField(min_length=10, max_length=10, required = False, validators=[alphanumeric])


def tag_splitter(tag_string):
	return map(unicode.lower, re.findall('\w+', tag_string, re.UNICODE))

