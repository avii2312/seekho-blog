# Seekho Community Blog Module
### VISANET Software Pvt. Ltd. — Summer Internship Project
**Project Code:** `VSN-INT-SEEKHO-BLOG`  
**Batch:** Summer Training 2026  
**Stack:** Python · Flask · MySQL (XAMPP) · Bootstrap 5  

---

## What You Are Building

A community blog section for **Seekho** — VISANET's skill-exchange platform. People who want to learn or teach skills can publish short articles, share progress, and help newcomers.

This is a **standalone reference implementation** — not the live Seekho codebase. You build it as a working prototype with its own database and repository.

---

## Quick Links

| Document | Location |
|---|---|
| Full SRS (Project Guide) | [`docs/SRS_Seekho_Blog_Module.pdf`](docs/SRS_Seekho_Blog_Module.pdf) |
| Database Schema | [`sql/schema.sql`](sql/schema.sql) |
| Sample Data | [`sql/sample_data.sql`](sql/sample_data.sql) |
| Git & Contribution Guide | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Week-by-Week Plan | [`docs/WEEK_PLAN.md`](docs/WEEK_PLAN.md) |

---

## Team

| Name | Role | GitHub |
|---|---|---|
| _Your Name_ | Database & Models | [@username]() |
| _Your Name_ | Backend & Routes | [@username]() |
| _Your Name_ | Frontend & Templates | [@username]() |
| _Your Name_ | Integration, Git & Testing | [@username]() |

> **Update this table on Day 1** — add your real names and GitHub usernames.

---

## Project Structure

```
seekho-blog/
├── app.py                  ← Creates the Flask app, registers all routes
├── config.example.py       ← Copy this to config.py and fill in your DB details
├── db.py                   ← Database connection and shared query helpers
├── auth.py                 ← Register / Login / Logout routes
├── posts.py                ← Post CRUD + public blog views
├── requirements.txt        ← All Python packages needed
├── README.md               ← This file
├── CONTRIBUTING.md         ← Git workflow and contribution rules
├── .gitignore              ← Files that must NOT go to GitHub
│
├── /templates              ← Jinja2 HTML templates
│   ├── base.html           ← Shared layout (header, nav, footer)
│   ├── index.html          ← Home page — list of posts
│   ├── post_detail.html    ← Single post full view
│   ├── post_form.html      ← Create AND edit post (same form)
│   ├── dashboard.html      ← Author's own posts
│   ├── login.html          ← Login page
│   ├── register.html       ← Registration page
│   └── category.html       ← Posts filtered by category
│
├── /static
│   ├── /css
│   │   └── seekho.css      ← Your custom styles (dark/violet theme)
│   ├── /js
│   │   └── main.js         ← Small JS helpers (confirm dialogs, etc.)
│   └── /images             ← Logo and any static images
│
├── /sql
│   ├── schema.sql          ← Creates all tables (run this first!)
│   └── sample_data.sql     ← Seed data for demo
│
└── /docs
    ├── SRS_Seekho_Blog_Module.pdf
    └── WEEK_PLAN.md
```

---

## Setup Instructions (Read Every Step Carefully)

### Step 1 — Install the Requirements

Make sure these are installed on your machine before anything else:

- **Python 3.10 or newer** — check with `python --version`
- **XAMPP** — for MySQL. Start Apache and MySQL from the XAMPP Control Panel.
- **Git** — check with `git --version`
- **VS Code** — with the Python extension installed

---

### Step 2 — Clone the Repository

Open a terminal (Command Prompt or VS Code terminal):

```bash
git clone https://github.com/avii2312/seekho-blog.git
cd seekho-blog
```

---

### Step 3 — Create a Virtual Environment

A virtual environment keeps project packages separate from your system Python. **This is not optional.**

```bash
# Create the virtual environment
python -m venv venv

# Activate it — Windows:
venv\Scripts\activate

# Activate it — Mac/Linux:
source venv/bin/activate
```

You will see `(venv)` at the start of your terminal line. Good. Now every `pip install` goes into this project only.

---

### Step 4 — Install Python Packages

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist yet (first person setting up):

