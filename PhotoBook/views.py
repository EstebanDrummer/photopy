from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from PhotoBook.models import Album, Foto

def nuevo_usuario(request):
	if request.method=='POST':
		formulario=UserCreationForm(request.POST)
		if formulario.is_valid:
			formulario.save()
			return HttpResponseRedirect('/ingresar')
	else:
		formulario = UserCreationForm()
	return render_to_response('nuevousuario.html', {'formulario': formulario}, context_instance=RequestContext(request))

def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/privado')
	if request.method=='POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/privado')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html', {'formulario': formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def privado(request):
	usuario = request.user
	listaUsuarios = User.objects.all()
	return render_to_response('privado.html',{'usuario':usuario, 'listaUsuarios':listaUsuarios}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def listaAlbum(request, var):
	usuario = User.objects.get(username=var)
	usuarioProp = request.user
	pk = usuario.id
	nombre = usuario.username
	listaAlbum = Album.objects.filter(usuario_id=pk)
	return render_to_response('listaAlbum.html',{'nombreDuenio':nombre, 'usuario':usuarioProp, 'listaAlbum':listaAlbum}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def listaFoto(request, var):
	album = Album.objects.get(nombre=var)
	nombreAlbum=var
	usuarioProp = request.user
	duenio = User.objects.get(id=album.usuario_id)
	nombre = duenio.username
	pk = album.id
	if request.user.has_perm('can_view_all') or (request.user.id==album.usuario_id):
		listaFotos=Foto.objects.filter(album_id=pk)
	else:
		listaFotos=Foto.objects.filter(album_id=pk,es_publica='1')	
	return render_to_response('listaFotos.html',{'usuario':usuarioProp, 'nombreDuenio':nombre,'listaFotos':listaFotos, 'nombreAlbum':nombreAlbum}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def fotoInfo(request, var):
	foto=Foto.objects.get(nombre=var)
	album_id= foto.album_id
	album = Album.objects.get(id=album_id)
	duenio = User.objects.get(id=album.usuario_id)
	usuarioProp = request.user
	pk = album.id
	if (request.user.has_perm('can_view_all') or (request.user.id==album.usuario_id)) or (foto.es_publica==1):
		fotoInfo=Foto.objects.get(id=foto.id)
	else:
		return HttpResponseRedirect('/ingresar')	
	return render_to_response('FotoInfo.html',{'usuario':usuarioProp, 'fotoInfo':fotoInfo, 'album':album, 'duenio':duenio}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/ingresar')	