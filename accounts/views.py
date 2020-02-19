from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from .models import *
from .forms import OrderForm
from .filters import OrderFilter

def home(request):
    
    orders = Order.objects.all() # Get all the orders
    customers = Customer.objects.all() # Get all the customers

    # Count total customers and orders.
    total_customers = customers.count()
    total_orders = orders.count()

    # Filter Delivered and Pending Orders and count.
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers':customers, 
    'total_orders':total_orders, 'delivered':delivered, 
    'pending':pending}

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all() # Get all the products

    return render(request, 'accounts/products.html', {'products':products})

def customer(request, pk_test):
    # Get specific customer with customer id
    customer = Customer.objects.get(id=pk_test)

    # Get orders from specific customer and count.
    orders = customer.order_set.all()
    order_count = orders.count()

    # Fiter Order Table from fields
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    #---------------------------------

    context = {'customer': customer, 'orders': orders, 
    'order_count': order_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):
    """
    Create New Single Order

	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
    return render(request, 'accounts/order_form.html', context)
    """

    # Create New Multiple Orders
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    #-----------------------------------

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
    # Get specific order with order id
    order = Order.objects.get(id=pk)
    # Fill specific order instances in Form
    form = OrderForm(instance=order)

    # Update specific order instances.
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    #------------------------------------

    context = {'formset':form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
    # Get specific order with order id
    order = Order.objects.get(id=pk)

    # Delete order if submit button is clicked.
    if request.method == "POST":
        order.delete()
        return redirect('/')
    #--------------------------------------

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)