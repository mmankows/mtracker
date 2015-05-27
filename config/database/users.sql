CREATE TABLE `users` (
	  `user_id` bigint(5) NOT NULL auto_increment,
	  `device_id` char(32) NOT NULL,
	  `tracked_from` timestamp NOT NULL default CURRENT_TIMESTAMP,
	  `comment` varchar(255) default NULL,
	  `login` char(30) NOT NULL,
	  `pass` char(32) NOT NULL,
	  `token` char(32) NOT NULL,
	  PRIMARY KEY  (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2003 DEFAULT CHARSET=latin2;
