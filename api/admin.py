from django.contrib import admin
from .models import (
    AssessmentTax, BusinessTax, IndustrialTax, TradeLicense,
    Payment, Document, Notification
)

@admin.register(AssessmentTax)
class AssessmentTaxAdmin(admin.ModelAdmin):
    list_display = ('user', 'property_id', 'amount', 'due_date', 'status', 'installment_option')
    list_filter = ('status', 'installment_option')
    search_fields = ('user__username', 'property_id')

@admin.register(BusinessTax)
class BusinessTaxAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_id', 'business_name', 'amount', 'due_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'business_id', 'business_name')

@admin.register(IndustrialTax)
class IndustrialTaxAdmin(admin.ModelAdmin):
    list_display = ('user', 'industry_id', 'industry_name', 'amount', 'due_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'industry_id', 'industry_name')

@admin.register(TradeLicense)
class TradeLicenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_id', 'business_name', 'amount', 'due_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'license_id', 'business_name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'tax_type', 'amount', 'payment_date', 'payment_method', 'status')
    list_filter = ('tax_type', 'payment_method', 'status')
    search_fields = ('user__username', 'transaction_id')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'document_type', 'uploaded_at', 'status')
    list_filter = ('document_type', 'status')
    search_fields = ('user__username', 'title')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'created_at', 'read')
    list_filter = ('notification_type', 'read')
    search_fields = ('user__username', 'title')
