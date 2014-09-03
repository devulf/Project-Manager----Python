# Create your views here.
from django.conf.urls.defaults import patterns, include, url
from projects.models import Project, Ticket, User, Status, TicketForm, ProjectForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, render, redirect, get_list_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.template import loader, Context

def index(request):
  if request.user.is_authenticated():
    latest_project_list = Project.objects.all().order_by('start_date')[:15]
    return render_to_response('projects/index.html', {'latest_project_list':
    latest_project_list}, context_instance=RequestContext(request))
  else:
    return redirect(login_user)

def search(request):
  query = request.GET.get('q', '')
  if query != "":
    projects = Project.objects.filter(name__contains=query)
    return render(request, 'projects/results.html', {"projects" : projects})
    projects = []



def logout(request):
  auth_logout(request)
  request.flash['notice'] = 'Logged out!'
  return redirect(login_user)

def project_for_user(request):
  user = request.user
  projects = Projects.objects.filter(added_by_user = user)

def detail(request, project_id):
  if request.user.is_authenticated():
    project = get_object_or_404(Project, pk= project_id)
    users = project.project_user.all()
    return render_to_response('projects/detail.html', {'project' : project, 'users' : users },
    context_instance=RequestContext(request))
  else:
    return redirect(login_user)

def ticket_detail(request, ticket_id, project_id):
  if request.user.is_authenticated():
    project = get_object_or_404(Project, pk= project_id)
    ticket = get_object_or_404(Ticket, pk= ticket_id)
    return render_to_response('projects/ticket_detail.html', {'ticket' : ticket, 'project' : project},
    context_instance=RequestContext(request))
  else:
    return redirect(login_user)

def login_user(request):
  state = "Log in"
  username = password = ''
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        request.flash['notice'] = 'Logged in'
        return redirect(index)
    else:
      request.flash['warning'] = 'Wrong details'
  if request.user.is_authenticated():
    return redirect(index)

  return render_to_response('projects/auth.html',{'state':state, 'username': username},
  context_instance=RequestContext(request))

def project_add(request):
  if request.user.is_authenticated():
    if request.method == "POST":
      form = ProjectForm(request.POST)
      if form.is_valid():
        form.instance.user = request.user
        form.save()
        request.flash['notice'] = 'Project added'
        return redirect(index)
    else:
      form = ProjectForm()
  else:
    return redirect(login_user)

  return render(request, 'projects/add.html', {'form' : form})

def ticket_add(request, project_id):
  if request.user.is_authenticated():
    project = get_object_or_404(Project, pk= project_id)
    users = project.project_user.all()
    user = request.user
    if user in users or project.owner_by_user(user):
      if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
          form.instance.user = request.user
          project = get_object_or_404(Project, pk = project_id)
          form.instance.project = project
          form.save()
          request.flash['notice'] = 'Ticket added'
          return redirect('detail', project.id)
      else:
        form = TicketForm()
    else:
      request.flash['warning'] = 'You are not the owner of the project or an assigned user to the project!'
      return redirect('detail', ticket.id)
  else:
    return redirect(login_user)

  return render(request, 'projects/ticket_add.html', {'form' : form})


def delete(request, project_id):
  project = get_object_or_404(Project, pk = project_id)
  if project.owner_by_user(request.user):
    if request.method == "GET":
      project.delete()
      request.flash['notice'] = 'Project deleted'
      return redirect(index)
  else:
    request.flash['warning'] = 'You are not the owner of this project'
    return redirect('detail', project.id)

def ticket_delete(request, ticket_id, project_id):
  ticket = get_object_or_404(Ticket, pk = ticket_id)
  project = get_object_or_404(Project, pk = project_id)
  if ticket.owner_by_user(request.user):
    if request.method == "GET":
      project = get_object_or_404(Project, pk = project_id)
      ticket.delete()
      request.flash['notice'] = 'Ticket deleted'
      return redirect('detail', project.id)
  else:
    request.flash['warning'] = 'You are not the owner of this ticket'
    return redirect('ticket_detail', project.id, ticket.id)

def edit(request, project_id):
  if request.user.is_authenticated():
    project = get_object_or_404(Project, pk = project_id)
    if project.owner_by_user(request.user):
      if request.method == "POST":
        form = ProjectForm(request.POST, instance = project)
        if form.is_valid():
            form.save()
            request.flash['notice'] = 'Project edited'
            return redirect('detail', project.id)
      else:
        form = ProjectForm(instance = project)
      return render(request,  'projects/edit.html' , {"form" : form, "project" : project })
    else:
      request.flash['warning'] = 'You are not the owner of this project'
      return redirect('detail', project.id)
  else:
    return redirect(login_user)

def ticket_edit(request, ticket_id, project_id):
  if request.user.is_authenticated():
    ticket = get_object_or_404(Ticket, pk = ticket_id)
    project = get_object_or_404(Project, pk = project_id)
    if ticket.owner_by_user(request.user):
      if request.method == "POST":
        form = TicketForm(request.POST, instance = ticket)
        if form.is_valid():
          form.save()
          request.flash['notice'] = 'Ticket edited!'
          return redirect('ticket_detail', project.id, ticket.id)
      else:
        request.flash['notice'] = 'Ticket fel!'
        form = TicketForm(instance = ticket)
      return render(request,  'projects/ticket_edit.html' , {"form" : form, "ticket" : ticket })
    else:
      request.flash['warning'] = 'You are not the owner of this ticket'
      return redirect('ticket_detail', project.id, ticket.id)
  else:
    return redirect(login_user)
