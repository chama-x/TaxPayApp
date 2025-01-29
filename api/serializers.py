from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    AssessmentTax, BusinessTax, IndustrialTax, TradeLicense,
    Payment, Document, Notification
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'address', 
                 'pradeshiya_sabha', 'category', 'profile_photo')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class AssessmentTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentTax
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class BusinessTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessTax
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class IndustrialTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustrialTax
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class TradeLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeLicense
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('user', 'payment_date', 'transaction_id')

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('user', 'uploaded_at')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('user', 'created_at') 