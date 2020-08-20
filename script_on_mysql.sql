CREATE DATABASE AI_ROM IF NOT EXISTS AI_ROM DEFAULT CHARSET utf8 COLLATE utf8_general_ci 
#创建数据库并设定编码集为utf8


use mysql;
CREATE USER 'developer'@'%' IDENTIFIED BY '3rhva5'

GRANT SELECT ,INSERT,UPDATE,CREATE ON ai_rom.* TO 'developer'@'%';

USE ai_rom;
CREATE TABLE IF NOT EXISTS `user_info`(
   `user_id` INT UNSIGNED AUTO_INCREMENT,
   `user_account` VARCHAR(24) NOT NULL,
   `user_pwd` VARCHAR(100) NOT NULL,
   `user_class` INT NOT NULL,
   `register_time` DATE,
   PRIMARY KEY ( `user_id` ),
	 UNIQUE(`user_account`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

USE ai_rom;
CREATE TABLE IF NOT EXISTS `user_operation_log`(
   `operation_id` INT UNSIGNED AUTO_INCREMENT,
   `user_id` INT NOT NULL,
   `module_id` INT NOT NULL,
   `task_id` INT NOT NULL,
   `operate_time` DATETIME,
   PRIMARY KEY ( `operation_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `module_info`(
   `module_id` INT UNSIGNED AUTO_INCREMENT,
   `module_def` VARCHAR(24) NOT NULL,
	  PRIMARY KEY ( `module_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into task_status_info (task_status_id,task_status_def) values (1,'sign');
insert into task_status_info (task_status_id,task_status_def) values (2,'change password');
insert into task_status_info (task_status_id,task_status_def) values (3,'view task result');


USE ai_rom;
CREATE TABLE IF NOT EXISTS `task_info`(
   `task_id` INT UNSIGNED AUTO_INCREMENT,
   `user_id` INT NOT NULL,
   `task_class_id` INT NOT NULL,
   `doctor_id` INT ,
   `create_time` DATE,
   `task_status_id` INT,
   `tmp_file_name` VARCHAR(300),
   PRIMARY KEY ( `task_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


USE ai_rom;
CREATE TABLE IF NOT EXISTS `task_status_info`(
   `task_status_id` INT UNSIGNED AUTO_INCREMENT,
   `task_status_def` VARCHAR(24) NOT NULL,
	  PRIMARY KEY ( `task_status_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into task_status_info (task_status_id,task_status_def) values (1,'to be analyzed');
insert into task_status_info (task_status_id,task_status_def) values (2,'finished');
insert into task_status_info (task_status_id,task_status_def) values (3,'canceled');

USE ai_rom;
CREATE TABLE IF NOT EXISTS `task_class_info`(
   `task_class_id` INT UNSIGNED AUTO_INCREMENT,
   `task_class_def` VARCHAR(24) NOT NULL,
   `result_table_name` VARCHAR(36) NOT NULL,
	  PRIMARY KEY ( `task_class_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into task_class_info (task_class_id,task_class_def,result_table_name) values (1,'拇指桡侧外展测量','shoulder_thumb_result');
insert into task_class_info (task_class_id,task_class_def,result_table_name) values (2,'正面右侧肩关节外展测量','shoulder_thumb_result');

CREATE TABLE IF NOT EXISTS `shoulder_thumb_result`(
   `task_id` INT  NOT NULL,
   `frame` INT NOT NULL,
   `body_part` INT NOT NULL,
   `angle` float(6,2) NOT NULL,
   `cross_point` VARCHAR(100) NOT NULL,
   `line1` VARCHAR(400) NOT NULL,
   `line2` VARCHAR(400) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


SELECT `AUTO_INCREMENT`
FROM  INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'ai_rom'
AND   TABLE_NAME   = 'task_class_info';