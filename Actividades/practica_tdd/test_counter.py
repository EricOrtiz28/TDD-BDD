"""
Casos de prueba para el servicio web de contador
"""
import pytest
from counter import app
from http import HTTPStatus
import status


@pytest.fixture
def client():
    # Configuración del cliente de prueba de Flask
    with app.test_client() as client:
        # Limpieza antes de cada prueba
        client.delete("/counters/test_counter")
        yield client  # Proveer el cliente para la prueba
        # Limpieza después de cada prueba (en este caso, se asegura que no existan contadores)
        client.delete("/counters/test_counter")

def test_create_a_counter(client):
    """Debe crear un contador"""
    # Arrange: No hay configuración previa específica necesaria

    # Act: Creamos un nuevo contador
    result = client.post("/counters/test_counter")

    # Assert: Verificamos que el contador fue creado exitosamente
    assert result.status_code == HTTPStatus.CREATED
    data = result.get_json()
    assert "test_counter" in data
    assert data["test_counter"] == 0

def test_duplicate_counter(client):
    """Debe devolver un error para duplicados"""
    # Arrange: Crear el contador inicial
    result = client.post("/counters/test_counter")

    # Act: Intentar crear el mismo contador nuevamente
    result = client.post("/counters/test_counter")

    # Assert: Verificamos que devuelve un error de conflicto
    assert result.status_code == status.HTTP_409_CONFLICT

def test_update_counter(client):
    """verifica si fue actualizado"""
     # Arrange: Crear el contador y obtener el valor actual del contador
    client.post("/counters/test_counter")
    result = client.get("/counters/test_counter")
    data = result.get_json()
    old_counter = data["message"]

    # Act: Actualizar el contador
    result = client.put("/counters/test_counter")

    # Assert: Verificamos la actualización del contador
    assert result.status_code == status.HTTP_200_OK
    new_data = result.get_json()
    new_counter = new_data["update_message"]
    assert old_counter == new_counter - 1

def test_get_counter(client):
    """verifica si fue actualizado"""
    # Arrange: Crear el contador
    client.post("/counters/test_counter")

    # Act: Obtener el valor del contador
    result = client.get("/counters/test_counter")

    # Assert: Verificamos que el contador se obtiene correctamente
    assert result.status_code == status.HTTP_200_OK

def test_set_value(client):
    """Probemos seteando un valor"""
    # Arrange: Crear el contador y definir el valor deseado
    client.post("/counters/test_counter")
    value = {"value":4}

    # Act: Establecer el valor en el contador
    result = client.put("/counters/test_counter/set", json = value)

    # Assert: Verificamos que el valor fue establecido correctamente
    assert result.status_code == status.HTTP_200_OK
    result = client.get("/counters/test_counter")
    data = result.get_json()
    assert data["message"] == value["value"]

def test_delete_counter(client):
    """Eliminar algun usuario"""
    # Arrange: Crear el contador
    client.post("/counters/test_counter")

    # Act: Eliminamos el contador
    result = client.delete("/counters/test_counter")

    # Assert: Verificamos que el contador ha sido eliminado correctamente
    assert result.status_code == status.HTTP_200_OK
    result = client.get("/counters/test_counter")
    assert result.status_code == status.HTTP_404_NOT_FOUND

