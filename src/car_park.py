from sensor import Sensor
from display import Display
from pathlib import Path
from datetime import datetime # we'll use this to timestamp entries

class CarPark:
    """ Holds the state and behaviours of a car park"""

    def __init__(self,
                 location,
                 capacity,
                 plates = None,
                 sensors = None,
                 displays = None,
                 log_file=Path("log.txt")
                 ):
        self.location = location
        self.capacity = capacity
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []
        self.log_file = log_file if isinstance(log_file, Path) else Path(log_file)
        # creates the file if it doesn't exist:
        self.log_file.touch(exist_ok=True)

    @property
    def available_bays(self):
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
        if len(self.plates) < self.capacity and plate not in self.plates:
            self.plates.append(plate)


    def remove_car(self, plate):
        if plate in self.plates:
            self.plates.remove(plate)
        else:
            raise ValueError(f"Car with plate '{plate}' not found in the car park.")


    def update_displays(self):
        for display in self.displays:
            display.update({"Bays": self.available_bays,
                            "Temperature": 42, }
                            )
            print(f"Updating: {display}")

    def _log_car_activity(self, plate, action):
        with self.log_file.open("a") as f:
            f.write(f"{plate} {action} at {datetime.now():%Y-%m-%d %H:%M:%S}\n")

    def add_car(self, plate):
        self.plates.append(plate)
        self.update_displays()
        self._log_car_activity(plate, "entered")