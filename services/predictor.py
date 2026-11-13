import pandas as pd
from sklearn.ensemble import RandomForestRegressor


class ParkingPredictor:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
        self.is_trained = False

    def prepare_data(self):
        df = self.data_manager.load_records()

        if df.empty:
            return None

        df["entry_time"] = pd.to_datetime(
            df["entry_time"],
            format="mixed"
        )

        df["day_number"] = df["entry_time"].dt.dayofweek
        df["hour"] = df["entry_time"].dt.hour

        demand_data = (
            df.groupby(["day_number", "hour"])
            .size()
            .reset_index(name="demand")
        )

        return demand_data

    def train_model(self):
        data = self.prepare_data()

        if data is None or len(data) < 10:
            return False

        X = data[["day_number", "hour"]]
        y = data["demand"]

        self.model.fit(X, y)
        self.is_trained = True

        return True

    def predict_demand(self, day_number, hour):
        if not self.is_trained:
            if not self.train_model():
                return None

        prediction = self.model.predict(
            pd.DataFrame(
                [[day_number, hour]],
                columns=["day_number", "hour"]
            )
        )

        return max(0, round(prediction[0]))