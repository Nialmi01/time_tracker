-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'employee')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Time records table
CREATE TABLE IF NOT EXISTS time_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    login_time TIMESTAMP,
    logout_time TIMESTAMP,
    total_work_time INTEGER DEFAULT 0,  -- In seconds
    total_break_time INTEGER DEFAULT 0,  -- In seconds
    total_lunch_time INTEGER DEFAULT 0,  -- In seconds
    total_bathroom_time INTEGER DEFAULT 0,  -- In seconds
    total_meeting_time INTEGER DEFAULT 0,  -- In seconds
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Activity logs table
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL,
    activity_type TEXT NOT NULL CHECK (activity_type IN ('work', 'break', 'lunch', 'bathroom', 'meeting')),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration INTEGER DEFAULT 0,  -- In seconds
    FOREIGN KEY (record_id) REFERENCES time_records (id)
);