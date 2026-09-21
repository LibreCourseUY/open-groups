-- upgrade

CREATE TABLE IF NOT EXISTS group_tags (
    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (group_id, tag_id)
);

CREATE TABLE IF NOT EXISTS "groups" (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    url VARCHAR(500),
    pinned BOOLEAN DEFAULT FALSE,
    created_at DATETIME
);

CREATE TABLE IF NOT EXISTS important_links (
    id INTEGER NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    url VARCHAR(500) NOT NULL,
    created_at DATETIME
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created_at DATETIME,
    UNIQUE (name)
);

-- rollback

DROP TABLE tags

DROP TABLE important_links

DROP TABLE groups

DROP TABLE group_tags
