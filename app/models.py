from datetime import datetime
import uuid
from app import db


class Phrase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    english_text = db.Column(db.String(500), nullable=False, index=True)
    korean_text = db.Column(db.String(500), nullable=False)
    audio_path = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<Phrase {self.english_text}>"

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "english_text": self.english_text,
            "korean_text": self.korean_text,
            "audio_path": self.audio_path,
            "created_at": self.created_at.isoformat(),
        }
