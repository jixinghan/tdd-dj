from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item, List
from lists.forms import ItemForm


## data-representation-view should use a template to render response
def home_page(request):
    return render(request, 'lists/home.html', {'form': ItemForm()})


## data-representation-view should use a template to render response
#def list_page(request, list_id):
#    list_ = List.objects.get(id=list_id)
#
#    if request.method == 'POST':
#        item = Item(text=request.POST['text'], list=list_)
#        try: 
#            item.full_clean()
#        except ValidationError:
#            error = "You can't have an empty list item"
#            return render(
#                request,
#                'lists/list.html',
#                {'list': list_, 'error': error}
#            )
#        else:
#            item.save()
#            return redirect(list_)

def list_page(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)
    return render(request, 'lists/list.html', {'list': list_, 'form': form })


## date-manipulation-view should bascilly do two things:
## 1) save data into database
## 2) redirect to a data-representation-view
## 3) do some validations
#def create_new_list(request):
#    list_ = List.objects.create()
#    item = Item.objects.create(text=request.POST['text'], list=list_)
#    try:
#        # Generally, when you save a model object, django will receive
#        # database level validation errors if exist. But some databases
#        # don't actually support some validation. (e.g. sqlite)
#        # So, full_clean is used to enforce database level validation
#        # even if just has created a model object, not yet saved it
#        item.full_clean()
#    except ValidationError:
#        # This will also automaticly delete item, because of cascade-deleting
#        list_.delete()
#        error = "You can't have an empty list item"
#        return render(request, 'lists/home.html', {'error': error})
#    #return redirect(f'/lists/{list_.id}/')
#    return redirect(list_)  # List has implemented get_abosolute_url
def create_new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'lists/home.html', {'form': form})
