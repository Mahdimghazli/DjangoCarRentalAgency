from pyexpat import model
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse , HttpResponseRedirect
from django.db.models import Q

from .models import Car, Order, PrivateMsg
from .forms import CarForm, OrderForm, MessageForm
from django.contrib import messages
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def home(request):
    return render(request,'home.html')

def car_list(request):
    car = Car.objects.all()
    # pagination
    paginator = Paginator(car, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        car = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        car = paginator.page(paginator.num_pages)
    context = {
        'car': car,
    }
    return render(request, 'car_list.html', context)


def car_detail(request, id=None):
    detail = get_object_or_404(Car,id=id)
    context = {
        "detail": detail
    }
    return render(request, 'car_detail.html', context)


def index_order(request):
    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        employee_name = request.POST.get('employee_name')
        cell_no = request.POST.get('cell_no')
        address = request.POST.get('address')
        date = request.POST.get('date')
        to = request.POST.get('to')

        existing_order = Order.objects.filter(date=date,car_name=car_name).first()
        if existing_order:
            messages.error(request, 'La réservation pour cette date existe déjà !')
            return render(request, 'index.html')
        if date >= to:
            messages.error(request, 'La date de départ doit être postérieure à la date darrivée !')
            return render(request, 'index.html')
        
        order = Order(car_name=car_name, employee_name=employee_name, cell_no=cell_no,
                      address=address, date=date, to=to)
        order.save()
        
        messages.success(request, 'Votre réservation a réussi !')
        
        return render(request, 'index.html')
    

def msg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        privateMsg = PrivateMsg(name=name, email=email, message=message)
        privateMsg.save()
        
        messages.success(request, 'Your booking was successful!')
        
    return render(request,'home.html')


def order_detail(request, id=None):
    detail = get_object_or_404(Order,id=id)
    context = {
        "detail": detail,
    }
    return render(request, 'order_detail.html', context)


def order_created(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    form = OrderForm(request.POST or None)  # Remove the 'car_name' argument
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form = OrderForm(initial={'car_name': car.car_name})  # Set the initial value
    context = {
        "form": form,
        "title": "Create Order"
    }
    return render(request, 'index.html', context)


def newcar(request):
    new = Car.objects.order_by('-id')
    #seach
    query = request.GET.get('q')
    if query:
        new = new.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query)
        )

    # pagination
    paginator = Paginator(new, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        new = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        new = paginator.page(paginator.num_pages)
    context = {
        'car': new,
    }
    return render(request, 'new_car.html', context)


def like_update(request, id=None):
    new = Car.objects.order_by('-id')
    like_count = get_object_or_404(Car, id=id)
    like_count.like+=1
    like_count.save()
    context = {
        'car': new,
    }
    return render(request,'new_car.html',context)


def popular_car(request):
    new = Car.objects.order_by('-like')
    # seach
    query = request.GET.get('q')
    if query:
        new = new.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query)
        )

    # pagination
    paginator = Paginator(new, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        new = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        new = paginator.page(paginator.num_pages)
    context = {
        'car': new,
    }
    return render(request, 'new_car.html', context)




#WEB_SCRAPING
def scrape_cars(request):
    url = 'https://oyamacar.fr/location-voiture-marrakech'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    car_items = soup.select('.item-list')
    cars = []

    for item in car_items:
        car_name = item.select_one('.item-title').text.strip()
        car_price = item.select_one('.price-sign').text.strip()
        car_image = item.select_one('.car-img img')['src']
        num_of_doors = item.select_one('.ic-doors').text.strip()
        num_of_suitcases = item.select_one('.ic-suitcases').text.strip()
        transmission_type = item.select_one('.ic-transmission').text.strip()
        fuel_type = item.select_one('.ic-carburant').text.strip()

        car = {
            'car_name': car_name,
            'car_price': car_price,
            'car_image': car_image,
            'num_of_doors': num_of_doors,
            'num_of_suitcases': num_of_suitcases,
            'transmission_type': transmission_type,
            'fuel_type': fuel_type,
        }
        cars.append(car)

    return render(request, 'car_scraping.html', {'cars': cars})


