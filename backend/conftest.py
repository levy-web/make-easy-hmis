import pytest
from django.contrib.auth import get_user_model
from customuser.models import CustomUser
from company.models import InsuranceCompany
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

# @pytest.fixture
# def custom_user():
#     return CustomUser.objects.create_user(email="test@example.com", password="password")

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
        quantity_at_hand=10,
        re_order_level=5,
        buying_price=10.0,
        selling_price=20.0,
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
        requisition_item=requisition_item,
        supplier=supplier,
    )

@pytest.fixture
def incoming_item(item, supplier, purchase_order):
    return IncomingItem.objects.create(
        item=item,
        item_code=item.item_code,
        supplier=supplier,
        purchase_order=purchase_order,
        quantity=10,
        sale_price=20.0,
        packed="1",
        subpacked="12",
        category_one="resale",

    )

@pytest.fixture
def inventory(item):
    return Inventory.objects.create(
        item=item,
        quantity_in_stock=10,
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