from django.db import models
from patient.models import Patient
from django.conf import settings
from customusers.models import CustomUser
from inventory.models import Item, SaleOrder

class LabReagent(models.Model):
    name = models.CharField(max_length=255)
    cas_number = models.CharField(max_length=255)
    molecular_weight = models.DecimalField(max_digits=10, decimal_places=2)
    purity = models.DecimalField(max_digits=10, decimal_places=2)
    sale_id =  models.ForeignKey(SaleOrder, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class LabTestProfile(models.Model):
    name = models.CharField(max_length=255)
    cost = models.CharField(max_length=255)
    item_number = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.name    
    
class LabTestPanel(models.Model):
    name = models.CharField(max_length=255)
    test_profile_ID = models.ForeignKey(LabTestProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name        

class LabTestRequest(models.Model):
    patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_profile_ID = models.ForeignKey(LabTestProfile, on_delete=models.CASCADE)
    sale_order_ID = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
    note = models.TextField()

    def __str__(self):
        return self.patient_ID   

class LabTestResult(models.Model):
    lab_test_request_ID = models.ForeignKey(LabTestRequest, on_delete=models.CASCADE)
    title = models.CharField(max_length=45)
    test_element =  models.CharField(max_length=45)
    value = models.CharField(max_length=45)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title  

class LabTestCategory(models.Model):
    category = models.CharField(max_length=45)

    def __str__(self):
        return self.category 