
CREATE DATABASE `direct_democracy`;
USE `direct_democracy`;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

CREATE TABLE IF NOT EXISTS `propositions` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `updated` int(12) NOT NULL,
  `upvotes` int(10) NOT NULL,
  `downvotes` int(10) NOT NULL,
  `title` text NOT NULL,
  `url` text NOT NULL,
  `pub_date` int(12) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(9) NOT NULL AUTO_INCREMENT,
  `username` text NOT NULL,
  `email` text NOT NULL,
  `firstname` text NOT NULL,
  `lastname` text NOT NULL,
  `personal_number` varchar(12) NOT NULL,
  `hash` varchar(64) NOT NULL,
  `salt` varchar(64) NOT NULL,
  `regdate` int(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `votes` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `proposition_id` int(12) NOT NULL,
  `user_id` int(12) NOT NULL,
  `vote` int(1) NOT NULL,
  `timestamp` int(12) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_index`(`user_id`, `proposition_id`)
  -- OLD, WRONG: UNIQUE KEY `proposition_id` (`proposition_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='VOTE: 0 for no, 1 for yes' AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;