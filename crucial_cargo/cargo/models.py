from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Cargo(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('clearing', 'Clearing'),
        ('forwarding', 'Forwarding'),
        ('delivered', 'Delivered'),
    ]

    tracking_id = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery = models.DateField()
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tracking_id} - {self.get_status_display()}"

class CargoImage(models.Model):
    cargo = models.ForeignKey(Cargo, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cargo_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.cargo.tracking_id}"

class Invoice(models.Model):
    invoice_id = models.CharField(max_length=20, unique=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    pdf = models.FileField(upload_to='invoices/', null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice_id} - ${self.amount}"

class Quotation(models.Model):
    cargo = models.OneToOneField(Cargo, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Quotation for {self.cargo.tracking_id}"