import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class ComplaintPrioritizer:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.category_encoder = LabelEncoder()
        self.urgency_encoder = LabelEncoder()
        self.is_trained = False
        
    def train_model(self, training_data):
        """Train the priority prediction model"""
        df = pd.DataFrame(training_data)
        
        # Encode categorical variables
        df['category_encoded'] = self.category_encoder.fit_transform(df['category'])
        df['urgency_encoded'] = self.urgency_encoder.fit_transform(df['urgency_level'])
        
        # Features for training
        features = ['category_encoded', 'urgency_encoded']
        X = df[features]
        y = df['priority_score']  # This should be based on historical resolution times
        
        self.model.fit(X, y)
        self.is_trained = True
        
        # Save model
        joblib.dump(self.model, 'complaint_priority_model.pkl')
        joblib.dump(self.category_encoder, 'category_encoder.pkl')
        joblib.dump(self.urgency_encoder, 'urgency_encoder.pkl')
    
    def calculate_priority(self, complaint_data):
        """Calculate priority score for a new complaint"""
        if not self.is_trained:
            # Load pre-trained model or use default scoring
            return self._default_priority_score(complaint_data)
        
        try:
            category_encoded = self.category_encoder.transform([complaint_data['category']])[0]
            urgency_encoded = self.urgency_encoder.transform([complaint_data['urgency_level']])[0]
            
            features = [[category_encoded, urgency_encoded]]
            priority_score = self.model.predict(features)[0]
            
            return max(0, min(100, priority_score))  # Normalize to 0-100
        except:
            return self._default_priority_score(complaint_data)
    
    def _default_priority_score(self, complaint_data):
        """Default priority scoring when ML model is not available"""
        urgency_scores = {
            'critical': 90,
            'high': 70,
            'medium': 50,
            'low': 30
        }
        
        category_multipliers = {
            'electricity': 1.2,
            'plumbing': 1.1,
            'sewage': 1.3,
            'maintenance': 1.0,
            'other': 0.9
        }
        
        base_score = urgency_scores.get(complaint_data['urgency_level'], 50)
        multiplier = category_multipliers.get(complaint_data['category'], 1.0)
        
        return min(100, base_score * multiplier)
