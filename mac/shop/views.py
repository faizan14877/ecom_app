from math import ceil, floor, prod
from multiprocessing import context
from urllib import response
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.test import RequestFactory
import math
from .models import Product, Contact, Orders, OrderUpdate
import json
# Create your views here.

def shop(request):
    allProds = []
    catProds = Product.objects.values('category','id')
    # print(catProds) 
    cats = {item ['category'] for item in catProds}

    for cat in cats:
        prods = Product.objects.filter(category=cat)
        # print(prods)
        prodsLen = len(prods)
        nSlides = prodsLen // 4 + math.ceil(prodsLen/4 - prodsLen//4)
        allProds.append([prods, range(1, nSlides), nSlides])
    
    context = {'allProds': allProds}
    return render(request, 'shop/index.html', context)


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catProds = Product.objects.values('category','id')
    # print(catProds)
    cats = {item ['category'] for item in catProds}

    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prods = [item for item in prodtemp if searchMatch(query, item)]
        # print(prods)
        prodsLen = len(prods)
        nSlides = prodsLen // 4 + math.ceil(prodsLen/4 - prodsLen//4)
        if prodsLen > 0:
            allProds.append([prods, range(1, nSlides), nSlides])
    
    context = {'allProds': allProds, 'msg': ''}
    if len(allProds) == 0 or len(query) < 4:
        context = {'msg': 'Please enter relevant search query'}
    return render(request, 'shop/search.html', context)


def about(request):
    allProds = []
    catProds = Product.objects.values('category','id')
    cats = {item ['category'] for item in catProds}
    for cat in cats:
        prods = Product.objects.filter(category=cat)
        prodsLen = prods.count()
        nSlides = prodsLen // 4 + math.ceil(prodsLen/4 - prodsLen//4)
        allProds.append([prods, range(1, nSlides), nSlides])
    
    context = {'allProds': allProds}
    return render(request, 'shop/about.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        return render (request, 'shop/contact.html', {'thank': thank})
    return render (request, 'shop/contact.html')

def productView(request, myid):
    product = Product.objects.get(id=myid)
    # fetch the product using the id
    # product = Product.objects.filter(id=myid)
    return render (request, 'shop/product.html', {'product': product})


def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        itemsJson = request.POST.get('itemsJson')
        email = request.POST.get('email')
        contact = request.POST.get('phone')
        address = request.POST.get('address1') + " " + request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        order = Orders(name=name, items_json=itemsJson, email=email, contact=contact, address=address, city=city, state=state, zip_code=zip_code,)
        order.save()

        thank = True
        id = order.order_id
        context = {'thank': thank, 'id': id}
        updateOrder = OrderUpdate(order_id = order.order_id, update_desc="Your order is ready to be shipped")
        updateOrder.save()
        return render(request, 'shop/checkout.html', context)

    return render(request, 'shop/checkout.html')

def tracker(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        email = request.POST.get('email')

        # print(email)
        # print(order_id)
        try:
            order = Orders.objects.filter(order_id=order_id, email=email)
            updates = []
            if(len(order) > 0):
                update = OrderUpdate.objects.filter(order_id=order_id)
                # print(update)
                for item in update:
                    updates.append({'update_desc': item.update_desc, 'timestamp': item.timestamp})
                    # print(item)
            else:
                pass  
            
            
            response = json.dumps({'status': 'success', 'updates': updates, 'itemsJson': order[0].items_json}, default=str)
            return HttpResponse(response)       
        except Exception as e:
            print(e)
            return HttpResponse('{"status": "error"}')

    return render(request, 'shop/tracker.html')
