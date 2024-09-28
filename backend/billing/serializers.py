from .models import Invoice, InvoiceItem, PaymentMode
from rest_framework import serializers


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'       


class InvoiceItemSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    item_name = serializers.SerializerMethodField()
    item_code = serializers.SerializerMethodField()
    payment_mode_name = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = '__all__'

    def get_category(self, obj):
        item = obj.item
        return item.category if item else None
    
    def get_item_name(self, obj):
        item = obj.item
        return item.name if item else None

    def get_item_code(self, obj):
        item = obj.item
        return item.item_code if item else None
    
    def get_payment_mode_name(self, obj):
        item = obj.payment_mode
        return item.paymet_mode if item  else None


class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode 
        fields = '__all__'       