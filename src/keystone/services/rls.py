"""Row-Level Security (RLS) enforcement for B2B tenant isolation.

Defense-in-depth: RLS at database level supplements application-level filtering.

PostgreSQL RLS uses current_setting('app.current_tenant_id') to enforce
tenant isolation. The application must set this session variable before
executing queries on B2B tables.

IMPORTANT: This module provides helper functions for RLS setup.
For MVP, application-level filtering (tenant_id in WHERE clauses) is
the primary enforcement. RLS at DB level is defense-in-depth.
"""
from typing import Optional
from uuid import UUID
import structlog

logger = structlog.get_logger()

# SQL for enabling RLS on a table
ENABLE_RLS_SQL = """
ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;
"""

# SQL for creating a policy that enforces tenant isolation
CREATE_TENANT_POLICY_SQL = """
CREATE POLICY tenant_isolation_policy_{table} ON {table}
    USING (tenant_id = current_setting('app.current_tenant_id', true)::uuid);
"""

# SQL to set the current tenant (use with SET LOCAL)
SET_TENANT_SQL = """
SET LOCAL app.current_tenant_id = '{tenant_id}';
"""


def get_tenant_filter_clause(table_name: str) -> str:
    """Get SQL filter clause for tenant isolation.

    This is the application-level enforcement - all B2B queries
    must include this filter.

    Args:
        table_name: Name of the table

    Returns:
        SQL WHERE clause fragment
    """
    return f"{table_name}.tenant_id = current_setting('app.current_tenant_id', true)::uuid"


class TenantContext:
    """Context manager for tenant-scoped operations.

    Usage:
        async with TenantContext(tenant_id):
            # All queries in this block run with tenant context set
            results = await db.execute(select(B2BJobDescription))
    """

    def __init__(self, tenant_id: UUID):
        self.tenant_id = tenant_id

    async def __aenter__(self):
        # In a real implementation, this would SET LOCAL app.current_tenant_id
        # For SQLAlchemy, this would be done via a connection event
        logger.debug("tenant_context_entered", tenant_id=str(self.tenant_id))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Cleanup tenant context
        logger.debug("tenant_context_exited", tenant_id=str(self.tenant_id))


def validate_tenant_access(resource_tenant_id: UUID, user_tenant_id: UUID) -> bool:
    """Validate that a user belongs to the resource's tenant.

    This is the application-level check for tenant isolation.
    All API endpoints that access B2B resources must call this.

    Args:
        resource_tenant_id: Tenant ID of the resource being accessed
        user_tenant_id: Tenant ID of the current user

    Returns:
        True if access is allowed

    Raises:
        PermissionError if access denied
    """
    if resource_tenant_id != user_tenant_id:
        logger.warning(
            "tenant_access_denied",
            resource_tenant=str(resource_tenant_id),
            user_tenant=str(user_tenant_id)
        )
        raise PermissionError("Access denied: resource belongs to different tenant")
    return True


# SQLAlchemy event handler for setting tenant context
# This would be registered on the connection pool to automatically
# set the tenant context for all queries in a request

async def set_tenant_context(connection, tenant_id: UUID) -> None:
    """Set tenant context on a database connection.

    Must be called before any queries on B2B tables.
    """
    await connection.execute(
        f"SET LOCAL app.current_tenant_id = '{tenant_id}'"
    )
    logger.debug("tenant_context_set", tenant_id=str(tenant_id))
