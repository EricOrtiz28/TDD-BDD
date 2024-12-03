# test_flight_control.py

import pytest
from flight_control import FlightControl

@pytest.fixture
def flight():
    return FlightControl(altitude=0, speed=150, engine_status='on', flaps_position='extended')

# Pruebas para can_takeoff
def test_can_takeoff_true(flight):
    assert flight.can_takeoff() == True

def test_can_takeoff_false_low_speed(flight):
    flight.update_status(speed=140)
    assert flight.can_takeoff() == False

def test_can_takeoff_false_engines_off(flight):
    flight.update_status(engine_status='off')
    assert flight.can_takeoff() == False

def test_can_takeoff_false_flaps_retracted(flight):
    flight.update_status(flaps_position='retracted')
    assert flight.can_takeoff() == False

def test_can_takeoff_false_negative_altitude(flight):
    flight.update_status(altitude=-100)
    assert flight.can_takeoff() == False

# Pruebas para initiate_landing
def test_initiate_landing_true(flight):
    flight.update_status(altitude=10000, speed=200)
    assert flight.initiate_landing() == True

def test_initiate_landing_false_high_altitude(flight):
    flight.update_status(altitude=15000, speed=200)
    assert flight.initiate_landing() == False

def test_initiate_landing_false_high_speed(flight):
    flight.update_status(altitude=10000, speed=250)
    assert flight.initiate_landing() == False

def test_initiate_landing_false_engines_off(flight):
    flight.update_status(altitude=10000, speed=200, engine_status='off')
    assert flight.initiate_landing() == False

def test_initiate_landing_false_flaps_retracted(flight):
    flight.update_status(altitude=10000, speed=200, flaps_position='retracted')
    assert flight.initiate_landing() == False

# Pruebas para emergency_landing
def test_emergency_landing_true_low_altitude(flight):
    flight.update_status(altitude=4000, engine_status='off')
    assert flight.emergency_landing() == True

def test_emergency_landing_true_low_speed(flight):
    flight.update_status(speed=240, engine_status='off')
    assert flight.emergency_landing() == True

def test_emergency_landing_false_high_altitude_speed(flight):
    flight.update_status(altitude=6000, speed=260, engine_status='off')
    assert flight.emergency_landing() == False

def test_emergency_landing_false_engines_on(flight):
    flight.update_status(engine_status='on')
    assert flight.emergency_landing() == False

def test_emergency_landing_false_flaps_retracted(flight):
    flight.update_status(flaps_position='retracted')
    assert flight.emergency_landing() == False

def test_emergency_landing_combined_conditions(flight):
    flight.update_status(altitude=4000, speed=260, engine_status='off', flaps_position='extended')
    assert flight.emergency_landing() == True

# Pruebas para update_status
def test_update_altitude(flight):
    flight.update_status(altitude=5000)
    assert flight.altitude == 5000

def test_update_speed(flight):
    flight.update_status(speed=180)
    assert flight.speed == 180

def test_update_engine_status(flight):
    flight.update_status(engine_status='off')
    assert flight.engine_status == 'off'

def test_update_flaps_position(flight):
    flight.update_status(flaps_position='retracted')
    assert flight.flaps_position == 'retracted'

def test_update_multiple_status(flight):
    flight.update_status(altitude=3000, speed=220, engine_status='off', flaps_position='extended')
    assert flight.altitude == 3000
    assert flight.speed == 220
    assert flight.engine_status == 'off'
    assert flight.flaps_position == 'extended'