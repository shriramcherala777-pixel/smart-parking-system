import streamlit as st
import plotly.express as px

from models.parking_lot import ParkingLot
from models.vehicle import Car, Bike, ElectricCar
from services.data_manager import DataManager
from services.analytics import ParkingAnalytics
from services.predictor import ParkingPredictor
from utils.parking_map import display_parking_map


st.set_page_config(
    page_title="Smart Parking System",
    page_icon="🅿️",
    layout="wide"
)


if "parking_lot" not in st.session_state:
    st.session_state.parking_lot = ParkingLot(total_slots=20)

if "predictor" not in st.session_state:
    data_manager = DataManager()
    predictor = ParkingPredictor(data_manager)
    predictor.train_model()
    st.session_state.predictor = predictor


parking_lot = st.session_state.parking_lot
data_manager = DataManager()
analytics = ParkingAnalytics(data_manager)
predictor = st.session_state.predictor


# ---------------- SIDEBAR ----------------

st.sidebar.title("🅿️ Parking Controls")

st.sidebar.subheader("🚗 Vehicle Entry")

with st.sidebar.form("entry_form", clear_on_submit=True):
    vehicle_number = st.text_input("Vehicle Number")
    vehicle_type = st.selectbox(
        "Vehicle Type",
        ["Car", "Bike", "Electric Car"]
    )

    submit_entry = st.form_submit_button("Park Vehicle")


if submit_entry:
    vehicle_number = vehicle_number.strip().upper()

    if not vehicle_number:
        st.sidebar.error("Please enter a vehicle number.")
    else:
        if vehicle_type == "Car":
            vehicle = Car(vehicle_number)
        elif vehicle_type == "Bike":
            vehicle = Bike(vehicle_number)
        else:
            vehicle = ElectricCar(vehicle_number)

        ticket = parking_lot.park_vehicle(vehicle)

        if ticket:
            st.sidebar.success(
                f"Vehicle parked in {ticket.get_slot_number()}"
            )
        else:
            st.sidebar.error(
                "Vehicle already exists or no slots are available."
            )


st.sidebar.divider()

st.sidebar.subheader("🚪 Vehicle Exit")

with st.sidebar.form("exit_form", clear_on_submit=True):
    exit_vehicle_number = st.text_input(
        "Vehicle Number to Exit"
    )

    submit_exit = st.form_submit_button("Exit Vehicle")


if submit_exit:
    exit_vehicle_number = exit_vehicle_number.strip().upper()

    if not exit_vehicle_number:
        st.sidebar.error("Please enter a vehicle number.")
    else:
        result = parking_lot.exit_vehicle(exit_vehicle_number)

        if result:
            st.sidebar.success(
                f"Vehicle exited successfully!\n\n"
                f"Slot: {result['slot_number']}\n\n"
                f"Parking Fee: ₹{result['fee']:.2f}"
            )
        else:
            st.sidebar.error("Vehicle not found.")


# ---------------- MAIN DASHBOARD ----------------

st.title("🅿️ Smart Parking Management System")
st.write("Real-time parking monitoring, analytics and demand prediction")


tab1, tab2, tab3 = st.tabs([
    "🅿️ Live Parking",
    "📊 Analytics",
    "🤖 ML Prediction"
])


# ---------------- LIVE PARKING ----------------

with tab1:
    stats = parking_lot.get_statistics()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Slots", stats["total_slots"])
    col2.metric("Available Slots", stats["available_slots"])
    col3.metric("Occupied Slots", stats["occupied_slots"])
    col4.metric(
        "Occupancy",
        f"{stats['occupancy_percentage']}%"
    )

    st.divider()

    st.subheader("🗺️ Live Parking Lot Status")
    st.caption("🟢 Available   |   🔴 Occupied")

    display_parking_map(parking_lot)


# ---------------- ANALYTICS ----------------

with tab2:
    data = analytics.get_data()

    if data.empty:
        st.warning("No historical parking data available.")

    else:
        rush_hour = analytics.get_rush_hour()
        busiest_day = analytics.get_busiest_day()
        highest_income_day = analytics.get_highest_income_day()
        lowest_income_day = analytics.get_lowest_income_day()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rush Hour", f"{rush_hour}:00")
        col2.metric("Busiest Day", busiest_day)
        col3.metric("Highest Income Day", highest_income_day)
        col4.metric("Lowest Income Day", lowest_income_day)

        st.divider()

        hourly_data = analytics.get_hourly_data()

        fig_hourly = px.bar(
            hourly_data,
            x="entry_hour",
            y="vehicles",
            title="Vehicle Traffic by Hour",
            labels={
                "entry_hour": "Hour of Day",
                "vehicles": "Number of Vehicles"
            }
        )

        st.plotly_chart(
            fig_hourly,
            use_container_width=True
        )

        col1, col2 = st.columns(2)

        with col1:
            daily_income = analytics.get_daily_income()

            fig_income = px.bar(
                daily_income,
                x="day",
                y="income",
                title="Income by Day",
                labels={
                    "day": "Day",
                    "income": "Income (₹)"
                }
            )

            st.plotly_chart(
                fig_income,
                use_container_width=True
            )

        with col2:
            vehicle_data = analytics.get_vehicle_distribution()

            fig_vehicle = px.pie(
                vehicle_data,
                names="vehicle_type",
                values="count",
                title="Vehicle Type Distribution"
            )

            st.plotly_chart(
                fig_vehicle,
                use_container_width=True
            )


# ---------------- ML PREDICTION ----------------

with tab3:
    st.subheader("🤖 Parking Demand Prediction")

    st.write(
        "Predict the expected number of vehicle arrivals "
        "based on the selected day and time."
    )

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    selected_day = st.selectbox(
        "Select Day",
        days
    )

    selected_hour = st.slider(
        "Select Hour",
        min_value=0,
        max_value=23,
        value=9
    )

    day_number = days.index(selected_day)

    if st.button("Predict Parking Demand"):
        prediction = predictor.predict_demand(
            day_number,
            selected_hour
        )

        if prediction is not None:
            st.metric(
                "Predicted Vehicle Arrivals",
                f"{prediction} vehicles"
            )

            if prediction >= 60:
                st.error(
                    "High demand expected. Parking may become crowded."
                )
            elif prediction >= 35:
                st.warning(
                    "Moderate demand expected."
                )
            else:
                st.success(
                    "Low demand expected. Parking should be available."
                )
        else:
            st.error(
                "Not enough historical data to make a prediction."
            )

    st.caption(
        "Prediction is based on synthetic historical parking data "
        "generated for this project prototype."
    )