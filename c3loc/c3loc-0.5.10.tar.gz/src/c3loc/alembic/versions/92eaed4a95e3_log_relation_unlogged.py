"""log_relation_unlogged

Revision ID: 92eaed4a95e3
Revises: 720d3e9a9af0
Create Date: 2021-03-18 09:41:27.914377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92eaed4a95e3'
down_revision = '720d3e9a9af0'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DROP TABLE log;")
    op.execute("""CREATE UNLOGGED TABLE log (
    tag_id int,
    zone_id int,
    ts timestamp without time zone default (now() at time zone 'utc'),
    distance numeric(4,2),
    variance real,
    listener_id varchar,
    data jsonb,
    anchor_dist numeric(4,2),
    anchor_ts_delta int,
    anchor_id int,
    reason report_reason,
    CONSTRAINT fk_tag
                 FOREIGN KEY (tag_id)
                 REFERENCES tags(id)
                 ON DELETE CASCADE,
    CONSTRAINT fk_zone
                 FOREIGN KEY (zone_id)
                 REFERENCES zones(id)
                 ON DELETE SET NULL,
    CONSTRAINT fk_anchor
                 FOREIGN KEY (anchor_id)
                 REFERENCES tags(id)
                 ON DELETE SET NULL,
    CONSTRAINT fk_listener
                 FOREIGN KEY (listener_id)
                 REFERENCES listeners(id)
                 ON DELETE SET NULL
);""")


def downgrade():
    pass
