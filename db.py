# =============================================================
# db.py — Database connection and shared query helpers
# VISANET Software Pvt. Ltd. · VSN-INT-SEEKHO-BLOG
# =============================================================
# This file has ONE job: talk to MySQL.
# All other files (auth.py, posts.py) import from here.
# Never build SQL strings with f-strings or + operator.
# Always use parameterised queries (%s placeholders).
# =============================================================

import mysql.connector
import config


def get_connection():
    """
    Opens and returns a new MySQL connection.
    Call this at the start of every route that needs the database.
    Always close it when done — use a try/finally block.
    """
    connection = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )
    return connection


def query_db(sql, args=(), one=False):
    """
    Run a SELECT query and return results as a list of dicts.

    Parameters:
        sql  — the SQL string, using %s for every value placeholder
        args — a tuple of values to substitute in (default: empty)
        one  — if True, return only the first row (or None)

    Examples:
        # Get all published posts
        posts = query_db("SELECT * FROM posts WHERE status = %s", ('published',))

        # Get one user by username
        user = query_db("SELECT * FROM users WHERE username = %s", (username,), one=True)
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)   # dictionary=True → rows are dicts
        cursor.execute(sql, args)
        results = cursor.fetchall()
        return (results[0] if results else None) if one else results
    finally:
        cursor.close()
        conn.close()


def execute_db(sql, args=()):
    """
    Run an INSERT, UPDATE, or DELETE query.
    Returns the lastrowid (useful after INSERT to get the new row's id).

    Examples:
        # Insert a new post
        new_id = execute_db(
            "INSERT INTO posts (title, slug, body, category_id, author_id) VALUES (%s,%s,%s,%s,%s)",
            (title, slug, body, category_id, author_id)
        )

        # Update a post
        execute_db(
            "UPDATE posts SET title=%s, body=%s WHERE id=%s",
            (title, body, post_id)
        )

        # Delete a post
        execute_db("DELETE FROM posts WHERE id=%s", (post_id,))
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, args)
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()


# =============================================================
# Slug helper
# =============================================================

import re
import unicodedata

def make_slug(text):
    """
    Convert a post title into a URL-friendly slug.
    Example: "My First Blog Post!" → "my-first-blog-post"

    Used in the create-post route.
    """
    # Normalise unicode characters
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Lowercase
    text = text.lower()
    # Replace any non-alphanumeric character with a hyphen
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Strip leading/trailing hyphens
    text = text.strip('-')
    return text


def unique_slug(base_slug, table, existing_id=None):
    """
    Make sure a slug is unique in the given table.
    If 'base_slug' is already taken, appends -2, -3, etc.

    Parameters:
        base_slug   — the slug generated from the title
        table       — 'posts' or 'categories'
        existing_id — when editing, pass the current row id to
                      exclude it from the uniqueness check

    Example:
        slug = unique_slug(make_slug(title), 'posts')
    """
    slug = base_slug
    counter = 2
    while True:
        if existing_id:
            row = query_db(
                f"SELECT id FROM {table} WHERE slug = %s AND id != %s",
                (slug, existing_id),
                one=True
            )
        else:
            row = query_db(
                f"SELECT id FROM {table} WHERE slug = %s",
                (slug,),
                one=True
            )
        if not row:
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1
