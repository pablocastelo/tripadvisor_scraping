-- phpMyAdmin SQL Dump
-- version 3.5.6
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 30, 2014 at 11:33 PM
-- Server version: 5.5.34-0ubuntu0.13.04.1
-- PHP Version: 5.3.28

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `tripadvisor`
--

-- --------------------------------------------------------

--
-- Table structure for table `destination`
--

CREATE TABLE IF NOT EXISTS `destination` (
  `destination_id` int(8) NOT NULL AUTO_INCREMENT,
  `timestamp_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(120) NOT NULL,
  `country` varchar(120) NOT NULL,
  `description` text NOT NULL,
  `tripadvisor_url_main` varchar(250) NOT NULL,
  `tripadvisor_url_rest` varchar(250) NOT NULL,
  `tripadvisor_url_hotel` varchar(250) NOT NULL,
  `tripadvisor_url_attract` varchar(250) NOT NULL,
  `tripadvisor_url_forum` varchar(250) NOT NULL,
  PRIMARY KEY (`destination_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `ta_attractions`
--

CREATE TABLE IF NOT EXISTS `ta_attractions` (
  `ta_attraction_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `destination_id` int(11) NOT NULL,
  `name` varchar(180) NOT NULL,
  `website` varchar(240) NOT NULL,
  `address` varchar(240) NOT NULL,
  `type` varchar(180) NOT NULL,
  `owner_desc` varchar(240) NOT NULL,
  `useful_info` text NOT NULL,
  PRIMARY KEY (`ta_attraction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `ta_attraction_review`
--

CREATE TABLE IF NOT EXISTS `ta_attraction_review` (
  `ta_attract_review_id` int(10) NOT NULL AUTO_INCREMENT,
  `timestamp_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ta_attraction` varchar(120) NOT NULL,
  `user` varchar(60) NOT NULL,
  `user_title` varchar(120) NOT NULL,
  `user_city` varchar(60) NOT NULL,
  `user_country` varchar(60) NOT NULL,
  `review_title` varchar(240) NOT NULL,
  `review_date` date NOT NULL,
  `visited_date` date NOT NULL,
  `review_body` text NOT NULL,
  `rating` int(1) NOT NULL,
  PRIMARY KEY (`ta_attract_review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `ta_hotel`
--

CREATE TABLE IF NOT EXISTS `ta_hotel` (
  `ta_hotel_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `destination_id` int(11) NOT NULL,
  `name` varchar(80) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `hotel_class` varchar(50) NOT NULL,
  `website` varchar(240) CHARACTER SET utf8 COLLATE utf8_spanish_ci DEFAULT NULL,
  `address` varchar(240) CHARACTER SET utf8 COLLATE utf8_spanish_ci DEFAULT NULL,
  `ta_hotel_url` varchar(240) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`ta_hotel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `ta_hotel_review`
--

CREATE TABLE IF NOT EXISTS `ta_hotel_review` (
  `ta_hotel_review_id` int(10) NOT NULL AUTO_INCREMENT,
  `timestamp_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ta_hotel_id` int(11) NOT NULL,
  `user` varchar(80) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `user_title` varchar(150) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `user_city` varchar(100) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `review_title` varchar(150) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `review_date` varchar(100) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `stayed_date` varchar(150) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `rating` varchar(25) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `review_body` text CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `rating_value` varchar(25) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `rating_location` varchar(25) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `rating_sleep_quality` varchar(25) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `rating_rooms` varchar(25) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `rating_cleanliness` varchar(25) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `rating_service` varchar(25) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `room_tip` varchar(180) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`ta_hotel_review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `ta_restaurant`
--

CREATE TABLE IF NOT EXISTS `ta_restaurant` (
  `ta_restaurant_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `destination_id` int(11) NOT NULL,
  `ta_url` varchar(240) NOT NULL,
  `name` varchar(80) NOT NULL,
  `price_range` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `cuisine` varchar(150) NOT NULL,
  `dining_options` varchar(240) DEFAULT NULL,
  `website` varchar(240) DEFAULT NULL,
  `address` varchar(240) DEFAULT NULL,
  PRIMARY KEY (`ta_restaurant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `ta_rest_review`
--

CREATE TABLE IF NOT EXISTS `ta_rest_review` (
  `ta_rest_review_id` int(10) NOT NULL AUTO_INCREMENT,
  `timestamp_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ta_restaurant_id` int(10) NOT NULL,
  `user` varchar(50) NOT NULL,
  `user_title` varchar(150) NOT NULL,
  `user_city` varchar(100) NOT NULL,
  `review_title` varchar(150) NOT NULL,
  `review_date` varchar(100) NOT NULL,
  `visit_date` varchar(100) NOT NULL,
  `rating` varchar(60) NOT NULL,
  `review_body` text NOT NULL,
  `rating_food` varchar(60) NOT NULL,
  `rating_service` varchar(60) NOT NULL,
  `rating_value` varchar(60) NOT NULL,
  `rating_atm` varchar(60) NOT NULL,
  PRIMARY KEY (`ta_rest_review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
