class ParkingSlot:
    def __init__(self, slot_number):
        self.__slot_number = slot_number
        self.__vehicle = None

    def get_slot_number(self):
        return self.__slot_number

    def get_vehicle(self):
        return self.__vehicle

    def is_available(self):
        return self.__vehicle is None

    def park_vehicle(self, vehicle):
        if self.is_available():
            self.__vehicle = vehicle
            return True
        return False

    def remove_vehicle(self):
        if not self.is_available():
            vehicle = self.__vehicle
            self.__vehicle = None
            return vehicle
        return None