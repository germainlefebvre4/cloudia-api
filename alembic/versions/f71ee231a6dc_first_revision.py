"""First revision

Revision ID: f71ee231a6dc
Revises:
Create Date: 2023-1-17 13:53:32.978401

"""

# revision identifiers, used by Alembic.
revision = "f71ee231a6dc"
down_revision = "6e523d653806"
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, Float, String, DateTime, Date, Time)
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import JSON


def upgrade():
    op.create_table(
        'setting',
        Column('id', Integer, primary_key=True, index=True),
        Column('key', String, index=True),
        Column('value', String),
        Column('type', String),
        Column('category', String),
        Column('description', String),
    )



def downgrade():
    op.drop_table("setting")
