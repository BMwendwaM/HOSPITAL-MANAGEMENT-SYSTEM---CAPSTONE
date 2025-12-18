from rest_framework import serializers
from .models import Invoice, BillItem

class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        fields = ["id", "description", "amount"]

class InvoiceSerializer(serializers.ModelSerializer):
    # Nested serialization for related BillItem objects
    
    items = BillItemSerializer(many=True, read_only=True)
    # Show cashier's username instead of ID.
    cashier_name = serializers.CharField(source="cashier.username", read_only=True)
    
    class Meta:
        model = Invoice
        fields = ["id", "visit", "total_amount", "paid", "items", "issued_at", "cashier_name"]