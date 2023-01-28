import sqlalchemy

from db import metadata
from models.enums import Status

state = sqlalchemy.Table(
    "states",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "service_id",
        sqlalchemy.ForeignKey("services.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "status",
        sqlalchemy.Enum(Status),
        nullable=False,
    ),
    sqlalchemy.Column("state_description", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
    ),
)
