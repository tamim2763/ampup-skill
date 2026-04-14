-- AmpUp Skill Database Schema

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Career tracks (Blockchain, Backend Engineering, DevOps, ML)
CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    color TEXT,
    roadmap_url TEXT
);

-- Phases within a track
CREATE TABLE IF NOT EXISTS phases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id INTEGER NOT NULL,
    phase_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);

-- Individual lectures (YouTube videos)
CREATE TABLE IF NOT EXISTS lectures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phase_id INTEGER NOT NULL,
    lecture_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    youtube_url TEXT NOT NULL,
    youtube_id TEXT NOT NULL,
    duration TEXT,
    resource_links TEXT,
    FOREIGN KEY (phase_id) REFERENCES phases(id)
);

-- User progress tracking
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    lecture_id INTEGER NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, lecture_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (lecture_id) REFERENCES lectures(id)
);

-- Website visit tracking
CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_visits INTEGER DEFAULT 0,
    today_visits INTEGER DEFAULT 0,
    last_visit_date DATE
);

-- Visit cooldown tracking by IP
CREATE TABLE IF NOT EXISTS visit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitor_key TEXT NOT NULL UNIQUE,
    last_counted_at TIMESTAMP NOT NULL
);
