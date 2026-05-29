-- =============================================================
-- Seekho Community Blog Module — Database Schema
-- VISANET Software Pvt. Ltd. · VSN-INT-SEEKHO-BLOG
-- =============================================================
-- How to use:
--   1. Open phpMyAdmin → http://localhost/phpmyadmin
--   2. Create database: seekho_blog
--   3. Click on seekho_blog → SQL tab
--   4. Paste this file and click Go
-- =============================================================

CREATE DATABASE IF NOT EXISTS seekho_blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE seekho_blog;

-- -------------------------------------------------------------
-- Table: users
-- Stores all registered accounts (authors and the admin)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id           INT           NOT NULL AUTO_INCREMENT,
    full_name    VARCHAR(100)  NOT NULL,
    username     VARCHAR(50)   NOT NULL,
    email        VARCHAR(150)  NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin     TINYINT(1)    NOT NULL DEFAULT 0,   -- 0 = normal author, 1 = admin
    created_at   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_username (username),
    UNIQUE KEY uq_email    (email)
) ENGINE=InnoDB;


-- -------------------------------------------------------------
-- Table: categories
-- Topics under which posts are organised
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
    id          INT          NOT NULL AUTO_INCREMENT,
    name        VARCHAR(80)  NOT NULL,
    slug        VARCHAR(100) NOT NULL,   -- URL-friendly: "web-development"
    description VARCHAR(255)     NULL,

    PRIMARY KEY (id),
    UNIQUE KEY uq_cat_name (name),
    UNIQUE KEY uq_cat_slug (slug)
) ENGINE=InnoDB;


-- -------------------------------------------------------------
-- Table: posts
-- The main blog articles
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS posts (
    id          INT          NOT NULL AUTO_INCREMENT,
    title       VARCHAR(200) NOT NULL,
    slug        VARCHAR(220) NOT NULL,   -- Generated from title
    body        TEXT         NOT NULL,
    status      VARCHAR(20)  NOT NULL DEFAULT 'published',  -- 'draft' or 'published'
    category_id INT              NULL,
    author_id   INT          NOT NULL,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_post_slug (slug),
    CONSTRAINT fk_post_category FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE SET NULL,
    CONSTRAINT fk_post_author   FOREIGN KEY (author_id)   REFERENCES users     (id) ON DELETE CASCADE
) ENGINE=InnoDB;


-- -------------------------------------------------------------
-- Table: comments  (Tier 2 — FR-4.1)
-- Comments left on posts by logged-in users
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS comments (
    id        INT      NOT NULL AUTO_INCREMENT,
    post_id   INT      NOT NULL,
    author_id INT      NOT NULL,
    body      TEXT     NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT fk_comment_post   FOREIGN KEY (post_id)   REFERENCES posts (id) ON DELETE CASCADE,
    CONSTRAINT fk_comment_author FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB;


-- =============================================================
-- Notes for the Database & Models owner:
-- 
-- 1. ON DELETE SET NULL  for posts.category_id means: if an
--    admin removes a category, the posts in it keep existing
--    but their category becomes NULL. Handle NULL category_id
--    gracefully in your templates (show "Uncategorised").
--    Document this decision in your README.
--
-- 2. ON DELETE CASCADE for posts.author_id and both comment
--    FKs means: deleting a user removes all their posts and
--    comments. This is acceptable for a training project.
--
-- 3. Slug uniqueness: two posts with the same title will
--    produce the same slug and fail the UNIQUE constraint.
--    Your application code must handle this — append a number
--    if the slug already exists (e.g. "my-post-2").
--
-- 4. The admin account is NOT created via the registration page.
--    Insert it directly using sample_data.sql and set is_admin=1.
-- =============================================================
