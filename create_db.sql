-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: css2
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cont_check_table`
--

DROP TABLE IF EXISTS `cont_check_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cont_check_table` (
  `elem_id` int NOT NULL AUTO_INCREMENT,
  `cont_name` text,
  `user_id` int DEFAULT NULL,
  `upload_time` date DEFAULT NULL,
  `cont_content` text,
  `backup` text,
  PRIMARY KEY (`elem_id`)
) ENGINE=InnoDB AUTO_INCREMENT=935 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cont_comparison_backup_table`
--

DROP TABLE IF EXISTS `cont_comparison_backup_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cont_comparison_backup_table` (
  `obj_id` int NOT NULL AUTO_INCREMENT COMMENT '元素ID',
  `add_time` datetime DEFAULT NULL COMMENT '添加到数据的时间',
  `request_ip` varchar(100) DEFAULT NULL COMMENT '请求IP',
  `firstDocxID` varchar(500) DEFAULT NULL COMMENT '文档1的ID',
  `secondDocxID` varchar(500) DEFAULT NULL COMMENT '文档2的ID',
  `fileName` text COMMENT '文件名称',
  `firstVersion` varchar(500) DEFAULT NULL COMMENT '文档1的版本',
  `secondVersion` varchar(500) DEFAULT NULL COMMENT '文档2的版本',
  `first_content` text COMMENT '文档1的内容',
  `second_content` text COMMENT '文档2的内容',
  `backup1` text COMMENT '备用1',
  `backup2` text COMMENT '备用2',
  PRIMARY KEY (`obj_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4220 DEFAULT CHARSET=latin1 COMMENT='保存上传的存档';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cont_docx_backup_table`
--

DROP TABLE IF EXISTS `cont_docx_backup_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cont_docx_backup_table` (
  `docx_id` int NOT NULL AUTO_INCREMENT COMMENT '文档ID',
  `add_time` datetime DEFAULT NULL COMMENT '添加到数据的时间',
  `request_ip` varchar(100) DEFAULT NULL COMMENT '请求IP',
  `docx_content` text COMMENT '文档1的内容',
  `backup1` text COMMENT '备用1',
  `backup2` text COMMENT '备用2',
  PRIMARY KEY (`docx_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9971 DEFAULT CHARSET=latin1 COMMENT='对比审核保存的存档';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cont_ext_element_table`
--

DROP TABLE IF EXISTS `cont_ext_element_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cont_ext_element_table` (
  `elem_id` int NOT NULL AUTO_INCREMENT COMMENT '合同要素ID',
  `con_id` int DEFAULT NULL COMMENT '合同ID',
  `elem_name` varchar(500) DEFAULT NULL COMMENT '合同要素名字',
  `elem_key` varchar(500) DEFAULT NULL COMMENT '合同要素关键字',
  `elem_type` varchar(255) DEFAULT NULL COMMENT '合同要素类型',
  `elem_check_re` varchar(500) DEFAULT NULL COMMENT '合同要素正则表达是检查方法',
  `elem_info` text COMMENT '合同要素说明',
  `backup1` text COMMENT '备用字段1',
  `backup2` text COMMENT '备用字段2',
  `backup3` text COMMENT '备用字段3',
  PRIMARY KEY (`elem_id`),
  KEY `cont_element_table_contract_ext_table_cont_id_fk` (`con_id`)
) ENGINE=InnoDB AUTO_INCREMENT=508 DEFAULT CHARSET=utf8mb4 COMMENT='合同要素表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cont_ext_result`
--

DROP TABLE IF EXISTS `cont_ext_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cont_ext_result` (
  `rid` int NOT NULL AUTO_INCREMENT,
  `add_time` datetime DEFAULT NULL,
  `con_id` int DEFAULT NULL COMMENT '合同ID',
  `elem_id` int DEFAULT NULL COMMENT '合同要素ID',
  `context` text COMMENT '合同要素内容',
  `doc_name` text COMMENT '文件名',
  PRIMARY KEY (`rid`),
  UNIQUE KEY `cont_ext_result_rid_uindex` (`rid`),
  KEY `cont_ext_result_cont_element_table_elem_id_fk` (`elem_id`),
  KEY `cont_ext_result_contract_ext_table_cont_id_fk` (`con_id`),
  CONSTRAINT `cont_ext_result_cont_element_table_elem_id_fk` FOREIGN KEY (`elem_id`) REFERENCES `cont_ext_element_table` (`elem_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `cont_ext_result_contract_ext_table_cont_id_fk` FOREIGN KEY (`con_id`) REFERENCES `contract_ext_table` (`cont_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24773 DEFAULT CHARSET=utf8mb4   COMMENT='合同审核结果表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cont_gen_element_table`
--

DROP TABLE IF EXISTS `cont_gen_element_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cont_gen_element_table` (
  `elem_id` int NOT NULL AUTO_INCREMENT COMMENT '合同要素ID',
  `con_id` int DEFAULT NULL COMMENT '合同ID',
  `elem_name` varchar(500) DEFAULT NULL COMMENT '合同要素名字',
  `elem_key` varchar(500) DEFAULT NULL COMMENT '合同要素关键字',
  `elem_type` varchar(255) DEFAULT NULL COMMENT '合同要素类型',
  `elem_check_re` varchar(500) DEFAULT NULL COMMENT '合同要素正则表达是检查方法',
  `elem_info` text COMMENT '合同要素说明',
  `backup1` text COMMENT '备用字段1',
  `backup2` text COMMENT '备用字段2',
  `backup3` text COMMENT '备用字段3',
  PRIMARY KEY (`elem_id`),
  KEY `cont_gen_element_table_contract_gen_table_cont_id_fk` (`con_id`),
  CONSTRAINT `cont_gen_element_table_contract_gen_table_cont_id_fk` FOREIGN KEY (`con_id`) REFERENCES `contract_gen_table` (`cont_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=531 DEFAULT CHARSET=utf8mb4   COMMENT='合同生成表要素表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contract_ext_table`
--

DROP TABLE IF EXISTS `contract_ext_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contract_ext_table` (
  `cont_id` int NOT NULL AUTO_INCREMENT COMMENT '合同ID',
  `cont_category` varchar(500) DEFAULT NULL COMMENT '合同业务',
  `cont_name` text COMMENT '备用字段1',
  `cont_sub_category` varchar(500) DEFAULT NULL COMMENT '合同业务的子业务',
  `cont_info` text COMMENT '该合同的说明',
  `cont_path` text COMMENT '备用字段2',
  `backup3` text COMMENT '备用字段3',
  PRIMARY KEY (`cont_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4   COMMENT='合同审核表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contract_gen_table`
--

DROP TABLE IF EXISTS `contract_gen_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contract_gen_table` (
  `cont_id` int NOT NULL AUTO_INCREMENT COMMENT '合同ID',
  `cont_docx_path` varchar(500) DEFAULT NULL COMMENT '合同模板word文档路径',
  `cont_category` varchar(500) DEFAULT NULL COMMENT '合同业务类别',
  `cont_sub_category` varchar(500) DEFAULT NULL COMMENT '合同业务的子业务',
  `cont_info` text COMMENT '该合同的说明',
  `cont_name` text COMMENT '合同名',
  `backup2` text COMMENT '备用字段2',
  `backup3` text COMMENT '备用字段3',
  PRIMARY KEY (`cont_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4   COMMENT='合同生成表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `docx_table`
--

DROP TABLE IF EXISTS `docx_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `docx_table` (
  `docx_id` int NOT NULL AUTO_INCREMENT,
  `docx_bh` mediumtext,
  `docx_syy` mediumtext,
  `docx_xyrq` mediumtext,
  `docx_xydd` mediumtext,
  `docx_zrf` mediumtext,
  `docx_srf` mediumtext,
  `docx_zwf` mediumtext,
  `docx_zrffzr` mediumtext,
  `docx_srffzr` mediumtext,
  `docx_zwffzr` mediumtext,
  `docx_zrfzs` mediumtext,
  `docx_srfzs` mediumtext,
  `docx_zwfzs` mediumtext,
  `docx_zmbjye` mediumtext,
  `docx_lx` mediumtext,
  `docx_qtzq` mediumtext,
  `docx_ztzq` mediumtext,
  `docx_zrjk` mediumtext,
  `docx_zqje` mediumtext,
  `docx_wyj` mediumtext,
  `docx_jzr` mediumtext,
  `docx_bxze` mediumtext,
  `docx_bjye` mediumtext,
  `docx_qx` mediumtext,
  `docx_khyh` mediumtext,
  `docx_hm` mediumtext,
  `docx_zh` mediumtext,
  `docx_jybzz` mediumtext,
  PRIMARY KEY (`docx_id`)
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8mb4  ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `evaluation`
--

DROP TABLE IF EXISTS `evaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluation` (
  `evaluation_id` int NOT NULL AUTO_INCREMENT,
  `evaluation_CFi` varchar(500) DEFAULT NULL,
  `evaluation_Rfti` varchar(100) DEFAULT NULL,
  `evaluation_ti` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`evaluation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4  ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `flower`
--

DROP TABLE IF EXISTS `flower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flower` (
  `elem_id` int NOT NULL AUTO_INCREMENT,
  `cont_name` text,
  `para_content` text,
  `sim_cont_name` text,
  `user_id` int DEFAULT NULL,
  `upload_time` date DEFAULT NULL,
  `sims_content` text,
  `backup1` text,
  `backup2` text,
  PRIMARY KEY (`elem_id`)
) ENGINE=InnoDB AUTO_INCREMENT=248 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `log_time` datetime DEFAULT NULL,
  `log_loc` varchar(100) DEFAULT NULL,
  `log_ip` varchar(100) DEFAULT NULL,
  `log_brow` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1422 DEFAULT CHARSET=utf8mb4  ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log_user`
--

DROP TABLE IF EXISTS `log_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `user_pass` varchar(100) DEFAULT NULL,
  `user_email` varchar(100) DEFAULT NULL,
  `user_depat` varchar(100) DEFAULT NULL,
  `user_auth` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4  ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sugg`
--

DROP TABLE IF EXISTS `sugg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sugg` (
  `sugg_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `sugg_text` mediumtext,
  PRIMARY KEY (`sugg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `user_pass` varchar(100) DEFAULT NULL,
  `user_email` varchar(100) DEFAULT NULL,
  `user_depat` varchar(100) DEFAULT NULL,
  `user_auth` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_access_log`
--

DROP TABLE IF EXISTS `user_access_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_access_log` (
  `_id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `access_time` datetime DEFAULT NULL COMMENT '访问时间',
  `request_ip` varchar(100) DEFAULT NULL COMMENT '请求IP',
  `route_path` text COMMENT '请求的路由地址',
  `backup1` text COMMENT '备用1',
  `backup2` text COMMENT '备用2',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1615 DEFAULT CHARSET=latin1 COMMENT='用户访问路由的日志';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-17 22:06:10
