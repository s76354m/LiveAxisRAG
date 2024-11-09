"""ndar tables migration

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
    # Create CS_EXP_ProjectNotes
    op.create_table(
        'CS_EXP_ProjectNotes',
        sa.Column('RecordID', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('ProjectID', sa.NVARCHAR(12), nullable=True),
        sa.Column('Notes', sa.NVARCHAR(sa.text('max')), nullable=True),
        sa.Column('ActionItem', sa.NVARCHAR(3), nullable=True),
        sa.Column('ProjectStatus', sa.NVARCHAR(8), nullable=True),
        sa.Column('DataLoadDate', sa.DateTime(), nullable=True),
        sa.Column('LastEditDate', sa.DateTime(), nullable=True),
        sa.Column('OrigNoteMSID', sa.NVARCHAR(15), nullable=True),
        sa.Column('LastEditMSID', sa.NVARCHAR(15), nullable=True),
        sa.Column('ProjectCategory', sa.NVARCHAR(50), nullable=True),
        sa.PrimaryKeyConstraint('RecordID')
    )

    # Create CS_EXP_Sel_PLProducts
    op.create_table(
        'CS_EXP_Sel_PLProducts',
        sa.Column('RECORD_ID', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('ProjectID', sa.NVARCHAR(12), nullable=False),
        sa.Column('ProjectStatus', sa.NVARCHAR(10), nullable=False),
        sa.Column('NWNW_ID', sa.VARCHAR(12), nullable=False),
        sa.Column('NWPR_PFX', sa.VARCHAR(4), nullable=False),
        sa.Column('GRGR_ID', sa.VARCHAR(8), nullable=True),
        sa.Column('GRGR_NAME', sa.VARCHAR(50), nullable=True),
        sa.Column('LastEditMSID', sa.NVARCHAR(15), nullable=True),
        sa.Column('DataLoadDate', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('RECORD_ID')
    )

    # Create CS_EXP_YLine_Translation
    op.create_table(
        'CS_EXP_YLine_Translation',
        sa.Column('RecordID', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('ProjectID', sa.NVARCHAR(12), nullable=True),
        sa.Column('ProjectStatus', sa.NVARCHAR(10), nullable=True),
        sa.Column('NDB_Yline_ProdCd', sa.CHAR(2), nullable=True),
        sa.Column('NDB_Yline_IPA', sa.Integer(), nullable=True),
        sa.Column('NDB_Yline_MktNum', sa.Integer(), nullable=True),
        sa.Column('DataLoadDate', sa.DateTime(), nullable=True),
        sa.Column('LastEditDate', sa.DateTime(), nullable=True),
        sa.Column('LastEditMSID', sa.NVARCHAR(15), nullable=True),
        sa.Column('PreAward', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('RecordID')
    )

    # Create CS_EXP_zTrxServiceArea
    op.create_table(
        'CS_EXP_zTrxServiceArea',
        sa.Column('RecordID', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('ProjectID', sa.NVARCHAR(12), nullable=True),
        sa.Column('Region', sa.NVARCHAR(30), nullable=True),
        sa.Column('State', sa.NVARCHAR(2), nullable=True),
        sa.Column('County', sa.NVARCHAR(75), nullable=True),
        sa.Column('ReportInclude', sa.NVARCHAR(1), nullable=True),
        sa.Column('MaxMileage', sa.Integer(), nullable=True),
        sa.Column('DataLoadDate', sa.DateTime(), nullable=True),
        sa.Column('ProjectStatus', sa.NVARCHAR(10), nullable=True),
        sa.PrimaryKeyConstraint('RecordID')
    )

    # Create indexes with FILLFACTOR
    with op.batch_alter_table('CS_EXP_Competitor_Translation') as batch_op:
        batch_op.create_index('PK_CS_EXP_Competitor_Translation', ['RecordID'], 
                            unique=True, postgresql_with={'fillfactor': '80'})

    with op.batch_alter_table('CS_EXP_Project_Translation') as batch_op:
        batch_op.create_index('PK_CS_EXP_Project_Translation', ['RecordID'], 
                            unique=True, postgresql_with={'fillfactor': '80'})

    with op.batch_alter_table('CS_EXP_ProjectNotes') as batch_op:
        batch_op.create_index('PK_CS_EXP_ProjectNotes', ['RecordID'], 
                            unique=True, postgresql_with={'fillfactor': '80'})

    with op.batch_alter_table('CS_EXP_zTrxServiceArea') as batch_op:
        batch_op.create_index('PK_CS_EXP_zTrxServiceArea', ['RecordID'], 
                            unique=True, postgresql_with={'fillfactor': '80'})

def downgrade() -> None:
    op.drop_table('CS_EXP_zTrxServiceArea')
    op.drop_table('CS_EXP_YLine_Translation')
    op.drop_table('CS_EXP_Sel_PLProducts')
    op.drop_table('CS_EXP_ProjectNotes')