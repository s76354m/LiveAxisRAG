"""Initial schema migration

Revision ID: 001
Revises: None
Create Date: 2024-01-07
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create enum types
    op.execute("CREATE TYPE project_status AS ENUM ('Active', 'Pending', 'Completed')")
    op.execute("CREATE TYPE competitor_status AS ENUM ('Draft', 'Submitted', 'Approved')")
    
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.String(12), nullable=False),
        sa.Column('region', sa.String(100)),
        sa.Column('status', sa.Enum('Active', 'Pending', 'Completed', 
                                  name='project_status')),
        sa.Column('workflow_entity_id', sa.String(36)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
        sa.Column('created_by', sa.String(100)),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id')
    )
    
    # Create competitors table
    op.create_table(
        'competitors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.String(12)),
        sa.Column('product', sa.String(200)),
        sa.Column('status', sa.Enum('Draft', 'Submitted', 'Approved',
                                   name='competitor_status')),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
        sa.Column('created_by', sa.String(100)),
        sa.ForeignKeyConstraint(['project_id'], ['projects.project_id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('idx_project_search', 'projects', ['project_id', 'status'])
    op.create_index('idx_competitor_project', 'competitors', ['project_id'])

def downgrade():
    op.drop_table('competitors')
    op.drop_table('projects')
    op.execute('DROP TYPE competitor_status')
    op.execute('DROP TYPE project_status') 