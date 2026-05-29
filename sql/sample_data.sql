-- =============================================================
-- Seekho Community Blog — Sample / Seed Data
-- VISANET Software Pvt. Ltd. · VSN-INT-SEEKHO-BLOG
-- =============================================================
-- Run schema.sql FIRST, then run this file.
-- This loads demo data so the project looks alive during
-- evaluation. Reload any time to reset to a known state.
-- =============================================================

USE seekho_blog;

-- Clear existing data (safe to re-run)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE comments;
TRUNCATE TABLE posts;
TRUNCATE TABLE categories;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;


-- -------------------------------------------------------------
-- Users
-- Passwords below are hashed versions of the values shown.
-- The hash was generated with werkzeug's generate_password_hash.
--
-- Admin login  → username: admin      password: Admin@123
-- User 1       → username: priya      password: Priya@123
-- User 2       → username: rahul      password: Rahul@123
-- User 3       → username: sneha      password: Sneha@123
-- -------------------------------------------------------------
INSERT INTO users (full_name, username, email, password_hash, is_admin) VALUES
(
    'Admin VISANET',
    'admin',
    'admin@visanet.in',
    'scrypt:32768:8:1$XaBC$abc123placeholder_replace_with_real_hash',
    1
),
(
    'Priya Sharma',
    'priya',
    'priya@example.com',
    'scrypt:32768:8:1$XaBC$abc123placeholder_replace_with_real_hash',
    0
),
(
    'Rahul Deshmukh',
    'rahul',
    'rahul@example.com',
    'scrypt:32768:8:1$XaBC$abc123placeholder_replace_with_real_hash',
    0
),
(
    'Sneha Patil',
    'sneha',
    'sneha@example.com',
    'scrypt:32768:8:1$XaBC$abc123placeholder_replace_with_real_hash',
    0
);

-- ⚠️  IMPORTANT: The password hashes above are placeholders.
-- Run generate_seed_passwords.py to create real hashes, or
-- register the accounts through the web form and update this
-- file with the hashes from your database before submission.


-- -------------------------------------------------------------
-- Categories
-- -------------------------------------------------------------
INSERT INTO categories (name, slug, description) VALUES
('Web Development',  'web-development',  'HTML, CSS, JavaScript, Flask and everything web.'),
('Photography',      'photography',      'Cameras, composition, editing and visual storytelling.'),
('Spoken English',   'spoken-english',   'Tips for confident speaking, vocabulary and pronunciation.'),
('Music',            'music',            'Learning instruments, music theory and practice routines.'),
('Cooking',          'cooking',          'Recipes, techniques and kitchen skills from scratch.');


