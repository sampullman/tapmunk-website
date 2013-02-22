from django.core.context_processors import csrf
from django.shortcuts import render_to_response


def crsf_render(request, url):
    c = {}
    c.update(csrf(request))
    return render_to_response(url, c)

def cashground(request):
    return crsf_render(request, 'cashground.html');
