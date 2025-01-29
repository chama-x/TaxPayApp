from django.db import models
from django.conf import settings

class BaseTax(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AssessmentTax(BaseTax):
    property_id = models.CharField(max_length=50)
    installment_option = models.BooleanField(default=False)
    installments_paid = models.IntegerField(default=0)
    total_installments = models.IntegerField(default=3)

class BusinessTax(BaseTax):
    business_id = models.CharField(max_length=50)
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=50)

class IndustrialTax(BaseTax):
    industry_id = models.CharField(max_length=50)
    industry_name = models.CharField(max_length=100)
    industry_type = models.CharField(max_length=50)

class TradeLicense(BaseTax):
    license_id = models.CharField(max_length=50)
    business_name = models.CharField(max_length=100)
    license_type = models.CharField(max_length=50)

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tax_type = models.CharField(max_length=20, choices=[
        ('ASSESSMENT', 'Assessment Tax'),
        ('BUSINESS', 'Business Tax'),
        ('INDUSTRIAL', 'Industrial Tax'),
        ('TRADE', 'Trade License')
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=[
        ('CREDIT', 'Credit Card'),
        ('DEBIT', 'Debit Card'),
        ('AMEX', 'American Express')
    ])
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed')
    ])

class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ])

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=20, choices=[
        ('TAX_DUE', 'Tax Due'),
        ('PAYMENT', 'Payment'),
        ('DOCUMENT', 'Document'),
        ('GENERAL', 'General')
    ])
