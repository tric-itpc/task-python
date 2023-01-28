import sqlalchemy

from db import metadata

service = sqlalchemy.Table(
    "services",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "name", sqlalchemy.String(120), nullable=False, unique=True
    ),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=False),
)
