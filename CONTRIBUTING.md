# Contribution Guide
### Seekho Blog Module — Git Workflow for Interns

This document tells you exactly how to use Git on this project. Read it on Day 1. If you have never used Git before, go through the setup steps below with your mentor present.

---

## One Rule Above All

> **`main` must always run.** Never push broken code to `main`. If you are not sure your code works, finish testing before you merge.

---

## One-Time Setup (Do This on Day 1)

### 1. Configure your identity
Git needs to know who you are. Every commit will carry your name.

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your@email.com"
```

Verify it saved:
```bash
git config --global user.name
```

### 2. Clone the repo
```bash
git clone https://github.com/avii2312/seekho-blog.git
cd seekho-blog
```

### 3. Check you can see the remote
```bash
git remote -v
```
You should see two lines showing `origin` pointing to the GitHub URL.

---

## Daily Workflow — Step by Step

Every time you sit down to work, follow these steps in order.

### Step 1 — Pull the latest code first

Before you write a single line, pull what your teammates pushed since you last worked:

```bash
git checkout main
git pull origin main
```

If you skip this, you will have conflicts later. Always pull first.

---

### Step 2 — Create a branch for your feature

Never work directly on `main`. Every feature gets its own branch.

```bash
git checkout -b feature/your-feature-name
```

Branch naming rules — use `feature/` followed by a short description using hyphens:

```
feature/login-page
feature/post-crud
feature/comments
feature/category-admin
feature/pagination
feature/search
```

**Bad branch names:**
```
my-work         ← too vague
test            ← means nothing
feature1        ← what feature?
FINAL           ← nothing is final
```

---

### Step 3 — Write code and commit often

Do not write code all day and commit once at the end. Commit in small chunks as each small piece works.

**Check what files changed:**
```bash
git status
```

**See the actual changes:**
```bash
git diff
```

**Stage the files you want to commit:**
```bash
git add filename.py                 # add one specific file
git add templates/login.html        # add one template
git add .                           # add everything changed (be careful with this)
```

**Commit with a meaningful message:**
```bash
git commit -m "add login route with session handling"
```

---

### Commit Message Rules

A commit message must say what changed, in plain words.

**Good examples:**
```
add user registration form and route
hash password on register using werkzeug
add ownership check before post edit
fix login error message not showing
add category dropdown to post form
```

**Bad examples — these will be flagged in code review:**
```
updates
done
asdf
final
final2
fix
wip
changes
aaj ka kaam
```

One sentence. Present tense. What the commit does.

---

### Step 4 — Push your branch to GitHub

After committing, push your branch:

```bash
git push origin feature/your-feature-name
```

If this is the first push of this branch, Git may ask you to set the upstream. Just run what it suggests, or:

```bash
git push --set-upstream origin feature/your-feature-name
```

---

### Step 5 — Create a Pull Request on GitHub

1. Go to the repository on GitHub
2. You will see a yellow bar saying your branch was recently pushed — click **"Compare & pull request"**
3. Write a short description of what you built
4. Assign your Integration/Git teammate as reviewer
5. Click **"Create pull request"**

---

### Step 6 — After review, merge into main

Once your teammate (or mentor) approves the PR:

1. Click **"Merge pull request"** on GitHub
2. Click **"Confirm merge"**
3. Click **"Delete branch"** (keep the branch list clean)

Then on your local machine:

```bash
git checkout main
git pull origin main
```

---

## Files That Must Never Go to GitHub

These are already in `.gitignore` — do not remove them from that file:

```
config.py               ← contains your DB password
venv/                   ← your virtual environment (huge folder, not needed by others)
__pycache__/            ← Python compiled files
*.pyc                   ← compiled Python
.env                    ← if you use one
```

If you accidentally committed `config.py`, tell your mentor immediately.

---

## Common Git Situations

### "I get a merge conflict"

A conflict happens when two people changed the same line in the same file. Don't panic.

```bash
git status          # shows which files have conflicts
```

Open the conflicted file. You will see markers like this:

```
<<<<<<< HEAD
your version of the line
=======
your teammate's version of the line
>>>>>>> feature/their-branch
```

Read both versions. Keep the right one (or combine them). Delete the marker lines. Save. Then:

```bash
git add the-conflicted-file.py
git commit -m "resolve merge conflict in posts.py"
```

Ask your Integration owner or mentor if you are unsure which version to keep.

---

### "I want to see what everyone has committed"

```bash
git log --oneline --all
```

Or on GitHub, click the **"Commits"** tab.

---

### "I made changes on main by mistake"

Stop. Do not push. Tell your mentor. We can fix it without losing your work.

---

### "I want to undo my last commit (before pushing)"

```bash
git reset --soft HEAD~1
```

Your changes are still there, just uncommitted. Fix what you need to and recommit.

---

## Checking Individual Contributions

At evaluation time, mentors look at the Git log to see who committed what. If your name is not in the history, you cannot prove you wrote the code.

Check your own commits:

```bash
git log --author="Your Name" --oneline
```

Every team member should have meaningful commits across multiple files. "Only committed README" is not a contribution.

---

## Quick Reference Card

```bash
# Start of every session
git checkout main
git pull origin main
git checkout -b feature/what-im-building

# While working
git status                          # what changed?
git add filename.py                 # stage a file
git commit -m "short description"   # save a checkpoint

# Push and open PR
git push origin feature/what-im-building

# After PR is merged, clean up
git checkout main
git pull origin main
```

---

*Questions about Git? Raise it at stand-up. Don't fight Git alone for more than 15 minutes.*

*VISANET Software Pvt. Ltd. · Internal training document*
