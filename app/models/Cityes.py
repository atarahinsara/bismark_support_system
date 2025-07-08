from app import db

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.ProvinceID'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=True)

    # رابطه برای دسترسی آسان به استان
    province = db.relationship('Province', backref=db.backref('cities', lazy=True))

    def __repr__(self):
        return f"<City(id={self.id}, name='{self.name}', province_id={self.province_id})>"
