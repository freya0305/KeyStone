"""Add clerk_id to users, drop orphan user_consents.

Revision ID: 002
Revises: 001
Create Date: 2026-05-04

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add clerk_id to users for Clerk auth, drop orphan user_consents table."""
    # Add clerk_id column to users (unique, indexed for fast lookup)
    op.add_column(
        'users',
        sa.Column('clerk_id', sa.String(255), nullable=True, unique=True)
    )
    op.create_index('ix_users_clerk_id', 'users', ['clerk_id'], unique=True)

    # Drop orphan user_consents table (not defined in entities.py)
    op.drop_table('user_consents')


def downgrade() -> None:
    """Remove clerk_id, recreate user_consents."""
    op.drop_index('ix_users_clerk_id', 'users')
    op.drop_column('users', 'clerk_id')

    # Recreate user_consents as it was
    op.create_table(
        'user_consents',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('consent_type', sa.String(50), nullable=False),
        sa.Column('granted', sa.Boolean(), nullable=False),
        sa.Column('granted_at', sa.DateTime(), nullable=True),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
    )
