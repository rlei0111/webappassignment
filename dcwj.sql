-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        5.7.26 - MySQL Community Server (GPL)
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  12.16.0.7229
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 导出 dcwj 的数据库结构
CREATE DATABASE IF NOT EXISTS `dcwj` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `dcwj`;

-- 导出  表 dcwj.answers 结构
CREATE TABLE IF NOT EXISTS `answers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `response_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `option_id` int(11) DEFAULT NULL,
  `answer_text` text COLLATE utf8mb4_unicode_ci,
  `rating_value` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `option_id` (`option_id`),
  KEY `ix_answers_question_id` (`question_id`),
  KEY `ix_answers_response_id` (`response_id`)
) ENGINE=MyISAM AUTO_INCREMENT=179 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 正在导出表  dcwj.answers 的数据：178 rows
DELETE FROM `answers`;
INSERT INTO `answers` (`id`, `response_id`, `question_id`, `option_id`, `answer_text`, `rating_value`) VALUES
	(1, 1, 1, 1, NULL, NULL),
	(2, 1, 2, 7, NULL, NULL),
	(3, 1, 2, 6, NULL, NULL),
	(4, 1, 2, 8, NULL, NULL),
	(5, 1, 3, NULL, NULL, 9),
	(6, 2, 1, 5, NULL, NULL),
	(7, 2, 2, 7, NULL, NULL),
	(8, 2, 2, 9, NULL, NULL),
	(9, 2, 3, NULL, NULL, 9),
	(10, 3, 1, 1, NULL, NULL),
	(11, 3, 2, 7, NULL, NULL),
	(12, 3, 2, 10, NULL, NULL),
	(13, 3, 2, 9, NULL, NULL),
	(14, 3, 3, NULL, NULL, 9),
	(15, 3, 4, NULL, '服务很好，继续保持！', NULL),
	(16, 4, 1, 4, NULL, NULL),
	(17, 4, 2, 9, NULL, NULL),
	(18, 4, 2, 6, NULL, NULL),
	(19, 4, 3, NULL, NULL, 7),
	(20, 4, 4, NULL, '配送速度可以再快一些', NULL),
	(21, 5, 1, 4, NULL, NULL),
	(22, 5, 2, 10, NULL, NULL),
	(23, 5, 3, NULL, NULL, 9),
	(24, 5, 4, NULL, '配送速度可以再快一些', NULL),
	(25, 6, 1, 3, NULL, NULL),
	(26, 6, 2, 8, NULL, NULL),
	(27, 6, 2, 10, NULL, NULL),
	(28, 6, 2, 7, NULL, NULL),
	(29, 6, 3, NULL, NULL, 10),
	(30, 7, 1, 5, NULL, NULL),
	(31, 7, 2, 10, NULL, NULL),
	(32, 7, 3, NULL, NULL, 9),
	(33, 7, 4, NULL, '客服态度很好，解决问题及时', NULL),
	(34, 8, 1, 1, NULL, NULL),
	(35, 8, 2, 7, NULL, NULL),
	(36, 8, 2, 8, NULL, NULL),
	(37, 8, 2, 6, NULL, NULL),
	(38, 8, 3, NULL, NULL, 7),
	(39, 8, 4, NULL, '价格有点贵，希望能降价', NULL),
	(40, 9, 1, 4, NULL, NULL),
	(41, 9, 2, 8, NULL, NULL),
	(42, 9, 2, 6, NULL, NULL),
	(43, 9, 3, NULL, NULL, 6),
	(44, 9, 4, NULL, '建议增加更多产品种类', NULL),
	(45, 10, 1, 5, NULL, NULL),
	(46, 10, 2, 8, NULL, NULL),
	(47, 10, 3, NULL, NULL, 6),
	(48, 11, 1, 2, NULL, NULL),
	(49, 11, 2, 10, NULL, NULL),
	(50, 11, 3, NULL, NULL, 9),
	(51, 11, 4, NULL, '价格有点贵，希望能降价', NULL),
	(52, 12, 1, 2, NULL, NULL),
	(53, 12, 2, 8, NULL, NULL),
	(54, 12, 2, 6, NULL, NULL),
	(55, 12, 2, 10, NULL, NULL),
	(56, 12, 3, NULL, NULL, 9),
	(57, 13, 1, 5, NULL, NULL),
	(58, 13, 2, 8, NULL, NULL),
	(59, 13, 2, 9, NULL, NULL),
	(60, 13, 3, NULL, NULL, 10),
	(61, 14, 1, 3, NULL, NULL),
	(62, 14, 2, 6, NULL, NULL),
	(63, 14, 3, NULL, NULL, 7),
	(64, 14, 4, NULL, '建议增加更多产品种类', NULL),
	(65, 15, 1, 4, NULL, NULL),
	(66, 15, 2, 9, NULL, NULL),
	(67, 15, 2, 10, NULL, NULL),
	(68, 15, 2, 7, NULL, NULL),
	(69, 15, 3, NULL, NULL, 10),
	(70, 16, 1, 4, NULL, NULL),
	(71, 16, 2, 9, NULL, NULL),
	(72, 16, 2, 8, NULL, NULL),
	(73, 16, 2, 7, NULL, NULL),
	(74, 16, 3, NULL, NULL, 6),
	(75, 16, 4, NULL, '服务很好，继续保持！', NULL),
	(76, 17, 1, 4, NULL, NULL),
	(77, 17, 2, 6, NULL, NULL),
	(78, 17, 2, 10, NULL, NULL),
	(79, 17, 2, 9, NULL, NULL),
	(80, 17, 3, NULL, NULL, 9),
	(81, 17, 4, NULL, '希望能提供更多优惠活动', NULL),
	(82, 18, 1, 3, NULL, NULL),
	(83, 18, 2, 9, NULL, NULL),
	(84, 18, 2, 7, NULL, NULL),
	(85, 18, 2, 6, NULL, NULL),
	(86, 18, 3, NULL, NULL, 9),
	(87, 18, 4, NULL, '产品质量不错，很满意', NULL),
	(88, 19, 1, 1, NULL, NULL),
	(89, 19, 2, 9, NULL, NULL),
	(90, 19, 2, 10, NULL, NULL),
	(91, 19, 3, NULL, NULL, 9),
	(92, 20, 1, 5, NULL, NULL),
	(93, 20, 2, 8, NULL, NULL),
	(94, 20, 2, 9, NULL, NULL),
	(95, 20, 2, 7, NULL, NULL),
	(96, 20, 3, NULL, NULL, 10),
	(97, 21, 1, 1, NULL, NULL),
	(98, 21, 2, 7, NULL, NULL),
	(99, 21, 3, NULL, NULL, 9),
	(100, 22, 1, 3, NULL, NULL),
	(101, 22, 2, 7, NULL, NULL),
	(102, 22, 2, 10, NULL, NULL),
	(103, 22, 2, 9, NULL, NULL),
	(104, 22, 3, NULL, NULL, 9),
	(105, 22, 4, NULL, '产品质量不错，很满意', NULL),
	(106, 23, 1, 2, NULL, NULL),
	(107, 23, 2, 7, NULL, NULL),
	(108, 23, 2, 8, NULL, NULL),
	(109, 23, 3, NULL, NULL, 9),
	(110, 23, 4, NULL, '希望能提供更多优惠活动', NULL),
	(111, 24, 1, 5, NULL, NULL),
	(112, 24, 2, 10, NULL, NULL),
	(113, 24, 3, NULL, NULL, 10),
	(114, 25, 1, 5, NULL, NULL),
	(115, 25, 2, 9, NULL, NULL),
	(116, 25, 2, 6, NULL, NULL),
	(117, 25, 2, 8, NULL, NULL),
	(118, 25, 3, NULL, NULL, 10),
	(119, 26, 1, 5, NULL, NULL),
	(120, 26, 2, 10, NULL, NULL),
	(121, 26, 2, 8, NULL, NULL),
	(122, 26, 2, 9, NULL, NULL),
	(123, 26, 3, NULL, NULL, 6),
	(124, 27, 1, 2, NULL, NULL),
	(125, 27, 2, 7, NULL, NULL),
	(126, 27, 3, NULL, NULL, 10),
	(127, 27, 4, NULL, '配送速度可以再快一些', NULL),
	(128, 28, 1, 3, NULL, NULL),
	(129, 28, 2, 6, NULL, NULL),
	(130, 28, 2, 10, NULL, NULL),
	(131, 28, 3, NULL, NULL, 10),
	(132, 28, 4, NULL, '建议增加更多产品种类', NULL),
	(133, 29, 1, 2, NULL, NULL),
	(134, 29, 2, 8, NULL, NULL),
	(135, 29, 2, 9, NULL, NULL),
	(136, 29, 3, NULL, NULL, 6),
	(137, 29, 4, NULL, '希望能提供更多优惠活动', NULL),
	(138, 30, 1, 4, NULL, NULL),
	(139, 30, 2, 6, NULL, NULL),
	(140, 30, 3, NULL, NULL, 7),
	(141, 31, 5, 15, NULL, NULL),
	(142, 31, 6, NULL, NULL, 5),
	(143, 32, 5, 15, NULL, NULL),
	(144, 32, 6, NULL, NULL, 5),
	(145, 33, 5, 15, NULL, NULL),
	(146, 33, 6, NULL, NULL, 3),
	(147, 34, 5, 14, NULL, NULL),
	(148, 34, 6, NULL, NULL, 3),
	(149, 35, 5, 12, NULL, NULL),
	(150, 35, 6, NULL, NULL, 3),
	(151, 36, 5, 11, NULL, NULL),
	(152, 36, 6, NULL, NULL, 3),
	(153, 37, 5, 12, NULL, NULL),
	(154, 37, 6, NULL, NULL, 3),
	(155, 38, 5, 11, NULL, NULL),
	(156, 38, 6, NULL, NULL, 5),
	(157, 39, 5, 13, NULL, NULL),
	(158, 39, 6, NULL, NULL, 5),
	(159, 40, 5, 11, NULL, NULL),
	(160, 40, 6, NULL, NULL, 5),
	(161, 41, 5, 11, NULL, NULL),
	(162, 41, 6, NULL, NULL, 3),
	(163, 42, 5, 15, NULL, NULL),
	(164, 42, 6, NULL, NULL, 4),
	(165, 43, 5, 15, NULL, NULL),
	(166, 43, 6, NULL, NULL, 4),
	(167, 44, 5, 11, NULL, NULL),
	(168, 44, 6, NULL, NULL, 5),
	(169, 45, 5, 13, NULL, NULL),
	(170, 45, 6, NULL, NULL, 3),
	(171, 46, 1, 1, NULL, NULL),
	(172, 46, 2, 6, NULL, NULL),
	(173, 46, 2, 7, NULL, NULL),
	(174, 46, 2, 8, NULL, NULL),
	(175, 46, 2, 9, NULL, NULL),
	(176, 46, 2, 10, NULL, NULL),
	(177, 46, 3, NULL, NULL, 10),
	(178, 46, 4, NULL, '121212', NULL);

