"""Fix schema gaps: is_confirmed, gamification, clerk_id, duplicate index, unique constraint.

Revision ID: 005
Revises: 004
Create Date: 2026-05-12

Covers all gaps between entities.py and migrations 001-004:
1. Add is_confirmed to applications (Boolean, default=False, nullable=False)
2. Add gamification columns to users (current_streak, longest_streak, last_activity_date, earned_badges)
3. Fix clerk_id nullable mismatch: backfill existing rows, then add NOT NULL
4. Fix duplicate index: ix_suggestion_signals_suggestion_id created in both 001 and 004
5. Add unique constraint on suggestion_signals (anonymized_user_id, suggestion_id)
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Fix all schema gaps."""

    # -------------------------------------------------------------------------
    # 1. Add is_confirmed to applications
    # -------------------------------------------------------------------------
    op.add_column(
        'applications',
        sa.Column('is_confirmed', sa.Boolean(), default=False, nullable=False)
    )

    # -------------------------------------------------------------------------
    # 2. Add gamification columns to users
    # -------------------------------------------------------------------------
    op.add_column('users', sa.Column('current_streak', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('longest_streak', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('last_activity_date', sa.Date(), nullable=True))
    op.add_column('users', sa.Column('earned_badges', sa.JSON(), nullable=True))

    # -------------------------------------------------------------------------
    # 3. Fix clerk_id nullable mismatch
    # Backfill existing NULL rows with placeholder, then enforce NOT NULL
    # -------------------------------------------------------------------------
    op.execute("""
        UPDATE users
        SET clerk_id = 'missing_clerk_id_' || gen_random_uuid()::text
        WHERE clerk_id IS NULL
    """)
    op.alter_column('users', 'clerk_id', existing_type=sa.String(255), nullable=False)

    # -------------------------------------------------------------------------
    # 4. Fix duplicate index on suggestion_signals
    # Created in both 001 and 004 — use IF NOT EXISTS for idempotency
    # -------------------------------------------------------------------------
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_suggestion_signals_suggestion_id
        ON suggestion_signals (suggestion_id)
    """)

    # -------------------------------------------------------------------------
    # 5. Add unique constraint on suggestion_signals
    # -------------------------------------------------------------------------
    op.create_unique_constraint(
        'uq_suggestion_signals_user_signal',
        'suggestion_signals',
        ['anonymized_user_id', 'suggestion_id']
    )


def downgrade() -> None:
    """Revert all schema changes."""

    # -------------------------------------------------------------------------
    # 5. Drop unique constraint on suggestion_signals
    # -------------------------------------------------------------------------
    op.drop_constraint(
        'uq_suggestion_signals_user_signal',
        'suggestion_signals',
        type_='unique'
    )

    # -------------------------------------------------------------------------
    # 4. Index removal not needed — IF NOT EXISTS is only for creation safety

    # -------------------------------------------------------------------------
    # 3. Revert clerk_id to nullable
    # -------------------------------------------------------------------------
    op.alter_column('users', 'clerk_id', existing_type=sa.String(255), nullable=True)

    # -------------------------------------------------------------------------
    # 2. Drop gamification columns from users
    # -------------------------------------------------------------------------
    op.drop_column('users', 'earned_badges')
    op.drop_column('users', 'last_activity_date')
    op.drop_column('users', 'longest_streak')
    op.drop_column('users', 'current_streak')

    # -------------------------------------------------------------------------
    # 1. Drop is_confirmed from applications
    # -------------------------------------------------------------------------
    op.drop_column('applications', 'is_confirmed')
