"""
Advanced Prediction Service for Stock Management
Handles detailed predictions for raw materials with ML models
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import joblib
import os
import json

class AdvancedPredictionService:
    """Advanced prediction service with multiple algorithms"""
    
    def __init__(self):
        self.rf_model = None
        self.gb_model = None
        self.scaler = None
        self.model_dir = 'models'
        self.create_model_dir()
        self.load_or_train_models()
    
    def create_model_dir(self):
        """Create models directory if it doesn't exist"""
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
    
    def load_or_train_models(self):
        """Load existing models or train new ones"""
        try:
            rf_path = os.path.join(self.model_dir, 'rf_predictor.pkl')
            if os.path.exists(rf_path):
                self.rf_model = joblib.load(rf_path)
            else:
                self.train_rf_model()
        except Exception as e:
            print(f"[WARNING] Could not load RF model: {e}")
            self.train_rf_model()
    
    def train_rf_model(self):
        """Train Random Forest regression model"""
        # Expanded training data for better predictions
        X_train = np.array([
            [100, 5000, 1, 50],      # jumlah, harga, status_stok, hari_terjual
            [150, 7500, 1, 45],
            [80, 4000, 0, 20],
            [200, 10000, 1, 60],
            [120, 6000, 1, 40],
            [90, 4500, 0, 25],
            [180, 9000, 1, 55],
            [110, 5500, 1, 35],
            [75, 3750, 0, 15],
            [220, 11000, 1, 65],
            [140, 7000, 1, 48],
            [95, 4750, 0, 22],
            [170, 8500, 1, 52],
            [125, 6250, 1, 42],
            [85, 4250, 0, 18],
        ])
        
        # Target: predicted demand
        y_train = np.array([95, 140, 70, 190, 110, 80, 170, 105, 65, 210, 130, 85, 160, 120, 75])
        
        # Train model
        self.rf_model = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=3,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.rf_model.fit(X_train, y_train)
        
        # Save model
        joblib.dump(self.rf_model, os.path.join(self.model_dir, 'rf_predictor.pkl'))
        print("[INFO] Random Forest model trained and saved")
    
    def predict_demand(self, jumlah, harga, status_stok=1, hari_terjual=30):
        """
        Predict demand for a raw material
        
        Args:
            jumlah: Quantity (int/float)
            harga: Price (int/float)
            status_stok: Stock status (0=low, 1=normal, 2=high)
            hari_terjual: Days sold historically (int)
        
        Returns:
            dict: Prediction results with confidence and recommendation
        """
        try:
            if self.rf_model is None:
                return {
                    'error': 'Model tidak tersedia',
                    'status': 'error'
                }
            
            # Prepare features
            X = np.array([[jumlah, harga, status_stok, hari_terjual]])
            
            # Predict
            prediction = self.rf_model.predict(X)[0]
            
            # Calculate confidence (0-100%)
            confidence = min(85 + (hari_terjual / 100), 99)
            
            # Generate recommendation
            recommendation = self._generate_recommendation(
                jumlah=jumlah,
                prediction=prediction,
                harga=harga,
                status_stok=status_stok
            )
            
            return {
                'prediksi': float(prediction),
                'confidence': float(confidence),
                'recommendation': recommendation,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def predict_material_detail(self, bahan_id, current_stock, stok_minimum, stok_optimal, 
                                harga_per_unit, recent_days=30):
        """
        Predict detailed stock information for a specific material
        
        Args:
            bahan_id: Material ID
            current_stock: Current stock quantity
            stok_minimum: Minimum stock level
            stok_optimal: Optimal stock level
            harga_per_unit: Price per unit
            recent_days: Days of history to consider
        
        Returns:
            dict: Detailed prediction and recommendations
        """
        try:
            # Status determination
            if current_stock <= stok_minimum:
                status_stok = 0  # Low
            elif current_stock >= stok_optimal:
                status_stok = 2  # High
            else:
                status_stok = 1  # Normal
            
            # Get prediction
            prediction_result = self.predict_demand(
                jumlah=current_stock,
                harga=harga_per_unit,
                status_stok=status_stok,
                hari_terjual=recent_days
            )
            
            if prediction_result['status'] != 'success':
                return prediction_result
            
            predicted_demand = prediction_result['prediksi']
            
            # Calculate days until stockout
            if predicted_demand > 0:
                days_until_stockout = (current_stock / predicted_demand) * 30
            else:
                days_until_stockout = float('inf')
            
            # Generate action plan
            action_plan = self._generate_action_plan(
                current_stock=current_stock,
                predicted_demand=predicted_demand,
                stok_minimum=stok_minimum,
                stok_optimal=stok_optimal,
                days_until_stockout=days_until_stockout
            )
            
            return {
                'bahan_id': bahan_id,
                'current_stock': current_stock,
                'predicted_daily_demand': float(predicted_demand / 30),
                'predicted_monthly_demand': float(predicted_demand),
                'status_stock': ['Kritis', 'Normal', 'Tinggi'][status_stok],
                'days_until_stockout': float(days_until_stockout) if days_until_stockout != float('inf') else None,
                'estimated_cost': float(predicted_demand * harga_per_unit),
                'confidence': prediction_result['confidence'],
                'recommendation': prediction_result['recommendation'],
                'action_plan': action_plan,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def _generate_recommendation(self, jumlah, prediction, harga, status_stok):
        """Generate action recommendation based on prediction"""
        
        if prediction > jumlah * 0.8:
            return {
                'action': 'ORDER_IMMEDIATELY',
                'message': 'Prediksi permintaan tinggi. Lakukan pemesanan segera!',
                'priority': 'HIGH'
            }
        elif prediction > jumlah * 0.5:
            return {
                'action': 'PLAN_ORDER',
                'message': 'Rencanakan pemesanan dalam 2-3 hari ke depan',
                'priority': 'MEDIUM'
            }
        elif prediction > jumlah * 0.2:
            return {
                'action': 'MONITOR',
                'message': 'Pantau stok, belum perlu pemesanan mendesak',
                'priority': 'LOW'
            }
        else:
            return {
                'action': 'MAINTAIN',
                'message': 'Stok mencukupi untuk periode berikutnya',
                'priority': 'NONE'
            }
    
    def _generate_action_plan(self, current_stock, predicted_demand, stok_minimum, 
                              stok_optimal, days_until_stockout):
        """Generate detailed action plan"""
        
        actions = []
        
        # Immediate actions
        if current_stock <= stok_minimum:
            actions.append({
                'priority': 1,
                'action': 'URGENT_ORDER',
                'description': 'PERINGATAN: Stok kritis! Lakukan pemesanan darurat',
                'timeline': 'Hari ini'
            })
        
        # Short-term (1-7 days)
        if days_until_stockout and days_until_stockout < 7:
            actions.append({
                'priority': 2,
                'action': 'EXPEDITED_ORDER',
                'description': f'Pemesanan dipercepat (stok habis dalam {int(days_until_stockout)} hari)',
                'timeline': '1-2 hari'
            })
        
        # Medium-term (1-2 weeks)
        if current_stock < stok_optimal:
            actions.append({
                'priority': 3,
                'action': 'REGULAR_ORDER',
                'description': f'Pesan {int(stok_optimal - current_stock)} unit untuk mencapai optimal',
                'timeline': '3-7 hari'
            })
        
        # Long-term monitoring
        actions.append({
            'priority': 4,
            'action': 'MONITOR',
            'description': 'Pantau pola penjualan untuk optimalisasi stok',
            'timeline': 'Berkelanjutan'
        })
        
        return actions
    
    def get_batch_predictions(self, materials_list, database_session=None):
        """
        Get predictions for multiple materials at once
        
        Args:
            materials_list: List of dicts with material info
            database_session: SQLAlchemy session (optional)
        
        Returns:
            list: Prediction results for all materials
        """
        results = []
        for material in materials_list:
            result = self.predict_material_detail(
                bahan_id=material.get('id'),
                current_stock=material.get('current_stock', 0),
                stok_minimum=material.get('stok_minimum', 10),
                stok_optimal=material.get('stok_optimal', 50),
                harga_per_unit=material.get('harga_per_unit', 0),
                recent_days=material.get('recent_days', 30)
            )
            results.append(result)
        
        return results


# Initialize service globally
prediction_service = AdvancedPredictionService()
