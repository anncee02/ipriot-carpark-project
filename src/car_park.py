from sensor import Sensor
from display import Display
class CarPark:
    """ Holds the state and behaviours of a car park"""

    def __init__(self,
                 location,
                 capacity,
                 plates = None,
                 sensors = None,
                 displays = None
                 ):
        self.location = location
        self.capacity = capacity
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []
        self.available_bays = self.capacity

    @property
    def get_available_bays(self):
        # car_park.available_bays
        return max(0, self.capacity - len(self.plates))

    def __str__(self):
        return f'Car park at {self.location}, with {self.capacity} bays'

    def register(self, component):
        """Registers components of a car park"""
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Invalid component type")

        if isinstance(component, Sensor):
            self.sensors.append(component)
        elif isinstance(component, Display):
            self.displays.append(component)


    def add_car(self, plate):
        self.plates.append(plate)


    def remove_car(self, plate):
        self.plates.remove(plate)


    def update_displays(self):
        for display in self.displays:
            display.update({"Bays": self.available_bays,
                            "Temperature": 42, }
                            )
            print(f"Updating: {display}")