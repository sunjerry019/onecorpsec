-- Adminer 4.7.1 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

INSERT INTO `accounts_databaseuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `name`, `sign_off_name`, `reply_to`) VALUES
(1,	'pbkdf2_sha256$150000$RLLv944hc6iZ$9wOUleyidR7hanvd+biTteqgMhXS75azbQlvFv6mq1c=',	'2019-04-22 16:41:19.230980',	1,	'admin',	'',	'',	'yudong@onecorpsec.com',	1,	1,	'2019-03-17 01:22:48.738507',	'',	'',	'');





INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1,	'Can add log entry',	1,	'add_logentry'),
(2,	'Can change log entry',	1,	'change_logentry'),
(3,	'Can delete log entry',	1,	'delete_logentry'),
(4,	'Can view log entry',	1,	'view_logentry'),
(5,	'Can add permission',	2,	'add_permission'),
(6,	'Can change permission',	2,	'change_permission'),
(7,	'Can delete permission',	2,	'delete_permission'),
(8,	'Can view permission',	2,	'view_permission'),
(9,	'Can add group',	3,	'add_group'),
(10,	'Can change group',	3,	'change_group'),
(11,	'Can delete group',	3,	'delete_group'),
(12,	'Can view group',	3,	'view_group'),
(13,	'Can add content type',	4,	'add_contenttype'),
(14,	'Can change content type',	4,	'change_contenttype'),
(15,	'Can delete content type',	4,	'delete_contenttype'),
(16,	'Can view content type',	4,	'view_contenttype'),
(17,	'Can add session',	5,	'add_session'),
(18,	'Can change session',	5,	'change_session'),
(19,	'Can delete session',	5,	'delete_session'),
(20,	'Can view session',	5,	'view_session'),
(21,	'Can add user',	6,	'add_databaseuser'),
(22,	'Can change user',	6,	'change_databaseuser'),
(23,	'Can delete user',	6,	'delete_databaseuser'),
(24,	'Can view user',	6,	'view_databaseuser');

DROP TABLE IF EXISTS `csv_mapping`;
CREATE TABLE `csv_mapping` (
  `sn` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `tabletext` varchar(250) DEFAULT NULL,
  `plaintext` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`sn`),
  UNIQUE KEY `sn` (`sn`),
  UNIQUE KEY `tabletext` (`tabletext`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `csv_mapping` (`sn`, `tabletext`, `plaintext`) VALUES
(1,	'coyName',	'Company Name'),
(2,	'coyRegNo',	'Company Registration Number'),
(3,	'toEmail',	'To Emails'),
(4,	'ccEmail',	'CC Emails'),
(5,	'bccEmail',	'BCC Emails'),
(6,	'addresseeName',	'Address To'),
(7,	'fin_endMonth',	'FY End Month'),
(8,	'fin_endYear',	'FY End Year'),
(9,	'AGM_next',	'Next AGM Reminder'),
(10,	'AGM_done',	'Current AGM Done?'),
(11,	'GST_req',	'GST Required?'),
(12,	'GST_endMonth',	'GST End Month'),
(13,	'GST_done',	'Current GST Done?'),
(14,	'GST_type',	'GST Type'),
(15,	'GST_next',	'Next GST Reminder'),
(16,	'audit_req',	'Audit Required?'),
(17,	'audit_done',	'Current Audit Done?'),
(18,	'audit_next',	'Next Audit Reminder'),
(19,	'IRAS_done',	'Current Income Tax Done?'),
(20,	'IRAS_next',	'Next IRAS Reminder');


INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(6,	'accounts',	'databaseuser'),
(1,	'admin',	'logentry'),
(3,	'auth',	'group'),
(2,	'auth',	'permission'),
(4,	'contenttypes',	'contenttype'),
(5,	'sessions',	'session');

-- 2019-04-24 00:34:40
