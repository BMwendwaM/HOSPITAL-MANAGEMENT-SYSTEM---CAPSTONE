from rest_framework import viewsets, decorators, response, status
from .models import Invoice, BillItem
from .serializers import InvoiceSerializer, BillItemSerializer
from visits.models import Visit

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    # Add Cashier when creating an invoice
    def perform_create(self, serializer):
        serializer.save(cashier=self.request.user)

    # Add item to bill

    @decorators.action(detail=True, methods=["post"])
    def add_item(self, request, pk=None):
        invoice = self.get_object()
        desc = request.data.get("description")
        amount = request.data.get("amount")
        
        BillItem.objects.create(invoice=invoice, description=desc, amount=amount)
        
        # Recalculate total
        invoice.total_amount = sum(item.amount for item in invoice.items.all())
        invoice.save()
        
        return response.Response(InvoiceSerializer(invoice).data)

    # Pay the bill

    @decorators.action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        invoice = self.get_object()
        invoice.paid = True
        invoice.save()
        
        # Release the patient
        visit = invoice.visit
        visit.status = Visit.Status.COMPLETED
        visit.save()
        
        return response.Response({"status": "Paid & Discharged"})
    
    # Override destroy to prevent deletion of invoices
    def destroy(self, request, *args, **kwargs):
        return response.Response(
            {"error": "Security Alert: Financial records cannot be deleted. This event has been logged."}, 
            status=status.HTTP_403_FORBIDDEN
        )