-- phpMyAdmin SQL Dump
-- version 4.2.10
-- http://www.phpmyadmin.net
--
-- Host: localhost:8889
-- Generation Time: Apr 13, 2015 at 12:53 PM
-- Server version: 5.5.38
-- PHP Version: 5.6.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `sms`
--

-- --------------------------------------------------------

--
-- Table structure for table `inbox`
--

CREATE TABLE `inbox` (
`id` int(11) NOT NULL,
  `sender_number` varchar(50) NOT NULL,
  `sender_name` varchar(50) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `sms_date` varchar(50) NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `message` text NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `inbox`
--

INSERT INTO `inbox` (`id`, `sender_number`, `sender_name`, `sender_id`, `sms_date`, `date_created`, `message`) VALUES
(3, '639175991688', 'Marc Clemen Andres', 1, 'dasdasfweq5465465', '2015-04-13 03:51:33', 'anyong sayo!');

-- --------------------------------------------------------

--
-- Table structure for table `outbox`
--

CREATE TABLE `outbox` (
`id` int(11) NOT NULL,
  `outbox_since` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `mobile_number` varchar(50) NOT NULL,
  `recipient_name` varchar(255) NOT NULL,
  `priority` varchar(50) NOT NULL,
  `telco` varchar(50) NOT NULL,
  `message` text NOT NULL,
  `status` int(11) NOT NULL,
  `date_sent` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `date_drafted` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `date_failed` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `outbox`
--

INSERT INTO `outbox` (`id`, `outbox_since`, `mobile_number`, `recipient_name`, `priority`, `telco`, `message`, `status`, `date_sent`, `date_drafted`, `date_failed`) VALUES
(2, '2015-04-13 06:16:46', '09175991688', 'Marc', 'high', 'globe', 'this is a test', 1, '0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(3, '2015-04-13 09:00:17', '09175991688', 'Marc Clemen Andres', 'low', 'globe', 'how are you doing dude?', 0, '0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(4, '2015-04-13 09:01:21', '09178954586', 'Chris Botor', 'high', 'globe', 'how are you doing????', 0, '0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `phonebook`
--

CREATE TABLE `phonebook` (
`id` int(11) NOT NULL,
  `department` varchar(50) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `primary_number` varchar(50) NOT NULL,
  `secondary_number` varchar(50) DEFAULT NULL,
  `rank` varchar(50) DEFAULT NULL,
  `designation` varchar(50) DEFAULT NULL,
  `home_address` varchar(255) DEFAULT NULL,
  `user_created` varchar(50) DEFAULT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_updated` varchar(50) DEFAULT NULL,
  `date_updated` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `telco` varchar(50) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `phonebook`
--

INSERT INTO `phonebook` (`id`, `department`, `name`, `primary_number`, `secondary_number`, `rank`, `designation`, `home_address`, `user_created`, `date_created`, `user_updated`, `date_updated`, `telco`) VALUES
(1, '', 'Marc Clemen Andres', '09175991688', '', '', '', '', '', '2015-04-13 07:52:10', '', '0000-00-00 00:00:00', 'globe'),
(2, '', 'Chris Botor', '09178954586', '', '', '', '', '', '2015-04-13 07:52:27', '', '0000-00-00 00:00:00', 'globe'),
(4, '', 'hunter', '09175991688', NULL, '', '', '3754c Bautista St.', NULL, '2015-04-13 10:35:59', NULL, '0000-00-00 00:00:00', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
`id` int(11) NOT NULL,
  `username` varchar(45) DEFAULT NULL,
  `firstname` varchar(45) DEFAULT NULL,
  `lastname` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `role` varchar(45) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `firstname`, `lastname`, `email`, `password`, `role`, `timestamp`) VALUES
(1, 'hunter', 'Marc Clemen', 'Andres c/o Bing Tan', 'sombreroisland@gmail.com', 'dondon888', '', '2015-03-10 07:31:05'),
(4, 'noel', 'Noel', 'Macatangay', 'noel@fdsfsd', 'dondon888', '', '2015-03-10 07:45:57'),
(5, 'huntertest', 'fdsafsdaf', 'sdafdsaf', 'fadsfds@fdsfdsf', 'hunter888', 'user', '2015-03-10 07:56:41'),
(6, 'tester', 'test', 'test', 'tester@gmail.com', 'dondon888', 'admin', '2015-04-08 04:13:08');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `inbox`
--
ALTER TABLE `inbox`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `outbox`
--
ALTER TABLE `outbox`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `phonebook`
--
ALTER TABLE `phonebook`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
 ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `inbox`
--
ALTER TABLE `inbox`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `outbox`
--
ALTER TABLE `outbox`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `phonebook`
--
ALTER TABLE `phonebook`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=7;
