import os
import pandas as pd


class DataManager:
    def __init__(self, file_path="data/parking_history.csv"):
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            columns = [
                "ticket_id",
                "vehicle_number",
                "vehicle_type",
                "slot_number",
                "entry_time",
                "exit_time",
                "entry_day",
                "entry_hour",
                "duration_hours",
                "fee"
            ]

            pd.DataFrame(columns=columns).to_csv(
                self.file_path,
                index=False
            )

    def save_record(self, ticket):
        entry_time = ticket.get_entry_time()
        exit_time = ticket.get_exit_time()

        record = {
            "ticket_id": ticket.get_ticket_id(),
            "vehicle_number": ticket.get_vehicle().get_vehicle_number(),
            "vehicle_type": ticket.get_vehicle().get_vehicle_type(),
            "slot_number": ticket.get_slot_number(),
            "entry_time": entry_time,
            "exit_time": exit_time,
            "entry_day": entry_time.strftime("%A"),
            "entry_hour": entry_time.hour,
            "duration_hours": round(
                ticket.get_duration_hours(), 2
            ),
            "fee": ticket.get_fee()
        }

        df = pd.read_csv(self.file_path)

        df = pd.concat(
            [df, pd.DataFrame([record])],
            ignore_index=True
        )

        df.to_csv(self.file_path, index=False)

    def load_records(self):
        return pd.read_csv(self.file_path)