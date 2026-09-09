#!/usr/bin/env python3
"""
Consent Token Kill-Switch Demo — 2 minute walkthrough

Demonstrates:
1. Token creation with explicit scopes and expiry
2. Token signing (issuer proof)
3. Token verification (recipient check)
4. Revocation — the "kill switch" that stops future requests
5. Why revocation cannot delete already-received data

Run: python3 consent_kill_switch_demo.py

This is a reference implementation of CONSENT-TOKEN-SPEC-v0.1.md
"""

import time
from pathlib import Path
import sys

# Add the consent_transport module to path
consent_path = Path(__file__).parent.parent / "core" / "crystal-core" / "consent_transport"
sys.path.insert(0, str(consent_path.parent))

from consent_transport.token import ConsentToken, Scope, Constraints, SCHEMA_VERSION
from consent_transport.identity import Identity

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def demo():
    print_section("Consent Token Kill-Switch Demo")
    print(f"Schema version: {SCHEMA_VERSION}\n")

    # Step 1: Create identities (issuer and recipient)
    print_section("STEP 1: Create Identities")
    print("Creating issuer identity (Clementine operator)...")
    issuer_identity = Identity.generate()
    print(f"Issuer public key: {issuer_identity.sign_public_bytes.hex()[:16]}...\n")

    print("Creating recipient identity (guest AI agent)...")
    recipient_identity = Identity.generate()
    print(f"Recipient public key: {recipient_identity.sign_public_bytes.hex()[:16]}...\n")

    # Step 2: Create a token
    print_section("STEP 2: Create Consent Token")
    print("Issuer grants permission to recipient to:")
    print("  - Access 'status' and 'recall' tools only")
    print("  - Valid for 1 hour")
    print("  - Single use (must not be re-transmitted)\n")

    token = ConsentToken(
        issuer=issuer_identity.sign_public_bytes.hex(),
        recipient=recipient_identity.sign_public_bytes.hex(),
        purpose="Allow guest AI to query Clementine status and recall memories",
        scope=Scope(kinds=("episodic", "semantic"), max_bytes=1_000_000),
        constraints=Constraints(one_time_use=True, requires_ack=True, max_transfers=0),
        issued_at=time.time(),
        expires_at=time.time() + 3600,  # 1 hour
    )
    print(f"Token ID: {token.token_id}")
    print(f"Issued at: {time.ctime(token.issued_at)}")
    print(f"Expires at: {time.ctime(token.expires_at)}\n")

    # Step 3: Sign the token
    print_section("STEP 3: Sign Token (Issuer Proof)")
    token.sign(issuer_identity)
    print(f"Signature: {token.signature[:32]}...\n")
    print("✓ Token is now cryptographically signed by the issuer.\n")

    # Step 4: Verify the token
    print_section("STEP 4: Verify Token (Recipient Check)")
    print("Recipient verifying token is valid for them...\n")
    try:
        token.verify(
            recipient_identity.sign_public_bytes.hex(),
            now=time.time(),
            revoked_ids=set(),
            kind="episodic",
            want_bytes=500,
        )
        print("✓ Token verification PASSED")
        print("  - Issuer is valid")
        print("  - Recipient matches")
        print("  - Not expired")
        print("  - Not revoked")
        print("  - Scope permits 'episodic' fragments")
        print("  - Byte limit sufficient\n")
    except Exception as e:
        print(f"✗ Verification failed: {e}\n")
        return

    # Step 5: Demonstrate the kill switch
    print_section("STEP 5: Revocation — The Kill Switch")
    print("Scenario: Operator detects suspicious activity.")
    print("Operator revokes this token by adding its ID to the 'revoked_ids' set.\n")

    revoked_ids = {token.token_id}
    print(f"Revoked token ID: {token.token_id}\n")

    print("Now, recipient attempts to use the token again...\n")
    try:
        token.verify(
            recipient_identity.sign_public_bytes.hex(),
            now=time.time(),
            revoked_ids=revoked_ids,  # Token is now in revoked set
            kind="episodic",
            want_bytes=500,
        )
        print("✗ This should not print — token should be rejected.\n")
    except Exception as e:
        print(f"✗ Verification FAILED (as expected)")
        print(f"   Reason: {e}\n")
        print("✓ Kill switch ENGAGED")
        print("  - Future requests using this token are blocked immediately")
        print("  - No new data flows to the revoked recipient\n")

    # Step 6: Explain the limits
    print_section("STEP 6: What Revocation Cannot Do")
    print("Important: Revocation stops FUTURE requests.")
    print("It CANNOT delete data the recipient legitimately received BEFORE revocation.\n")

    print("Why? Because once data leaves the issuer's device:")
    print("  1. It is now on the recipient's own sovereign device")
    print("  2. The issuer cannot reach into that device to force deletion")
    print("  3. Forcing deletion would violate the same sovereignty principle")
    print("     that protects the issuer in the first place\n")

    print("Solution: Revocation is honest about its own limits.")
    print("  - Tell the human user: revocation stops new access, period.")
    print("  - If sensitive data was already shared, that is already lost.")
    print("  - Future token grants should factor in this risk.\n")

    # Step 7: Show token structure
    print_section("STEP 7: Token Structure (for inspection)")
    print("A signed ConsentToken is inspectable, not a black box:\n")
    print(f"Token ID:     {token.token_id}")
    print(f"Issuer:       {token.issuer[:16]}...")
    print(f"Recipient:    {token.recipient[:16]}...")
    print(f"Purpose:      {token.purpose}")
    print(f"Scope kinds:  {token.scope.kinds}")
    print(f"Max bytes:    {token.scope.max_bytes}")
    print(f"One-time use: {token.constraints.one_time_use}")
    print(f"Revocable:    {token.revocable}")
    print(f"Signature:    {token.signature[:32]}...\n")

    print_section("Demo Complete")
    print("This 2-minute walkthrough demonstrated:")
    print("  ✓ Token creation with explicit scopes and expiry")
    print("  ✓ Token signing (issuer proof)")
    print("  ✓ Token verification (recipient check)")
    print("  ✓ Revocation — the 'kill switch' in action")
    print("  ✓ Why revocation is honest about its own limits\n")
    print("For full spec details, see: CONSENT-TOKEN-SPEC-v0.1.md\n")

if __name__ == "__main__":
    demo()
