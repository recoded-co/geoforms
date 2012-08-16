from bs4 import BeautifulSoup
from django.shortcuts import render_to_response
from geoforms.models import Geoform
from geoforms.models import Questionnaire
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def questionnaire(request, questionnaire_slug):
    """
    This view creates the whole questionnaire html.
    """
    
    quest = Questionnaire.on_site.select_related().get(slug = questionnaire_slug)
    form_list = quest.geoforms.all().order_by('questionnaireform__order')
    elements = {}
    popup_set = set()
    for form in form_list:
        popup_elements = form.elements.filter(element_type = 'drawbutton').values_list('html', flat=True)
        for e in popup_elements:
            soup = BeautifulSoup(e)
            popup_set.add(soup.button['data-popup'])
            
        elements[form.slug] = form.elements.order_by('formelement__order', '?')
        
    popup_list = Geoform.objects.filter(type = 'popup').filter(name__in = popup_set)
    form_list = form_list.filter(type = 'form')
    
    return render_to_response('questionnaire.html',
                             {'form_list': form_list,
                              'popup_list': popup_list,
                              'elements': elements,
                              'questionnaire': quest,
                              'map_slug': 'questionnaire-map'},
                             context_instance = RequestContext(request))
