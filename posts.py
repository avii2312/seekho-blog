# =============================================================
# posts.py — Post CRUD and all public views
# VISANET Software Pvt. Ltd. · VSN-INT-SEEKHO-BLOG
# =============================================================
# Routes in this file:
#   GET  /                          — home: list of posts
#   GET  /post/<slug>               — single post view
#   GET  /category/<slug>           — posts in one category
#   GET  /search                    — search results (Tier 2)
#   GET  /dashboard                 — author's own posts
#   GET/POST /post/new              — create a post
#   GET/POST /post/<id>/edit        — edit a post
#   POST     /post/<id>/delete      — delete a post
#   POST     /post/<id>/comment     — add a comment (Tier 2)
#   GET/POST /admin/categories      — admin: manage categories
# =============================================================

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, abort
)
from db import query_db, execute_db, make_slug, unique_slug
from auth import login_required, admin_required

posts_bp = Blueprint('posts', __name__)


# ------------------------------------------------------------------
# HOME — list of published posts
# FR-3.1
# ------------------------------------------------------------------

@posts_bp.route('/')
def index():
    """
    Show all published posts, newest first.
    Each post shows: title, author name, category, date, short preview.
    """
    posts = query_db("""
        SELECT
            p.id, p.title, p.slug, p.body, p.created_at, p.status,
            u.full_name AS author_name,
            c.name      AS category_name,
            c.slug      AS category_slug
        FROM posts p
        JOIN users      u ON p.author_id   = u.id
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.status = 'published'
        ORDER BY p.created_at DESC
    """)

    return render_template('index.html', posts=posts)


# ------------------------------------------------------------------
# SINGLE POST PAGE
# FR-3.2
# ------------------------------------------------------------------

@posts_bp.route('/post/<slug>')
def post_detail(slug):
    """
    Show one full post by its slug.
    Also loads comments for the post (Tier 2).
    """
    post = query_db("""
        SELECT
            p.*,
            u.full_name  AS author_name,
            u.username   AS author_username,
            c.name       AS category_name,
            c.slug       AS category_slug
        FROM posts p
        JOIN users      u ON p.author_id   = u.id
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.slug = %s
    """, (slug,), one=True)

    if not post:
        abort(404)

    # Hide drafts from everyone except the author and admin
    if post['status'] == 'draft':
        if session.get('user_id') != post['author_id'] and not session.get('is_admin'):
            abort(404)

    # Load comments (Tier 2 — safe to leave empty list if not built yet)
    comments = query_db("""
        SELECT cm.*, u.full_name AS commenter_name, u.username
        FROM comments cm
        JOIN users u ON cm.author_id = u.id
        WHERE cm.post_id = %s
        ORDER BY cm.created_at ASC
    """, (post['id'],))

    return render_template('post_detail.html', post=post, comments=comments)


# ------------------------------------------------------------------
# BROWSE BY CATEGORY
# FR-3.3
# ------------------------------------------------------------------

@posts_bp.route('/category/<slug>')
def category(slug):
    """
    Show all published posts belonging to a specific category.
    """
    cat = query_db(
        "SELECT * FROM categories WHERE slug = %s", (slug,), one=True
    )
    if not cat:
        abort(404)

    posts = query_db("""
        SELECT
            p.id, p.title, p.slug, p.body, p.created_at,
            u.full_name AS author_name,
            c.name      AS category_name,
            c.slug      AS category_slug
        FROM posts p
        JOIN users      u ON p.author_id   = u.id
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.status = 'published' AND p.category_id = %s
        ORDER BY p.created_at DESC
    """, (cat['id'],))

    return render_template('category.html', category=cat, posts=posts)


# ------------------------------------------------------------------
# SEARCH (Tier 2 — FR-4.4)
# ------------------------------------------------------------------

@posts_bp.route('/search')
def search():
    """
    Search published posts by keyword in title or body.
    The keyword comes from the URL: /search?q=python
    """
    keyword = request.args.get('q', '').strip()
    posts   = []

    if keyword:
        # LIKE search — wrap the keyword in % wildcards
        pattern = f"%{keyword}%"
        posts = query_db("""
            SELECT
                p.id, p.title, p.slug, p.body, p.created_at,
                u.full_name AS author_name,
                c.name      AS category_name,
                c.slug      AS category_slug
            FROM posts p
            JOIN users      u ON p.author_id   = u.id
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.status = 'published'
              AND (p.title LIKE %s OR p.body LIKE %s)
            ORDER BY p.created_at DESC
        """, (pattern, pattern))

    return render_template('search.html', posts=posts, keyword=keyword)


