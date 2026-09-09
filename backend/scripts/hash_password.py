#!/usr/bin/env python3
"""Generate a bcrypt hash for ADMIN_PASSWORD_HASH in .env.

Usage:
    python backend/scripts/hash_password.py "your-password-here"
"""

import sys

sys.path.insert(0, __file__.rsplit("/", 2)[0])  # add backend/ to sys.path

from app.core.security import hash_password  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: hash_password.py <password>")
    print(hash_password(sys.argv[1]))


if __name__ == "__main__":
    main()
