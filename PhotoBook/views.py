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
	pk = usuario.id
	listaAlbum = Album.objects.filter(usuario_id=pk)
	return render_to_response('listaAlbum.html',{'listaAlbum':listaAlbum}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/ingresar')	