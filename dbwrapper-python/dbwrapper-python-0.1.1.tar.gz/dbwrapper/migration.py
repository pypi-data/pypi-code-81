
import typing
import logging

_LOGGER = logging.getLogger("Migrations")

def migrate(db, migrations: typing.Iterable[typing.Callable], migration_table="__migrations__"):

    vtbl = db.table(migration_table)

    if not vtbl.exists():
        with db:
            with vtbl.builder() as builder:
                builder.column("latest", db.dtypes.integer)
    
    v = vtbl.select(vtbl.columns.latest).execute()

    idx = 0 if len(v) == 0 else v[0]
    nmigrations = len(migrations)

    _LOGGER.info("Database Migration Level: %d. Available Migration Level: %d (Table %s)", idx, nmigrations, migration_table)

    applied = set()

    if idx < nmigrations:
        with db:
            for i in range(idx, nmigrations):
                _LOGGER.info("Applying Migration: %d", i)
                migrations[i](db)
                _LOGGER.info("Successfully Applied Migration: %d", i)
                applied.add(migrations[i])
        
            _LOGGER.info("Updating Migration Table To: %d", nmigrations)
            vtbl.delete().execute()
            vtbl.insert_one([nmigrations])
        _LOGGER.info("Successfully Migrated To: %d", nmigrations)
    else:
        _LOGGER.info("No Migrations Necessary")

    return applied
