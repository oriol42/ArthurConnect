from django.shortcuts import render

def index(request):
  return render(request,'ArthurConnect/index.html')

def category(request):
  return render(request,'ArthurConnect/category.html')

def contact(request):
  return render(request,'ArthurConnect/contact.html')

def cart(request):
  return render(request,'ArthurConnect/cart.html')

def checkout(request):
  return render(request,'ArthurConnect/checkout.html')

def singleproduct(request):
  return render(request,'ArthurConnect/single-product.html')

def about(request):
  return render(request,'ArthurConnect/about.html')

def service_client(request):
  return render(request,'ArthurConnect/service-client.html')