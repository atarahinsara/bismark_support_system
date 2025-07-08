from app import db

class Province(db.Model):
    __tablename__ = 'provinces'

    ProvinceID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Province(ProvinceID={self.ProvinceID}, Name='{self.Name}')>"
