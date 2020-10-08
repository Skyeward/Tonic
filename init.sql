SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `Customers`;
CREATE TABLE `Customers` (
  `customerID` int NOT NULL AUTO_INCREMENT,
  `customerName` varchar(100) NOT NULL,
  `favouriteDrink` varchar(100) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`customerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `Customers` (`customerID`, `customerName`, `favouriteDrink`, `active`) VALUES
(1,	'Bob',	'tea',	1),
(3,	'Simon',	'coffee',	1),
(5,	'Sasha',	'lemonade',	1),
(7,	'Abob',	'water',	1),
(8,	'Aaron',	'coffee',	0);

INSERT INTO `Drinks` (`drinkID`, `drinkName`, `drinkAvailable`) VALUES
(1,	'tea',	1),
(2,	'coffee',	1),
(3,	'water',	1),
(7,	'lemonade',	1);

INSERT INTO `OrderRequests` (`orderID`, `customerName`, `drinkName`) VALUES
(3,	'Bob',	'tea'),
(3,	'Simon',	'coffee'),
(3,	'Sasha',	'lemonade'),
(3,	'Abob',	'water'),
(4,	'Bob',	'tea'),
(4,	'Simon',	'coffee'),
(4,	'Sasha',	'lemonade'),
(4,	'Abob',	'water');

INSERT INTO `Orders` (`orderID`, `runner`, `timePlaced`) VALUES
(3,	'Bob',	'2020-10-07 23:36:23'),
(4,	'Bob',	'2020-10-08 08:57:50');

INSERT INTO `PeopleTest` (`username`, `firstName`, `lastName`, `jobTitle`, `mobileNum`, `postcode`) VALUES
('chris@contoso.com',	'Chris',	'Green',	'It Manager',	'123-555-6641',	'98052'),
('ben@contoso.com',	'Ben',	'Andrews',	'It Manager',	'123-555-6642',	'98052'),
('david@contoso.com',	'David',	'Longmuir',	'It Manager',	'123-555-6643',	'98052'),
('cynthia@contoso.com',	'Cynthia',	'Carey',	'It Manager',	'123-555-6644',	'98052'),
('melissa@contoso.com',	'Melissa',	'Macbeth',	'It Manager',	'123-555-6645',	'98052');