-- -------------------------------------------------------------
-- Posts (published)
-- author_id 2 = priya, 3 = rahul, 4 = sneha
-- category_id 1=Web, 2=Photo, 3=English, 4=Music, 5=Cooking
-- -------------------------------------------------------------
INSERT INTO posts (title, slug, body, status, category_id, author_id, created_at) VALUES
(
    'How I Learned HTML in One Week',
    'how-i-learned-html-in-one-week',
    'I started knowing nothing about HTML. Here is what I did differently...\n\nFirst, I stopped watching long tutorials. Instead I opened a blank file and typed every tag by hand.\n\nThe tags I focused on first: p, h1, a, img, div. Five tags. That is enough to build a real page.\n\nDay 3 I built a personal profile page. Ugly, but it worked. Seeing your own name on a browser tab for the first time is a feeling I recommend.',
    'published',
    1,
    2,
    '2026-05-01 10:30:00'
),
(
    'Bootstrap 5 Grid Explained Simply',
    'bootstrap-5-grid-explained-simply',
    'The Bootstrap grid confused me until I understood one thing: it is always 12 columns.\n\nEvery row has 12 invisible columns. A col-md-6 takes 6 of them — half the row. Two col-md-6 divs sit side by side on medium screens and stack on mobile. That is the whole idea.\n\nThree common patterns:\n- Two equal columns: col-md-6 + col-md-6\n- Sidebar layout: col-md-4 + col-md-8\n- Three equal columns: col-md-4 + col-md-4 + col-md-4',
    'published',
    1,
    3,
    '2026-05-05 14:00:00'
),
(
    'My First Month with Python',
    'my-first-month-with-python',
    'Python was my first proper programming language. Before it I had tried C++ in college and given up.\n\nPython was different because the code looks like English. print("hello") just works.\n\nThe thing that clicked for me: functions. Once I understood that a function is just a reusable set of instructions with a name, everything else made sense.\n\nI practised by writing small scripts for things I actually needed — a script to rename files in a folder, one to generate a timetable. Practical projects beat exercises from a book.',
    'published',
    1,
    4,
    '2026-05-08 09:15:00'
),
(
    'How to Take Better Photos with Your Phone',
    'how-to-take-better-photos-with-your-phone',
    'Most phone cameras today are excellent. The limiting factor is almost never the camera.\n\nRule 1: Clean your lens. It sounds obvious. Most people never do it. A smudged lens kills sharpness.\n\nRule 2: Tap to focus. Do not let the phone decide what is important in your frame.\n\nRule 3: Find the light. The best time to shoot outdoors is the hour after sunrise and the hour before sunset. Soft, warm, directional — nothing looks bad in that light.\n\nRule 4: Move your feet. Get closer. Get lower. Try a different angle before you tap the shutter. The first position you stand in is rarely the best one.',
    'published',
    2,
    2,
    '2026-05-10 11:00:00'
),
(
    'Five English Speaking Habits That Helped Me',
    'five-english-speaking-habits-that-helped-me',
    'I grew up speaking Marathi at home. English at college felt like a performance.\n\nHabit 1: Listen more than you speak. I watched one English YouTube video every day and repeated sentences out loud, alone, like an actor learning lines.\n\nHabit 2: Stop translating in your head. Think in English even for small things — grocery lists, what you will eat, what you see outside.\n\nHabit 3: Write one paragraph every day. Writing slows your brain down and forces correct grammar.\n\nHabit 4: Do not apologise for your accent. Your accent is your voice. Clarity matters, accent does not.\n\nHabit 5: Speak first, perfect later. Waiting until you are confident means waiting forever.',
    'published',
    3,
    3,
    '2026-05-12 16:30:00'
),
(
    'Learning to Cook Dal Tadka From Scratch',
    'learning-to-cook-dal-tadka-from-scratch',
    'I am a hostel student. I learned to cook because I had no choice.\n\nDal tadka was my first real recipe. I failed it three times.\n\nFailure 1: I added too much water. The dal was soup.\nFailure 2: I forgot the turmeric until after everything was cooked. It tasted wrong.\nFailure 3: I burned the tadka because the oil was already too hot before I added the cumin.\n\nFourth time: I had it. The smell of mustard seeds, cumin and garlic hitting hot oil is one of the best smells in a kitchen.\n\nLesson: recipes are not instructions, they are guides. You learn by cooking, not by reading.',
    'published',
    5,
    4,
    '2026-05-14 13:00:00'
),
(
    'Why I Started Learning Guitar at 22',
    'why-i-started-learning-guitar-at-22',
    'Everyone told me I was too old to start. I was 22.\n\nI bought a second-hand guitar for 800 rupees from OLX. No brand, scratched body, but it held tune.\n\nI learned three chords in the first month: G, C, Em. With those three you can play most simple songs.\n\nThe hardest part is the first three weeks. Your fingertips hurt. Your chord changes are slow. You sound nothing like the song you are trying to play. This is normal. Everyone goes through it.\n\nI play every morning for twenty minutes before college. Nothing big. Just twenty minutes. Six months in and I can play songs people actually recognise.',
    'published',
    4,
    2,
    '2026-05-16 08:00:00'
),
(
    'Understanding Flask Routes — A Beginner Explanation',
    'understanding-flask-routes-beginner-explanation',
    'A Flask route is a connection between a URL and a Python function.\n\nWhen someone visits /about, Flask looks through your routes, finds the one for /about, and runs the function attached to it. That function returns HTML — a page.\n\n@app.route("/about")\ndef about():\n    return "<h1>About Page</h1>"\n\nThat is the whole idea. The decorator @app.route tells Flask which URL triggers this function.\n\nYou can pass values in the URL too:\n\n@app.route("/post/<slug>")\ndef post_detail(slug):\n    # slug now holds whatever is in the URL\n    # use it to look up the post from the database\n    pass\n\nI spent two days confused about routes. Then it clicked in about ten minutes once someone explained it this way.',
    'published',
    1,
    3,
    '2026-05-18 10:00:00'
);


-- -------------------------------------------------------------
-- Comments (Tier 2 sample data)
-- -------------------------------------------------------------
INSERT INTO comments (post_id, author_id, body, created_at) VALUES
(1, 3, 'This is exactly how I felt when I started. The personal project idea really works!', '2026-05-02 09:00:00'),
(1, 4, 'Which tutorials did you watch? I am looking for good ones.', '2026-05-02 14:00:00'),
(3, 2, 'Python was my first too. The function explanation is spot on.', '2026-05-09 10:00:00'),
(4, 4, 'The tip about tapping to focus changed my photos immediately. Thank you.', '2026-05-11 17:00:00'),
(5, 2, 'Habit 5 is the one I need to work on most. I wait too long before speaking.', '2026-05-13 08:30:00'),
(6, 3, 'I had the same burnt tadka problem my first time!', '2026-05-15 12:00:00');


-- =============================================================
-- After loading this file, use these logins for your demo:
--
--   Admin:  username=admin   password=Admin@123
--   Author: username=priya   password=Priya@123
--
-- ⚠️  Remember: the hashes above are placeholders.
--     Run the app, register accounts through the form,
--     then copy the real hashes from your DB into this file.
-- =============================================================
