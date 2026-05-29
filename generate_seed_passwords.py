"""
generate_seed_passwords.py
==========================
Run this script once to generate real Werkzeug password hashes
for the accounts in sql/sample_data.sql.

Usage:
    python generate_seed_passwords.py

Copy the output hashes into sql/sample_data.sql,
replacing the 'abc123placeholder...' values.

Do NOT commit this file's output to GitHub — 
the sample_data.sql with real hashes is fine,
but never commit real passwords anywhere.
"""

from werkzeug.security import generate_password_hash

accounts = [
    ("admin",  "Admin@123"),
    ("priya",  "Priya@123"),
    ("rahul",  "Rahul@123"),
    ("sneha",  "Sneha@123"),
]

print("=" * 60)
print("Copy these hashes into sql/sample_data.sql")
print("=" * 60)
for username, password in accounts:
    hashed = generate_password_hash(password)
    print(f"\n-- {username}  (password: {password})")
    print(f"   Hash: {hashed}")
print("\n" + "=" * 60)
