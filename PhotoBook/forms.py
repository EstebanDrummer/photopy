from django.forms import ModelForm
from django import forms
from PhotoBook.models import Foto, Album
from django.contrib.auth.models import User

class AlbumForm (forms.Form):
	##nombre = models.CharField(max_length=200)
	##usuario = models.ForeignKey(User)
	class Meta:
		model = Album