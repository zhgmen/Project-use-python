create database zhgmen

use zhgmen

CREATE TABLE `authors` (
  `name` varchar(20) NOT NULL,
  `region` varchar(20) DEFAULT 'chinese',
  `description` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8；

CREATE TABLE `books` (
  `id` int(10) NOT NULL,
  `name` char(20) DEFAULT NULL,
  `author` varchar(20) NOT NULL,
  `description` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author` (`author`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`author`) REFERENCES `authors` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8；
