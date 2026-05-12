"""Add missing tables: application_stages, invite_links, b2b_aggregate_reports,
raw_jds, normalized_roles, role_skill_frequency, jd_generation_logs.

Also adds missing RLS policies for b2b_tenants and b2b_share_links/b2b_versions
(parent-child via FK, not via direct policy).

Revision ID: 003
Revises: 002
Create Date: 2026-05-10

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add missing tables from entities.py not covered in 001/002."""

    # --- Application Stages (normalized stage events for application tracking) ---
    op.create_table(
        'application_stages',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('application_id', sa.UUID(), sa.ForeignKey('applications.id'), nullable=False),
        sa.Column('stage_type', sa.String(20), nullable=False),  # response|screening|interview|final|offer|rejection|withdrawal
        sa.Column('round_number', sa.Integer(), nullable=True),  # 1-5 for interviews
        sa.Column('format', sa.String(50), nullable=True),  # email|phone|video|in-person|assessment_centre|panel|technical|case
        sa.Column('outcome', sa.String(20), nullable=True),  # passed|failed|pending|withdrawn
        sa.Column('stage_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_application_stages_application_id', 'application_stages', ['application_id'])

    # --- Invite Links (B2B team onboarding) ---
    op.create_table(
        'invite_links',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('tenant_id', sa.UUID(), sa.ForeignKey('b2b_tenants.id'), nullable=False),
        sa.Column('token', sa.String(64), nullable=False, unique=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('access_level', sa.String(20), nullable=False),  # admin|member
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column('created_by_id', sa.UUID(), sa.ForeignKey('b2b_users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_invite_links_token', 'invite_links', ['token'])
    op.create_index('ix_invite_links_tenant_id', 'invite_links', ['tenant_id'])

    # --- B2B Aggregate Reports ---
    op.create_table(
        'b2b_aggregate_reports',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('tenant_id', sa.UUID(), sa.ForeignKey('b2b_tenants.id'), nullable=False),
        sa.Column('cohort_period', sa.String(50), nullable=False),  # e.g., "2025-S1"
        sa.Column('aggregate_stats_json', sa.JSON(), nullable=False),
        sa.Column('generated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_b2b_aggregate_reports_tenant_id', 'b2b_aggregate_reports', ['tenant_id'])

    # --- Raw JDs (JD Generator v2: raw job descriptions from all sources) ---
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE jd_source_platform AS ENUM ('mcf', 'jobstreet', 'linkedin', 'direct');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE jd_data_source AS ENUM ('scraped', 'user_submitted', 'partner');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    op.create_table(
        'raw_jds',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('source_url', sa.Text(), nullable=True),
        sa.Column('source_platform', sa.String(50), nullable=True),
        sa.Column('data_source', sa.String(50), nullable=False),
        sa.Column('job_title_raw', sa.Text(), nullable=True),
        sa.Column('company', sa.Text(), nullable=True),
        sa.Column('company_type', sa.String(50), nullable=False),
        sa.Column('industry', sa.String(50), nullable=False),
        sa.Column('seniority', sa.String(50), nullable=False),
        sa.Column('raw_text', sa.Text(), nullable=True),
        sa.Column('posted_at', sa.DateTime(), nullable=True),
        sa.Column('scraped_at', sa.DateTime(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('consent_given', sa.Boolean(), default=False),
        sa.Column('is_duplicate', sa.Boolean(), default=False),
        sa.Column('is_spam', sa.Boolean(), default=False),
        sa.Column('is_stale', sa.Boolean(), default=False),
    )
    op.create_index('ix_raw_jds_company_title_posted', 'raw_jds', ['company', 'job_title_raw', 'posted_at'])
    op.create_index('ix_raw_jds_data_source', 'raw_jds', ['data_source'])
    op.create_index('ix_raw_jds_industry_seniority', 'raw_jds', ['industry', 'seniority'])

    # --- Normalized Roles ---
    op.create_table(
        'normalized_roles',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('title_normalized', sa.Text(), nullable=False),
        sa.Column('title_variants', sa.JSON(), nullable=True),
        sa.Column('industry', sa.String(50), nullable=False),
        sa.Column('seniority', sa.String(50), nullable=False),
        sa.Column('total_jds', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_normalized_roles_title', 'normalized_roles', ['title_normalized'])
    op.create_index(
        'ix_normalized_roles_lookup',
        'normalized_roles',
        ['title_normalized', 'industry', 'seniority'],
        unique=True,
        postgresql_where=sa.text('title_normalized IS NOT NULL')
    )

    # --- Role Skill Frequency (ETL read table) ---
    op.create_table(
        'role_skill_frequency',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('normalized_role_id', sa.UUID(), sa.ForeignKey('normalized_roles.id'), nullable=True),
        sa.Column('title_normalized', sa.Text(), nullable=False),
        sa.Column('industry', sa.String(50), nullable=False),
        sa.Column('seniority', sa.String(50), nullable=False),
        sa.Column('company_type', sa.String(50), nullable=False),
        sa.Column('skills_json', sa.JSON(), nullable=False),
        sa.Column('total_jds_analyzed', sa.Integer(), nullable=False),
        sa.Column('recency_weight', sa.Float(), default=1.0),
        sa.Column('last_updated', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_role_skill_freq_title', 'role_skill_frequency', ['title_normalized'])
    op.create_index(
        'ix_role_skill_freq_lookup',
        'role_skill_frequency',
        ['title_normalized', 'industry', 'seniority', 'company_type'],
        unique=True,
        postgresql_where=sa.text('title_normalized IS NOT NULL')
    )

    # --- JD Generation Logs ---
    op.create_table(
        'jd_generation_logs',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('input_title', sa.Text(), nullable=True),
        sa.Column('input_industry', sa.String(50), nullable=True),
        sa.Column('input_seniority', sa.String(50), nullable=True),
        sa.Column('input_company_type', sa.String(50), nullable=True),
        sa.Column('input_skills_user', sa.JSON(), nullable=True),
        sa.Column('skills_from_frequency', sa.JSON(), nullable=True),
        sa.Column('generation_source', sa.String(50), nullable=False),
        sa.Column('adopted', sa.Boolean(), nullable=True),
        sa.Column('edited', sa.Boolean(), nullable=True),
        sa.Column('used_in_posting', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_jd_generation_logs_created_at', 'jd_generation_logs', ['created_at'])

    # --- Add missing RLS policies ---
    # b2b_tenants: enable RLS (was enabled but no policy created)
    op.execute("ALTER TABLE b2b_tenants ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY b2b_tenants_tenant_isolation ON b2b_tenants
            FOR ALL
            USING (id::text = current_setting('app.current_tenant_id', true))
    """)

    # b2b_share_links and b2b_versions: inherit via FK to b2b_job_descriptions
    # They have FK to b2b_job_descriptions.tenant_id, so they are protected
    # by the parent's RLS policy when joining. Add explicit policies for defense-in-depth.
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

    # b2b_aggregate_reports: tenant isolation
    op.execute("""
        CREATE POLICY b2b_aggregate_reports_tenant_isolation ON b2b_aggregate_reports
            FOR ALL
            USING (tenant_id::text = current_setting('app.current_tenant_id', true))
    """)


def downgrade() -> None:
    """Drop all tables and RLS policies added in this migration."""

    # Drop RLS policies
    op.execute("DROP POLICY IF EXISTS b2b_tenants_tenant_isolation ON b2b_tenants")
    op.execute("DROP POLICY IF EXISTS b2b_share_links_tenant_isolation ON b2b_share_links")
    op.execute("DROP POLICY IF EXISTS b2b_versions_tenant_isolation ON b2b_versions")
    op.execute("DROP POLICY IF EXISTS b2b_aggregate_reports_tenant_isolation ON b2b_aggregate_reports")

    # Disable RLS on b2b_tenants
    op.execute("ALTER TABLE b2b_tenants DISABLE ROW LEVEL SECURITY")

    # Drop tables (reverse dependency order)
    op.drop_table('jd_generation_logs')
    op.drop_table('role_skill_frequency')
    op.drop_table('normalized_roles')
    op.drop_table('raw_jds')
    op.drop_table('b2b_aggregate_reports')
    op.drop_table('invite_links')
    op.drop_table('application_stages')

    # Drop enum types
    op.execute("DROP TYPE IF EXISTS jd_source_platform")
    op.execute("DROP TYPE IF EXISTS jd_data_source")