-- 导出  表 dcwj.options 结构
CREATE TABLE IF NOT EXISTS `options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `option_text_zh` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `option_text_en` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `order_num` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 正在导出表  dcwj.options 的数据：18 rows
DELETE FROM `options`;
INSERT INTO `options` (`id`, `question_id`, `option_text_zh`, `option_text_en`, `order_num`) VALUES
	(1, 1, '非常满意', 'Very Satisfied', 0),
	(2, 1, '满意', 'Satisfied', 1),
	(3, 1, '一般', 'Neutral', 2),
	(4, 1, '不满意', 'Dissatisfied', 3),
	(5, 1, '非常不满意', 'Very Dissatisfied', 4),
	(6, 2, '产品质量', 'Product Quality', 0),
	(7, 2, '服务态度', 'Service Attitude', 1),
	(8, 2, '价格优惠', 'Competitive Price', 2),
	(9, 2, '配送速度', 'Delivery Speed', 3),
	(10, 2, '售后服务', 'After-sales Service', 4),
	(11, 5, '18岁以下', 'Under 18', 0),
	(12, 5, '18-25岁', '18-25', 1),
	(13, 5, '26-35岁', '26-35', 2),
	(14, 5, '36-45岁', '36-45', 3),
	(15, 5, '46岁以上', 'Over 46', 4),
	(16, 7, '技术培训', 'Technical Training', 0),
	(17, 7, '管理培训', 'Management Training', 1),
	(18, 7, '沟通技巧', 'Communication Skills', 2);

-- 导出  表 dcwj.questions 结构
CREATE TABLE IF NOT EXISTS `questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `survey_id` int(11) NOT NULL,
  `question_text_zh` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `question_text_en` text COLLATE utf8mb4_unicode_ci,
  `question_type` enum('single','multiple','text','rating') COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_required` tinyint(1) DEFAULT NULL,
  `order_num` int(11) NOT NULL,
  `max_length` int(11) DEFAULT NULL,
  `rating_scale` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `survey_id` (`survey_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 正在导出表  dcwj.questions 的数据：7 rows
