from models.parking_slot import ParkingSlot
from models.parking_ticket import ParkingTicket
from services.data_manager import DataManager


class ParkingLot:
    def __init__(self, total_slots=20):
        self.__slots = []
        self.__active_tickets = {}
        self.__ticket_counter = 1
        self.__data_manager = DataManager()

        for i in range(total_slots):
            slot_number = f"S{i + 1}"
            self.__slots.append(ParkingSlot(slot_number))

    def get_slots(self):
        return self.__slots

    def get_available_slots(self):
        return [
            slot for slot in self.__slots
            if slot.is_available()
        ]

    def get_occupied_slots(self):
        return [
            slot for slot in self.__slots
            if not slot.is_available()
        ]

    def park_vehicle(self, vehicle):
        vehicle_number = vehicle.get_vehicle_number()

        if self.find_vehicle(vehicle_number):
            return None

        for slot in self.__slots:
            if slot.is_available():
                slot.park_vehicle(vehicle)

                ticket_id = f"T{self.__ticket_counter:04d}"

                ticket = ParkingTicket(
                    ticket_id,
                    vehicle,
                    slot.get_slot_number()
                )

                self.__active_tickets[vehicle_number] = ticket
                self.__ticket_counter += 1

                return ticket

        return None

    def find_vehicle(self, vehicle_number):
        for slot in self.__slots:
            vehicle = slot.get_vehicle()

            if vehicle and vehicle.get_vehicle_number() == vehicle_number:
                return slot

        return None

    def exit_vehicle(self, vehicle_number):
        slot = self.find_vehicle(vehicle_number)

        if slot is None:
            return None

        ticket = self.__active_tickets.get(vehicle_number)

        if ticket is None:
            return None

        fee = ticket.close_ticket()
        vehicle = slot.remove_vehicle()

        self.__data_manager.save_record(ticket)

        del self.__active_tickets[vehicle_number]

        return {
            "vehicle": vehicle,
            "ticket": ticket,
            "fee": fee,
            "slot_number": slot.get_slot_number()
        }

    def get_statistics(self):
        total = len(self.__slots)
        available = len(self.get_available_slots())
        occupied = total - available

        occupancy = 0
        if total > 0:
            occupancy = round((occupied / total) * 100, 2)

        return {
            "total_slots": total,
            "available_slots": available,
            "occupied_slots": occupied,
            "occupancy_percentage": occupancy
        }