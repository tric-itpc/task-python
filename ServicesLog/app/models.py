from utils.database.models import gino as db

class ServicesList(db.Model):
    __tablename__ = "services_list"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Unicode(length=25), nullable=False, unique=True)
    url = db.Column(db.Unicode(length=1024), nullable=False)
    des = db.Column(db.Unicode(length=1024), nullable=False)
class ServicesStatusesList(db.Model):
    __tablename__ = "services_statuses_list"
    id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)