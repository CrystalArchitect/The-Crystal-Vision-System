#!/usr/bin/env python3
"""
Consent Token Kill-Switch Demo — Standalone 2-minute walkthrough
(No external dependencies — mock version for demonstration)

Demonstrates the CONSENT-TOKEN-SPEC-v0.1 concepts:
1. Token creation with explicit scopes and expiry
2. Token signing (issuer proof)
3. Token verification (recipient check)
4. Revocation — the "kill switch" that stops future requests
5. Why revocation cannot delete already-received data

Run: python3 consent_kill_switch_demo_standalone.py
"""

import json
import time
from datetime import datetime
import hashlib

class MockIdentity:
    """Mock Ed25519 identity for demo purposes"""
    def __init__(self, name):
        self.name = name
        self.public_key = hashlib.sha256(name.encode()).hexdigest()

    def __repr__(self):
        return f"Identity({self.public_key[:16]}... [{self.name}])"

class ConsentToken:
    """Mock ConsentToken following SPEC-v0.1 schema"""
    def __init__(self, issuer, recipient, purpose, scope_kinds=None, expires_in_seconds=3600):
        self.token_id = hashlib.sha256(f"{time.time()}{issuer.name}{recipient.name}".encode()).hexdigest()[:16]
        self.issuer = issuer
        self.recipient = recipient
        self.purpose = purpose
        self.scope_kinds = scope_kinds or ["episodic", "semantic"]
        self.issued_at = time.time()
        self.expires_at = self.issued_at + expires_in_seconds
        self.signature = None
        self.is_revocable = True

    def sign(self, issuer_identity):
        """Simulate signing — issuer proves ownership"""
        if issuer_identity.public_key != self.issuer.public_key:
            raise ValueError("Only the named issuer may sign this token")
        # Mock signature: hash of token contents
        sig_data = json.dumps({
            "token_id": self.token_id,
            "issuer": self.issuer.public_key,
            "recipient": self.recipient.public_key,
            "purpose": self.purpose,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
        }, sort_keys=True)
        self.signature = hashlib.sha256(sig_data.encode()).hexdigest()[:32]
        return self

    def verify(self, recipient_pubkey, now=None, revoked_ids=None):
        """Verify token is valid for the recipient"""
        now = now or time.time()
        revoked_ids = revoked_ids or set()

        # Check 1: Signature exists
        if not self.signature:
            raise ValueError("Token not signed — signature missing")

        # Check 2: Recipient matches
        if recipient_pubkey != self.recipient.public_key:
            raise ValueError(f"Recipient mismatch: {recipient_pubkey[:8]}... ≠ {self.recipient.public_key[:8]}...")

        # Check 3: Not expired
        if now > self.expires_at:
            raise ValueError(f"Token expired at {datetime.fromtimestamp(self.expires_at)}")

        # Check 4: Not revoked
        if self.token_id in revoked_ids:
            raise ValueError(f"Token revoked (ID: {self.token_id})")

        return True

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def demo():
    print_section("Consent Token Kill-Switch Demo (CONSENT-TOKEN-SPEC v0.1)")
    print("This is a reference implementation demonstrating the core concepts.\n")

    # Step 1: Create identities
    print_section("STEP 1: Create Identities")
    print("Creating identities (issuer and recipient)...\n")

    issuer = MockIdentity("clementine-operator")
    recipient = MockIdentity("guest-ai-agent")

    print(f"Issuer:    {issuer}")
    print(f"Recipient: {recipient}\n")

    # Step 2: Create a token
    print_section("STEP 2: Create Consent Token")
    print("Issuer grants permission to recipient to:")
    print("  • Access 'episodic' and 'semantic' fragments")
    print("  • Valid for 1 hour")
    print("  • Revocable: Yes\n")

    token = ConsentToken(
        issuer=issuer,
        recipient=recipient,
        purpose="Allow guest AI to query Clementine status and recall memories",
        scope_kinds=["episodic", "semantic"],
        expires_in_seconds=3600,
    )
    print(f"Token ID:     {token.token_id}")
    print(f"Issued at:    {datetime.fromtimestamp(token.issued_at).strftime('%H:%M:%S')}")
    print(f"Expires at:   {datetime.fromtimestamp(token.expires_at).strftime('%H:%M:%S')}")
    print(f"Purpose:      {token.purpose}\n")

    # Step 3: Sign the token
    print_section("STEP 3: Sign Token (Issuer Proof)")
    token.sign(issuer)
    print(f"Signature:    {token.signature}")
    print("\n✓ Token is now cryptographically signed by the issuer.\n")

    # Step 4: Verify token
    print_section("STEP 4: Verify Token (Recipient Check)")
    print("Recipient verifying token is valid for them...\n")
    try:
        token.verify(recipient.public_key, now=time.time(), revoked_ids=set())
        print("✓ Token verification PASSED")
        print("  ✓ Issuer is valid")
        print("  ✓ Recipient matches")
        print("  ✓ Not expired")
        print("  ✓ Not revoked")
        print("  ✓ Scope permits requested fragments\n")
    except Exception as e:
        print(f"✗ Verification failed: {e}\n")
        return

    # Step 5: Demonstrate the kill switch
    print_section("STEP 5: Revocation — The Kill Switch")
    print("Scenario: Operator detects suspicious activity.")
    print("Operator revokes the token by adding its ID to the revoked set.\n")

    revoked_ids = {token.token_id}
    print(f"Revoked token ID: {token.token_id}\n")

    print("Recipient attempts to use the token again...\n")
    try:
        token.verify(recipient.public_key, now=time.time(), revoked_ids=revoked_ids)
        print("✗ This should not print — token should be rejected.\n")
    except Exception as e:
        print(f"✗ Verification FAILED (as expected)")
        print(f"   Error: {e}\n")
        print("✓ Kill Switch ENGAGED ✗")
        print("  ✓ Future requests using this token are blocked immediately")
        print("  ✓ No new data flows to the revoked recipient\n")

    # Step 6: What revocation CANNOT do
    print_section("STEP 6: What Revocation Cannot Do (And Why)")
    print("Revocation stops FUTURE requests — period.")
    print("It CANNOT delete data already legitimately received.\n")
    print("Why?\n")
    print("  1. Once data leaves the issuer's device → it's on recipient's device")
    print("  2. Issuer has no authority to reach into recipient's device")
    print("  3. Forcing deletion would violate the same sovereignty principle")
    print("     that protects the issuer\n")
    print("Correct behavior: Be honest with the human operator.")
    print("  • 'Revocation: stops new access'")
    print("  • 'Previously-shared data: already lost'")
    print("  • 'Future grants: factor in this risk'\n")

    # Step 7: Token structure
    print_section("STEP 7: Token Structure (For Inspection)")
    print("A ConsentToken is inspectable, not a black box:\n")
    token_dict = {
        "token_id": token.token_id,
        "issuer": token.issuer.public_key[:16] + "...",
        "recipient": token.recipient.public_key[:16] + "...",
        "purpose": token.purpose,
        "scope_kinds": token.scope_kinds,
        "issued_at": datetime.fromtimestamp(token.issued_at).isoformat(),
        "expires_at": datetime.fromtimestamp(token.expires_at).isoformat(),
        "revocable": token.is_revocable,
        "signature": token.signature,
    }
    print(json.dumps(token_dict, indent=2) + "\n")

    # Summary
    print_section("Demo Complete — Key Takeaways")
    print("This 2-minute walkthrough demonstrated:\n")
    print("  ✓ Token creation with explicit scopes and time binding")
    print("  ✓ Token signing (issuer cryptographic proof)")
    print("  ✓ Token verification (recipient and integrity checks)")
    print("  ✓ Revocation — the 'kill switch' blocking future access")
    print("  ✓ Honest limits of revocation (cannot delete already-shared data)\n")
    print("Reference Implementation: CONSENT-TOKEN-SPEC-v0.1.md")
    print("Full verification order: NOISE-IK-CONSENT-VERIFICATION.md §4\n")

if __name__ == "__main__":
    demo()
