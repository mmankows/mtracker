CREATE TABLE `users` (
	  `user_id` bigint(5) NOT NULL auto_increment,
	  `device_id` char(32) NOT NULL,
	  `tracked_from` timestamp NOT NULL default CURRENT_TIMESTAMP,
	  `comment` varchar(255) default NULL,
	  `login` char(30) NOT NULL,
	  `pass` char(32) NOT NULL,
	  `token` char(32) NOT NULL,
	  PRIMARY KEY  (`user_id`),
	  UNIQUE (`device_id`),
	  UNIQUE (`login`)
);
