import uuid

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID


from src.database import Base

class ServiceStatus(Base):
    __tablename__ = 'statuses'

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        index=True, 
        nullable=False, 
        default=uuid.uuid4
        )
    name = Column(String, nullable=False)
    service_status = Column(String, nullable=False)
    description = Column(String)
    
