# =============================================================
# Seekho Blog — Configuration (EXAMPLE FILE)
# VISANET Software Pvt. Ltd. · VSN-INT-SEEKHO-BLOG
# =============================================================
# HOW TO USE THIS FILE:
#   1. Copy this file:  cp config.example.py config.py
#   2. Fill in your local database password below
#   3. Never commit config.py to GitHub (it is in .gitignore)
# =============================================================

# --- Database ---
DB_HOST     = "localhost"
DB_USER     = "root"
DB_PASSWORD = ""          # XAMPP default is an empty string — fill in yours if different
DB_NAME     = "seekho_blog"

# --- Flask ---
# Change this to any long random string in your local config.py
# Example: "seekho-intern-2026-random-xyz-789"
SECRET_KEY  = "change-this-to-something-random-before-you-run"

# --- App settings ---
DEBUG       = True        # Set to False before any real deployment
POSTS_PER_PAGE = 6        # Used by pagination (Tier 2)
