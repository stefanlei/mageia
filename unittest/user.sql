/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : localhost:3306
 Source Schema         : test

 Target Server Type    : MySQL
 Target Server Version : 80023
 File Encoding         : 65001

 Date: 12/04/2021 17:14:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `addr` varchar(255) DEFAULT NULL,
  `birthday` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES (1, 'Jack', 19, 'sz', '2021-04-12 17:14:33.231835');
INSERT INTO `user` VALUES (2, 'Stefan', 20, 'nc', '2021-04-12 17:14:33.236892');
INSERT INTO `user` VALUES (3, 'Tom', 21, 'wh', '2021-04-12 17:14:33.241191');
INSERT INTO `user` VALUES (4, 'delete_user', 21, 'nc', '2021-04-12 17:14:33.245420');
INSERT INTO `user` VALUES (5, 'merge_user', 21, 'bj', '2021-04-12 17:14:33.249597');
INSERT INTO `user` VALUES (6, 'merge_many_user', 21, 'sh', '2021-04-12 17:14:33.253810');
INSERT INTO `user` VALUES (7, 'merge_many_user', 21, 'sh', '2021-04-12 17:14:33.257874');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
