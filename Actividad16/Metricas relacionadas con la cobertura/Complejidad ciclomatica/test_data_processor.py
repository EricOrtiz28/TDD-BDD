# test_data_processor.py

import pytest
from data_processor import DataProcessor

@pytest.fixture
def valid_data():
    return [1, 2.5, 'hello', 3, 4.75, 'world']

@pytest.fixture
def invalid_data_type():
    return "Not a list"

@pytest.fixture
def mixed_data():
    return [1, -2, 3.5, 'hello123', 'world', {}, 4.0, 'Test']

def test_initialization_valid(valid_data):
    processor = DataProcessor(valid_data)
    assert processor.data == valid_data
    assert processor.processed_data == []
    assert processor.errors == []

def test_initialization_invalid_type(invalid_data_type):
    with pytest.raises(TypeError) as excinfo:
        DataProcessor(invalid_data_type)
    assert "Data debe ser una lista." in str(excinfo.value)

def test_process_all_valid(valid_data):
    processor = DataProcessor(valid_data)
    processor.process()
    assert processor.get_processed_data() == [2, 1.25, 'HELLO', 6, 2.38, 'WORLD']
    assert processor.get_errors() == []

def test_process_with_errors(mixed_data):
    processor = DataProcessor(mixed_data)
    processor.process()
    expected_processed = [2, 3.5, 'WORLD', 4.0]
    expected_errors = [
        {'index': 1, 'error': "Los enteros deben ser positivos."},
        {'index': 3, 'error': "Las cadenas deben contener solo letras."},
        {'index': 5, 'error': "Tipo de dato no soportado: <class 'dict'>"}
    ]
    assert processor.get_processed_data() == expected_processed
    assert processor.get_errors() == expected_errors

def test_process_empty_list():
    processor = DataProcessor([])
    processor.process()
    assert processor.get_processed_data() == []
    assert processor.get_errors() == []

def test_process_only_integers():
    data = [1, 2, 3, 4, 5]
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == [2, 4, 6, 8, 10]
    assert processor.get_errors() == []

def test_process_only_floats():
    data = [1.0, 2.5, 3.75]
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == [0.5, 1.25, 1.88]
    assert processor.get_errors() == []

def test_process_only_strings():
    data = ['hello', 'world', 'test']
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == ['HELLO', 'WORLD', 'TEST']
    assert processor.get_errors() == []

def test_process_unsupported_type():
    data = [1, 'hello', None]
    processor = DataProcessor(data)
    processor.process()
    expected_processed = [2, 'HELLO']
    expected_errors = [{'index': 2, 'error': "Tipo de dato no soportado: <class 'NoneType'>"}]
    assert processor.get_processed_data() == expected_processed
    assert processor.get_errors() == expected_errors

def test_summarize_no_errors(valid_data):
    processor = DataProcessor(valid_data)
    processor.process()
    summary = processor.summarize()
    assert summary['total_items'] == 6
    assert summary['processed_items'] == 6
    assert summary['errors'] == 0

def test_summarize_with_errors(mixed_data):
    processor = DataProcessor(mixed_data)
    processor.process()
    summary = processor.summarize()
    assert summary['total_items'] == 8
    assert summary['processed_items'] == 4
    assert summary['errors'] == 3

def test_summarize_empty_list():
    processor = DataProcessor([])
    processor.process()
    summary = processor.summarize()
    assert summary['total_items'] == 0
    assert summary['processed_items'] == 0
    assert summary['errors'] == 0

def test_multiple_process_calls():
    processor = DataProcessor([1, 'hello'])
    processor.process()
    assert processor.get_processed_data() == [2, 'HELLO']
    assert processor.get_errors() == []
    # Second call should process the same data again
    processor.process()
    assert processor.get_processed_data() == [2, 'HELLO', 2, 'HELLO']
    assert processor.get_errors() == []

def test_transaction_history():
    processor = DataProcessor([1, 2.0, 'test'])
    processor.process()
    assert processor.get_processed_data() == [2, 1.0, 'TEST']
    assert len(processor.get_errors()) == 0

def test_process_with_zero_integer():
    data = [0]
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == [0]
    assert processor.get_errors() == []

def test_process_with_zero_float():
    data = [0.0]
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == [0.0]
    assert processor.get_errors() == []

def test_process_string_with_spaces():
    data = ['hello world']
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == ['HELLO WORLD']
    assert processor.get_errors() == []

def test_process_string_with_numbers():
    data = ['hello123']
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == []
    expected_errors = [{'index': 0, 'error': "Las cadenas deben contener solo letras."}]
    assert processor.get_errors() == expected_errors

def test_process_large_dataset():
    data = list(range(1000)) + [1.5]*500 + ['test']*300
    processor = DataProcessor(data)
    processor.process()
    assert len(processor.get_processed_data()) == 1000 + 500 + 300
    assert len(processor.get_errors()) == 0

def test_process_with_mixed_valid_invalid():
    data = [10, -5, 3.5, 'valid', 'invalid1', 0, 2.2, 'TEST123']
    processor = DataProcessor(data)
    processor.process()
    expected_processed = [20, 1.75, 'VALID', 0, 1.1]
    expected_errors = [
        {'index': 1, 'error': "Los enteros deben ser positivos."},
        {'index': 4, 'error': "Las cadenas deben contener solo letras."},
        {'index': 7, 'error': "Las cadenas deben contener solo letras."}
    ]
    assert processor.get_processed_data() == expected_processed
    assert processor.get_errors() == expected_errors