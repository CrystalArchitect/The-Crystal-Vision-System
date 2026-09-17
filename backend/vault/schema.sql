-- MemoryCore Vault: Canonical Decision Authority
-- SHA-256 receipt chain for immutable audit trails

CREATE SCHEMA IF NOT EXISTS vault;

-- Workspace isolation: all operations scoped to workspace_id
CREATE TABLE IF NOT EXISTS vault.workspaces (
    workspace_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Administrative Decisions with immutable SHA-256 chain
CREATE TABLE IF NOT EXISTS vault.decisions (
    decision_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES vault.workspaces(workspace_id) ON DELETE CASCADE,

    -- Decision identity
    decision_code VARCHAR(50) NOT NULL,  -- e.g., ADM-001, ADM-002
    title VARCHAR(500) NOT NULL,
    description TEXT,

    -- Decision content and enforcement
    decision_type VARCHAR(50) NOT NULL,  -- 'linting_standard', 'deprecation_status', 'policy'
    payload JSONB NOT NULL,  -- The actual decision content (varies by type)
    enforcement_scope VARCHAR(255),  -- e.g., 'repository', 'organization', 'global'

    -- Steward approval
    created_by UUID NOT NULL,  -- Steward UUID
    approved_by UUID,  -- Approving steward UUID (if multi-step approval)

    -- Status and versioning
    status VARCHAR(50) NOT NULL DEFAULT 'draft',  -- draft, awaiting_approval, active, superseded, revoked
    version INT DEFAULT 1,
    supersedes_decision_id UUID REFERENCES vault.decisions(decision_id),

    -- Immutable audit chain
    previous_hash VARCHAR(64),  -- SHA-256 of previous decision for this code
    event_hash VARCHAR(64) NOT NULL,  -- SHA-256 of this decision (immutable receipt)

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP WITH TIME ZONE,
    effective_at TIMESTAMP WITH TIME ZONE,
    revoked_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(workspace_id, decision_code, version),
    CHECK (status IN ('draft', 'awaiting_approval', 'active', 'superseded', 'revoked'))
);

-- Immutable audit log for all decision mutations
CREATE TABLE IF NOT EXISTS vault.audit_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES vault.workspaces(workspace_id) ON DELETE CASCADE,

    -- Event classification
    event_category VARCHAR(50) NOT NULL,  -- 'decision_created', 'decision_approved', 'decision_revoked', etc.
    event_action VARCHAR(255) NOT NULL,

    -- Related entities
    decision_id UUID REFERENCES vault.decisions(decision_id),
    actor_steward_id UUID NOT NULL,  -- Steward who caused this event

    -- Event details
    outcome VARCHAR(50) NOT NULL DEFAULT 'success',  -- success, failed, blocked, revoked
    detail TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Immutable receipt chain
    previous_event_hash VARCHAR(64),  -- SHA-256 of previous event
    event_hash VARCHAR(64) NOT NULL,  -- SHA-256 of this event

    -- Timestamp (immutable)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CHECK (outcome IN ('success', 'failed', 'blocked', 'revoked'))
);

-- Steward registry with biometric enrollment status
CREATE TABLE IF NOT EXISTS vault.stewards (
    steward_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES vault.workspaces(workspace_id) ON DELETE CASCADE,

    -- Identity
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,

    -- Authentication
    biometric_enrolled BOOLEAN DEFAULT FALSE,
    biometric_type VARCHAR(50),  -- 'face_id', 'touch_id', 'windows_hello', 'fingerprint'
    voice_signature_enrolled BOOLEAN DEFAULT FALSE,

    -- Authorization
    can_create_decisions BOOLEAN DEFAULT FALSE,
    can_approve_decisions BOOLEAN DEFAULT FALSE,
    can_revoke_decisions BOOLEAN DEFAULT FALSE,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_active_at TIMESTAMP WITH TIME ZONE,

    UNIQUE(workspace_id, email)
);

-- Decision enforcement log for UK portfolio CI/CD integration
CREATE TABLE IF NOT EXISTS vault.enforcement_log (
    enforcement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES vault.workspaces(workspace_id) ON DELETE CASCADE,

    -- Repository and decision being enforced
    repository_name VARCHAR(255) NOT NULL,
    decision_id UUID NOT NULL REFERENCES vault.decisions(decision_id),
    decision_code VARCHAR(50) NOT NULL,

    -- Enforcement result
    enforced_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    outcome VARCHAR(50) NOT NULL,  -- 'approved', 'rejected', 'warning'
    enforcement_detail TEXT,

    -- CI/CD context
    ci_run_id VARCHAR(255),  -- GitHub Actions run ID, GitLab pipeline ID, etc.
    ci_commit_sha VARCHAR(40),
    ci_branch VARCHAR(255),

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_decisions_workspace ON vault.decisions(workspace_id);
CREATE INDEX IF NOT EXISTS idx_decisions_code ON vault.decisions(workspace_id, decision_code);
CREATE INDEX IF NOT EXISTS idx_decisions_status ON vault.decisions(workspace_id, status);
CREATE INDEX IF NOT EXISTS idx_decisions_hash ON vault.decisions(event_hash);
CREATE INDEX IF NOT EXISTS idx_audit_events_workspace ON vault.audit_events(workspace_id);
CREATE INDEX IF NOT EXISTS idx_audit_events_decision ON vault.audit_events(decision_id);
CREATE INDEX IF NOT EXISTS idx_audit_events_hash ON vault.audit_events(event_hash);
CREATE INDEX IF NOT EXISTS idx_enforcement_log_decision ON vault.enforcement_log(decision_id);
CREATE INDEX IF NOT EXISTS idx_enforcement_log_repo ON vault.enforcement_log(repository_name);
CREATE INDEX IF NOT EXISTS idx_stewards_workspace ON vault.stewards(workspace_id);
CREATE INDEX IF NOT EXISTS idx_stewards_email ON vault.stewards(workspace_id, email);

-- Create initial workspace
INSERT INTO vault.workspaces (name, metadata)
VALUES ('Crystal Vision Default', '{"description": "Default workspace for Crystal Vision system"}')
ON CONFLICT DO NOTHING;
