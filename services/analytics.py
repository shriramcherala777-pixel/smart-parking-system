import pandas as pd


class ParkingAnalytics:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def get_data(self):
        df = self.data_manager.load_records()

        if df.empty:
            return df
        
        df["entry_time"] = pd.to_datetime(
            df["entry_time"],
            format="mixed"
        )

        df["exit_time"] = pd.to_datetime(
            df["exit_time"],
            format="mixed"
        )

        return df

    def get_rush_hour(self):
        df = self.get_data()

        if df.empty:
            return None

        return df["entry_hour"].value_counts().idxmax()

    def get_busiest_day(self):
        df = self.get_data()

        if df.empty:
            return None

        return df["entry_day"].value_counts().idxmax()

    def get_highest_income_day(self):
        df = self.get_data()

        if df.empty:
            return None

        df["exit_day"] = df["exit_time"].dt.day_name()
        return df.groupby("exit_day")["fee"].sum().idxmax()

    def get_lowest_income_day(self):
        df = self.get_data()

        if df.empty:
            return None

        df["exit_day"] = df["exit_time"].dt.day_name()
        return df.groupby("exit_day")["fee"].sum().idxmin()

    def get_hourly_data(self):
        df = self.get_data()

        if df.empty:
            return pd.DataFrame()

        return (
            df.groupby("entry_hour")
            .size()
            .reset_index(name="vehicles")
            .sort_values("entry_hour")
        )

    def get_daily_income(self):
        df = self.get_data()

        if df.empty:
            return pd.DataFrame()

        df["exit_day"] = df["exit_time"].dt.day_name()

        day_order = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ]

        result = (
            df.groupby("exit_day")["fee"]
            .sum()
            .reindex(day_order, fill_value=0)
            .reset_index()
        )

        result.columns = ["day", "income"]
        return result

    def get_vehicle_distribution(self):
        df = self.get_data()

        if df.empty:
            return pd.DataFrame()

        result = df["vehicle_type"].value_counts().reset_index()
        result.columns = ["vehicle_type", "count"]

        return result