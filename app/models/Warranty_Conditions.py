from app import db

class WarrantyCondition(db.Model):
    __tablename__ = 'warrantyconditions'

    ConditionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.Text)
    IsActive = db.Column(db.Boolean, default=True)
    CreatedAt = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    UpdatedAt = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<WarrantyCondition {self.ConditionID} - {self.Title}>"
