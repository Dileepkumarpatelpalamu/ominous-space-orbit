from django import template
register = template.Library()
@register.filter(name='getformat')
def getformat(value):
	return "%s"%(float(value))+"%"