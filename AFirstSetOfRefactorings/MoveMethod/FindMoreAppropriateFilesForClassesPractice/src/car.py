class Car:
    def __init__(self, gears_number: int) -> None:
        self._gears_number = gears_number
        self.engine_started = False
        self._gear = 0

    @property
    def gear(self) -> int:
        return self._gear

    @gear.setter
    def gear(self, value: int) -> None:
        if value > self._gears_number or value < 0:
            raise RuntimeError("Invalid gear")
        self._gear = value
