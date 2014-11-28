from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Album(models.Model):
	nombre = models.CharField(max_length=200)
	usuario = models.ForeignKey(User)

	def __unicode__(self):
		return self.nombre

	def __str__(self):
		return self.nombre

class Foto(models.Model):
	nombre = models.CharField(max_length=200)
	fuente = models.ImageField(upload_to="imagenes/fotos/")
	album = models.ForeignKey(Album)
	slug = models.SlugField(max_length=40)
	es_publica = models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombre

	def __str__(self):
		return self.nombre

	class Meta:
		permissions = (
			("can_view_all", "puede ver todo"),
			("can_view", "puede ver"),)
	