DELETE FROM `questions`;
INSERT INTO `questions` (`id`, `survey_id`, `question_text_zh`, `question_text_en`, `question_type`, `is_required`, `order_num`, `max_length`, `rating_scale`) VALUES
	(1, 1, '您对我们的服务总体满意度如何？', 'How satisfied are you with our service overall?', 'single', 1, 0, NULL, 5),
	(2, 1, '您最看重我们的哪些方面？（可多选）', 'What aspects do you value most about us? (Multiple choices)', 'multiple', 1, 1, NULL, 5),
	(3, 1, '您会向朋友推荐我们的服务吗？（1-10分）', 'Would you recommend our service to friends? (1-10)', 'rating', 1, 2, NULL, 10),
	(4, 1, '您对我们有什么建议或意见？', 'Do you have any suggestions or comments for us?', 'text', 0, 3, 500, 5),
	(5, 2, '您的年龄段是？', 'What is your age group?', 'single', 1, 0, NULL, 5),
	(6, 2, '您对新产品的外观设计评分（1-5分）', 'Rate the design of the new product (1-5)', 'rating', 1, 1, NULL, 5),
	(7, 3, '您希望参加哪些培训？', 'What training would you like to attend?', 'multiple', 1, 0, NULL, 5);

-- 导出  表 dcwj.responses 结构
CREATE TABLE IF NOT EXISTS `responses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `survey_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_agent` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_response` (`survey_id`,`user_id`),
  KEY `user_id` (`user_id`),
  KEY `idx_survey_ip` (`survey_id`,`ip_address`)
) ENGINE=MyISAM AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 正在导出表  dcwj.responses 的数据：46 rows
DELETE FROM `responses`;
INSERT INTO `responses` (`id`, `survey_id`, `user_id`, `ip_address`, `user_agent`, `submitted_at`) VALUES
	(1, 1, 2, '192.168.1.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-31 15:23:31'),
	(2, 1, 3, '192.168.1.2', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-30 15:23:31'),
	(3, 1, 4, '192.168.1.3', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-03 15:23:31'),
	(4, 1, 5, '192.168.1.4', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-30 15:23:31'),
	(5, 1, 6, '192.168.1.5', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-31 15:23:31'),
	(6, 1, NULL, '192.168.1.6', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-05 15:23:31'),
	(7, 1, NULL, '192.168.1.7', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-05 15:23:31'),
	(8, 1, NULL, '192.168.1.8', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-04 15:23:31'),
	(9, 1, NULL, '192.168.1.9', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-04 15:23:31'),
	(10, 1, NULL, '192.168.1.10', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-31 15:23:31'),
	(11, 1, NULL, '10.0.0.11', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-01 15:23:31'),
	(12, 1, NULL, '10.0.0.12', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-01 15:23:31'),
	(13, 1, NULL, '10.0.0.13', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-02 15:23:31'),
	(14, 1, NULL, '10.0.0.14', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-30 15:23:31'),
	(15, 1, NULL, '10.0.0.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-03 15:23:31'),
	(16, 1, NULL, '10.0.0.16', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-02 15:23:31'),
	(17, 1, NULL, '10.0.0.17', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-02 15:23:31'),
	(18, 1, NULL, '10.0.0.18', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-04 15:23:31'),
	(19, 1, NULL, '10.0.0.19', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-04 15:23:31'),
	(20, 1, NULL, '10.0.0.20', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-02 15:23:31'),
	(21, 1, NULL, '10.0.0.21', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-05 15:23:31'),
	(22, 1, NULL, '10.0.0.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-05 15:23:31'),
	(23, 1, NULL, '10.0.0.23', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-30 15:23:31'),
	(24, 1, NULL, '10.0.0.24', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-30 15:23:31'),
	(25, 1, NULL, '10.0.0.25', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-04 15:23:31'),
	(26, 1, NULL, '10.0.0.26', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-05 15:23:31'),
	(27, 1, NULL, '10.0.0.27', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-04 15:23:31'),
	(28, 1, NULL, '10.0.0.28', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-30 15:23:31'),
	(29, 1, NULL, '10.0.0.29', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-03 15:23:31'),
	(30, 1, NULL, '10.0.0.30', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-05 15:23:31'),
	(31, 2, NULL, '172.16.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-04 15:23:31'),
	(32, 2, 3, '172.16.0.2', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-03 15:23:31'),
	(33, 2, NULL, '172.16.0.3', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-31 15:23:31'),
	(34, 2, 5, '172.16.0.4', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-31 15:23:31'),
	(35, 2, NULL, '172.16.0.5', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-03 15:23:31'),
	(36, 2, 2, '172.16.0.6', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-02 15:23:31'),
	(37, 2, NULL, '172.16.0.7', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-01 15:23:31'),
	(38, 2, 4, '172.16.0.8', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-02 15:23:31'),
	(39, 2, NULL, '172.16.0.9', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-04 15:23:31'),
	(40, 2, 6, '172.16.0.10', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-03-31 15:23:31'),
	(41, 2, NULL, '172.16.0.11', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-03 15:23:31'),
	(42, 2, NULL, '172.16.0.12', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-02 15:23:31'),
	(43, 2, NULL, '172.16.0.13', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-04 15:23:31'),
	(44, 2, NULL, '172.16.0.14', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-05 15:23:31'),
	(45, 2, NULL, '172.16.0.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2026-04-03 15:23:31'),
	(46, 1, NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36', '2026-04-05 15:46:08');

-- 导出  表 dcwj.surveys 结构
CREATE TABLE IF NOT EXISTS `surveys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title_zh` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title_en` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description_zh` text COLLATE utf8mb4_unicode_ci,
  `description_en` text COLLATE utf8mb4_unicode_ci,
  `status` enum('draft','published','closed') COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `response_count` int(11) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `allow_anonymous` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 正在导出表  dcwj.surveys 的数据：3 rows
DELETE FROM `surveys`;
INSERT INTO `surveys` (`id`, `title_zh`, `title_en`, `description_zh`, `description_en`, `status`, `created_by`, `created_at`, `updated_at`, `response_count`, `start_time`, `end_time`, `allow_anonymous`) VALUES
	(1, '客户满意度调查', 'Customer Satisfaction Survey', '感谢您参与我们的客户满意度调查，您的反馈对我们非常重要！', 'Thank you for participating in our customer satisfaction survey. Your feedback is very important to us!', 'published', 1, '2026-04-05 15:23:31', '2026-04-05 15:46:08', 31, '2026-03-29 15:23:31', '2026-05-05 15:23:31', 1),
	(2, '新产品反馈调查', 'New Product Feedback Survey', '我们推出了新产品，期待您的宝贵意见！', 'We have launched a new product and look forward to your valuable feedback!', 'published', 1, '2026-04-05 15:23:31', '2026-04-05 15:23:31', 15, NULL, NULL, 1),
	(3, '员工培训需求调查', 'Employee Training Needs Survey', '了解员工培训需求，提升团队能力', 'Understand employee training needs and improve team capabilities', 'draft', 1, '2026-04-05 15:23:31', '2026-04-05 15:23:31', 0, NULL, NULL, 0);

-- 导出  表 dcwj.users 结构
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role` enum('user','admin') COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 正在导出表  dcwj.users 的数据：6 rows
DELETE FROM `users`;
INSERT INTO `users` (`id`, `username`, `password`, `email`, `role`, `created_at`) VALUES
	(1, 'admin', 'pbkdf2:sha256:260000$GfdX2oPsYGltPMR0$29f137a7118e6deb09c489d8f1001a8c55d8c888a154b7cd430833b90719fa54', 'admin@example.com', 'admin', '2026-04-05 15:23:29'),
	(2, 'user1', 'pbkdf2:sha256:260000$z3uhKR1nFzyAEXod$6b2ae7daf0c89eac7a827b03aa947d7078a4739c9d84a0bd4e0e7c045ddb5abb', 'user1@example.com', 'user', '2026-04-05 15:23:31'),
	(3, 'user2', 'pbkdf2:sha256:260000$phalweRK4mhyAGpQ$c14a98b14e7879064ef195961609b15433faa9e36e759d8e3670ed58e96e38ad', 'user2@example.com', 'user', '2026-04-05 15:23:31'),
	(4, 'user3', 'pbkdf2:sha256:260000$wc8qqis1z88i3XXm$42db148628516e85e4e9ef371b43b8a23cdb6320ca9915d21f19dbef3cf477d7', 'user3@example.com', 'user', '2026-04-05 15:23:31'),
	(5, 'user4', 'pbkdf2:sha256:260000$ZoM2sp4wfSDpVCev$7b9b30884c8e67960d9f0e7f15e432c609cd4316579676c121ae0d8fa1f2a1db', 'user4@example.com', 'user', '2026-04-05 15:23:31'),
	(6, 'user5', 'pbkdf2:sha256:260000$J4TNzKELZLqzzxRD$ae55d57c9ea9aee96f04ed7ae2cc4659fb293454db219feede28d635dee05dae', 'user5@example.com', 'user', '2026-04-05 15:23:31');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
