#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2019 Christoph Fink, University of Helsinki
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 3
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.

"""Update the database schema if necessary."""


__all__ = ["DatabaseSchemaUpdater"]


import sys

import sqlalchemy

from ..engine import engine


# for now, schema updates are SQL only and work on PostgreSQL, only.
# GeoAlchemy2 doesn’t really support SQLite, anyway
SCHEMA_UPDATES = {
    # 0 -> 1
    1: """
        BEGIN;

        ALTER TABLE
            places
        ADD COLUMN
            country_code TEXT;

        UPDATE
            places p
        SET
            country_code = c.code
        FROM
            countries c
        WHERE
            p.country_name = c.name;

        ALTER TABLE
            places
        DROP COLUMN
            country_name
                CASCADE;

        ALTER TABLE
            countries
        DROP CONSTRAINT
            countries_pkey,
        DROP CONSTRAINT
            countries_code_key,
        ADD CONSTRAINT
            countries_pkey PRIMARY KEY (code);

        ALTER TABLE
            places
        ADD CONSTRAINT
            places_country_code_fkey
                FOREIGN KEY (country_code)
                REFERENCES countries (code);

        COMMIT;
    """,
    # 1 -> 2
    2: """
        BEGIN;

        ALTER TABLE
            places
        ADD COLUMN
            geom GEOMETRY('GEOMETRYCOLLECTION', 4326);

        COMMIT;
    """,
    # 2 -> 3
    3: """
        BEGIN;

        ALTER TABLE
            search_terms
        DROP CONSTRAINT
            search_terms_pkey
                CASCADE,
        ADD COLUMN
            id SERIAL PRIMARY KEY;

        ALTER TABLE
            search_term_tweet_associations
        ADD COLUMN
            search_term_id INTEGER REFERENCES search_terms (id);

        UPDATE
            search_term_tweet_associations a
        SET
            search_term_id = s.id
        FROM
            search_terms s
        WHERE
            a.search_term_search_term = s.search_term;

        ALTER TABLE
            search_term_tweet_associations
        DROP COLUMN
            search_term_search_term
                CASCADE,
        ADD CONSTRAINT
            search_term_tweet_associations_pkey
                PRIMARY KEY (tweet_id, search_term_id);

        CREATE INDEX ON
            users
        USING
            BTREE(username);

        COMMIT;
    """,
    # 3 -> 4
    4: """
        BEGIN;

        UPDATE
            countries
        SET
            name = ''
        WHERE
            name IS NULL;

        ALTER TABLE
            countries
        ALTER COLUMN
            name
                SET NOT NULL;

        ALTER TABLE
            media_types
        DROP CONSTRAINT
            media_types_pkey
                CASCADE,
        ADD COLUMN
            id SERIAL PRIMARY KEY,
        ADD UNIQUE
            (media_type);

        ALTER TABLE
            media_items
        ADD COLUMN
            media_type_id INTEGER REFERENCES media_types (id);

        UPDATE
            media_items i
        SET
            media_type_id = t.id
        FROM
            media_types t
        WHERE
            i.media_type_media_type = t.media_type;

        ALTER TABLE
            media_items
        DROP COLUMN
            media_type_media_type
                CASCADE;

        ALTER TABLE
            place_types
        DROP CONSTRAINT
            place_types_pkey
                CASCADE,
        ADD COLUMN
            id SERIAL PRIMARY KEY,
        ADD UNIQUE
            (place_type);

        ALTER TABLE
            places
        ADD COLUMN
            place_type_id INTEGER REFERENCES place_types (id);

        UPDATE
            places p
        SET
            place_type_id = t.id
        FROM
            place_types t
        WHERE
            p.place_type_place_type = t.place_type;

        ALTER TABLE
            places
        DROP COLUMN
            place_type_place_type
                CASCADE;

        ALTER TABLE
            tweet_reference_types
        DROP CONSTRAINT
            tweet_reference_types_pkey
                CASCADE,
        ADD COLUMN
            id SERIAL PRIMARY KEY,
        ADD UNIQUE
            (reference_type);

        ALTER TABLE
            tweet_references
        ADD COLUMN
            reference_type_id INTEGER REFERENCES tweet_reference_types (id);

        UPDATE
            tweet_references r
        SET
            reference_type_id = t.id
        FROM
            tweet_reference_types t
        WHERE
            r.reference_type_reference_type = t.reference_type;

        ALTER TABLE
            tweet_references
        DROP COLUMN
            reference_type_reference_type
                CASCADE;

        ALTER TABLE
            urls
        DROP CONSTRAINT
            urls_pkey
                CASCADE,
        ADD COLUMN
            id BIGSERIAL PRIMARY KEY,
        ADD UNIQUE
            (url);

        ALTER TABLE
            url_tweet_associations
        DROP CONSTRAINT
            url_tweet_associations_pkey
                CASCADE,
        ADD COLUMN
            url_id INTEGER REFERENCES urls (id);

        UPDATE
            url_tweet_associations a
        SET
            url_id = u.id
        FROM
            urls u
        WHERE
            a.url_url = u.url;

        ALTER TABLE
            url_tweet_associations
        ADD PRIMARY KEY
            (url_id, tweet_id),
        DROP COLUMN
            url_url
                CASCADE;

        ALTER TABLE
            url_user_associations
        DROP CONSTRAINT
            url_user_associations_pkey
                CASCADE,
        ADD COLUMN
            url_id INTEGER REFERENCES urls (id);

        UPDATE
            url_user_associations a
        SET
            url_id = u.id
        FROM
            urls u
        WHERE
            a.url_url = u.url;

        ALTER TABLE
            url_user_associations
        ADD PRIMARY KEY
            (url_id, user_id),
        DROP COLUMN
            url_url
                CASCADE;

        ALTER TABLE
            users
        ADD COLUMN
            profile_image_url_id BIGINT REFERENCES urls (id);

        UPDATE
            users u1
        SET
            profile_image_url_id = u2.id
        FROM
            urls u2
        WHERE
            u1.profile_image_url_id IS NOT NULL
        AND
            u1.profile_image_url_url = u2.url;

        ALTER TABLE
            users
        DROP COLUMN
            profile_image_url_url
                CASCADE;

        COMMIT;
    """,
    # 4 -> 5
    5: """
        BEGIN;

        ALTER TABLE
            tweet_references
        DROP CONSTRAINT
            tweet_references_pkey,
        ADD PRIMARY KEY (
            referencing_tweet_id,
            referenced_tweet_id,
            reference_type_id
        );

        COMMIT;
    """
}


