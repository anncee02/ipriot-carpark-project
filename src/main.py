from car_park import CarPark
from sensor import EntrySensor, ExitSensor
from display import Display

# Creates a car park object
car_park = CarPark("Moondalup", 100, log_file="moondalup.txt")

# Creates an entry sensor object with id 1, is_active True, and car_park car_park
entry_sensor = EntrySensor(id=1, is_active=True, car_park=car_park)

# Creates an exit sensor object
exit_sensor = ExitSensor(id=2, is_active=True, car_park=car_park)

# Creates a display object
display = Display(id=1, message="Welcome to Moondalup", is_on=True, car_park=car_park)

# Registers sensors and display
car_park.register(entry_sensor)
car_park.register(exit_sensor)
car_park.register(display)

# Drives 10 cars into the car park
for i in range(10):
    entry_sensor.detect_vehicle()

# Drives 2 cars out of the car park
for i in range(2):
    exit_sensor.detect_vehicle()

# Saves car park configuration
car_park.write_config()

print("Simulation complete. Config and logs updated.")