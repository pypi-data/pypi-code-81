"""Modify history for start/end

Revision ID: 44f605b1cfa0
Revises: 92eaed4a95e3
Create Date: 2021-04-16 13:25:35.679663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44f605b1cfa0'
down_revision = '92eaed4a95e3'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE history RENAME ts TO end_ts")
    op.execute("ALTER TABLE history ADD COLUMN start_ts timestamp without time zone default (now() at time zone 'utc')")
    op.execute("ALTER TABLE history ALTER COLUMN end_ts SET DEFAULT NULL")
    op.execute("""WITH cte AS (
            SELECT tag_id, end_ts, lead(end_ts) OVER (PARTITION BY tag_id ORDER BY end_ts DESC) as new_start FROM history)
            UPDATE history SET start_ts = cte.new_start from cte where history.end_ts = cte.end_ts and history.tag_id = cte.tag_id;
        """)
    op.execute("DROP FUNCTION append_history CASCADE")
    op.execute("""CREATE FUNCTION append_history()
        RETURNS TRIGGER
        LANGUAGE plpgsql
    AS $$
    BEGIN
        UPDATE history SET end_ts = (now() at time zone 'utc') WHERE tag_id = OLD.id AND end_ts IS NULL;
        INSERT INTO history (tag_id, zone_id, distance, zone_name)
        VALUES (NEW.id, NEW.zone_id, NEW.distance,
                (SELECT zones.name from zones where zones.id = NEW.zone_id));
        RETURN NEW;
    END;
    $$""")
    op.execute("""CREATE TRIGGER tags_update_zone
        AFTER UPDATE OF zone_id ON tags FOR EACH ROW
        WHEN (OLD.zone_id IS DISTINCT FROM NEW.zone_id)
        EXECUTE PROCEDURE append_history();""")
    op.execute("DELETE FROM history where start_ts IS NULL")


def downgrade():
    op.execute("DROP FUNCTION append_history CASCADE")
    op.execute("""CREATE FUNCTION append_history()
    RETURNS TRIGGER
    LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO history (tag_id, zone_id, ts, distance, zone_name)
    VALUES (OLD.id, OLD.zone_id, OLD.last_seen, OLD.distance,
            (SELECT zones.name from zones where zones.id = OLD.zone_id));
    RETURN NEW;
END;
$$""")
    op.execute("""CREATE TRIGGER tags_update_zone
        AFTER UPDATE OF zone_id ON tags FOR EACH ROW
        WHEN (OLD.zone_id IS DISTINCT FROM NEW.zone_id AND OLD.zone_id IS NOT NULL)
        EXECUTE PROCEDURE append_history();""")
    op.execute("ALTER TABLE history ALTER COLUMN end_ts SET DEFAULT (now() at time zone 'utc')")
    op.execute("ALTER TABLE history DROP COLUMN start_ts")
    op.execute("ALTER TABLE history RENAME end_ts TO ts")
