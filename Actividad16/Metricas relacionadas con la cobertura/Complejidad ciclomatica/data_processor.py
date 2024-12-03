# data_processor.py

class DataProcessor:
    def __init__(self, data):
        if not isinstance(data, list):
            raise TypeError("Data debe ser una lista.")
        self.data = data
        self.processed_data = []
        self.errors = []

    def process(self):
        for index, item in enumerate(self.data):
            try:
                if isinstance(item, int):
                    self.process_integer(item)
                elif isinstance(item, float):
                    self.process_float(item)
                elif isinstance(item, str):
                    self.process_string(item)
                else:
                    raise ValueError(f"Tipo de dato no soportado: {type(item)}")
            except Exception as e:
                self.errors.append({'index': index, 'error': str(e)})

    def process_integer(self, item):
        if item < 0:
            raise ValueError("Los enteros deben ser positivos.")
        result = item * 2
        self.processed_data.append(result)

    def process_float(self, item):
        if item < 0.0:
            raise ValueError("Los floats deben ser positivos.")
        result = round(item / 2, 2)
        self.processed_data.append(result)

    def process_string(self, item):
        if not item.isalpha():
            raise ValueError("Las cadenas deben contener solo letras.")
        result = item.upper()
        self.processed_data.append(result)

    def get_processed_data(self):
        return self.processed_data

    def get_errors(self):
        return self.errors

    def summarize(self):
        summary = {
            'total_items': len(self.data),
            'processed_items': len(self.processed_data),
            'errors': len(self.errors)
        }
        return summary