from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

from .constants import DATE_FORMAT


class CustomSerializerMixin(SerializerMixin):
    date_format = "%s"  # Unixtimestamp (seconds)
    datetime_format = DATE_FORMAT
    time_format = "%H:%M.%f"
    decimal_format = "{:0>10.3}"
    serialize_types = ()


db = SQLAlchemy()


class User(db.Model, CustomSerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    vms = db.relationship("Vm", backref="owner", lazy=True)

    serialize_only = ("id", "username", "email")

    def __str__(self):
        return "ID=%d, Username=%s, Email=%d" % (
            self.id, self.username, self.email)


class Vm(db.Model, CustomSerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(80), nullable=False)
    reservation_start = db.Column(db.DateTime, server_default=db.func.now())
    reservation_end = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now()
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    serialize_only = (
        "id",
        "name",
        "ip",
        "description",
        "status",
        "reservation_start",
        "reservation_end",
        "user_id",
    )

    def __str__(self):
        return "ID=%d, Name=%s, ip=%d" % (self.id, self.name, self.ip)
