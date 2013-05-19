"""
{{ PROJECT_NAME }}.context_processors
-------------------------------------
"""

from django.conf import settings
from django.contrib.sites.models import Site


def domain(request):
    current_site = Site.objects.get_current()
    domain = getattr(settings, 'DOMAIN', 'http://%s' % current_site.domain)
    return {
        'DOMAIN': domain,
        'site': current_site,
    }
