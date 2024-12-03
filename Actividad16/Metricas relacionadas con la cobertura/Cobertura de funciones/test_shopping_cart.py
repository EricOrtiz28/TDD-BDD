# test_shopping_cart.py

import pytest
from shopping_cart import Item, ShoppingCart

# Fixtures
@pytest.fixture
def item():
    return Item(name='Laptop', price=999.99, quantity=1)

@pytest.fixture
def multiple_items():
    return [
        Item(name='Laptop', price=999.99, quantity=1),
        Item(name='Mouse', price=49.99, quantity=2),
        Item(name='Keyboard', price=79.99, quantity=1)
    ]

@pytest.fixture
def shopping_cart():
    return ShoppingCart()

# Pruebas para la clase Item
def test_item_initialization_valid():
    item = Item(name='Phone', price=499.99, quantity=2)
    assert item.name == 'Phone'
    assert item.price == 499.99
    assert item.quantity == 2

def test_item_initialization_invalid_name():
    with pytest.raises(TypeError):
        Item(name=123, price=49.99)

def test_item_initialization_invalid_price_type():
    with pytest.raises(TypeError):
        Item(name='Tablet', price='Free')

def test_item_initialization_negative_price():
    with pytest.raises(ValueError):
        Item(name='Tablet', price=-50.00)

def test_item_initialization_invalid_quantity_type():
    with pytest.raises(TypeError):
        Item(name='Headphones', price=199.99, quantity=1.5)

def test_item_initialization_zero_quantity():
    with pytest.raises(ValueError):
        Item(name='Headphones', price=199.99, quantity=0)

def test_item_total_price(item):
    assert item.total_price() == 999.99

def test_item_total_price_multiple_quantities():
    item = Item(name='Monitor', price=299.99, quantity=3)
    assert item.total_price() == 899.97

# Pruebas para la clase ShoppingCart
def test_shopping_cart_initialization(shopping_cart):
    assert shopping_cart.items == {}
    assert shopping_cart.applied_discount == 0

def test_add_item_valid(shopping_cart, item):
    shopping_cart.add_item(item)
    assert 'Laptop' in shopping_cart.items
    assert shopping_cart.items['Laptop'].quantity == 1

def test_add_item_multiple_times(shopping_cart, item):
    shopping_cart.add_item(item)
    shopping_cart.add_item(item)
    assert shopping_cart.items['Laptop'].quantity == 2

def test_add_item_invalid_type(shopping_cart):
    with pytest.raises(TypeError):
        shopping_cart.add_item('NotAnItem')

def test_remove_item_valid(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.remove_item('Mouse', quantity=1)
    assert shopping_cart.items['Mouse'].quantity == 1

def test_remove_item_entire_quantity(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.remove_item('Mouse', quantity=2)
    assert 'Mouse' not in shopping_cart.items

def test_remove_item_nonexistent(shopping_cart):
    with pytest.raises(ValueError):
        shopping_cart.remove_item('Nonexistent')

def test_remove_item_invalid_quantity_type(shopping_cart, item):
    shopping_cart.add_item(item)
    with pytest.raises(TypeError):
        shopping_cart.remove_item('Laptop', quantity='two')

def test_remove_item_exceeding_quantity(shopping_cart, item):
    shopping_cart.add_item(item)
    with pytest.raises(ValueError):
        shopping_cart.remove_item('Laptop', quantity=2)

def test_apply_discount_valid(shopping_cart):
    shopping_cart.apply_discount(10)
    assert shopping_cart.applied_discount == 10

def test_apply_discount_zero(shopping_cart):
    shopping_cart.apply_discount(0)
    assert shopping_cart.applied_discount == 0

def test_apply_discount_full(shopping_cart):
    shopping_cart.apply_discount(100)
    assert shopping_cart.applied_discount == 100

def test_apply_discount_invalid_type(shopping_cart):
    with pytest.raises(TypeError):
        shopping_cart.apply_discount('ten')

def test_apply_discount_negative(shopping_cart):
    with pytest.raises(ValueError):
        shopping_cart.apply_discount(-5)

def test_apply_discount_over_100(shopping_cart):
    with pytest.raises(ValueError):
        shopping_cart.apply_discount(150)

def test_calculate_total_no_discount(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    total = shopping_cart.calculate_total()
    expected_total = 999.99 + (49.99 * 2) + 79.99
    assert total == round(expected_total, 2)

def test_calculate_total_with_discount(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.apply_discount(10)
    total = shopping_cart.calculate_total()
    expected_total = (999.99 + (49.99 * 2) + 79.99) * 0.9
    assert total == round(expected_total, 2)

def test_calculate_total_with_zero_discount(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.apply_discount(0)
    total = shopping_cart.calculate_total()
    expected_total = 999.99 + (49.99 * 2) + 79.99
    assert total == round(expected_total, 2)

def test_list_items_empty(shopping_cart):
    assert shopping_cart.list_items() == []

def test_list_items_with_items(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    items_list = shopping_cart.list_items()
    expected_list = [
        {'name': 'Laptop', 'price': 999.99, 'quantity': 1, 'total_price': 999.99},
        {'name': 'Mouse', 'price': 49.99, 'quantity': 2, 'total_price': 99.98},
        {'name': 'Keyboard', 'price': 79.99, 'quantity': 1, 'total_price': 79.99}
    ]
    assert items_list == expected_list

def test_clear_cart(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.apply_discount(15)
    shopping_cart.clear_cart()
    assert shopping_cart.items == {}
    assert shopping_cart.applied_discount == 0

def test_is_empty_true(shopping_cart):
    assert shopping_cart.is_empty() == True

def test_is_empty_false(shopping_cart, item):
    shopping_cart.add_item(item)
    assert shopping_cart.is_empty() == False

def test_add_multiple_items(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    assert len(shopping_cart.items) == 3
    assert shopping_cart.items['Laptop'].quantity == 1
    assert shopping_cart.items['Mouse'].quantity == 2
    assert shopping_cart.items['Keyboard'].quantity == 1

def test_calculate_total_large_quantities(shopping_cart):
    item1 = Item(name='Pen', price=1.5, quantity=100)
    item2 = Item(name='Notebook', price=3.0, quantity=50)
    shopping_cart.add_item(item1)
    shopping_cart.add_item(item2)
    total = shopping_cart.calculate_total()
    expected_total = (1.5 * 100) + (3.0 * 50)
    assert total == round(expected_total, 2)

def test_calculate_total_large_quantities_with_discount(shopping_cart):
    item1 = Item(name='Pen', price=1.5, quantity=100)
    item2 = Item(name='Notebook', price=3.0, quantity=50)
    shopping_cart.add_item(item1)
    shopping_cart.add_item(item2)
    shopping_cart.apply_discount(20)
    total = shopping_cart.calculate_total()
    expected_total = ((1.5 * 100) + (3.0 * 50)) * 0.8
    assert total == round(expected_total, 2)

def test_remove_all_items_one_by_one(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.remove_item('Mouse', quantity=2)
    shopping_cart.remove_item('Laptop', quantity=1)
    shopping_cart.remove_item('Keyboard', quantity=1)
    assert shopping_cart.is_empty() == True
    assert shopping_cart.calculate_total() == 0 

def test_remove_item_partial_quantity(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.remove_item('Mouse', quantity=1)
    assert shopping_cart.items['Mouse'].quantity == 1
    assert 'Mouse' in shopping_cart.items