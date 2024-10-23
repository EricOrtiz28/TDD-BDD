import json
import pytest
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Configura la base de datos antes y después de todas las pruebas"""
    # Se ejecuta antes de todas las pruebas
    db.create_all()
    yield
    # Se ejecuta después de todas las pruebas
    db.session.close()

class TestAccountModel:
    """Modelo de Pruebas de Cuenta"""

    @classmethod
    def setup_class(cls):
        """Conectar y cargar los datos necesarios para las pruebas"""
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)
        print(f"ACCOUNT_DATA cargado: {ACCOUNT_DATA}")

    @classmethod
    def teardown_class(cls):
        """Desconectar de la base de datos"""
        pass  # Agrega cualquier acción de limpieza si es necesario

    def setup_method(self):
        """Truncar las tablas antes de cada prueba"""
        db.session.query(Account).delete()
        db.session.commit()

    def teardown_method(self):
        """Eliminar la sesión después de cada prueba"""
        db.session.remove()

    ######################################################################
    #  C A S O S   D E   P R U E B A
    ######################################################################

    def test_create_an_account(self):
        """Probar la creación de una sola cuenta"""
        data = ACCOUNT_DATA[0]  # obtener la primera cuenta
        account = Account(**data)
        account.create()
        assert len(Account.all()) == 1

    def test_create_all_accounts(self):
        """Probar la creación de múltiples cuentas"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        assert len(Account.all()) == len(ACCOUNT_DATA)

    def test_repr(self):
        """Prueba la representación de una cuenta"""
        account = Account()
        account.name = "Foo"
        assert str(account) == "<Account 'Foo'>"

    def test_to_dict(self):
        """Prueba la conversión de una cuenta a diccionario"""
        # Seleccionar una cuenta aleatoria de ACCOUNT_DATA
        random_key = random.randint(0, len(ACCOUNT_DATA) - 1)
        data = ACCOUNT_DATA[random_key]  # obtener una cuenta aleatoria
        account = Account(**data)
        result = account.to_dict()

        # Verificar que los datos convertidos a diccionario sean correctos
        assert account.name == result["name"]
        assert account.email == result["email"]
        assert account.phone_number == result["phone_number"]
        assert account.disabled == result["disabled"]
        assert account.date_joined == result["date_joined"]

    def test_from_dict(self):
        """Prueba establecer atributos de una cuenta desde un diccionario"""
        # Seleccionar una cuenta aleatoria de ACCOUNT_DATA
        random_key = random.randint(0, len(ACCOUNT_DATA) - 1)
        data = ACCOUNT_DATA[random_key]  # obtener una cuenta aleatoria
        account = Account()
        account.from_dict(data)
        assert account.name == data["name"]
        assert account.email == data["email"]
        assert account.phone_number == data["phone_number"]
        assert account.disabled == data["disabled"]

    def test_update_account(self):
        """Prueba la actualización de una cuenta utilizando datos conocidos"""
        # Seleccionar una cuenta aleatoria de ACCOUNT_DATA
        random_key = random.randint(0, len(ACCOUNT_DATA) - 1)
        data = ACCOUNT_DATA[random_key]  # obtener una cuenta aleatoria
        account = Account(**data)
        account.create()
        assert account.id is not None
        account.name = "Rumpelstiltskin"
        account.update()
        found = Account.find(account.id)
        assert found.name == account.name

    def test_update_invalid_id(self):
        """Prueba la actualización de una cuenta con ID inválido"""
        # Seleccionar una cuenta aleatoria de ACCOUNT_DATA
        random_key = random.randint(0, len(ACCOUNT_DATA) - 1)
        data = ACCOUNT_DATA[random_key]  # obtener una cuenta aleatoria
        account = Account(**data)
        account.id = None
        with pytest.raises(DataValidationError):
            account.update()

    def test_delete_account(self):
        """Prueba la eliminación de una cuenta utilizando datos conocidos"""
        # Seleccionar una cuenta aleatoria de ACCOUNT_DATA
        random_key = random.randint(0, len(ACCOUNT_DATA) - 1)
        data = ACCOUNT_DATA[random_key]  # obtener una cuenta aleatoria
        account = Account(**data)
        account.create()
        assert len(Account.all()) == 1
        account.delete()
        assert len(Account.all()) == 0