"""
Incognita Lattice Orchestrator
Part of Civilisation.One + CrystalCoreOS integration
Version: v0.1 (Routing & Coordination Stub)

Routes messages and reasoning results between lattice components
based on coordinate-based addressing and consent constraints.

This is a stub providing the interface and core routing logic.
Future versions will add:
- Consent-based message filtering
- Authority delegation
- Cross-component orchestration
- Transaction logging via Chronicle
"""

from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
import json
from .coordinate import LatticeCoordinate, CoordinateRegistry


class RoutingTable:
    """
    Central routing table for lattice components.

    Maintains the mapping from route keys to handler functions,
    enabling deterministic message dispatch.
    """

    def __init__(self):
        """Initialize empty routing table."""
        self.routes: Dict[str, Callable] = {}
        self.route_log: List[Dict[str, Any]] = []

    def register_route(self, route_key: str, handler: Callable) -> bool:
        """
        Register a handler for a route.

        Args:
            route_key: Target route (Layer:Agent:Session format)
            handler: Callable(message: Dict) -> Dict

        Returns:
            True if registered; False if collision
        """
        if route_key in self.routes:
            return False

        self.routes[route_key] = handler
        self.route_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "REGISTER_ROUTE",
            "route_key": route_key,
            "handler": handler.__name__ if hasattr(handler, "__name__") else str(handler)
        })
        return True

    def lookup_route(self, route_key: str) -> Optional[Callable]:
        """Look up handler for a route."""
        return self.routes.get(route_key)

    def dispatch(self, route_key: str, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Dispatch a message to a route handler.

        Args:
            route_key: Target route
            message: Message payload

        Returns:
            Handler result or None if route not found
        """
        handler = self.lookup_route(route_key)
        if handler is None:
            self._log_dispatch("NOT_FOUND", route_key, message)
            return None

        try:
            result = handler(message)
            self._log_dispatch("SUCCESS", route_key, message, result)
            return result
        except Exception as e:
            self._log_dispatch("ERROR", route_key, message, error=str(e))
            return None

    def _log_dispatch(self, status: str, route_key: str, message: Dict,
                      result: Optional[Dict] = None, error: Optional[str] = None):
        """Internal: log dispatch event."""
        self.route_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "DISPATCH",
            "status": status,
            "route_key": route_key,
            "message_keys": list(message.keys()) if message else [],
            "result_keys": list(result.keys()) if result else [],
            "error": error
        })

    def list_routes(self) -> List[str]:
        """List all registered routes."""
        return list(self.routes.keys())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize routing table state."""
        return {
            "total_routes": len(self.routes),
            "routes": self.list_routes(),
            "recent_dispatches": self.route_log[-10:]
        }


class MessageEnvelope:
    """
    Standardized message format for lattice communication.

    Every message carries:
    - Source and destination coordinates
    - Payload
    - Authority and consent metadata
    - Cryptographic hash for integrity
    """

    def __init__(self, source: LatticeCoordinate, destination: LatticeCoordinate,
                 payload: Dict[str, Any], authority: Optional[str] = None,
                 consent_required: Optional[int] = None):
        """
        Initialize a message envelope.

        Args:
            source: Originating coordinate
            destination: Target coordinate
            payload: Message content
            authority: Authority level required to process
            consent_required: Consent bitmask (if any)
        """
        self.source = source
        self.destination = destination
        self.payload = payload
        self.authority = authority or "default"
        self.consent_required = consent_required or 0
        self.timestamp = datetime.utcnow().isoformat()
        self.message_id = f"{source.full_key()}→{destination.full_key()}@{self.timestamp}"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize envelope to dictionary."""
        return {
            "source": self.source.to_dict(),
            "destination": self.destination.to_dict(),
            "payload": self.payload,
            "authority": self.authority,
            "consent_required": self.consent_required,
            "timestamp": self.timestamp,
            "message_id": self.message_id
        }

    def to_json(self) -> str:
        """Serialize envelope to JSON."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageEnvelope":
        """Deserialize envelope from dictionary."""
        source = LatticeCoordinate.from_full_key(data["source"]["full_key"])
        destination = LatticeCoordinate.from_full_key(data["destination"]["full_key"])
        return cls(
            source=source,
            destination=destination,
            payload=data["payload"],
            authority=data.get("authority", "default"),
            consent_required=data.get("consent_required", 0)
        )

    def route_key(self) -> str:
        """Get the route key for this message's destination."""
        return self.destination.route_key()

    def __str__(self) -> str:
        """String representation."""
        return f"Envelope: {self.source.agent}→{self.destination.agent}"


class LatticeOrchestrator:
    """
    Central orchestrator for lattice-wide coordination.

    Responsibilities:
    - Route messages between components
    - Track component state
    - Enforce authority boundaries
    - Log all activities via Chronicle (future)
    """

    def __init__(self, registry: Optional[CoordinateRegistry] = None):
        """
        Initialize orchestrator.

        Args:
            registry: Coordinate registry (creates new if None)
        """
        self.registry = registry or CoordinateRegistry()
        self.routing_table = RoutingTable()
        self.message_log: List[MessageEnvelope] = []
        self.state_cache: Dict[str, Dict[str, Any]] = {}

    def register_component(self, coord: LatticeCoordinate,
                          handler: Optional[Callable] = None) -> bool:
        """
        Register a lattice component.

        Args:
            coord: Component coordinate
            handler: Optional message handler for this component

        Returns:
            True if registered successfully
        """
        if not self.registry.register(coord):
            return False

        if handler:
            self.routing_table.register_route(coord.route_key(), handler)

        return True

    def send_message(self, envelope: MessageEnvelope) -> Optional[Dict[str, Any]]:
        """
        Send a message through the lattice.

        Args:
            envelope: Message to send

        Returns:
            Response from recipient or None if routing failed
        """
        self.message_log.append(envelope)
        route_key = envelope.route_key()
        result = self.routing_table.dispatch(route_key, envelope.to_dict())
        return result

    def get_component_state(self, coord: LatticeCoordinate) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached state of a component.

        Args:
            coord: Component coordinate

        Returns:
            Cached state or None if not found
        """
        return self.state_cache.get(coord.full_key())

    def update_component_state(self, coord: LatticeCoordinate,
                               state: Dict[str, Any]) -> bool:
        """
        Update cached state of a component.

        Args:
            coord: Component coordinate
            state: New state

        Returns:
            True if updated successfully
        """
        self.state_cache[coord.full_key()] = {
            "state": state,
            "updated_at": datetime.utcnow().isoformat()
        }
        return True

    def list_components(self) -> List[LatticeCoordinate]:
        """List all registered components."""
        return list(self.registry.coordinates.values())

    def list_components_by_layer(self, layer: str) -> List[LatticeCoordinate]:
        """List all components in a layer."""
        return self.registry.list_layer(layer)

    def get_routing_status(self) -> Dict[str, Any]:
        """Get current routing table status."""
        return self.routing_table.to_dict()

    def get_message_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve recent messages.

        Args:
            limit: Maximum number of messages to return

        Returns:
            List of message dictionaries (most recent first)
        """
        return [msg.to_dict() for msg in self.message_log[-limit:]]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize orchestrator state."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "components_registered": len(self.registry.coordinates),
            "routes_registered": len(self.routing_table.routes),
            "messages_processed": len(self.message_log),
            "layers": self.registry.to_dict()["layers"],
            "recent_routes": self.routing_table.list_routes()[-10:],
            "recent_messages": len(self.message_log)
        }


