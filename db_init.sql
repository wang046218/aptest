create database apitest;
use apitest;

CREATE TABLE `role_user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL DEFAULT '' COMMENT '姓名',
  `email` varchar(30) NOT NULL DEFAULT '' COMMENT '邮箱',
  `is_admin` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否是超级管理员 1表示是 0 表示不是',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1：有效 0：无效',
  `updated_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '插入时间',
  PRIMARY KEY (`id`),
  KEY `idx_email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='用户表';

CREATE TABLE `role_role` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '角色名称',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1：有效 0：无效',
  `updated_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '插入时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色表';

CREATE TABLE `role_userrole` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL DEFAULT '0' COMMENT '用户id',
  `role_id` int(11) NOT NULL DEFAULT '0' COMMENT '角色ID',
  `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '插入时间',
  PRIMARY KEY (`id`),
  KEY `idx_uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户角色表';

CREATE TABLE `role_access` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL DEFAULT '' COMMENT '权限名称',
  `urls` varchar(1000) NOT NULL DEFAULT '' COMMENT 'url',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1：有效 0：无效',
  `updated_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '插入时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='权限详情表';

CREATE TABLE `role_roleaccess` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL DEFAULT '0' COMMENT '角色id',
  `access_id` int(11) NOT NULL DEFAULT '0' COMMENT '权限id',
  `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '插入时间',
  PRIMARY KEY (`id`),
  KEY `idx_role_id` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色权限表';


CREATE TABLE `role_blog` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL DEFAULT ' ' COMMENT 'title',
  `author_id` int(11) NOT NULL DEFAULT '0' COMMENT 'author_user',
  `created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT 'time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色权限表';


INSERT INTO `role_user` (`id`, `name`, `email`, `is_admin`, `status`, `updated_time`, `created_time`)
VALUES(1, 'admin', 'test@zjwang.com', 1, 1, '2018-4-27 13:36:30', '2018-4-27 13:36:30');

INSERT INTO `role_user` (`id`, `name`, `email`, `is_admin`, `status`, `updated_time`, `created_time`)
VALUES(2, 'random1', 'test@zjwang.com', 0, 1, '2018-4-27 13:36:30', '2018-4-27 13:36:30');

INSERT INTO `role_user` (`id`, `name`, `email`, `is_admin`, `status`, `updated_time`, `created_time`)
VALUES(3, 'random2', 'test@zjwang.com', 0, 1, '2018-4-27 13:36:30', '2018-4-27 13:36:30');

INSERT INTO `role_role` (`id`, `name`, `status`, `updated_time`, `created_time`)
VALUES(1, 'admin', 1, '2018-4-27 13:36:30', '2018-4-27 13:36:30');

INSERT INTO `role_role` (`id`, `name`, `status`, `updated_time`, `created_time`)
VALUES(2, 'other', 1, '2018-4-27 13:36:30', '2018-4-27 13:36:30');

INSERT INTO `role_userrole` (`id`, `uid`, `role_id`, `created_time`)
VALUES(1, 1, 1, '2018-4-27 13:36:30');

INSERT INTO `role_userrole` (`id`, `uid`, `role_id`, `created_time`)
VALUES(2, 2, 2, '2018-4-27 13:36:30');

INSERT INTO `role_userrole` (`id`, `uid`, `role_id`, `created_time`)
VALUES(3, 3, 2, '2018-4-27 13:36:30');

INSERT INTO `role_access` (`id`, `title`, `urls`, `status`, `updated_time`, `created_time`)
VALUES(1, '', '/api/blogs/', 1, '2018-04-27 13:36:30', '2018-04-27 13:36:30');


INSERT INTO `role_roleaccess` (`id`, `role_id`, `access_id`, `created_time`)
VALUES(1, 1, 1, '2018-04-27 13:36:30');
INSERT INTO `role_roleaccess` (`id`, `role_id`, `access_id`, `created_time`)
VALUES(2, 2, 1, '2018-04-27 13:36:30');
