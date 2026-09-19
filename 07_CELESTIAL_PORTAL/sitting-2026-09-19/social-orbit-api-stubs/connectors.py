from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID, uuid4

from .models import (
    CapabilityMatrix,
    ConnectCallbackRequest,
    ConnectorAccount,
    ConnectorStatus,
    PlatformVariant,
    ProviderId,
    PublicationJob,
    PublicationTarget,
    utc_now,
)


class ConnectorNotImplemented(RuntimeError):
    """Raised when a provider adapter is still a safe, non-publishing stub."""


class ConnectorAuthError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProviderSpec:
    provider: ProviderId
    scopes: tuple[str, ...]
    capability: CapabilityMatrix


PROVIDER_SPECS: dict[ProviderId, ProviderSpec] = {
    ProviderId.YOUTUBE: ProviderSpec(
        ProviderId.YOUTUBE,
        ("openid", "youtube.upload", "youtube.readonly"),
        CapabilityMatrix(provider=ProviderId.YOUTUBE, can_publish_video=True, can_schedule=True, can_fetch_analytics=True, supports_drafts=False, supported_asset_kinds=["video", "thumbnail", "caption"]),
    ),
    ProviderId.INSTAGRAM: ProviderSpec(
        ProviderId.INSTAGRAM,
        ("instagram_basic", "instagram_content_publish"),
        CapabilityMatrix(provider=ProviderId.INSTAGRAM, can_publish_video=True, can_publish_image=True, can_publish_carousel=True, can_fetch_analytics=True, requires_business_account=True, supported_asset_kinds=["video", "image", "carousel", "caption"]),
    ),
    ProviderId.TIKTOK: ProviderSpec(
        ProviderId.TIKTOK,
        ("user.info.basic", "video.publish"),
        CapabilityMatrix(provider=ProviderId.TIKTOK, can_publish_video=True, can_fetch_analytics=True, requires_manual_review=True, supported_asset_kinds=["video", "caption"], notes=["Verify current app review and direct-post eligibility before enabling."]),
    ),
    ProviderId.X: ProviderSpec(
        ProviderId.X,
        ("tweet.read", "tweet.write", "users.read", "offline.access"),
        CapabilityMatrix(provider=ProviderId.X, can_publish_image=True, can_publish_video=True, can_fetch_comments=True, can_fetch_analytics=True, supported_asset_kinds=["image", "video", "caption"]),
    ),
    ProviderId.LINKEDIN: ProviderSpec(
        ProviderId.LINKEDIN,
        ("openid", "profile", "w_member_social"),
        CapabilityMatrix(provider=ProviderId.LINKEDIN, can_publish_image=True, can_publish_video=True, can_fetch_analytics=True, requires_manual_review=True, supported_asset_kinds=["image", "video", "caption"]),
    ),
}

for provider in (ProviderId.FACEBOOK, ProviderId.REDDIT, ProviderId.DISCORD, ProviderId.TELEGRAM, ProviderId.SLACK):
    PROVIDER_SPECS.setdefault(
        provider,
        ProviderSpec(provider, tuple(), CapabilityMatrix(provider=provider, notes=["Adapter contract reserved; provider-specific implementation pending."])),
    )


class SocialConnector(ABC):
    provider: ProviderId

    @abstractmethod
    def capabilities(self) -> CapabilityMatrix:
        raise NotImplementedError

    @abstractmethod
    def authorization_url(self, state: str) -> tuple[str, list[str]]:
        raise NotImplementedError

    @abstractmethod
    def connect(self, request: ConnectCallbackRequest) -> ConnectorAccount:
        raise NotImplementedError

    @abstractmethod
    def refresh(self, account: ConnectorAccount) -> ConnectorAccount:
        raise NotImplementedError

    @abstractmethod
    def publish(self, job: PublicationJob, target: PublicationTarget, variant: PlatformVariant) -> str:
        raise NotImplementedError

    @abstractmethod
    def revoke(self, account: ConnectorAccount) -> ConnectorAccount:
        raise NotImplementedError


class StubConnector(SocialConnector):
    def __init__(self, provider: ProviderId) -> None:
        self.provider = provider
        self.spec = PROVIDER_SPECS[provider]

    def capabilities(self) -> CapabilityMatrix:
        return self.spec.capability

    def authorization_url(self, state: str) -> tuple[str, list[str]]:
        # Never use this placeholder URL for production OAuth. Configure the real
        # provider authorization endpoint through server-side settings.
        return (f"https://connect.invalid/{self.provider.value}/authorize?state={state}", list(self.spec.scopes))

    def connect(self, request: ConnectCallbackRequest) -> ConnectorAccount:
        if request.code.startswith("stub_"):
            return ConnectorAccount(
                workspace_id=request.workspace_id,
                provider=self.provider,
                provider_account_id=f"stub-account-{uuid4().hex[:12]}",
                display_name=f"Stub {self.provider.value.title()} account",
                status=ConnectorStatus.CONNECTED,
                scopes=list(self.spec.scopes),
                capabilities=self.capabilities(),
                connected_at=utc_now(),
                last_refreshed_at=utc_now(),
            )
        raise ConnectorAuthError("Provider OAuth exchange is intentionally not implemented in this stub.")

    def refresh(self, account: ConnectorAccount) -> ConnectorAccount:
        if account.status in {ConnectorStatus.REVOKED, ConnectorStatus.ERROR}:
            raise ConnectorAuthError("Cannot refresh a revoked or errored connector account.")
        return account.model_copy(update={"last_refreshed_at": utc_now(), "status": ConnectorStatus.CONNECTED})

    def publish(self, job: PublicationJob, target: PublicationTarget, variant: PlatformVariant) -> str:
        raise ConnectorNotImplemented(f"{self.provider.value} publishing is a stub; no external request was made.")

    def revoke(self, account: ConnectorAccount) -> ConnectorAccount:
        return account.model_copy(update={"status": ConnectorStatus.REVOKED, "revoked_at": utc_now()})


def connector_for(provider: ProviderId) -> SocialConnector:
    return StubConnector(provider)
