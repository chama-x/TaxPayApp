from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import json

def index(request):
    return render(request, 'frontend/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Get JWT token
        response = requests.post('http://127.0.0.1:8000/api/token/', 
                               data={'username': username, 'password': password})
        
        if response.status_code == 200:
            data = response.json()
            request.session['access_token'] = data['access']
            request.session['refresh_token'] = data['refresh']
            return redirect('dashboard')
        else:
            return render(request, 'frontend/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'frontend/login.html')

@login_required
def dashboard(request):
    access_token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get user's tax information
    assessment_tax = requests.get('http://127.0.0.1:8000/api/assessment-tax/', headers=headers).json()
    business_tax = requests.get('http://127.0.0.1:8000/api/business-tax/', headers=headers).json()
    industrial_tax = requests.get('http://127.0.0.1:8000/api/industrial-tax/', headers=headers).json()
    trade_license = requests.get('http://127.0.0.1:8000/api/trade-license/', headers=headers).json()
    
    context = {
        'assessment_tax': assessment_tax,
        'business_tax': business_tax,
        'industrial_tax': industrial_tax,
        'trade_license': trade_license,
    }
    
    return render(request, 'frontend/dashboard.html', context)

@login_required
def payments(request):
    access_token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    
    if request.method == 'POST':
        # Process payment
        payment_data = {
            'tax_type': request.POST.get('tax_type'),
            'amount': request.POST.get('amount'),
            'payment_method': request.POST.get('payment_method'),
        }
        
        response = requests.post('http://127.0.0.1:8000/api/payments/', 
                               headers=headers, data=payment_data)
        
        if response.status_code == 201:
            return redirect('payment_success')
        else:
            return render(request, 'frontend/payments.html', {'error': 'Payment failed'})
    
    # Get payment history
    payments = requests.get('http://127.0.0.1:8000/api/payments/', headers=headers).json()
    return render(request, 'frontend/payments.html', {'payments': payments})

@login_required
def documents(request):
    access_token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    
    if request.method == 'POST' and request.FILES:
        files = {'file': request.FILES['document']}
        data = {
            'title': request.POST.get('title'),
            'document_type': request.POST.get('document_type'),
        }
        
        response = requests.post('http://127.0.0.1:8000/api/documents/', 
                               headers=headers, data=data, files=files)
        
        if response.status_code == 201:
            return redirect('documents')
    
    # Get documents list
    documents = requests.get('http://127.0.0.1:8000/api/documents/', headers=headers).json()
    return render(request, 'frontend/documents.html', {'documents': documents})

@login_required
def notifications(request):
    access_token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    
    notifications = requests.get('http://127.0.0.1:8000/api/notifications/', 
                               headers=headers).json()
    return render(request, 'frontend/notifications.html', {'notifications': notifications})

def logout_view(request):
    logout(request)
    return redirect('login') 