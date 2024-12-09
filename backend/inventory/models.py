import uuid
import random
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from customuser.models import CustomUser
from company.models import InsuranceCompany
from customuser.models import CustomUser

class Department(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
    
class Supplier(models.Model):
    official_name = models.CharField(max_length=255)  
    common_name = models.CharField(max_length=30) 
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.official_name} ({self.common_name})"
    
class Item(models.Model):
    UNIT_CHOICES = [
        ('unit', 'Unit'),
        ('mg', 'Milligram'),
        ('g', 'Gram'),
        ('kg', 'Kilogram'),
        ('ml', 'Milliliter'),
        ('L', 'Liter'),
    ]
    CATEGORY_CHOICES = [
        
        ('SurgicalEquipment', 'Surgical Equipment'),
        ('LabReagent', 'Lab Reagent'),
        ('Drug', 'Drug'),
        ('Furniture', 'Furniture'),
        ('Lab Test', 'Lab Test'),
        ('General Appointment', 'General Appointment'),
        ('Specialized Appointment', 'Specialized Appointment'),
        ('general', 'General'),
    ]
    item_code=models.CharField(max_length=255, unique=True, editable=False)
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    units_of_measure = models.CharField(max_length=255, choices=UNIT_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    vat_rate= models.DecimalField(max_digits=5, decimal_places=2, default=16.0) 

    def save(self, *args, **kwargs):
        ''' Generate unique item code'''
        name_abbr = ''.join([part[:3].upper() for part in self.name.split()[:2]])
        category_abbr = ''.join([part[:3].upper() for part in self.category.split()[:1]])
        unique_id = str(uuid.uuid4().hex[:4].upper())

        item_code = f"{name_abbr}-{category_abbr}-{unique_id}"
        self.item_code = item_code

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Requisition(models.Model):
    requisition_number = models.CharField(max_length=50, unique=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='requisitions', null=True, blank=True)
    department_approved = models.BooleanField(default=False)
    procurement_approved = models.BooleanField(default=False)
    department_approval_date = models.DateTimeField(null=True, blank=True)
    procurement_approval_date = models.DateTimeField(null=True, blank=True)
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, max_length=255, null=False, blank=False)
    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='req_requested_by')
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='req_approved_by')


    def save(self, *args, **kwargs):
        '''Generate requisition number'''
        today = timezone.now()
        year = today.year % 100
        month = today.month
        day = today.day
        abbr = self.department.name[:3].upper()
        random_code = random.randint(1000, 9999)

        self.requisition_number = f"{abbr}/{year}/{month:02d}/{day:02d}/{random_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.requisition_number
      
        
class RequisitionItem(models.Model):
    quantity_requested = models.IntegerField()
    quantity_approved = models.IntegerField(default=0)  
    date_created = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='items')
    preferred_supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item.name} - Requested: {self.quantity_requested}, Approved: {self.quantity_approved}"


class PurchaseOrder(models.Model):
    PO_number = models.CharField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='purchase-orders', null=True, blank=True)
    is_dispatched = models.BooleanField(default=False)
    ordered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ordered_by')
    approved_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='po_approved_by')
    requisition = models.ForeignKey(Requisition, on_delete=models.SET_NULL, null=True, blank=True, related_name='requisition')

    def save(self, *args, **kwargs):
        '''Generate purchase order number'''
        today = timezone.now()
        year = today.year % 100
        month = today.month
        day = today.day
        random_code = random.randint(1000, 9999)
        self.PO_number= f"PO/{year}/{month:02d}/{day:02d}/{random_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase Order by {self.ordered_by} - Status: {self.PO_number}"


class PurchaseOrderItem(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    quantity_received = models.IntegerField(default=0)
    packed = models.CharField(max_length=255)
    subpacked = models.CharField(max_length=255)

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplier')
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='purchase_order')
    requisition_item = models.ForeignKey(RequisitionItem, on_delete=models.CASCADE, null=True, blank=True, related_name='purchase_order_items')

    def __str__(self):
        return f"{self.requisition_item.item.name} - Purchased: {self.requisition_item.item.quantity_approved}"  

class IncomingItemsReceiptNote(models.Model):
    goods_receipt_number = models.CharField(max_length=100, unique=True)  
    invoice_number = models.CharField(max_length=100)
    updated_by= models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_by')
    checked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='checked_by')
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='incoming_item_purchase_order')

    def save(self, *args, **kwargs):
        '''Generate goods receipt number'''
        if not self.goods_receipt_number:  
            today = timezone.now()
            year = today.year % 100
            month = today.month
            day = today.day
            random_code = random.randint(1000, 9999)
            self.goods_receipt_number = f"GRN/{year}/{month:02d}/{day:02d}/{random_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.goods_receipt_number


class GoodsReceiptNote(models.Model):
    '''
    Create a signal to gen pdf
    '''
    receipt_no = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def gen_receipt_no(self): 
        # generate receipt number using celery
        return f"GRN-{timezone.now().year}-{timezone.now().month}-{timezone.now().day}-{timezone.now().hour}-{timezone.now().minute}-{timezone.now().second}"  

class SupplierAccount(models.Model):
    '''
    Create signal to update this from IncoingItem
    '''
    STATUS=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    account_no = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    invoice_no = models.CharField(max_length=255, null=True, blank=True)# get from IncomingItem.supplier_invoice
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255, choices=STATUS, default="pending")

    def __str__(self):    
        return self.account_no

class SupplierInvoice(models.Model):
    STATUS=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255, choices=STATUS, default="pending")

    def __str__(self):    
        return self.invoice_no

class IncomingItem(models.Model):
    '''
    Update inventory
    Associate with PO
    Update Invoice Number
    Generate Good receipt note
    Update supplier account
    '''
    CATEGORY_1_CHOICES = [
        ('Resale', 'resale'),
        ('Internal', 'internal'),
    ]
    item_code= models.CharField(max_length=255) # so as to hide names from user
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    packed = models.CharField(max_length=255)
    subpacked = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quantity = models.IntegerField()
    category_one = models.CharField(max_length=255, choices=CATEGORY_1_CHOICES) 
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True,)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True)
    supplier_invoice = models.CharField(max_length=255, null=True, blank=True) # supplier's Invoice, manual input
    lot_no= models.CharField(max_length=255, null=True, blank=True)
    expiry_date= models.DateField(null=True, blank=True)
    supplier_invoice= models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.item.name} - {self.date_created}"

class Inventory(models.Model):
    CATEGORY_ONE_CHOICES = [
        ('Resale', 'resale'),
        ('Internal', 'internal'),
    ]
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='inventory')
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=10)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=20)
    quantity_at_hand = models.PositiveIntegerField()
    re_order_level= models.PositiveIntegerField(default=5)
    packed = models.CharField(max_length=255, default=10)
    subpacked = models.CharField(max_length=255, default=50)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    category_one = models.CharField(max_length=255, choices=CATEGORY_ONE_CHOICES)

    def clean(self):
        if self.buying_price > self.selling_price:
            raise ValidationError("Buying price cannot exceed selling price")

        if self.re_order_level > self.quantity_at_hand:
            raise ValidationError("Re-order leves cannot exceed the quantity at hand")
    def __str__(self):
        return f"{self.item.name} - {self.date_created}"
    
    class Meta:
        verbose_name_plural = 'Inventory'
    
class InventoryInsuranceSaleprice(models.Model):
    inventory_item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    insurance_company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.inventory_item.item.name} - {self.insurance_company.name}"
    
    class Meta:
        unique_together = ('inventory_item', 'insurance_company')
    
class DepartmentInventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    packed = models.CharField(max_length=255)
    subpacked = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.item)










