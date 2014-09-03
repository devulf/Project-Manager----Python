from django import template
register = template.Library()

@register.filter(name='ownership')
def ownership(project, user):
    return project.user== user

@register.filter(name='ownership')
def ownership(ticket, user):
    return ticket.user== user
