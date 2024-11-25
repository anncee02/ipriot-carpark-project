import unittest
from car_park import CarPark
from sensor import EntrySensor, ExitSensor


class TestCarPark(unittest.TestCase):
    def setUp(self):
        self.car_park = CarPark("123 Example Street", 100)
        self.entry_sensor = EntrySensor(id=1, car_park=self.car_park, is_active=True)
        self.exit_sensor = ExitSensor(id=2, car_park=self.car_park, is_active=True)

    def test_entry_sensor_adds_car_to_car_park(self):
        self.assertEqual(self.car_park.available_bays, 100)
        self.entry_sensor.update_car_park("TEST-001")
        self.assertEqual(self.car_park.plates, ["TEST-001"])
        self.assertEqual(self.car_park.available_bays, 99)

    def test_exit_sensor_removes_car_from_car_park(self):
        self.car_park.add_car("TEST-001")  # Add a car manually
        self.assertEqual(self.car_park.available_bays, 99)
        self.assertEqual(self.car_park.plates, ["TEST-001"])

        self.exit_sensor.update_car_park("TEST-001")
        self.assertEqual(self.car_park.plates, [])
        self.assertEqual(self.car_park.available_bays, 100)

    if __name__ == "__main__":
        unittest.main()
