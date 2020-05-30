CREATE TABLE IF NOT EXISTS users (
  -- it increments by default without need for AUTOINCREMENT
  -- https://www.sqlite.org/autoinc.html
  id INTEGER PRIMARY KEY, 
  slack_user_id TEXT UNIQUE,
  slack_user_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS warmshowers (
  user_id TEXT NOT NULL,
  praise TEXT NOT NULL,
  createdON DATETIME,
  lastModifiedOn DATETIME,
  FOREIGN KEY(user_id) REFERENCES users(slack_user_id)
);
