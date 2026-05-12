"""Add missing schema: analyzed_jobs, user_consents, missing columns, indexes, and RLS.

Revision ID: 004
Revises: 003
Create Date: 2026-05-11

Covers all gaps between entities.py and migrations 001-003:
- analyzed_jobs table (completely missing)
- user_consents table (dropped in 002, model still in entities.py)
- Missing columns on users, applications, b2b_tenants, b2b_users
- Missing indexes and unique constraints
- RLS policies for b2b_share_links and b2b_versions (added in 001 but no policies)
- Fix invite_links column name (created_by -> created_by_id)
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add all missing schema elements."""

    # -------------------------------------------------------------------------
    # Enum types needed for user_consents
    # -------------------------------------------------------------------------
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE consenttype AS ENUM (
                'registration', 'storage', 'ai_processing',
                'b2b_sharing', 'outcome_tracking', 'marketing', 'ai_training'
            );
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # -------------------------------------------------------------------------
    # analyzed_jobs table (job URL dedup for free-tier gating)
    # -------------------------------------------------------------------------
    op.create_table(
        'analyzed_jobs',
        sa.Column('id', UUID(), primary_key=True),
        sa.Column('user_id', UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('job_url_hash', sa.String(64), nullable=False),
        sa.Column('job_title', sa.String(500), nullable=True),
        sa.Column('analyzed_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_analyzed_jobs_user_id', 'analyzed_jobs', ['user_id'])
    op.create_index('ix_analyzed_jobs_job_url_hash', 'analyzed_jobs', ['job_url_hash'])
    op.create_index(
        'ix_analyzed_jobs_user_url',
        'analyzed_jobs',
        ['user_id', 'job_url_hash'],
        unique=True,
    )

    # -------------------------------------------------------------------------
    # user_consents table (re-created with current model schema)
    # Dropped in 002; model still in entities.py so table is needed.
    # Schema matches current UserConsent model (not the 001 version).
    # -------------------------------------------------------------------------
    op.create_table(
        'user_consents',
        sa.Column('id', UUID(), primary_key=True),
        sa.Column('user_id', UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('consent_type', sa.Enum(
            'registration', 'storage', 'ai_processing',
            'b2b_sharing', 'outcome_tracking', 'marketing', 'ai_training',
            name='consenttype', create_type=False
        ), nullable=False),
        sa.Column('granted_at', sa.DateTime(), nullable=False),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_user_consents_user_id', 'user_consents', ['user_id'])
    op.create_index('ix_user_consents_user_type', 'user_consents', ['user_id', 'consent_type'], unique=True)

    # -------------------------------------------------------------------------
    # Missing columns on users
    # -------------------------------------------------------------------------
    op.add_column('users', sa.Column('phone_hash', sa.String(64), nullable=True, unique=True))
    op.add_column('users', sa.Column('phone_verified', sa.Boolean(), default=False, nullable=True))
    op.add_column('users', sa.Column('phone_verified_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('persona', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('last_login_at', sa.DateTime(), nullable=True))

    # -------------------------------------------------------------------------
    # Missing columns on applications
    # -------------------------------------------------------------------------
    op.add_column('applications', sa.Column('job_url', sa.Text(), nullable=True))
    op.add_column('applications', sa.Column('applied_date', sa.DateTime(), nullable=True))
    op.add_column('applications', sa.Column(
        'suggestion_set_id', UUID(), sa.ForeignKey('job_analyses.id'), nullable=True
    ))
    op.add_column('applications', sa.Column('last_activity_at', sa.DateTime(), nullable=True))
    op.add_column('applications', sa.Column('auto_closed_at', sa.DateTime(), nullable=True))

    # -------------------------------------------------------------------------
    # Missing indexes on applications
    # -------------------------------------------------------------------------
    op.create_index('ix_applications_job_url', 'applications', ['job_url'])
    op.create_index('ix_applications_suggestion_set_id', 'applications', ['suggestion_set_id'])

    # -------------------------------------------------------------------------
    # Missing unique constraint on resumes.content_hash
    # -------------------------------------------------------------------------
    op.create_index(
        'ix_resumes_content_hash',
        'resumes',
        ['content_hash'],
        unique=True,
        postgresql_where=sa.text('content_hash IS NOT NULL')
    )

    # -------------------------------------------------------------------------
    # Missing indexes on suggestion_signals
    # -------------------------------------------------------------------------
    op.create_index('ix_suggestion_signals_suggestion_id', 'suggestion_signals', ['suggestion_id'])
    op.create_index('ix_suggestion_signals_anonymized_user_id', 'suggestion_signals', ['anonymized_user_id'])

    # -------------------------------------------------------------------------
    # Missing columns on b2b_tenants
    # -------------------------------------------------------------------------
    op.add_column('b2b_tenants', sa.Column(
        'stripe_subscription_id', sa.String(255), nullable=True, unique=True
    ))
    op.add_column('b2b_tenants', sa.Column('tier', sa.String(20), nullable=False, server_default='free'))
    op.add_column('b2b_tenants', sa.Column('jd_generation_count', sa.Integer(), default=0))
    op.add_column('b2b_tenants', sa.Column('jd_limit', sa.Integer(), default=-1))
    op.add_column('b2b_tenants', sa.Column('jd_limit_reset_at', sa.DateTime(), nullable=True))
    op.add_column('b2b_tenants', sa.Column('is_suspended', sa.Boolean(), default=False))
    op.add_column('b2b_tenants', sa.Column('updated_at', sa.DateTime(), nullable=True))

    # -------------------------------------------------------------------------
    # Missing columns on b2b_users
    # -------------------------------------------------------------------------
    op.add_column('b2b_users', sa.Column('invited_at', sa.DateTime(), nullable=True))
    op.add_column('b2b_users', sa.Column('joined_at', sa.DateTime(), nullable=True))

    # -------------------------------------------------------------------------
    # Fix invite_links column name (003 used 'created_by' but model uses 'created_by_id')
    # Check if column exists before trying to rename
    # -------------------------------------------------------------------------
    # Note: Migration 003 creates 'created_by_id' correctly.
    # This section is a no-op placeholder for safety if a previous version used 'created_by'.
    # Running SELECT to check column existence:
    op.execute("""
        DO $$ BEGIN
            -- Rename column if it was created with wrong name (safety check)
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'invite_links' AND column_name = 'created_by'
            ) THEN
                ALTER TABLE invite_links RENAME COLUMN created_by TO created_by_id;
            END IF;
        EXCEPTION WHEN undefined_table THEN null;
        END $$;
    """)

    # -------------------------------------------------------------------------
    # RLS policies for b2b_share_links and b2b_versions
    # (Created in 001 but no RLS policies were added)
    # -------------------------------------------------------------------------
    op.execute("ALTER TABLE b2b_share_links ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY b2b_share_links_tenant_isolation ON b2b_share_links
            FOR ALL
            USING (
                jd_id IN (
                    SELECT id FROM b2b_job_descriptions
                    WHERE tenant_id::text = current_setting('app.current_tenant_id', true)
                )
            )
    """)

    op.execute("ALTER TABLE b2b_versions ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY b2b_versions_tenant_isolation ON b2b_versions
            FOR ALL
            USING (
                jd_id IN (
                    SELECT id FROM b2b_job_descriptions
                    WHERE tenant_id::text = current_setting('app.current_tenant_id', true)
                )
            )
    """)

    # -------------------------------------------------------------------------
    # RLS policy for analyzed_jobs (user isolation - user can only see own rows)
    # -------------------------------------------------------------------------
    op.execute("ALTER TABLE analyzed_jobs ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY analyzed_jobs_user_isolation ON analyzed_jobs
            FOR ALL
            USING (user_id::text = current_setting('app.current_user_id', true))
    """)

    # -------------------------------------------------------------------------
    # RLS policy for user_consents (user can only see own consent records)
    # -------------------------------------------------------------------------
    op.execute("ALTER TABLE user_consents ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY user_consents_user_isolation ON user_consents
            FOR ALL
            USING (user_id::text = current_setting('app.current_user_id', true))
    """)


def downgrade() -> None:
    """Remove all schema elements added in this migration."""

    # Drop RLS policies
    op.execute("DROP POLICY IF EXISTS user_consents_user_isolation ON user_consents")
    op.execute("DROP POLICY IF EXISTS analyzed_jobs_user_isolation ON analyzed_jobs")
    op.execute("DROP POLICY IF EXISTS b2b_versions_tenant_isolation ON b2b_versions")
    op.execute("DROP POLICY IF EXISTS b2b_share_links_tenant_isolation ON b2b_share_links")

    # Disable RLS
    op.execute("ALTER TABLE user_consents DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE analyzed_jobs DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE b2b_versions DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE b2b_share_links DISABLE ROW LEVEL SECURITY")

    # Drop tables
    op.drop_table('user_consents')
    op.drop_table('analyzed_jobs')

    # Drop indexes on suggestion_signals
    op.drop_index('ix_suggestion_signals_suggestion_id', 'suggestion_signals')
    op.drop_index('ix_suggestion_signals_anonymized_user_id', 'suggestion_signals')

    # Drop unique constraint on resumes.content_hash
    op.drop_index('ix_resumes_content_hash', 'resumes', postgresql_where=sa.text('content_hash IS NOT NULL'))

    # Drop indexes on applications
    op.drop_index('ix_applications_suggestion_set_id', 'applications')
    op.drop_index('ix_applications_job_url', 'applications')

    # Drop columns from applications
    op.drop_column('applications', 'auto_closed_at')
    op.drop_column('applications', 'last_activity_at')
    op.drop_column('applications', 'suggestion_set_id')
    op.drop_column('applications', 'applied_date')
    op.drop_column('applications', 'job_url')

    # Drop columns from users
    op.drop_column('users', 'last_login_at')
    op.drop_column('users', 'persona')
    op.drop_column('users', 'phone_verified_at')
    op.drop_column('users', 'phone_verified')
    op.drop_column('users', 'phone_hash')

    # Drop columns from b2b_users
    op.drop_column('b2b_users', 'joined_at')
    op.drop_column('b2b_users', 'invited_at')

    # Drop columns from b2b_tenants
    op.drop_column('b2b_tenants', 'updated_at')
    op.drop_column('b2b_tenants', 'is_suspended')
    op.drop_column('b2b_tenants', 'jd_limit_reset_at')
    op.drop_column('b2b_tenants', 'jd_limit')
    op.drop_column('b2b_tenants', 'jd_generation_count')
    op.drop_column('b2b_tenants', 'tier')
    op.drop_column('b2b_tenants', 'stripe_subscription_id')

    # Drop enum type
    op.execute("DROP TYPE IF EXISTS consenttype")
