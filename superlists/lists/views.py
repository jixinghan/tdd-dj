from django.shortcuts import redirect, render
from django.http import HttpResponse

from lists.models import Item, List


## data-representation-view should use a template to render response
def home_page(request):
    return render(request, 'lists/home.html')

## data-representation-view should use a template to render response
def list_page(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'lists/list.html', {'list': list_})

## date-manipulation-view should bascilly do two things:
## 1) save data into database
## 2) redirect to a data-representation-view
def create_new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

## date-manipulation-view should bascilly do two things:
## 1) save data into database
## 2) redirect to a data-representation-view
def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
