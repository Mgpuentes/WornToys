CREATE DATABASE IF NOT EXISTS `WornToys`;
USE `WornToys`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(55) DEFAULT NULL,
  `last_name` varchar(55) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `username` varchar(50),
  PRIMARY KEY (`user_id`)
);

DROP TABLE IF EXISTS `seller`;
CREATE TABLE `seller` (
  `seller_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `first_name` varchar(55) DEFAULT NULL,
  `last_name` varchar(55) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`seller_id`),
  FOREIGN KEY (`user_id`) REFERENCES user(`user_id`)
);

DROP TABLE IF EXISTS `toy`;
CREATE TABLE `toy` (
	`toy_id` int(11) NOT NULL AUTO_INCREMENT,
	`seller_id` int(11) NOT NULL,
	`name` varchar(55) DEFAULT NULL,
	`list_date` datetime DEFAULT NULL,
	`toy_image` varchar(55) DEFAULT NULL,
	PRIMARY KEY (`toy_id`),
	FOREIGN KEY(`seller_id`) REFERENCES seller(`seller_id`)
);
