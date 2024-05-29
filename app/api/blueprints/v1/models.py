from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class ConversionCache(db.Model):
    __tablename__ = "conversion_cache"
    id = db.Column(db.Integer, primary_key=True)
    cache_key = db.Column(db.String(32), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    parse_mode = db.Column(db.String(255), nullable=False)
    langs = db.Column(db.String(255), nullable=False)
    extract_images = db.Column(db.Boolean, nullable=False)
    result = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())