from abc import ABC, abstractmethod
import random

class Sensor(ABC):
    """Provides sensors to detect cars"""
    def __init__(self,
                 id,
                 car_park,
                 is_active = False
                 ):
        self.id = id
        self.car_park = car_park
        self.is_active = is_active

    def _scan_plate(self):
        return "FAKE-" + format(random.radint(0, 999), '03d')

    @abstractmethod
    def update_car_park(self, plate):
        pass

    def detect_vehicle(self):
        plate = self._scan_plate()
        self.update_car_park(plate)

    def __str(self):
        return f'{self.id}: Sensor is {"is active" if self.is_active else "if active"}'

class EntrySensor(Sensor):

    def update_car_park(self, plate):
        self.car_park.add_car(plate)
        print(f"Incoming 🚘 vehicle detected. Plate: {plate}")

class ExitSensor(Sensor):

    def _scan_plate(self):
        # To demo scan on exit
        return random.choice(self.car_park.plates)

    def update_car_park(self, plate):
        self.car_park.remove_car(plate)
        print(f"Outgoing 🚗 vehicle detected. Plate: {plate}")