# =============================================================
# app.py — Flask application entry point
# VISANET Software Pvt. Ltd. · VSN-INT-SEEKHO-BLOG
# =============================================================
# This file does three things only:
#   1. Creates the Flask app object
#   2. Loads config
#   3. Registers blueprints (route files)
#
# Application logic lives in auth.py and posts.py, NOT here.
# =============================================================

from flask import Flask
import config

app = Flask(__name__)

# Load settings from config.py
app.secret_key = config.SECRET_KEY

# ------------------------------------------------------------------
# Register route modules
# ------------------------------------------------------------------
# Import auth routes (register, login, logout)
from auth import auth_bp
app.register_blueprint(auth_bp)

# Import post routes (create, edit, delete, public views, admin)
from posts import posts_bp
app.register_blueprint(posts_bp)


# ------------------------------------------------------------------
# Template context helpers
# ------------------------------------------------------------------
from db import query_db

@app.context_processor
def inject_categories():
    """
    Makes 'all_categories' available in every template automatically.
    Used by the navigation bar to list categories.
    """
    categories = query_db("SELECT * FROM categories ORDER BY name")
    return dict(all_categories=categories)


# ------------------------------------------------------------------
# Error pages
# ------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return "404 — Page not found. <a href='/'>Go home</a>", 404

@app.errorhandler(403)
def forbidden(e):
    return "403 — You are not allowed to do that. <a href='/'>Go home</a>", 403


# ------------------------------------------------------------------
# Run
# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=config.DEBUG)
