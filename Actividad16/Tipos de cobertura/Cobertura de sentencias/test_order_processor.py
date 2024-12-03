# test_order_processor.py

import pytest
from order_processor import OrderProcessor

@pytest.fixture
def processor():
    return OrderProcessor()

def test_add_order_valid(processor):
    order = {'id': 1, 'amount': 100}
    processor.add_order(order)
    assert len(processor.orders) == 1
    assert processor.orders[0] == order

def test_add_order_invalid_type(processor):
    with pytest.raises(TypeError):
        processor.add_order(['id', 2, 'amount', 200])

def test_add_order_missing_fields(processor):
    with pytest.raises(ValueError):
        processor.add_order({'id': 3})

def test_process_orders_success(processor):
    orders = [
        {'id': 1, 'amount': 100},
        {'id': 2, 'amount': 200, 'discount': 0.1}
    ]
    for order in orders:
        processor.add_order(order)
    processor.process_orders()
    assert len(processor.processed_orders) == 2
    assert len(processor.failed_orders) == 0
    assert processor.processed_orders[1]['final_amount'] == 180.0

def test_process_orders_with_failure(processor):
    orders = [
        {'id': 1, 'amount': -50},
        {'id': 2, 'amount': 200, 'simulate_failure': True}
    ]
    for order in orders:
        processor.add_order(order)
    processor.process_orders()
    assert len(processor.processed_orders) == 0
    assert len(processor.failed_orders) == 2
    assert 'monto inválido' in processor.failed_orders[0]['error']
    assert 'Error al procesar la orden' in processor.failed_orders[1]['error']

def test_get_order_status(processor):
    orders = [
        {'id': 1, 'amount': 100},
        {'id': 2, 'amount': -50},
        {'id': 3, 'amount': 150, 'simulate_failure': True}
    ]
    for order in orders:
        processor.add_order(order)
    processor.process_orders()
    assert processor.get_order_status(1) == 'Procesada'
    assert 'Fallida' in processor.get_order_status(2)
    assert 'Fallida' in processor.get_order_status(3)
    assert processor.get_order_status(4) == 'Pendiente'