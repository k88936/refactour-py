from car import Car


class Driver:
    def __init__(self, car: Car) -> None:
        self._car = car

    def _start(self) -> None:
        self._car.engine_started = True
        self._car.gear = 1

    def _stop(self) -> None:
        self._car.gear = 0
        self._car.engine_started = False

    def change_car(self, car: Car) -> None:
        self._car = car

    def _driving(self, destination: str) -> None:
        print(f"The driver is coming to {destination}")

    def drive_to(self, destination: str) -> None:
        print("Start driving")
        self._start()
        self._driving(destination)
        self._stop()
        print("Arrived at destination")

