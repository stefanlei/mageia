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

 Date: 12/04/2021 17:14:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_multiple_pk
-- ----------------------------
DROP TABLE IF EXISTS `user_multiple_pk`;
CREATE TABLE `user_multiple_pk` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `age` int DEFAULT NULL,
  PRIMARY KEY (`id`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of user_multiple_pk
-- ----------------------------
BEGIN;
INSERT INTO `user_multiple_pk` VALUES (1, 'stefan', 19);
INSERT INTO `user_multiple_pk` VALUES (2, 'tom', 20);
INSERT INTO `user_multiple_pk` VALUES (3, 'delete_user', 21);
INSERT INTO `user_multiple_pk` VALUES (4, 'delete_user', 24);
INSERT INTO `user_multiple_pk` VALUES (5, 'merge_user', 24);
INSERT INTO `user_multiple_pk` VALUES (6, 'merge_user', 24);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
