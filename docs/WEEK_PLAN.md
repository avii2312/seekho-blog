# Week-by-Week Plan
### Seekho Blog Module — Summer Internship 2026

This is the expected pace for the month. It is not a suggestion. If your group is a week behind this plan, raise it with your mentor immediately.

---

## Week 1 — Foundation

**Goal by end of week:** Every member can run the app locally. Database schema exists in MySQL. The Flask app runs and shows one real page reading from the database.

### Day 1
- [ ] Everyone clones the repository
- [ ] Everyone completes the setup checklist in `README.md`
- [ ] Set up the virtual environment and install packages
- [ ] XAMPP running, can open phpMyAdmin
- [ ] Each member runs `flask --app app run --debug` and sees the starter page
- [ ] Update `README.md` team table with your names and GitHub usernames
- [ ] Assign roles (Database, Backend, Frontend, Integration)
- [ ] Create your first feature branches

### Day 2–3
- [ ] Database owner designs the schema — discuss as a group first
- [ ] Run `sql/schema.sql` in phpMyAdmin — all four tables created
- [ ] `db.py` — database connection working, can do a test query
- [ ] `app.py` — Flask app starts, one route (`/`) returns something
- [ ] `base.html` — shared layout with Seekho dark/violet theme started

### Day 4–5
- [ ] Home page (`/`) fetches real rows from `posts` table and shows them
- [ ] Commit the working schema and home page
- [ ] Seed the database with `sql/sample_data.sql`
- [ ] End-of-week check: can everyone run the project from a fresh clone?

**By Friday of Week 1:**  
✅ App is running locally for every member  
✅ Schema is in MySQL and in `sql/schema.sql`  
✅ Home page shows data from the database  

---

## Week 2 — Core Build (Authentication + Post CRUD)

**Goal by end of week:** A person can register, log in, create a post, edit it, and delete it. Everything saved in MySQL.

### Day 1–2: Authentication
- [ ] `auth.py` — registration route (FR-1.1)
  - Form: full name, username, email, password × 2
  - Check username/email not already taken
  - Hash the password with `generate_password_hash`
  - Insert into `users`
- [ ] `auth.py` — login route (FR-1.2)
  - Find user by username
  - Verify with `check_password_hash`
  - Store `user_id` in session
  - Redirect to dashboard on success
- [ ] `auth.py` — logout route (FR-1.3)
  - Clear the session
- [ ] Route protection (FR-1.4) — decorator or check at top of protected routes

### Day 3–5: Post CRUD
- [ ] `posts.py` — create post route `/post/new` (FR-2.1)
  - Title, body, category dropdown
  - Generate slug from title
  - Save with `author_id` from session
- [ ] `posts.py` — edit post route `/post/<id>/edit` (FR-2.3)
  - Check `author_id == session user` on server (FR-2.5)
  - Update the row and set `updated_at`
- [ ] `posts.py` — delete post route `/post/<id>/delete` (FR-2.4)
  - POST only (not GET)
  - Ownership check
  - Confirmation on frontend
- [ ] `posts.py` — author dashboard `/dashboard` (FR-2.6)
  - List logged-in user's posts with Edit / Delete links

**By Friday of Week 2:**  
✅ Can register and log in  
✅ Can create, edit, delete own posts  
✅ Cannot edit another user's post even by URL  

---

## Week 3 — Public Side + Tier 2

**Goal by end of week:** All of Tier 1 complete. At least one or two Tier 2 features in progress. First code review with mentor.

### Day 1–2: Public views (last of Tier 1)
- [ ] Home page lists published posts, newest first, with author/category/date (FR-3.1)
- [ ] Single post page `/post/<slug>` shows the full post (FR-3.2)
- [ ] Category page `/category/<slug>` shows posts in that category (FR-3.3)
- [ ] Admin: category management `/admin/categories` (FR-2.7)

### Run the full Tier 1 acceptance checklist
Go through every item in `README.md` checklist. Fix everything before moving on.

### Day 3: Code review with mentor
- Mentor reviews code quality, security rules, and Git history
- Fix all feedback before starting Tier 2

### Day 4–5: Start Tier 2
Pick the Tier 2 features in this order (they build on each other):
- [ ] Pagination (FR-4.2) — simplest, good to start with
- [ ] Draft/Published status (FR-4.3) — small change to posts table and queries
- [ ] Comments (FR-4.1) — new table, new route, shows under post
- [ ] Search (FR-4.4) — `LIKE` query on title and body

**By Friday of Week 3:**  
✅ Tier 1 fully working and reviewed  
✅ One or two Tier 2 features started  

---

## Week 4 — Finish, Test and Polish

**Goal by end of week:** Stable, tested, documented project ready to demo.

### Day 1–2
- [ ] Complete any in-progress Tier 2 features
- [ ] No half-finished features left switched on — if it doesn't work, comment it out or remove it
- [ ] Fix every bug found in Week 3 review

### Day 3: Final testing
- [ ] Run through the entire acceptance checklist one more time as a group
- [ ] Test every wrong-case scenario (bad password, empty form, someone else's post URL)
- [ ] Test from a **fresh clone** — delete the project folder, clone again, follow only the README
- [ ] Verify all members' names appear in `git log`

### Day 4: Documentation
- [ ] `README.md` — complete and accurate (someone else can run it with only this file)
- [ ] Short project report (2–3 pages) — what you built, how you divided work, problems faced
- [ ] `sql/sample_data.sql` — enough seed data for a live demo (categories, users, posts, comments)
- [ ] Verify `config.py` is NOT in the repository

### Day 5: Demo prep
- [ ] Rehearse the demo as a group — one person navigates, others explain
- [ ] Every member should be able to explain any file in the project
- [ ] Submit the repository link to your mentor

---

## What "Done" Means

A feature is **done** only when:
1. It works correctly in the normal case
2. It handles at least one wrong/edge case gracefully
3. The code is committed to `main` via a reviewed PR
4. The feature is ticked in the README checklist

"I'll fix it later" is not done. "It works on my machine" is not done.

---

*VISANET Software Pvt. Ltd. · Internal training document*
