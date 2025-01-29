from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import (
    AssessmentTax, BusinessTax, IndustrialTax, TradeLicense,
    Payment, Document, Notification
)
from .serializers import (
    UserSerializer, AssessmentTaxSerializer, BusinessTaxSerializer,
    IndustrialTaxSerializer, TradeLicenseSerializer, PaymentSerializer,
    DocumentSerializer, NotificationSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'Welcome to Tax Payment System API',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'authentication': {
                'obtain_token': '/api/token/',
                'refresh_token': '/api/token/refresh/',
            },
            'tax_management': {
                'assessment_tax': '/api/assessment-tax/',
                'business_tax': '/api/business-tax/',
                'industrial_tax': '/api/industrial-tax/',
                'trade_license': '/api/trade-license/',
            },
            'payments': '/api/payments/',
            'documents': '/api/documents/',
            'notifications': '/api/notifications/',
        }
    })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

class AssessmentTaxViewSet(viewsets.ModelViewSet):
    queryset = AssessmentTax.objects.all()
    serializer_class = AssessmentTaxSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AssessmentTax.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def pay_installment(self, request, pk=None):
        tax = self.get_object()
        if tax.installment_option and tax.installments_paid < tax.total_installments:
            tax.installments_paid += 1
            if tax.installments_paid == tax.total_installments:
                tax.status = 'PAID'
            tax.save()
            return Response({'status': 'Installment paid'})
        return Response({'error': 'Invalid installment payment'}, 
                       status=status.HTTP_400_BAD_REQUEST)

class BusinessTaxViewSet(viewsets.ModelViewSet):
    queryset = BusinessTax.objects.all()
    serializer_class = BusinessTaxSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BusinessTax.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IndustrialTaxViewSet(viewsets.ModelViewSet):
    queryset = IndustrialTax.objects.all()
    serializer_class = IndustrialTaxSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IndustrialTax.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TradeLicenseViewSet(viewsets.ModelViewSet):
    queryset = TradeLicense.objects.all()
    serializer_class = TradeLicenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TradeLicense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Here you would typically integrate with a payment gateway
        # For now, we'll just create a payment record
        serializer.save(
            user=self.request.user,
            status='SUCCESS',
            transaction_id=f"TX-{self.request.user.id}-{serializer.validated_data['amount']}"
        )

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response({'status': 'marked as read'})