# Try to create database table for schema version
with engine.begin() as connection:
    connection.execute(
        """
            CREATE TABLE IF NOT EXISTS
                schema_versions
                (
                    update TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    version INTEGER PRIMARY KEY
                );
        """
    )


class DatabaseSchemaUpdater:
    """Update the database schema if necessary."""

    LATEST = "LATEST"  # “magic”, see def set_schema_version

    @property
    def installed_version(self):
        """Current version."""
        with engine.connect() as connection:
            installed_version = (
                connection.execute(
                    sqlalchemy.text("""
                        SELECT
                            COALESCE(
                                MAX(version),
                                0
                            ) AS version
                        FROM
                            schema_versions;
                    """)
                ).scalar_one_or_none()
            )
        return installed_version

    def update_to_latest(self):
        """Update to the latest schema version."""
        installed_version = self.installed_version
        while installed_version < max(SCHEMA_UPDATES.keys()):
            print(
                "Updating database schema (db version {:d}->{:d})".format(
                    installed_version,
                    installed_version + 1
                ),
                file=sys.stderr
            )
            with engine.begin() as connection:
                next_version = self.installed_version + 1
                connection.execute(sqlalchemy.text(SCHEMA_UPDATES[next_version]))
                self.set_schema_version(next_version)
            installed_version = self.installed_version

    @classmethod
    def set_schema_version(cls, version):
        """Set the schema version (without running update scripts)."""
        if version == cls.LATEST:
            version = max(SCHEMA_UPDATES.keys())
        with engine.begin() as connection:
            connection.execute(
                sqlalchemy.text("""
                    INSERT INTO
                        schema_versions (version)
                    VALUES (
                        :version
                    );
                """),
                {
                    "version": version
                }
            )
