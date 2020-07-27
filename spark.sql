-- MySQL dump 10.13  Distrib 5.6.48, for Linux (x86_64)
--
-- Host: localhost    Database: Spark
-- ------------------------------------------------------
-- Server version	5.7.18-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `rClassStudent`
--

DROP TABLE IF EXISTS `rClassStudent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rClassStudent` (
  `classId` int(11) NOT NULL,
  `studentId` int(11) NOT NULL,
  `isFeedback` int(1) DEFAULT '0',
  `mark` int(1) DEFAULT '0',
  `improvements` text,
  PRIMARY KEY (`classId`,`studentId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tClass`
--

DROP TABLE IF EXISTS `tClass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tClass` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `volunteerId` int(11) DEFAULT '0',
  `classTime` date NOT NULL,
  `createTime` timestamp NOT NULL DEFAULT '1970-01-01 16:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `isFeedback` int(1) DEFAULT '0',
  `classBehavior` text,
  `classContent` text,
  `improvements` text,
  `changes` text,
  `notes` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tStudent`
--

DROP TABLE IF EXISTS `tStudent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tStudent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wxOpenId` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `gender` enum('MAN','WOMEN') DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `school` varchar(128) DEFAULT NULL,
  `grade` varchar(128) DEFAULT NULL,
  `qq` varchar(32) DEFAULT NULL,
  `location` text,
  `applyDate` datetime DEFAULT NULL,
  `applySchedule` enum('DOING','DONE','REJECT') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tUser`
--

DROP TABLE IF EXISTS `tUser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tUser` (
  `wxOpenId` varchar(128) NOT NULL,
  `wxSessionKey` varchar(128) NOT NULL,
  `role` varchar(32) DEFAULT NULL,
  `createTime` timestamp NULL DEFAULT '1970-01-01 16:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`wxOpenId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tVolunteer`
--

DROP TABLE IF EXISTS `tVolunteer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tVolunteer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wxOpenId` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `gender` enum('MAN','WOMEN') DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `school` varchar(128) DEFAULT NULL,
  `grade` int(11) DEFAULT NULL,
  `qq` varchar(32) DEFAULT NULL,
  `time` text,
  `parentType` enum('FATHER','MOTHER') DEFAULT NULL,
  `parentName` varchar(128) DEFAULT NULL,
  `parentPhone` varchar(20) DEFAULT NULL,
  `parentJob` varchar(128) DEFAULT NULL,
  `teachExpirence` text,
  `hobby` varchar(128) DEFAULT NULL,
  `department` varchar(128) DEFAULT NULL,
  `applyDate` datetime DEFAULT NULL,
  `applySchedule` enum('DOING','DONE','REJECT') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-27 20:44:15
