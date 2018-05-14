from django.shortcuts import redirect, render
from django.http import HttpResponse

from lists.models import Item, List


## data-representation-view should use a template to render response
def home_page(request):
    return render(request, 'lists/home.html')

## data-representation-view should use a template to render response
def list_page(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})

## date-manipulation-view should bascilly do two things:
## 1) save data into database
## 2) redirect to a data-representation-view
def create_new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
