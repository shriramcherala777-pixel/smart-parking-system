from datetime import datetime


class ParkingTicket:
    def __init__(self, ticket_id, vehicle, slot_number):
        self.__ticket_id = ticket_id
        self.__vehicle = vehicle
        self.__slot_number = slot_number
        self.__entry_time = datetime.now()
        self.__exit_time = None
        self.__fee = None

    def get_ticket_id(self):
        return self.__ticket_id

    def get_vehicle(self):
        return self.__vehicle

    def get_slot_number(self):
        return self.__slot_number

    def get_entry_time(self):
        return self.__entry_time

    def get_exit_time(self):
        return self.__exit_time

    def get_fee(self):
        return self.__fee

    def close_ticket(self):
        self.__exit_time = datetime.now()

        duration = self.__exit_time - self.__entry_time
        hours = max(1, duration.total_seconds() / 3600)

        self.__fee = self.__vehicle.calculate_fee(hours)
        return self.__fee

    def get_duration_hours(self):
        end_time = self.__exit_time or datetime.now()
        duration = end_time - self.__entry_time
        return duration.total_seconds() / 3600