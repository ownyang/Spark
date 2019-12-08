CREATE TABLE IF NOT EXISTS `tVolunteer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wxOpenId` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `gende` enum('MAN','WOMEN') DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `school` varchar(128) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `qq` varchar(32) DEFAULT NULL,
  `parentName` varchar(128) DEFAULT NULL,
  `parentPhone` varchar(20) DEFAULT NULL,
  `parentJob` varchar(128) DEFAULT NULL,
  `studyAbroad` varchar(128) DEFAULT NULL,
  `teachExpirence` text,
  `advice` text,
  `hoby` varchar(128) DEFAULT NULL,
  `socialExpirence` text,
  `department` varchar(128) DEFAULT NULL,
  `applyDate` datetime DEFAULT NULL,
  `applySchedule` enum('DOING','DONE','REJECT') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `tStudent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wxOpenId` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `gende` enum('MAN','WOMEN') DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `school` varchar(128) DEFAULT NULL,
  `grade` varchar(128) DEFAULT NULL,
  `qq` varchar(32) DEFAULT NULL,
  `parentName` varchar(128) DEFAULT NULL,
  `parentPhone` varchar(20) DEFAULT NULL,
  `parentJob` varchar(128) DEFAULT NULL,
  `applyDate` datetime DEFAULT NULL,
  `applySchedule` enum('DOING','DONE','REJECT') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `tClass` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `volunteerId` int(11)  default 0,
  `startTime` datetime NOT NULL,
  `endTime` datetime NOT NULL,
  `createTime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `rClassStudent` (
  `classId` int(11) NOT NULL,
  `studentId` int(11) NOT NULL,
  `state` int(11) default 0,
  PRIMARY KEY (`classId`,`studentId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;