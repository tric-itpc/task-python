from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, unique=True, index=True)
    state = Column(String, index=True, default="работает")
    description = Column(String, index=True, default=None)


class ServiceHistory(Base):
    __tablename__ = 'serviceHistory'
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)
    from_state = Column(String, index=True)
    to_state = Column(String, index=True)
    change_time = Column(DateTime, index=True)
    time_not_working = Column(DateTime, index=True)


