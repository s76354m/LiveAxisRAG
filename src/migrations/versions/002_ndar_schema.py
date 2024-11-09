"""ndar database schema

Revision ID: 002
Revises: 001
Create Date: 2024-01-09 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # CS_EXP_Competitor_Translation
    op.create_table(
        'CS_EXP_Competitor_Translation',
        sa.Column('RecordID', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ProjectID', sa.NVARCHAR(12)),
        sa.Column('ProjectStatus', sa.NVARCHAR(10)),
        sa.Column('StrenuusProductCode', sa.VARCHAR(50)),
        sa.Column('Payor', sa.VARCHAR(50)),
        sa.Column('Product', sa.VARCHAR(60)),
        sa.Column('EI', sa.Boolean()),
        sa.Column('CS', sa.Boolean()),
        sa.Column('MR', sa.Boolean()),
        sa.Column('DataLoadDate', sa.DateTime()),
        sa.Column('LastEditMSID', sa.NVARCHAR(15))
    )

    # CS_EXP_Project_Translation
    op.create_table(
        'CS_EXP_Project_Translation',
        sa.Column('RecordID', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ProjectID', sa.NVARCHAR(12)),
        sa.Column('BenchmarkFileID', sa.NVARCHAR(100)),
        sa.Column('ProjectType', sa.NVARCHAR(1)),
        sa.Column('ProjectDesc', sa.NVARCHAR(100)),
        sa.Column('Analyst', sa.NVARCHAR(30)),
        sa.Column('PM', sa.NVARCHAR(30)),
        sa.Column('GoLiveDate', sa.NVARCHAR(10)),
        sa.Column('MaxMileage', sa.Integer()),
        sa.Column('Status', sa.NVARCHAR(10)),
        sa.Column('NewMarket', sa.NVARCHAR(1)),
        sa.Column('ProvRef', sa.NVARCHAR(1)),
        sa.Column('DataLoadDate', sa.NVARCHAR(10)),
        sa.Column('LastEditDate', sa.NVARCHAR(10)),
        sa.Column('LastEditMSID', sa.NVARCHAR(15)),
        sa.Column('NDB_LOB', sa.NVARCHAR(50)),
        sa.Column('RefreshInd', sa.Integer())
    )

    # Add other tables following the same pattern...
    # Reference to stored_procedures.py for SP creation: 