class OrchestratorFactory:
    """Factory for creating pre-configured orchestrators."""

    @staticmethod
    def create_mind_orchestrator() -> LatticeOrchestrator:
        """
        Create orchestrator for Mind layer.
        Pre-registers TruthSeeker, Guardian, Visionary, Creator placeholders.
        """
        orchestrator = LatticeOrchestrator()

        def truth_seeker_handler(msg: Dict) -> Dict:
            return {"agent": "TruthSeeker", "status": "received", "message_id": msg.get("message_id")}

        def guardian_handler(msg: Dict) -> Dict:
            return {"agent": "Guardian", "status": "received", "message_id": msg.get("message_id")}

        def visionary_handler(msg: Dict) -> Dict:
            return {"agent": "Visionary", "status": "received", "message_id": msg.get("message_id")}

        def creator_handler(msg: Dict) -> Dict:
            return {"agent": "Creator", "status": "received", "message_id": msg.get("message_id")}

        coords = [
            (LatticeCoordinate("Mind", "TruthSeeker", "instance-001", "v0.1"), truth_seeker_handler),
            (LatticeCoordinate("Mind", "Guardian", "instance-001", "v0.1"), guardian_handler),
            (LatticeCoordinate("Mind", "Visionary", "instance-001", "v0.1"), visionary_handler),
            (LatticeCoordinate("Mind", "Creator", "instance-001", "v0.1"), creator_handler),
        ]

        for coord, handler in coords:
            orchestrator.register_component(coord, handler)

        return orchestrator

    @staticmethod
    def create_substrate_orchestrator() -> LatticeOrchestrator:
        """
        Create orchestrator for substrate layers.
        Pre-registers Memory, Flow, Evolve placeholders.
        """
        orchestrator = LatticeOrchestrator()

        def memory_handler(msg: Dict) -> Dict:
            return {"layer": "Memory", "status": "received", "message_id": msg.get("message_id")}

        def flow_handler(msg: Dict) -> Dict:
            return {"layer": "Flow", "status": "received", "message_id": msg.get("message_id")}

        def evolve_handler(msg: Dict) -> Dict:
            return {"layer": "Evolve", "status": "received", "message_id": msg.get("message_id")}

        coords = [
            (LatticeCoordinate("Memory", "CrystalMemory", "instance-001", "v0.8"), memory_handler),
            (LatticeCoordinate("Flow", "CrystalFlow", "instance-001", "v0.7"), flow_handler),
            (LatticeCoordinate("Evolve", "CrystalEvolve", "instance-001", "v0.6"), evolve_handler),
        ]

        for coord, handler in coords:
            orchestrator.register_component(coord, handler)

        return orchestrator
