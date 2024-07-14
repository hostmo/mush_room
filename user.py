from mr_config import mr_init as mr
from sqlalchemy import Table, Column,Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import mapper
Base = mr.Model
class User(mr.Model):
    __tablename__ = 'userlo'
    username = mr.Column(mr.String(255), primary_key=True, nullable=False)
    email = mr.Column(mr.String(255), nullable=False)
    gender = mr.Column(mr.String(255), nullable=False)
    password = mr.Column(mr.String(255), nullable=False)

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'gender': self.gender,
            'password': self.password
        }

class Record(mr.Model):
    __tablename__ = 'records'
    id = mr.Column(mr.Integer, primary_key=True,autoincrement=True)
    user_id = mr.Column(mr.String(255), mr.ForeignKey('userlo.username'), nullable=False)
    detection_time = mr.Column(mr.DateTime, default=datetime.utcnow)
    predicted_class = mr.Column(mr.String(255), nullable=False)
    confidence = mr.Column(mr.Float, nullable=False)
    image_path = mr.Column(mr.String(255), nullable=False)
    model_used = mr.Column(mr.String(50))
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'detection_time': self.detection_time.strftime('%Y-%m-%d %H:%M:%S'),
            'predicted_class': self.predicted_class,
            'confidence': self.confidence,
            'image_path': self.image_path,
            'model_used': self.model_used

        }