import pytest
from datetime import date

from django.contrib.auth import get_user_model

from customuser.models import CustomUser, Doctor, DoctorProfile, PatientUser
from company.models import InsuranceCompany
from patient.models import Patient
from company.models import Company
from inventory.models import (
    Department,
    Supplier,
    Item,
    Requisition,
    RequisitionItem,
    PurchaseOrder,
    PurchaseOrderItem,
    IncomingItem,
    Inventory,
    SupplierInvoice,
    InventoryInsuranceSaleprice,
    DepartmentInventory,
)

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        email="9jg4t@example.com",
        password="password",
        first_name="Test",
        last_name="User",
        role="patient",
        profession="Test Profession",
        phone="+1234567890"
        )

@pytest.fixture
def authenticated_client(client, django_user_model, user):
    from rest_framework_simplejwt.tokens import RefreshToken
    
    # Generate a token
    refresh = RefreshToken.for_user(user)
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {refresh.access_token}'
    return client

@pytest.fixture
def company(db):
    return Company.objects.create(
        name="Test Company",
        logo=None  # Update with a valid file or `None` to test missing logo behavior.
    )

@pytest.fixture
def patient(db):
    user = PatientUser.objects.create(
        email="patientuser@example.com",
        password="password123",
        first_name="Alice",
        last_name="Smith",
        role=CustomUser.PATIENT,
        date_of_birth=date(1990, 1, 1),
        phone="1234567890",
    )

    insurance_1 = InsuranceCompany.objects.create(name="Insurance A")
    insurance_2 = InsuranceCompany.objects.create(name="Insurance B")

    patient = Patient.objects.create(
        first_name=user.first_name,
        second_name=user.last_name,
        date_of_birth=user.date_of_birth,
        gender="F",
        user=user
    )

    patient.insurances.add(insurance_1, insurance_2)

    return patient

@pytest.fixture
def doctor(db):
    user = Doctor.objects.create(
        email="doctoruser@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
        role=CustomUser.DOCTOR,
        date_of_birth=date(1985, 5, 15),
        phone="0987654321",
    )

    doctor_profile = DoctorProfile.objects.create(user=user)
    return user


@pytest.fixture
def department():
    return Department.objects.create(name="Test Department")

@pytest.fixture
def supplier():
    return Supplier.objects.create(official_name="Test Supplier", common_name="Test")

@pytest.fixture
def item():
    return Item.objects.create(
        name="Test Item",
        desc="Test Description",
        category="General",
        units_of_measure="Unit",
        vat_rate=16.0,
        item_code="ABC123",
    )


@pytest.fixture
def insurance_company():
    return InsuranceCompany.objects.create(name="Test Insurance Company")

@pytest.fixture
def requisition(user, department):
    return Requisition.objects.create(
        requested_by=user,
        department=department,
    )

@pytest.fixture
def requisition_item(requisition, item):
    return RequisitionItem.objects.create(
        requisition=requisition,
        item=item,
        quantity_requested=10,
    )

@pytest.fixture
def purchase_order(user, requisition):
    return PurchaseOrder.objects.create(
        ordered_by=user,
        requisition=requisition,
    )


@pytest.fixture
def purchase_order_item(purchase_order, requisition_item, supplier):
    return PurchaseOrderItem.objects.create(
        purchase_order=purchase_order,
        requisition_item=requisition_item
    )

@pytest.fixture
def supplier_invoice(db, supplier, purchase_order):
    return SupplierInvoice.objects.create(
        invoice_no="INV-2024-002",
        status="pending",
        supplier=supplier,
        purchase_order=purchase_order
    )


@pytest.fixture
def incoming_item(item, supplier, purchase_order, supplier_invoice):
    return IncomingItem.objects.create(
        item=item,
        supplier=supplier,
        supplier_invoice=supplier_invoice,
        purchase_order=purchase_order,
        quantity=10,
        sale_price=20.0,
        category_one="resale",
    )


@pytest.fixture
def inventory(item):
    return Inventory.objects.create(
        item=item,
        quantity_at_hand=10,
    )



@pytest.fixture
def inventory_insurance_saleprice(inventory, insurance_company):
    return InventoryInsuranceSaleprice.objects.create(
        inventory_item=inventory,
        insurance_company=insurance_company,
        sale_price=20.0,
    )

@pytest.fixture
def department_inventory(item, department):
    return DepartmentInventory.objects.create(
        item=item,
        department=department,
    )

