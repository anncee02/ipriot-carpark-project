import json
from pathlib import Path
from sensor import Sensor
from display import Display
from datetime import datetime  # we'll use this to timestamp entries


class CarPark:
    """
    Manages car park state, behaviour and associated components.

    The CarPark class handles the addition and removal of cars,
    tracking the number of available parking bays and logging
    activity. It integrates with sensors and displays to provide
    real-time updates on the car park's status.

    Usage:
        Create an instance of the CarPark class, then register sensors and displays.
        Use `add_car` and `remove_car` to manage cars and update the state.
        Call `write_config` and `from_config` to persist and load configurations.
    """

    def __init__(self,
                 location,
                 capacity,
                 plates=None,
                 sensors=None,
                 displays=None,
                 log_file=Path("log.txt"),
                 config_file=Path("config.json")
                 ):
        self.location = location
        self.capacity = capacity
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []
        self.log_file = log_file if isinstance(log_file, Path) else Path(log_file)
        self.config_file = config_file if isinstance(config_file, Path) else Path(config_file)
        # creates the file if it doesn't exist:
        self.log_file.touch(exist_ok=True)
        self.config_file.touch(exist_ok=True)

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

    def remove_car(self, plate):
        self.plates.remove(plate)
        self.update_displays()
        self._log_car_activity(plate, "exited")

    def write_config(self):
        with open("config.json",
                  "w") as f:  # Done - TODO: use self.config_file; use Path; add optional parm to __init__
            json.dump({"location": self.location,
                       "capacity": self.capacity,
                       "log_file": str(self.log_file)}, f)

    # ... inside the CarPark class
    @classmethod
    def from_config(cls, config_file=Path("config.json")):
        config_file = config_file if isinstance(config_file, Path) else Path(config_file)
        with config_file.open() as f:
            config = json.load(f)
        return cls(config["location"], config["capacity"], log_file=config["log_file"])


if __name__ == "__main__":
    car_park = CarPark("Moondalup", 100, config_file="custom_config.json")
    car_park.write_config()
    print(f"Configuration saved to {car_park.config_file}")