```bash
pip install flask
pip install mysql-connector-python
pip freeze > requirements.txt
```

Then commit `requirements.txt` to the repo.

---

### Step 5 — Set Up the Database

1. Open **phpMyAdmin** in your browser: `http://localhost/phpmyadmin`
2. Create a new database called `seekho_blog`
3. Click on `seekho_blog`, go to the **SQL** tab
4. Copy and paste the contents of `sql/schema.sql` and click **Go**
5. Do the same for `sql/sample_data.sql` (loads demo content)

---

### Step 6 — Create Your Config File

```bash
# Make a copy of the example config
copy config.example.py config.py        # Windows
cp config.example.py config.py          # Mac/Linux
```

Open `config.py` and fill in your database password:

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""          # ← XAMPP default is empty string
DB_NAME = "seekho_blog"
SECRET_KEY = "change-this-to-something-random-in-your-copy"
```

> ⚠️ **`config.py` must NEVER be pushed to GitHub.** It is already listed in `.gitignore`. Do not remove it from there.

---

### Step 7 — Run the App

```bash
flask --app app run --debug
```

Open your browser and go to: **`http://127.0.0.1:5000`**

You should see the Seekho Blog home page.

---

### Demo Admin Login

After loading sample data, use this account to test admin features:

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `Admin@123` |

> Change this in `sql/sample_data.sql` before your demo if you prefer.

---

## Features Checklist

### Tier 1 — Must Have (build these first)
- [ ] User registration with hashed password
- [ ] User login and logout
- [ ] Route protection (dashboard and post actions require login)
- [ ] Create a blog post (title, body, category)
- [ ] Edit own post
- [ ] Delete own post (with confirmation)
- [ ] Ownership check — cannot edit/delete someone else's post
- [ ] Author dashboard — list of own posts
- [ ] Home page — published posts, newest first
- [ ] Single post page
- [ ] Browse posts by category
- [ ] Admin: add, rename, remove categories

### Tier 2 — Should Have (start after Tier 1 is complete)
- [ ] Comments on posts (logged-in only)
- [ ] Pagination on home and category pages
- [ ] Draft / Published status for posts
- [ ] Search by keyword

### Tier 3 — Stretch Goals (only if ahead)
- [ ] Public author profile page
- [ ] Cover image upload per post
- [ ] Like / bookmark a post
- [ ] Admin moderation page

---

## Common Mistakes — Read This Now

These have cost previous batches real marks:

1. **Storing passwords as plain text.** Always use `generate_password_hash`. From the very first version.
2. **Building SQL with f-strings** like `f"SELECT * FROM users WHERE username = '{name}'"`. This is SQL injection. Use `?` placeholders always.
3. **One giant `app.py`.** Split your code into `auth.py`, `posts.py`, `db.py` from day one. See the folder structure above.
4. **Not using Git until the last day.** Commit after every working session. If your name is not in the commit history, you did not build it.
5. **Hiding the Edit button and calling it security.** Ownership must be checked on the **server** inside the route code. A hidden button is still reachable by URL.
6. **Treating Week 1 as settling-in time.** The database must be designed and the app must be running by end of Week 1. Without this, Week 2 cannot start.
7. **Chasing Tier 3 with Tier 1 broken.** Image upload is fun. Fixing login is marks.

---

## Evaluation Breakdown

| Criterion | Marks |
|---|---|
| Tier 1 functionality working end to end | 35 |
| Tier 2 functionality | 15 |
| Database design | 10 |
| Security (hashing, parameterised queries, access control) | 10 |
| Code quality and structure | 15 |
| Git usage (regular commits, all members contributing) | 5 |
| README + project report | 5 |
| Demo and individual viva | 5 |
| **Total** | **100** |

---

## Questions and Blockers

If you are stuck for more than **30 minutes** on the same problem — that is a blocker. Write it down and raise it at the daily stand-up. Do not sit quietly with a broken problem all day.

Stand-up format (15 minutes, every working day):
1. What did I do yesterday?
2. What will I do today?
3. What is blocking me?

---

*VISANET Software Pvt. Ltd. · Washim, Maharashtra · Internal training document — not for external distribution*
