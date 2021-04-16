from __future__ import absolute_import, print_function

import logging

from flask_babelex import gettext
from invenio_db import db
from speaklater import make_lazy_gettext
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

_ = make_lazy_gettext(lambda: gettext)

logger = logging.getLogger('nr-pidstore')


class NRIdentifier(db.Model):
    """Sequence generator for integer record identifiers.

    The sole purpose of this model is to generate integer record identifiers in
    sequence using the underlying database's auto increment features in a
    transaction friendly manner. The feature is primarily provided to support
    legacy Invenio instances to continue their current record identifier
    scheme. For new instances we strong encourage to not use auto incrementing
    record identifiers, but instead use e.g. UUIDs as record identifiers.
    """

    __tablename__ = 'nr_id'

    nr_id = db.Column(
        db.BigInteger().with_variant(db.Integer, "sqlite"),
        primary_key=True, autoincrement=True)

    @classmethod
    def next(cls):
        """Return next available record identifier."""
        try:
            with db.session.begin_nested():
                obj = cls()
                db.session.add(obj)
        except IntegrityError:  # pragma: no cover
            with db.session.begin_nested():
                # Someone has likely modified the table without using the
                # models API. Let's fix the problem.
                cls._set_sequence(cls.max())
                obj = cls()
                db.session.add(obj)
        return obj.nr_id

    @classmethod
    def max(cls):
        """Get max record identifier."""
        max_nr_id = db.session.query(func.max(cls.nr_id)).scalar()
        return max_nr_id if max_nr_id else 0

    @classmethod
    def _set_sequence(cls, val):
        """Internal function to reset sequence to specific value.

        Note: this function is for PostgreSQL compatibility.

        :param val: The value to be set.
        """
        if db.engine.dialect.name == 'postgresql':  # pragma: no cover
            db.session.execute(
                "SELECT setval(pg_get_serial_sequence("
                "'{0}', 'nr_id'), :newval)".format(
                    cls.__tablename__), dict(newval=val))

    @classmethod
    def insert(cls, val):
        """Insert a record identifier.

        :param val: The `nr_id` column value to insert.
        """
        with db.session.begin_nested():
            obj = cls(nr_id=val)
            db.session.add(obj)
            cls._set_sequence(cls.max())
