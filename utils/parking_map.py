import streamlit as st


def display_parking_map(parking_lot):
    slots = parking_lot.get_slots()
    columns_per_row = 5

    for start in range(0, len(slots), columns_per_row):
        row_slots = slots[start:start + columns_per_row]
        columns = st.columns(columns_per_row)

        for column, slot in zip(columns, row_slots):
            with column:
                if slot.is_available():
                    st.success(
                        f"🅿️ **{slot.get_slot_number()}**\n\n"
                        "Available"
                    )
                else:
                    vehicle = slot.get_vehicle()

                    st.error(
                        f"🚗 **{slot.get_slot_number()}**\n\n"
                        f"{vehicle.get_vehicle_number()}\n\n"
                        f"{vehicle.get_vehicle_type()}"
                    )