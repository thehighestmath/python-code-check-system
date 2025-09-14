#!/usr/bin/env python3
"""
Script to run database migrations.
"""

import subprocess
import sys
import os


def run_migration():
    """Run Alembic migration."""
    try:
        # Generate migration
        print("Generating migration...")
        result = subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", "Initial migration"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Migration generated successfully")

        # Apply migration
        print("Applying migration...")
        result = subprocess.run(["alembic", "upgrade", "head"], check=True, capture_output=True, text=True)
        print("Migration applied successfully")

    except subprocess.CalledProcessError as e:
        print(f"Error running migration: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_migration()
