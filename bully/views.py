from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import amazon_scrape
# Create your views here.



def index(request):
    if request.method =='POST':
        item = request.POST['item']
        url = amazon_scrape.search_amazon(item)
        list_of_items = amazon_scrape.amazon(url)
        message = list_of_items[0]
        return render (request, 'bully/index.html', {'message':message})

    return render (request, 'bully/index.html')
