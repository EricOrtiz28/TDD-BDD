# order_processor.py

class OrderProcessor:
    def __init__(self):
        self.orders = []
        self.processed_orders = []
        self.failed_orders = []

    def add_order(self, order):
        if not isinstance(order, dict):
            raise TypeError("La orden debe ser un diccionario.")
        if 'id' not in order or 'amount' not in order:
            raise ValueError("La orden debe contener 'id' y 'amount'.")
        self.orders.append(order)

    def process_orders(self):
        for order in self.orders:
            try:
                self._process_order(order)
                self.processed_orders.append(order)
            except Exception as e:
                self.failed_orders.append({'order': order, 'error': str(e)})

    def _process_order(self, order):
        if order['amount'] <= 0:
            raise ValueError(f"Orden {order['id']} tiene un monto inválido.")
        # Simulación de procesamiento (e.g., interacción con una API externa)
        if order.get('simulate_failure'):
            raise RuntimeError(f"Error al procesar la orden {order['id']}.")
        # Supongamos que el procesamiento implica descuentos
        if 'discount' in order:
            order['final_amount'] = order['amount'] - (order['amount'] * order['discount'])
        else:
            order['final_amount'] = order['amount']

    def get_order_status(self, order_id):
        for order in self.processed_orders:
            if order['id'] == order_id:
                return 'Procesada'
        for failed in self.failed_orders:
            if failed['order']['id'] == order_id:
                return f"Fallida: {failed['error']}"
        return 'Pendiente'