# ------------------------------------------------------------------
# AUTHOR DASHBOARD
# FR-2.6
# ------------------------------------------------------------------

@posts_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Show the logged-in author's own posts (all statuses).
    """
    posts = query_db("""
        SELECT p.*, c.name AS category_name
        FROM posts p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.author_id = %s
        ORDER BY p.created_at DESC
    """, (session['user_id'],))

    return render_template('dashboard.html', posts=posts)


# ------------------------------------------------------------------
# CREATE POST
# FR-2.1
# ------------------------------------------------------------------

@posts_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def post_new():
    """
    GET:  Show the empty post creation form.
    POST: Validate and save the new post to the database.
    """
    categories = query_db("SELECT * FROM categories ORDER BY name")

    if request.method == 'GET':
        return render_template('post_form.html',
                               categories=categories,
                               action='create')

    # --- POST: read form values ---
    title       = request.form.get('title', '').strip()
    body        = request.form.get('body', '').strip()
    category_id = request.form.get('category_id', '').strip()
    status      = request.form.get('status', 'published')

    # --- Validate ---
    errors = []
    if not title:
        errors.append("Post title cannot be empty.")
    if not body:
        errors.append("Post body cannot be empty.")
    if not category_id:
        errors.append("Please choose a category.")

    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('post_form.html',
                               categories=categories,
                               action='create',
                               title=title,
                               body=body,
                               category_id=category_id)

    # --- Generate unique slug ---
    base_slug = make_slug(title)
    slug      = unique_slug(base_slug, 'posts')

    # --- Insert ---
    execute_db("""
        INSERT INTO posts (title, slug, body, category_id, author_id, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (title, slug, body, category_id, session['user_id'], status))

    flash("Post published successfully!", 'success')
    return redirect(url_for('posts.post_detail', slug=slug))


# ------------------------------------------------------------------
# EDIT POST
# FR-2.3 + FR-2.5 (ownership check)
# ------------------------------------------------------------------

@posts_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def post_edit(post_id):
    """
    GET:  Show the edit form pre-filled with existing content.
    POST: Validate and update the post in the database.

    IMPORTANT: Ownership is checked on the SERVER here, not just
    by hiding the button in the template. (FR-2.5, NFR-4)
    """
    post = query_db("SELECT * FROM posts WHERE id = %s", (post_id,), one=True)

    if not post:
        abort(404)

    # Ownership check — is this user the author?
    if post['author_id'] != session['user_id'] and not session.get('is_admin'):
        flash("You can only edit your own posts.", 'danger')
        return redirect(url_for('posts.dashboard'))

    categories = query_db("SELECT * FROM categories ORDER BY name")

    if request.method == 'GET':
        return render_template('post_form.html',
                               categories=categories,
                               action='edit',
                               post=post)

    # --- POST: read and validate ---
    title       = request.form.get('title', '').strip()
    body        = request.form.get('body', '').strip()
    category_id = request.form.get('category_id', '').strip()
    status      = request.form.get('status', 'published')

    errors = []
    if not title:
        errors.append("Post title cannot be empty.")
    if not body:
        errors.append("Post body cannot be empty.")
    if not category_id:
        errors.append("Please choose a category.")

    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('post_form.html',
                               categories=categories,
                               action='edit',
                               post=post,
                               title=title,
                               body=body,
                               category_id=category_id)

    # Regenerate slug only if title changed
    if title != post['title']:
        base_slug = make_slug(title)
        slug      = unique_slug(base_slug, 'posts', existing_id=post_id)
    else:
        slug = post['slug']

    execute_db("""
        UPDATE posts
        SET title=%s, slug=%s, body=%s, category_id=%s, status=%s
        WHERE id=%s
    """, (title, slug, body, category_id, status, post_id))

    flash("Post updated.", 'success')
    return redirect(url_for('posts.post_detail', slug=slug))


# ------------------------------------------------------------------
# DELETE POST
# FR-2.4 + FR-2.5
# ------------------------------------------------------------------

