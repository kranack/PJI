CREATE TABLE IF NOT EXISTS Titles (
	id			integer			PRIMARY KEY AUTOINCREMENT,
	raw_data	varchar(500)	NOT NULL
);

CREATE TABLE IF NOT EXISTS Tasks (
	id 			integer			UNIQUE,
	name 		varchar(500)	NOT NULL,
	date_create	date			NOT NULL,
	date_limit	date			DEFAULT NULL,
	status		integer			DEFAULT 0,	-- 0: OPEN; 1: DONE; 2: PENDING;
	priority	varchar(10)		DEFAULT '*',
	raw_titles	integer			REFERENCES Titles (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Depend_Tasks (
	task_id		integer		REFERENCES Tasks (id) ON UPDATE CASCADE,
	depend_id	integer		REFERENCES Tasks (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Users (
	id			integer			PRIMARY KEY AUTOINCREMENT,
	email		varchar(150)	NOT NULL,
	passwd		char(512)		NOT NULL
);

CREATE TABLE IF NOT EXISTS Assign_Tasks (
	user_id		integer		REFERENCES Users (id) ON UPDATE CASCADE,
	task_id		integer		REFERENCES Tasks (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Follow_Tasks (
	user_id		integer		REFERENCES Users (id) ON UPDATE CASCADE,
	task_id		integer		REFERENCES Tasks (id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Tags (
	id			integer			PRIMARY KEY AUTOINCREMENT,
	label		varchar(150)	NOT NULL
);

CREATE TABLE IF NOT EXISTS Attach_Tag (
	tag_id		integer		REFERENCES Tags (id) ON UPDATE CASCADE,
	task_id		integer		REFERENCES Tasks (id) ON UPDATE CASCADE
);
