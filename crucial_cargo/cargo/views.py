from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Cargo, CargoImage, Invoice, Quotation
from .forms import (CargoRegistrationForm, InvoiceGenerationForm, 
                   UserRegistrationForm, LoginForm)
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from fpdf import FPDF
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.models import User


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['signupUsername']
        email = request.POST['signupEmail']
        password = request.POST['signupPassword']
        confirm_password = request.POST['confirmPassword']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully')
        return redirect('login')
    
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user_cargos = Cargo.objects.filter(client=request.user).order_by('-created_at')[:5]
    active_count = Cargo.objects.filter(client=request.user, status='processing').count()
    delivered_count = Cargo.objects.filter(client=request.user, status='delivered').count()
    
    context = {
        'recent_cargos': user_cargos,
        'active_count': active_count,
        'delivered_count': delivered_count,
    }
    return render(request, 'dashboard.html', context)

@login_required
def cargo_registration(request):
    if request.method == 'POST':
        form = CargoRegistrationForm(request.POST)
        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.client = request.user
            cargo.tracking_id = f"#CARGO{Cargo.objects.count() + 1000}"
            cargo.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for img in images:
                CargoImage.objects.create(cargo=cargo, image=img)
            
            # Create a sample quotation (in real app, calculate properly)
            Quotation.objects.create(
                cargo=cargo,
                amount=150 * len(images) if images else 100,  # Example calculation
                valid_until=datetime.now() + timedelta(days=7)
            )
            
            return redirect('cargo_update')
    else:
        form = CargoRegistrationForm()
    
    return render(request, 'registration.html', {'form': form})

@login_required
def cargo_update(request):
    cargos = Cargo.objects.filter(client=request.user).order_by('-updated_at')
    return render(request, 'cargoupdate.html', {'cargos': cargos})

@login_required
def generate_invoice(request, cargo_id):
    cargo = get_object_or_404(Cargo, id=cargo_id, client=request.user)
    
    if request.method == 'POST':
        form = InvoiceGenerationForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.cargo = cargo
            invoice.invoice_id = f"#INV{Invoice.objects.count() + 1000}"
            
            # Generate PDF invoice
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            pdf.cell(200, 10, txt="Crucial Cargo Movers Invoice", ln=1, align='C')
            pdf.cell(200, 10, txt=f"Invoice ID: {invoice.invoice_id}", ln=1, align='L')
            pdf.cell(200, 10, txt=f"Client: {request.user.username}", ln=1, align='L')
            pdf.cell(200, 10, txt=f"Cargo: {cargo.tracking_id}", ln=1, align='L')
            pdf.cell(200, 10, txt=f"Amount: ${invoice.amount}", ln=1, align='L')
            pdf.cell(200, 10, txt=f"Due Date: {invoice.due_date}", ln=1, align='L')
            
            fs = FileSystemStorage()
            filename = f"invoice_{invoice.invoice_id}.pdf"
            filepath = os.path.join(settings.MEDIA_ROOT, 'invoices', filename)
            pdf.output(filepath)
            
            invoice.pdf.name = f"invoices/{filename}"
            invoice.save()
            
            return redirect('reports')
    else:
        initial = {
            'amount': 100,  # Default amount, replace with real calculation
            'due_date': datetime.now() + timedelta(days=14)
        }
        form = InvoiceGenerationForm(initial=initial)
    
    return render(request, 'generate_invoice.html', {'form': form, 'cargo': cargo})

@login_required
def reports(request):
    invoices = Invoice.objects.filter(cargo__client=request.user).order_by('-issue_date')
    return render(request, 'reports.html', {'invoices': invoices})

@login_required
def download_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, cargo__client=request.user)
    file_path = invoice.pdf.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    raise Http404

def faq(request):
    return render(request, 'faq.html')