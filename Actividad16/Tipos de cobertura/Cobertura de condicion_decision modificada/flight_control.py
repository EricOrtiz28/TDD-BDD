
class FlightControl:
    def __init__(self, altitude, speed, engine_status, flaps_position):
        self.altitude = altitude 
        self.speed = speed
        self.engine_status = engine_status
        self.flaps_position = flaps_position

    def can_takeoff(self):
        altitude_ok = self.altitude >= 0
        speed_ok = self.speed >= 150
        engines_ok = self.engine_status == 'on'
        flaps_ok = self.flaps_position == 'extended'
        return altitude_ok and speed_ok and engines_ok and flaps_ok

    def initiate_landing(self):
        altitude_ok = self.altitude <= 10000
        speed_ok = self.speed <= 200
        engines_ok = self.engine_status == 'on'
        flaps_ok = self.flaps_position == 'extended'
        return altitude_ok and speed_ok and engines_ok and flaps_ok

    def emergency_landing(self):
        altitude_ok = self.altitude < 5000
        engines_ok = self.engine_status == 'off'
        flaps_ok = self.flaps_position == 'extended'
        speed_ok = self.speed < 250
        return (altitude_ok or speed_ok) and (engines_ok and flaps_ok)

    def update_status(self, altitude=None, speed=None, engine_status=None, flaps_position=None):
        if altitude is not None:
            self.altitude = altitude
        if speed is not None:
            self.speed = speed
        if engine_status is not None:
            self.engine_status = engine_status
        if flaps_position is not None:
            self.flaps_position = flaps_position