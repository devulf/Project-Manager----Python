from django.db import models
import datetime
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms.fields import DateField

class Project(models.Model):
  project_user = models.ManyToManyField(User, related_name = 'project_user')
  user = models.ForeignKey(User)
  name = models.CharField(max_length = 40)
  description = models.CharField(max_length = 100)
  start_date = models.DateTimeField('Start date')
  end_date = models.DateTimeField('End date')
  def __unicode__(self):
    return self.name
  def owner_by_user(self, user):
    return self.user == user

  class Meta:
    permissions = (
      ("can_add_projects", "Can add projects"),
      )

class Status(models.Model):
  status_name = models.CharField(max_length = 40)
  def __unicode__(self):
    return self.status_name

class Ticket(models.Model):
  user = models.ForeignKey(User)
  project = models.ForeignKey(Project)
  status = models.ForeignKey(Status)
  name = models.CharField(max_length = 40)
  description = models.CharField(max_length = 100)
  def __unicode__(self):
    return self.user
  def owner_by_user(self, user):
    return self.user == user

  class Meta:
    permissions = (
      ("can_add_tickets", "Can add tickets"),
      )

class TicketForm(ModelForm):
  class Meta:
    model = Ticket
    exclude = ('user', 'project')



class ProjectForm(ModelForm):
  class Meta:
    model = Project
    exclude = ('user')



