import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_models(data_path="data/penjualan.csv"):
    df = pd.read_csv(data_path)

    # misal dataset punya kolom: jumlah, harga, permintaan, status_stok
    X = df[["jumlah", "harga"]]
    y_reg = df["permintaan"]
    y_cls = df["status_stok"]

    # Linear Regression
    lr = LinearRegression()
    lr.fit(X, y_reg)

    # Random Forest
    rf = RandomForestClassifier()
    rf.fit(X, y_cls)

    # Simpan model
    joblib.dump(lr, "app/lr_model.pkl")
    joblib.dump(rf, "app/rf_model.pkl")

    print("✅ Model berhasil dilatih dan disimpan.")

if __name__ == "__main__":
    train_models()
