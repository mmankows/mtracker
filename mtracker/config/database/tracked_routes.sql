CREATE TABLE `tracked_routes` (
  `step_id`     bigint(10) NOT NULL auto_increment,
  `user_id`     bigint(5) NOT NULL,
  `latitude`    decimal(10,7) NOT NULL,
  `longitude`   decimal(10,7) NOT NULL,
  `logdate`     timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`step_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=187 DEFAULT CHARSET=latin2; 
