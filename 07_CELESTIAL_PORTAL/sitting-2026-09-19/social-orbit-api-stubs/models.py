from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ProviderId(str, Enum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    X = "x"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    REDDIT = "reddit"
    DISCORD = "discord"
    TELEGRAM = "telegram"
    SLACK = "slack"


class ConnectorStatus(str, Enum):
    PENDING = "pending"
    CONNECTED = "connected"
    EXPIRED = "expired"
    REVOKED = "revoked"
    ERROR = "error"


class JobStatus(str, Enum):
    DRAFT = "draft"
    AWAITING_APPROVAL = "awaiting_approval"
    QUEUED = "queued"
    UPLOADING = "uploading"
    PUBLISHED = "published"
    SCHEDULED = "scheduled"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class AssetKind(str, Enum):
    SCRIPT = "script"
    VIDEO = "video"
    IMAGE = "image"
    AUDIO = "audio"
    CAPTION = "caption"
    THUMBNAIL = "thumbnail"
    CAROUSEL = "carousel"


class DataClass(str, Enum):
    PROMPT = "prompt"
    DRAFT = "draft"
    MEDIA = "media"
    AUDIO = "audio"
    BIOMETRIC = "biometric"
    ACCOUNT_METADATA = "account_metadata"
    ANALYTICS = "analytics"
    PRIVATE_MESSAGES = "private_messages"


class AuditCategory(str, Enum):
    CONNECTION = "connection"
    CONSENT = "consent"
    PUBLICATION = "publication"
    ANALYTICS = "analytics"
    MEDIA = "media"
    SECURITY = "security"


class CapabilityMatrix(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: ProviderId
    can_publish_video: bool = False
    can_publish_image: bool = False
    can_publish_carousel: bool = False
    can_schedule: bool = False
    can_edit_after_publish: bool = False
    can_fetch_comments: bool = False
    can_fetch_analytics: bool = False
    requires_business_account: bool = False
    requires_manual_review: bool = True
    supports_webhooks: bool = False
    supports_drafts: bool = False
    supported_asset_kinds: list[AssetKind] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ConsentGrant(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    provider: ProviderId
    action: str = Field(min_length=1, max_length=80)
    data_classes: list[DataClass] = Field(min_length=1)
    purpose: str = Field(min_length=1, max_length=500)
    policy_version: int = Field(default=1, ge=1)
    granted: bool = False
    granted_by: UUID | None = None
    expires_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)

    def is_active(self, at: datetime | None = None) -> bool:
        now = at or utc_now()
        return self.granted and (self.expires_at is None or self.expires_at > now)


class ConnectorAccount(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    provider: ProviderId
    provider_account_id: str = Field(min_length=1, max_length=255)
    display_name: str = Field(min_length=1, max_length=255)
    status: ConnectorStatus = ConnectorStatus.PENDING
    scopes: list[str] = Field(default_factory=list)
    capabilities: CapabilityMatrix | None = None
    connected_at: datetime | None = None
    last_refreshed_at: datetime | None = None
    revoked_at: datetime | None = None


class ContentAsset(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    project_id: UUID
    kind: AssetKind
    storage_ref: str = Field(min_length=1, max_length=2000)
    mime_type: str = Field(min_length=1, max_length=120)
    byte_size: int = Field(ge=0)
    duration_seconds: float | None = Field(default=None, ge=0)
    width: int | None = Field(default=None, ge=1)
    height: int | None = Field(default=None, ge=1)
    checksum_sha256: str | None = Field(default=None, min_length=64, max_length=64)
    provenance: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("checksum_sha256")
    @classmethod
    def validate_checksum(cls, value: str | None) -> str | None:
        if value is not None:
            int(value, 16)
        return value


class PlatformVariant(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    source_asset_id: UUID
    provider: ProviderId
    title: str | None = Field(default=None, max_length=300)
    caption: str | None = Field(default=None, max_length=5000)
    hashtags: list[str] = Field(default_factory=list, max_length=50)
    asset_ids: list[UUID] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    validated: bool = False
    validation_errors: list[str] = Field(default_factory=list)


class PublicationTarget(BaseModel):
    model_config = ConfigDict(extra="forbid")

    connector_account_id: UUID
    provider: ProviderId
    variant_id: UUID
    scheduled_for: datetime | None = None
    destination_ref: str | None = Field(default=None, max_length=500)
    approved: bool = False


class PublicationJob(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    project_id: UUID
    idempotency_key: str = Field(min_length=8, max_length=200)
    targets: list[PublicationTarget] = Field(min_length=1)
    status: JobStatus = JobStatus.DRAFT
    consent_grant_ids: list[UUID] = Field(default_factory=list)
    attempts: int = Field(default=0, ge=0)
    provider_receipts: dict[str, str] = Field(default_factory=dict)
    failure_code: str | None = None
    failure_detail: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ApprovalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approved: bool
    reviewer_id: UUID
    note: str | None = Field(default=None, max_length=1000)


class ConsentDecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workspace_id: UUID
    provider: ProviderId
    action: str = Field(min_length=1, max_length=80)
    data_classes: list[DataClass] = Field(min_length=1)
    purpose: str = Field(min_length=1, max_length=500)


class ConsentDecision(BaseModel):
    allowed: bool
    reason: str
    policy_version: int = 1
    grant: ConsentGrant | None = None


class ConnectStartResponse(BaseModel):
    provider: ProviderId
    authorization_url: HttpUrl
    state: str
    requested_scopes: list[str]


class ConnectCallbackRequest(BaseModel):
    workspace_id: UUID
    code: str = Field(min_length=1, max_length=4096)
    state: str = Field(min_length=8, max_length=512)


class PublishRequest(BaseModel):
    workspace_id: UUID
    project_id: UUID
    idempotency_key: str = Field(min_length=8, max_length=200)
    targets: list[PublicationTarget] = Field(min_length=1)
    consent_grant_ids: list[UUID] = Field(default_factory=list)
    require_manual_approval: bool = True


class AnalyticsSnapshot(BaseModel):
    provider: ProviderId
    provider_object_id: str
    captured_at: datetime = Field(default_factory=utc_now)
    raw_metrics: dict[str, float] = Field(default_factory=dict)
    normalized_metrics: dict[str, float] = Field(default_factory=dict)
    normalization_rule_version: str = "v1"


class AuditEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    category: AuditCategory
    action: str = Field(min_length=1, max_length=120)
    outcome: Literal["started", "success", "failed", "blocked", "revoked"]
    provider: ProviderId | None = None
    subject: str = Field(min_length=1, max_length=300)
    detail: str = Field(default="", max_length=2000)
    previous_hash: str | None = None
    event_hash: str | None = None
    created_at: datetime = Field(default_factory=utc_now)


class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: UUID = Field(default_factory=uuid4)
