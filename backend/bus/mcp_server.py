"""
CrystalBus: Model Context Protocol server for canonical decision access.
Read-only MCP tool for UK portfolio repositories to fetch decisions.
"""

import json
import logging
from typing import Optional
import httpx
from datetime import datetime

logger = logging.getLogger(__name__)


class CrystalBusServer:
    """MCP server providing read-only access to decisions from MemoryCore Vault"""

    def __init__(self, portal_url: str = "http://localhost:8000"):
        self.portal_url = portal_url
        self.client = httpx.Client(timeout=10.0)

    def get_decision(self, decision_code: str) -> dict:
        """
        Fetch decision by code from MemoryCore Vault.
        Returns the current active decision with immutable receipt hash.

        Args:
            decision_code: Decision code (e.g., 'ADM-001', 'ADM-002')

        Returns:
            Decision object with decision_id, title, status, event_hash, payload
        """
        try:
            response = self.client.get(
                f"{self.portal_url}/v1/decisions/{decision_code}"
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch decision {decision_code}: {e}")
            return {
                "error": f"Decision {decision_code} not found or service unavailable",
                "decision_code": decision_code
            }

    def get_decision_payload(self, decision_code: str) -> Optional[dict]:
        """
        Fetch just the decision payload (for CI/CD enforcement).

        Args:
            decision_code: Decision code (e.g., 'ADM-001')

        Returns:
            Decision payload dict or None if not found
        """
        decision = self.get_decision(decision_code)
        if "error" not in decision:
            return decision.get("payload", {})
        return None

    def get_audit_chain(self, decision_id: str) -> list:
        """
        Fetch immutable audit chain for a decision.
        Each event includes SHA-256 hash for chain verification.

        Args:
            decision_id: UUID of decision

        Returns:
            List of audit events with hashes
        """
        try:
            response = self.client.get(
                f"{self.portal_url}/v1/audit-chain/{decision_id}"
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch audit chain for {decision_id}: {e}")
            return []

    def verify_audit_chain(self, audit_chain: list) -> bool:
        """
        Verify integrity of audit chain by checking hash sequence.

        Args:
            audit_chain: List of audit events from get_audit_chain()

        Returns:
            True if chain is valid (each event's previous_hash matches prior event's hash)
        """
        if not audit_chain:
            return True

        for i, event in enumerate(audit_chain):
            if i == 0:
                # First event should have no previous_hash
                if event.get("previous_event_hash") is not None:
                    logger.warning("First audit event has unexpected previous_hash")
                    return False
            else:
                # Verify previous_hash matches prior event's hash
                prior_event = audit_chain[i - 1]
                if event.get("previous_event_hash") != prior_event.get("event_hash"):
                    logger.error(f"Audit chain broken at event {i}")
                    return False

        return True


# Singleton instance
_bus_instance: Optional[CrystalBusServer] = None


def get_crystal_bus(portal_url: str = "http://localhost:8000") -> CrystalBusServer:
    """Get or create CrystalBus singleton"""
    global _bus_instance
    if _bus_instance is None:
        _bus_instance = CrystalBusServer(portal_url)
    return _bus_instance


# MCP Tool Definitions for integration with Claude/other agents
MCP_TOOLS = {
    "crystal_get_decision": {
        "description": "Fetch canonical decision from MemoryCore Vault by code",
        "inputSchema": {
            "type": "object",
            "properties": {
                "decision_code": {
                    "type": "string",
                    "description": "Decision code (e.g., 'ADM-001', 'ADM-002')"
                }
            },
            "required": ["decision_code"]
        }
    },
    "crystal_get_decision_payload": {
        "description": "Fetch decision payload for enforcement (used by CI/CD)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "decision_code": {
                    "type": "string",
                    "description": "Decision code"
                }
            },
            "required": ["decision_code"]
        }
    },
    "crystal_get_audit_chain": {
        "description": "Fetch immutable audit chain for decision (includes SHA-256 hashes)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "decision_id": {
                    "type": "string",
                    "description": "Decision UUID"
                }
            },
            "required": ["decision_id"]
        }
    },
    "crystal_verify_audit_chain": {
        "description": "Verify integrity of audit chain by checking hash sequence",
        "inputSchema": {
            "type": "object",
            "properties": {
                "audit_chain": {
                    "type": "array",
                    "description": "Audit chain from crystal_get_audit_chain"
                }
            },
            "required": ["audit_chain"]
        }
    }
}
