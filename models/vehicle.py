from abc import ABC, abstractmethod


class Vehicle(ABC):
    def __init__(self, vehicle_number):
        self.__vehicle_number = vehicle_number

    def get_vehicle_number(self):
        return self.__vehicle_number

    @abstractmethod
    def get_vehicle_type(self):
        pass

    @abstractmethod
    def calculate_fee(self, hours):
        pass


class Car(Vehicle):
    def get_vehicle_type(self):
        return "Car"

    def calculate_fee(self, hours):
        return max(50, hours * 30)


class Bike(Vehicle):
    def get_vehicle_type(self):
        return "Bike"

    def calculate_fee(self, hours):
        return max(20, hours * 15)


class ElectricCar(Car):
    def get_vehicle_type(self):
        return "Electric Car"

    def calculate_fee(self, hours):
        return max(60, hours * 35)