from django.shortcuts import render_to_response, get_object_or_404

from fruitynutters.catalogue.models import Aisle, Item

def aisle(request, aisle_id):
    """Aisle view"""
    aisle = Aisle.objects.get(id__exact=aisle_id)
    aisle_items = Item.objects.filter(aisle__exact=aisle_id).filter(active=True).order_by('name')
    return render_to_response('aisle.html', locals())
    
def aisle_index(request):
    aisle_list = Aisle.objects.all()
    return render_to_response('aisle_index.html', locals())