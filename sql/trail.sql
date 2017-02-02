CREATE DATABASE IF NOT EXISTS trails;

CREATE TABLE `trails`.`trail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `county` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `state` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `low_end` tinyint(4) DEFAULT NULL,
  `high_end` tinyint(4) DEFAULT NULL,
  `rock_crawling` tinyint(4) DEFAULT NULL,
  `dirt_mud` tinyint(4) DEFAULT NULL,
  `water_crossing` tinyint(4) DEFAULT NULL,
  `playgrounds` tinyint(4) DEFAULT NULL,
  `cliffs_ledges` tinyint(4) DEFAULT NULL,
  `climbs_descents` tinyint(4) DEFAULT NULL,
  `elevation` tinyint(4) DEFAULT NULL,
  `scenery` tinyint(4) DEFAULT NULL,
  `other` tinyint(4) DEFAULT NULL,
  `trail_type` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `season` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `length` float DEFAULT NULL,
  `low_point_elevation` int(11) DEFAULT NULL,
  `high_point_elevation` int(11) DEFAULT NULL,
  `elevation_change` int(11) DEFAULT NULL,
  `image_location` text COLLATE utf8_bin,
  `image_count` int(11) DEFAULT NULL,
  `trail_url` text COLLATE utf8_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
