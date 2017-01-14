-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        5.5.25 - MySQL Community Server (GPL)
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  8.3.0.4694
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- 导出 yun_crawler 的数据库结构
CREATE DATABASE IF NOT EXISTS `yun_crawler` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `yun_crawler`;


-- 导出  表 yun_crawler.task_list 结构
CREATE TABLE IF NOT EXISTS `task_list` (
  `task_id` int(11) NOT NULL AUTO_INCREMENT,
  `task_url` varchar(1024) DEFAULT NULL,
  `task_match_dom` varchar(1024) DEFAULT NULL,
  `task_pagination` varchar(1024) DEFAULT NULL,
  `task_max_page` int(11) DEFAULT '10',
  `task_add_time` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='任务列表';

-- 正在导出表  yun_crawler.task_list 的数据：~0 rows (大约)
/*!40000 ALTER TABLE `task_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_list` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
