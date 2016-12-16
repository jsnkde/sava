from django import forms
from catalog.models import Item

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['description', 'comment', 'tags']
