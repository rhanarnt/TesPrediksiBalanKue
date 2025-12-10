import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

class StokKuePredictor:
    def __init__(self):
        self.model = None
        self.model_path = 'stok_model.pkl'
        try:
            self.load_or_train()
        except Exception as e:
            print(f"[WARNING] Model initialization failed: {e}")
            print("[INFO] Using dummy model")
            self.model = None
    
    def load_or_train(self):
        """Load model if exists, otherwise train a new one"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
            else:
                self.train_model()
        except Exception as e:
            print(f"Warning: Could not load model: {e}")
            print("Training new model instead...")
            self.train_model()
    
    def train_model(self):
        """Train a simple Random Forest model with dummy data"""
        # Dummy training data: [jumlah_stok, harga]
        X_train = np.array([
            [10, 5000],
            [20, 10000],
            [15, 7500],
            [30, 15000],
            [25, 12500],
            [5, 2500],
            [40, 20000],
            [35, 17500],
            [12, 6000],
            [18, 9000],
        ])
        
        # Dummy target: permintaan stok yang diprediksi
        y_train = np.array([8, 18, 13, 28, 22, 4, 38, 32, 10, 16])
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Save model
        joblib.dump(self.model, self.model_path)
    
    def predict(self, jumlah, harga):
        """
        Predict stock demand
        Args:
            jumlah: Jumlah stok saat ini
            harga: Harga per satuan
        Returns:
            dict dengan prediksi dan status stok
        """
        try:
            # Prepare input
            X = np.array([[jumlah, harga]])
            
            if self.model is None:
                prediksi = jumlah * 0.8
            else:
                # Make prediction
                prediksi = self.model.predict(X)[0]
            
            # Determine stock status
            if prediksi > jumlah * 0.8:
                status = "Stok Rendah"
            elif prediksi > jumlah * 0.5:
                status = "Stok Sedang"
            else:
                status = "Stok Tinggi"
            
            return {
                'prediksi_permintaan': float(prediksi),
                'status_stok': status
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return {
                'prediksi_permintaan': float(jumlah * 0.8),
                'status_stok': 'Stok Sedang'
            }

# Initialize predictor
predictor = StokKuePredictor()
