from django.shortcuts import render_to_response, get_object_or_404

from fruitynutters.catalogue.models import Aisle

def aisle(request, aisle_id):
    """Aisle view"""
    return render_to_response('aisle.html', locals())
    
def aisle_index(request):
    aisle_list = Aisle.objects.all()
    return render_to_response('aisle_index.html', locals())