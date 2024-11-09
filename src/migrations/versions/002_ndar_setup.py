"""ndar database setup

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
    # Database configuration
    op.execute('ALTER DATABASE [ndar] SET ANSI_NULLS OFF')
    op.execute('ALTER DATABASE [ndar] SET ANSI_PADDING OFF')
    op.execute('ALTER DATABASE [ndar] SET ANSI_WARNINGS OFF')
    
    # Create tables with proper SQL Server types
    tables = [
        ('CS_EXP_Competitor_Translation', [
            sa.Column('RecordID', sa.Integer(), nullable=False, autoincrement=True),
            sa.Column('ProjectID', sa.NVARCHAR(12)),
            # ... other columns
        ]),
        ('CS_EXP_Project_Translation', [
            sa.Column('RecordID', sa.Integer(), nullable=False, autoincrement=True),
            sa.Column('ProjectID', sa.NVARCHAR(12)),
            # ... other columns
        ])
        # ... other tables
    ]
    
    for table_name, columns in tables:
        op.create_table(
            table_name,
            *columns,
            sa.PrimaryKeyConstraint(columns[0].name),
            postgresql_with={'fillfactor': '80'}
        )
        
    # Create indexes
    indexes = [
        ('idx_competitor_projectid', 'CS_EXP_Competitor_Translation', ['ProjectID']),
        ('idx_project_projectid', 'CS_EXP_Project_Translation', ['ProjectID']),
        # ... other indexes
    ]
    
    for idx_name, table_name, columns in indexes:
        op.create_index(idx_name, table_name, columns)

def downgrade() -> None:
    # Drop tables in reverse order
    tables = [
        'CS_EXP_zTrxServiceArea',
        'CS_EXP_YLine_Translation',
        'CS_EXP_Sel_PLProducts',
        'CS_EXP_ProjectNotes',
        'CS_EXP_Project_Translation',
        'CS_EXP_Competitor_Translation'
    ]
    
    for table in tables:
        op.drop_table(table) 