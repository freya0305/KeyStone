"""Initial schema with RLS for B2B tenant isolation.

Revision ID: 001
Revises:
Create Date: 2026-05-04

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial schema with RLS policies for B2B tables."""

    # Create enum types
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE subscriptiontier AS ENUM ('free', 'solo', 'pro', 'team');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    op.execute("""
        DO $$ BEGIN
            CREATE TYPE applicationstatus AS ENUM ('interested', 'applied', 'screening', 'interview', 'offer', 'rejected', 'withdrawn');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    op.execute("""
        DO $$ BEGIN
            CREATE TYPE accesslevel AS ENUM ('admin', 'member');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('subscription_tier', sa.Enum('free', 'solo', 'pro', 'team', name='subscriptiontier', create_type=False), nullable=False),
        sa.Column('stripe_customer_id', sa.String(255), nullable=True, unique=True),
        sa.Column('stripe_subscription_id', sa.String(255), nullable=True),
        sa.Column('consent_pdpa', sa.Boolean(), default=False),
        sa.Column('consent_marketing', sa.Boolean(), default=False),
        sa.Column('consent_ai_training', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Resumes table
    op.create_table(
        'resumes',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('content_hash', sa.String(64), nullable=False),
        sa.Column('parsed_json', sa.JSON(), nullable=True),
        sa.Column('sg_flags', sa.JSON(), nullable=True),
        sa.Column('s3_key', sa.String(512), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_resumes_user_id', 'resumes', ['user_id'])
    op.create_index('ix_resumes_content_hash', 'resumes', ['content_hash'])

    # B2B Tenants table
    op.create_table(
        'b2b_tenants',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('tenant_type', sa.String(50), nullable=True),
        sa.Column('contract_value', sa.Numeric(10, 2), nullable=True),
        sa.Column('seat_count', sa.Integer(), default=1),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # B2B Users table
    op.create_table(
        'b2b_users',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=False, unique=True),
        sa.Column('tenant_id', sa.UUID(), sa.ForeignKey('b2b_tenants.id'), nullable=False),
        sa.Column('access_level', sa.Enum('admin', 'member', name='accesslevel', create_type=False), nullable=False),
        sa.Column('provisioned_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_b2b_users_user_id', 'b2b_users', ['user_id'])
    op.create_index('ix_b2b_users_tenant_id', 'b2b_users', ['tenant_id'])

    # B2B Job Descriptions table
    op.create_table(
        'b2b_job_descriptions',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('tenant_id', sa.UUID(), sa.ForeignKey('b2b_tenants.id'), nullable=False),
        sa.Column('created_by_id', sa.UUID(), sa.ForeignKey('b2b_users.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('company', sa.String(255), nullable=False),
        sa.Column('company_type', sa.String(50), nullable=True),
        sa.Column('skills_json', sa.JSON(), nullable=False),
        sa.Column('seniority', sa.String(20), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('brand_template_id', sa.UUID(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('rating_feedback', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_b2b_jd_tenant_id', 'b2b_job_descriptions', ['tenant_id'])
    op.create_index('ix_b2b_jd_created_by_id', 'b2b_job_descriptions', ['created_by_id'])

    # B2B Share Links table
    op.create_table(
        'b2b_share_links',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('jd_id', sa.UUID(), sa.ForeignKey('b2b_job_descriptions.id'), nullable=False),
        sa.Column('token', sa.String(64), nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('view_count', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_b2b_share_token', 'b2b_share_links', ['token'])

    # B2B Versions table
    op.create_table(
        'b2b_versions',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('jd_id', sa.UUID(), sa.ForeignKey('b2b_job_descriptions.id'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # B2B Templates table
    op.create_table(
        'b2b_templates',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('tenant_id', sa.UUID(), sa.ForeignKey('b2b_tenants.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('logo_s3_key', sa.String(512), nullable=True),
        sa.Column('brand_primary_color', sa.String(7), default='#4F46E5'),
        sa.Column('brand_secondary_color', sa.String(7), default='#6B7280'),
        sa.Column('font_choice', sa.String(50), default='Inter'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # Job Analyses table
    op.create_table(
        'job_analyses',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('resume_id', sa.UUID(), sa.ForeignKey('resumes.id'), nullable=True),
        sa.Column('job_url', sa.Text(), nullable=True),
        sa.Column('job_parsed_json', sa.JSON(), nullable=True),
        sa.Column('company_type', sa.String(50), nullable=True),
        sa.Column('match_results', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_job_analyses_user_id', 'job_analyses', ['user_id'])

    # Suggestions table
    op.create_table(
        'suggestions',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('job_analysis_id', sa.UUID(), sa.ForeignKey('job_analyses.id'), nullable=False),
        sa.Column('section', sa.String(100), nullable=False),
        sa.Column('original_text', sa.Text(), nullable=False),
        sa.Column('suggested_text', sa.Text(), nullable=False),
        sa.Column('rationale', sa.Text(), nullable=True),
        sa.Column('sg_context', sa.JSON(), nullable=True),
        sa.Column('match_level', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # Suggestion Signals table
    op.create_table(
        'suggestion_signals',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('anonymized_user_id', sa.String(64), nullable=False),
        sa.Column('suggestion_id', sa.UUID(), sa.ForeignKey('suggestions.id'), nullable=False),
        sa.Column('action', sa.String(20), nullable=False),
        sa.Column('modified_text', sa.Text(), nullable=True),
        sa.Column('context_company_type', sa.String(50), nullable=True),
        sa.Column('context_role_level', sa.String(20), nullable=True),
        sa.Column('context_industry', sa.String(100), nullable=True),
        sa.Column('context_ns_related', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_suggestion_signals_created_at', 'suggestion_signals', ['created_at'])

    # Applications table
    op.create_table(
        'applications',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('job_analysis_id', sa.UUID(), sa.ForeignKey('job_analyses.id'), nullable=True),
        sa.Column('employer', sa.String(255), nullable=False),
        sa.Column('role', sa.String(255), nullable=False),
        sa.Column('applied_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.Enum('interested', 'applied', 'screening', 'interview', 'offer', 'rejected', 'withdrawn', name='applicationstatus', create_type=False), nullable=True),
        sa.Column('stages', sa.JSON(), default=[]),
        sa.Column('final_outcome', sa.String(50), nullable=True),
        sa.Column('source', sa.String(100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_applications_user_id', 'applications', ['user_id'])
    op.create_index('ix_applications_created_at', 'applications', ['created_at'])

    # User Consents table
    op.create_table(
        'user_consents',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('consent_type', sa.String(50), nullable=False),
        sa.Column('granted', sa.Boolean(), nullable=False),
        sa.Column('granted_at', sa.DateTime(), nullable=True),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
    )

    # ========== RLS POLICIES ==========
    # Enable RLS on B2B tables and create tenant isolation policies

    # B2B Tenants - admin access
    op.execute("ALTER TABLE b2b_tenants ENABLE ROW LEVEL SECURITY")

    # B2B Users - tenant isolation
    op.execute("ALTER TABLE b2b_users ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY b2b_users_tenant_isolation ON b2b_users
            FOR ALL
            USING (tenant_id::text = current_setting('app.current_tenant_id', true))
    """)

    # B2B Job Descriptions - tenant isolation
    op.execute("ALTER TABLE b2b_job_descriptions ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY b2b_jd_tenant_isolation ON b2b_job_descriptions
            FOR ALL
            USING (tenant_id::text = current_setting('app.current_tenant_id', true))
    """)

    # B2B Share Links - via JD tenant isolation
    op.execute("ALTER TABLE b2b_share_links ENABLE ROW LEVEL SECURITY")

    # B2B Versions - via JD tenant isolation
    op.execute("ALTER TABLE b2b_versions ENABLE ROW LEVEL SECURITY")

    # B2B Templates - tenant isolation
    op.execute("ALTER TABLE b2b_templates ENABLE ROW LEVEL SECURITY")
    op.execute("""
        CREATE POLICY b2b_templates_tenant_isolation ON b2b_templates
            FOR ALL
            USING (tenant_id::text = current_setting('app.current_tenant_id', true))
    """)

    # Create index for faster lookups
    op.create_index('ix_suggestion_signals_suggestion_id', 'suggestion_signals', ['suggestion_id'])


def downgrade() -> None:
    """Drop all tables and RLS policies."""
    # Drop RLS policies first
    op.execute("DROP POLICY IF EXISTS b2b_users_tenant_isolation ON b2b_users")
    op.execute("DROP POLICY IF EXISTS b2b_jd_tenant_isolation ON b2b_job_descriptions")
    op.execute("DROP POLICY IF EXISTS b2b_templates_tenant_isolation ON b2b_templates")

    # Disable RLS
    op.execute("ALTER TABLE b2b_tenants DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE b2b_users DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE b2b_job_descriptions DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE b2b_share_links DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE b2b_versions DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE b2b_templates DISABLE ROW LEVEL SECURITY")

    # Drop tables
    op.drop_table('user_consents')
    op.drop_table('applications')
    op.drop_table('suggestion_signals')
    op.drop_table('suggestions')
    op.drop_table('job_analyses')
    op.drop_table('b2b_templates')
    op.drop_table('b2b_versions')
    op.drop_table('b2b_share_links')
    op.drop_table('b2b_job_descriptions')
    op.drop_table('b2b_users')
    op.drop_table('b2b_tenants')
    op.drop_table('resumes')
    op.drop_table('users')

    # Drop enum types
    op.execute("DROP TYPE IF EXISTS subscriptiontier")
    op.execute("DROP TYPE IF EXISTS applicationstatus")
    op.execute("DROP TYPE IF EXISTS accesslevel")
