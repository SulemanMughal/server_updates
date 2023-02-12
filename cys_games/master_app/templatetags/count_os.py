from django import template
from master_app.models import  *
from master_app.views import customPrint
register = template.Library()
@register.simple_tag
def count_os(os_type , *args, **kwargs):
    try:
        return VirtualNetwork.objects.filter(operating_system = os_type).count()
    except Exception as e:
        customPrint(e)
        return 0