@posts_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    """
    Delete a post. Only the author or admin can do this.
    This route only accepts POST — a GET link cannot delete data.
    The confirmation is shown in the template before the form submits.
    """
    post = query_db("SELECT * FROM posts WHERE id = %s", (post_id,), one=True)

    if not post:
        abort(404)

    # Ownership check
    if post['author_id'] != session['user_id'] and not session.get('is_admin'):
        flash("You can only delete your own posts.", 'danger')
        return redirect(url_for('posts.dashboard'))

    execute_db("DELETE FROM posts WHERE id = %s", (post_id,))

    flash("Post deleted.", 'info')
    return redirect(url_for('posts.dashboard'))


# ------------------------------------------------------------------
# ADD COMMENT (Tier 2 — FR-4.1)
# ------------------------------------------------------------------

@posts_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """
    Add a comment to a post. Login required.
    """
    post = query_db("SELECT slug FROM posts WHERE id = %s", (post_id,), one=True)
    if not post:
        abort(404)

    body = request.form.get('body', '').strip()
    if not body:
        flash("Comment cannot be empty.", 'danger')
        return redirect(url_for('posts.post_detail', slug=post['slug']))

    execute_db(
        "INSERT INTO comments (post_id, author_id, body) VALUES (%s, %s, %s)",
        (post_id, session['user_id'], body)
    )

    flash("Comment added.", 'success')
    return redirect(url_for('posts.post_detail', slug=post['slug']))


# ------------------------------------------------------------------
# DELETE COMMENT (Tier 2)
# ------------------------------------------------------------------

@posts_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """
    Delete a comment. Only the comment author or admin can do this.
    """
    comment = query_db("SELECT * FROM comments WHERE id = %s", (comment_id,), one=True)
    if not comment:
        abort(404)

    post = query_db("SELECT slug FROM posts WHERE id = %s", (comment['post_id'],), one=True)

    if comment['author_id'] != session['user_id'] and not session.get('is_admin'):
        flash("You can only delete your own comments.", 'danger')
        return redirect(url_for('posts.post_detail', slug=post['slug']))

    execute_db("DELETE FROM comments WHERE id = %s", (comment_id,))
    flash("Comment deleted.", 'info')
    return redirect(url_for('posts.post_detail', slug=post['slug']))


# ------------------------------------------------------------------
# ADMIN — CATEGORY MANAGEMENT
# FR-2.7
# ------------------------------------------------------------------

@posts_bp.route('/admin/categories', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_categories():
    """
    Admin page: list, add, rename, and remove categories.
    GET:  Show current categories and an "add" form.
    POST: Handle the submitted action.
    """
    if request.method == 'POST':
        action = request.form.get('action')

        # --- ADD a new category ---
        if action == 'add':
            name = request.form.get('name', '').strip()
            if not name:
                flash("Category name cannot be empty.", 'danger')
            else:
                slug = unique_slug(make_slug(name), 'categories')
                desc = request.form.get('description', '').strip()
                try:
                    execute_db(
                        "INSERT INTO categories (name, slug, description) VALUES (%s, %s, %s)",
                        (name, slug, desc)
                    )
                    flash(f"Category '{name}' added.", 'success')
                except Exception:
                    flash("A category with that name already exists.", 'danger')

        # --- RENAME a category ---
        elif action == 'rename':
            cat_id   = request.form.get('category_id')
            new_name = request.form.get('name', '').strip()
            if not new_name:
                flash("Category name cannot be empty.", 'danger')
            else:
                new_slug = unique_slug(make_slug(new_name), 'categories', existing_id=cat_id)
                execute_db(
                    "UPDATE categories SET name=%s, slug=%s WHERE id=%s",
                    (new_name, new_slug, cat_id)
                )
                flash("Category renamed.", 'success')

        # --- REMOVE a category ---
        elif action == 'remove':
            cat_id = request.form.get('category_id')
            # Posts in this category will have category_id set to NULL
            # because of the ON DELETE SET NULL foreign key in schema.sql
            execute_db("DELETE FROM categories WHERE id=%s", (cat_id,))
            flash("Category removed. Posts in it are now uncategorised.", 'info')

        return redirect(url_for('posts.admin_categories'))

    categories = query_db("SELECT * FROM categories ORDER BY name")
    return render_template('admin_categories.html', categories=categories)
