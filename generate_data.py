import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

records = []
start_date = datetime.now() - timedelta(days=180)
ticket_counter = 1

vehicle_types = {
    "Car": {"rate": 30, "minimum": 50},
    "Bike": {"rate": 15, "minimum": 20},
    "Electric Car": {"rate": 35, "minimum": 60}
}

for day_offset in range(180):
    current_date = start_date + timedelta(days=day_offset)
    weekday = current_date.weekday()

    if weekday < 5:
        vehicles_today = random.randint(45, 75)
    else:
        vehicles_today = random.randint(30, 55)

    for _ in range(vehicles_today):

        rush_hours = (
            list(range(8, 11)) * 3
            + list(range(17, 21)) * 4
            + list(range(11, 17))
            + list(range(21, 24))
        )

        hour = random.choice(rush_hours)
        minute = random.randint(0, 59)

        entry_time = current_date.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        duration_hours = round(random.uniform(1, 6), 2)
        exit_time = entry_time + timedelta(hours=duration_hours)

        vehicle_type = random.choices(
            ["Car", "Bike", "Electric Car"],
            weights=[65, 25, 10]
        )[0]

        rate = vehicle_types[vehicle_type]["rate"]
        minimum = vehicle_types[vehicle_type]["minimum"]
        fee = round(max(minimum, duration_hours * rate), 2)

        record = {
            "ticket_id": f"T{ticket_counter:05d}",
            "vehicle_number": (
                f"TS{random.randint(1, 99):02d}"
                f"AB{random.randint(1000, 9999)}"
            ),
            "vehicle_type": vehicle_type,
            "slot_number": f"S{random.randint(1, 20)}",
            "entry_time": entry_time,
            "exit_time": exit_time,
            "entry_day": entry_time.strftime("%A"),
            "entry_hour": entry_time.hour,
            "duration_hours": duration_hours,
            "fee": fee
        }

        records.append(record)
        ticket_counter += 1


df = pd.DataFrame(records)

df.to_csv("data/parking_history.csv", index=False)

print(f"Generated {len(df)} parking records.")
print("Data saved to data/parking_history.csv")