-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: konferencia
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `cikkek`
--

DROP TABLE IF EXISTS `cikkek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cikkek` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cikk_cim` varchar(255) COLLATE utf8_hungarian_ci NOT NULL,
  `szerzo_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `szerzo_id` (`szerzo_id`),
  CONSTRAINT `cikkek_ibfk_1` FOREIGN KEY (`szerzo_id`) REFERENCES `felhasznalok` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_hungarian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cikkek`
--

LOCK TABLES `cikkek` WRITE;
/*!40000 ALTER TABLE `cikkek` DISABLE KEYS */;
INSERT INTO `cikkek` VALUES (1,'Cikk 1',1),(2,'Cikk 2',2),(3,'Cikk 3',3),(4,'Cikk 4',4),(5,'Cikk 5',5),(6,'Cikk 6',6),(7,'Cikk 7',7),(8,'Cikk 8',8),(9,'Cikk 9',9),(10,'Cikk 10',10),(11,'Cikk 11',11),(12,'Cikk 12',12),(13,'Cikk 13',13),(14,'Cikk 14',14),(15,'Cikk 15',15),(16,'Cikk 16',16),(17,'Cikk 17',17),(18,'Cikk 18',18),(19,'Cikk 19',19),(20,'Cikk 20',20),(21,'Cikk 21',21),(22,'Cikk 22',22),(23,'Cikk 23',23),(24,'Cikk 24',24),(25,'Cikk 25',25),(26,'Cikk 26',26),(27,'Cikk 27',27),(28,'Cikk 28',28),(29,'Cikk 29',29),(30,'Cikk 30',30),(31,'Cikk 31',31),(32,'Cikk 32',32),(33,'Cikk 33',33),(34,'Cikk 34',34),(35,'Cikk 35',35),(36,'Cikk 36',36),(37,'Cikk 37',37),(38,'Cikk 38',38),(39,'Cikk 39',39),(40,'Cikk 40',40),(41,'Cikk 41',41),(42,'Cikk 42',42),(43,'Cikk 43',43),(44,'Cikk 44',44),(45,'Cikk 45',45),(46,'Cikk 46',46),(47,'Cikk 47',47),(48,'Cikk 48',48),(49,'Cikk 49',49),(50,'Cikk 50',50),(53,'TesztCikkCím',3),(55,'TesztCikk',4),(61,'TesztCikkCimem123',12),(62,'TesztCikkUj12',12);
/*!40000 ALTER TABLE `cikkek` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eloadasok`
--

DROP TABLE IF EXISTS `eloadasok`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eloadasok` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cikk_id` int DEFAULT NULL,
  `cikk_cim` varchar(255) COLLATE utf8_hungarian_ci NOT NULL,
  `szekcio_id` int DEFAULT NULL,
  `kezdes_idopont` datetime NOT NULL,
  `eloado_nev` varchar(255) COLLATE utf8_hungarian_ci NOT NULL,
  `eloado_id` int DEFAULT NULL,
  `eloadas_hossz` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cikk_id` (`cikk_id`),
  KEY `szekcio_id` (`szekcio_id`),
  KEY `eloado_id` (`eloado_id`),
  CONSTRAINT `eloadasok_ibfk_1` FOREIGN KEY (`cikk_id`) REFERENCES `cikkek` (`id`),
  CONSTRAINT `eloadasok_ibfk_2` FOREIGN KEY (`szekcio_id`) REFERENCES `szekciok` (`id`),
  CONSTRAINT `eloadasok_ibfk_3` FOREIGN KEY (`eloado_id`) REFERENCES `felhasznalok` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_hungarian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eloadasok`
--

LOCK TABLES `eloadasok` WRITE;
/*!40000 ALTER TABLE `eloadasok` DISABLE KEYS */;
INSERT INTO `eloadasok` VALUES (52,1,'Cikk 1',1,'2023-11-01 10:00:00','Eloado 1',1,30),(53,2,'Cikk 2',1,'2023-11-01 11:30:00','Eloado 2',2,45),(54,3,'Cikk 3',2,'2023-11-01 14:00:00','Eloado 3',3,40),(55,4,'Cikk 4',2,'2023-11-01 15:30:00','Eloado 4',4,25),(56,5,'Cikk 5',3,'2023-11-01 16:00:00','Eloado 5',5,60),(57,6,'Cikk 6',3,'2023-11-01 17:30:00','Eloado 6',6,35),(58,7,'Cikk 7',4,'2023-11-01 09:00:00','Eloado 7',7,50),(59,8,'Cikk 8',4,'2023-11-01 10:30:00','Eloado 8',8,30),(60,9,'Cikk 9',5,'2023-11-01 12:00:00','Eloado 9',9,40),(61,10,'Cikk 10',5,'2023-11-01 13:30:00','Eloado 10',10,55),(62,11,'Cikk 11',1,'2023-11-02 10:00:00','Eloado 11',11,20),(63,12,'Cikk 12',1,'2023-11-02 11:30:00','Eloado 12',12,30),(64,13,'Cikk 13',2,'2023-11-02 14:00:00','Eloado 13',13,45),(65,14,'Cikk 14',2,'2023-11-02 15:30:00','Eloado 14',14,40),(66,15,'Cikk 15',3,'2023-11-02 16:00:00','Eloado 15',15,35),(67,16,'Cikk 16',3,'2023-11-02 17:30:00','Eloado 16',16,50),(68,17,'Cikk 17',4,'2023-11-02 09:00:00','Eloado 17',17,25),(69,18,'Cikk 18',4,'2023-11-02 10:30:00','Eloado 18',18,60),(70,19,'Cikk 19',5,'2023-11-02 12:00:00','Eloado 19',19,30),(71,20,'Cikk 20',5,'2023-11-02 13:30:00','Eloado 20',20,40),(72,21,'Cikk 21',10,'2023-11-03 16:30:00','Eloado 21',21,45),(73,22,'Cikk 22',11,'2023-11-03 18:00:00','Eloado 22',22,30),(74,23,'Cikk 23',11,'2023-11-03 20:30:00','Eloado 23',23,60),(75,24,'Cikk 24',12,'2023-11-04 10:00:00','Eloado 24',24,40),(76,25,'Cikk 25',12,'2023-11-04 11:30:00','Eloado 25',25,25),(77,26,'Cikk 26',13,'2023-11-04 14:00:00','Eloado 26',26,55),(78,27,'Cikk 27',13,'2023-11-04 15:30:00','Eloado 27',27,20),(79,28,'Cikk 28',14,'2023-11-04 17:00:00','Eloado 28',28,30),(80,29,'Cikk 29',14,'2023-11-04 18:30:00','Eloado 29',29,45),(81,30,'Cikk 30',15,'2023-11-05 09:00:00','Eloado 30',30,35),(82,31,'Cikk 31',15,'2023-11-05 10:30:00','Eloado 31',31,50),(83,32,'Cikk 32',16,'2023-11-05 12:00:00','Eloado 32',32,25),(84,33,'Cikk 33',16,'2023-11-05 13:30:00','Eloado 33',33,60),(85,34,'Cikk 34',17,'2023-11-05 15:00:00','Eloado 34',34,30),(86,35,'Cikk 35',17,'2023-11-05 16:30:00','Eloado 35',35,40),(87,36,'Cikk 36',18,'2023-11-06 10:00:00','Eloado 36',36,55),(88,37,'Cikk 37',18,'2023-11-06 11:30:00','Eloado 37',37,20),(89,38,'Cikk 38',19,'2023-11-06 14:00:00','Eloado 38',38,45),(90,39,'Cikk 39',19,'2023-11-06 15:30:00','Eloado 39',39,30),(91,40,'Cikk 40',20,'2023-11-06 17:00:00','Eloado 40',40,60),(92,41,'Cikk 41',21,'2023-11-07 10:00:00','Eloado 41',41,30),(93,42,'Cikk 42',21,'2023-11-07 11:30:00','Eloado 42',42,45),(94,43,'Cikk 43',22,'2023-11-07 14:00:00','Eloado 43',43,40),(95,44,'Cikk 44',22,'2023-11-07 15:30:00','Eloado 44',44,25),(96,45,'Cikk 45',23,'2023-11-07 16:00:00','Eloado 45',45,60),(97,46,'Cikk 46',23,'2023-11-07 17:30:00','Eloado 46',46,35),(98,47,'Cikk 47',24,'2023-11-08 09:00:00','Eloado 47',47,50),(99,48,'Cikk 48',24,'2023-11-08 10:30:00','Eloado 48',48,30),(100,49,'Cikk 49',25,'2023-11-08 12:00:00','Eloado 49',49,40),(101,50,'Cikk 50',25,'2023-11-08 13:30:00','Eloado 50',50,55);
/*!40000 ALTER TABLE `eloadasok` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `felhasznalok`
--

DROP TABLE IF EXISTS `felhasznalok`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `felhasznalok` (
  `id` int NOT NULL AUTO_INCREMENT,
  `felhasznalonev` varchar(255) COLLATE utf8_hungarian_ci NOT NULL DEFAULT 'alapertelmezett_nev',
  `elotag` varchar(255) COLLATE utf8_hungarian_ci DEFAULT NULL,
  `nev` varchar(255) COLLATE utf8_hungarian_ci NOT NULL,
  `szerepkor` varchar(255) COLLATE utf8_hungarian_ci NOT NULL DEFAULT 'szerző',
  `email` varchar(255) COLLATE utf8_hungarian_ci DEFAULT NULL,
  `intezmeny` varchar(255) COLLATE utf8_hungarian_ci DEFAULT NULL,
  `hashed_jelszo` varchar(255) COLLATE utf8_hungarian_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_hungarian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `felhasznalok`
--

LOCK TABLES `felhasznalok` WRITE;
/*!40000 ALTER TABLE `felhasznalok` DISABLE KEYS */;
INSERT INTO `felhasznalok` VALUES (1,'user1','Dr.','John Doe','szerző','user1@example.com','Intézmény 1','0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e'),(2,'user2',NULL,'Jane Smith','szerző','user2@example.com','Intézmény 2','6cf615d5bcaac778352a8f1f3360d23f02f34ec182e259897fd6ce485d7870d4'),(3,'user3','Dr.','Michael Brown','szerző','user3@example.com','Intézmény 3','5906ac361a137e2d286465cd6588ebb5ac3f5ae955001100bc41577c3d751764'),(4,'user4',NULL,'Sarah Johnson','szerző','user4@example.com','Intézmény 4','b97873a40f73abedd8d685a7cd5e5f85e4a9cfb83eac26886640a0813850122b'),(5,'user5','Prof.','Emily Wilson','adminisztrátor','user5@example.com','Intézmény 5','8b2c86ea9cf2ea4eb517fd1e06b74f399e7fec0fef92e3b482a6cf2e2b092023'),(6,'user6','Dr.','Tell Vilmos','szerző','user6@example.com','Intézmény 6','598a1a400c1dfdf36974e69d7e1bc98593f2e15015eed8e9b7e47a83b31693d5'),(7,'user7',NULL,'Olivia Lee','szerző','user7@example.com','Intézmény 7','5860836e8f13fc9837539a597d4086bfc0299e54ad92148d54538b5c3feefb7c'),(8,'user8','Prof.','David Miller','adminisztrátor','user8@example.com','Intézmény 8','57f3ebab63f156fd8f776ba645a55d96360a15eeffc8b0e4afe4c05fa88219aa'),(9,'user9','Dr.','Sophia Wilson','szerző','user9@example.com','Intézmény 9','9323dd6786ebcbf3ac87357cc78ba1abfda6cf5e55cd01097b90d4a286cac90e'),(10,'user10',NULL,'Ethan Anderson','szerző','user10@example.com','Intézmény 10','aa4a9ea03fcac15b5fc63c949ac34e7b0fd17906716ac3b8e58c599cdc5a52f0'),(11,'user11','Prof.','Isabella Taylor','adminisztrátor','user11@example.com','Intézmény 11','53d453b0c08b6b38ae91515dc88d25fbecdd1d6001f022419629df844f8ba433'),(12,'user12','Dr.','James Martinez','szerző','user12@example.com','Intézmény 12','b3d17ebbe4f2b75d27b6309cfaae1487b667301a73951e7d523a039cd2dfe110'),(13,'user13',NULL,'Mia Johnson','szerző','user13@example.com','Intézmény 13','48caafb68583936afd0d78a7bfd7046d2492fad94f3c485915f74bb60128620d'),(14,'user14','Prof.','Benjamin Wilson','adminisztrátor','user14@example.com','Intézmény 14','c6863e1db9b396ed31a36988639513a1c73a065fab83681f4b77adb648fac3d6'),(15,'user15','Dr.','Chloe Davis','szerző','user15@example.com','Intézmény 15','c63c2d34ebe84032ad47b87af194fedd17dacf8222b2ea7f4ebfee3dd6db2dfb'),(16,'user16',NULL,'Daniel Smith','szerző','user16@example.com','Intézmény 16','17a3379984b560dc311bb921b7a46b28aa5cb495667382f887a44a7fdbca7a7a'),(17,'user17','Prof.','Ava Brown','adminisztrátor','user17@example.com','Intézmény 17','69bfb918de05145fba9dcee9688dfb23f6115845885e48fa39945eebb99d8527'),(18,'user18','Dr.','Henry Anderson','szerző','user18@example.com','Intézmény 18','d2042d75a67922194c045da2600e1c92ff6d87e8fb6e0208606665f2d1dfa892'),(19,'user19',NULL,'Liam Martinez','szerző','user19@example.com','Intézmény 19','5790ac3d0b8ae8afc72c2c6fb97654f2b73651c328de0a3b74854ade562dd17a'),(20,'user20','Prof.','Sophia Taylor','adminisztrátor','user20@example.com','Intézmény 20','7535d8f2d8c35d958995610f971287288ab5e8c82a3c4fdc2b6fb5d757a5b9f8'),(21,'user21','Dr.','Ella Anderson','adminisztrátor','user21@example.com','Intézmény 21','91a9ef3563010ea1af916083f9fb03a117d4d0d2a697f82368da1f737629f717'),(22,'user22',NULL,'Jackson Smith','szerző','user22@example.com','Intézmény 22','d23c1038532dc71d0a60a7fb3d330d7606b7520e9e5ee0ddcdb27ee1bd5bc0cd'),(23,'user23','Prof.','Oliver Davis','szerző','user23@example.com','Intézmény 23','8b807aa0505a00b3ef49e26a2ade8e31fcd6c700d1a3aeee971b49d73da8e8ff'),(24,'user24','Dr.','Lily Taylor','adminisztrátor','user24@example.com','Intézmény 24','fc8a9296208a0b281f84690423c5d77785e493f435e6292cc322840f543729d3'),(25,'user25','Dr.','Noah Wilson','szerző','user25@example.com','Intézmény 25','0b544d6d8da1d1af25318e97e0ac5f6bc70bba49919463dc0074ede01a49d381'),(26,'user26',NULL,'Sophia Brown','szerző','user26@example.com','Intézmény 26','869f2a98b0e3a6ea928ff0542330ea3c1e0ff8591801693350f1fc3f1e57e4c5'),(27,'user27','Prof.','Lucas Johnson','adminisztrátor','user27@example.com','Intézmény 27','9c7568513b9c85e73f3650c8b00e3259501096ccee9d3dbdae6ff5e84aabe3af'),(28,'user28','Dr.','Emma Vagyok','szerző','user28@example.com','Intézmény 28','6f5ea1c4acc7a563ea8cb3381a55f0183a2394d679ebb7db8312e047bbf87e0d'),(29,'user29',NULL,'Rodriguez Alejandro','szerző','user29@example.com','Intézmény 29','48a94846b2a7386432b90ad13bcf9c66f1efdd3a97e0e14968c262c412fe22c8'),(30,'user30','Prof.','Chuckle Nugget','adminisztrátor','user30@example.com','Intézmény 30','7c682dea8e934e04343374e3d25cd51edce9cbeb47f7034296052cb5cd6bed84'),(31,'user31','Dr.','Carter Anderson','szerző','user31@example.com','Intézmény 31','a4239ae1725466d26621f102d58c1541c84ff1142f4341c7b66be92e32396d45'),(32,'user32',NULL,'Liam Smith','szerző','user32@example.com','Intézmény 32','078aa4687601ab09b1f7581014674b3bf1a3aa68b12c346d01024f1f5206f94b'),(33,'user33','Prof.','Evelyn Taylor','adminisztrátor','user33@example.com','Intézmény 33','ee13b7d4c8c0595dcabf6016290d65d8a50163569368db690595d5acaa5a168b'),(34,'user34','Dr.','Henry Johnson','szerző','user34@example.com','Intézmény 34','72f1ffa2d7a9c9d60c2369fffce54372eea054d567c77f8a518f4f4c06b3856a'),(35,'user35',NULL,'Charlotte Brown','szerző','user35@example.com','Intézmény 35','5bd40f88c4a6b2c20256389878ec2b59515ca478eb3eb0f3673663273bcb639b'),(36,'user36','Prof.','William Davis','adminisztrátor','user36@example.com','Intézmény 36','9777509ca199ac591368c5cfa9ef92b4879ff99098b7e34865172a5ea983542e'),(37,'user37','Dr.','Chloe Wilson','szerző','user37@example.com','Intézmény 37','ca02485287fd4f05de9540613f8ba982e99080b66f8452024cb4c4cc3de7042e'),(38,'user38',NULL,'James Smith','szerző','user38@example.com','Intézmény 38','014d020993865f93b80ec587e171554db5b45a1a46a9101510de52e148aa184f'),(39,'user39','Prof.','Ava Martinez','adminisztrátor','user39@example.com','Intézmény 39','f245ffb6352c8c101b0f9ed1187104f11e0a64622cc5da7082aef963dea5a83f'),(40,'user40','Dr.','Mia Davis','szerző','user40@example.com','Intézmény 40','825e233a9d192f81d3f6780cb8e181af518054a8d9c83381882e573eed014df2'),(41,'user41',NULL,'Noah Taylor','szerző','user41@example.com','Intézmény 41','a13b6ab0bb26b7d8bf31628b3b524efade4ac5b02712a95210c0abda5148ec85'),(42,'user42','Prof.','Ella Brown','adminisztrátor','user42@example.com','Intézmény 42','fe404abb6785bd17ac4c937c2837d3ad6d6ac1ed17e099a89a9c5e18d1e936fe'),(43,'user43','Dr.','Oliver Smith','szerző','user43@example.com','Intézmény 43','fe4597a9d0a16c51ab5c8224dae83f170b69cede0f1a7f40f447f163dcbf9295'),(44,'user44',NULL,'Sophia Johnson','szerző','user44@example.com','Intézmény 44','f9d07093d0de736c8881640c3e55714bebd5faf5d6ebbfb41e486e1660c8fc0e'),(45,'user45','Prof.','Lucas Davis','adminisztrátor','user45@example.com','Intézmény 45','0528d31561cee040ee92e2857a2d71a373605b91da87d09ae5359a0689c45e6c'),(46,'user46','Dr.','Emma Lee','szerző','user46@example.com','Intézmény 46','f7944ecca058c63c386de56353cddf278c98f3143bd4a00bb0b2015adb69ed39'),(47,'user47',NULL,'Mason Martinez','szerző','user47@example.com','Intézmény 47','7ff9543ea5b226aeb9dcbf13672c32e62623e70edc4177512b169ec4e39846ea'),(48,'user48','Prof.','Ava Davis','adminisztrátor','user48@example.com','Intézmény 48','172e362eecb6dff98dbeb4a7c42367109c1b288ecf45ff271fb79acd352ba8f9'),(49,'user49','Dr.','Carter Crab','szerző','user49@example.com','Intézmény 49','3cd00931dd1de5d07fcafb463ba5c4d95d31dca8a35480cac4a2beb771cb90df'),(50,'user50','Prof.','Alice Johnson','adminisztrátor','user50@example.com','Intézmény 50','b5d966eb0c2845953fab12c306c906a3561162262115c3b6fc19aead8d142157'),(51,'alapertelmezett_nev',NULL,'','szerző',NULL,NULL,'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),(52,'alapertelmezett_nev',NULL,'TesztRegisztraltUser','szerző',NULL,NULL,'252b88e3dee3e9ba21f2013758321269db891d9af95ea09f12ceafbbc3e76a43'),(53,'TesztRegElek','Dr.','Teszt RegElek','szerző','tesztmail@spam.com','TesztIntezmeny','da79250286f9dd54cb243147b7d4a92dd6891248801c2ad92fb16108374bf1f9');
/*!40000 ALTER TABLE `felhasznalok` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `szekciok`
--

DROP TABLE IF EXISTS `szekciok`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `szekciok` (
  `id` int NOT NULL AUTO_INCREMENT,
  `szekcio_nev` varchar(255) COLLATE utf8_hungarian_ci NOT NULL,
  `kezdes_idopont` datetime NOT NULL,
  `levezeto_elnok_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `levezeto_elnok_id` (`levezeto_elnok_id`),
  CONSTRAINT `szekciok_ibfk_1` FOREIGN KEY (`levezeto_elnok_id`) REFERENCES `felhasznalok` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_hungarian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `szekciok`
--

LOCK TABLES `szekciok` WRITE;
/*!40000 ALTER TABLE `szekciok` DISABLE KEYS */;
INSERT INTO `szekciok` VALUES (1,'Szekció 1','2023-11-01 10:00:00',1),(2,'Szekció 2','2023-11-01 14:00:00',2),(3,'Szekció 3','2023-11-02 09:00:00',3),(4,'Szekció 4','2023-11-02 13:00:00',4),(5,'Szekció 5','2023-11-03 11:00:00',5),(6,'Szekció 6','2023-11-03 15:00:00',6),(7,'Szekció 7','2023-11-04 10:00:00',7),(8,'Szekció 8','2023-11-04 14:00:00',8),(9,'Szekció 9','2023-11-05 09:00:00',9),(10,'Szekció 10','2023-11-05 13:00:00',10),(11,'Szekció 11','2023-11-06 11:00:00',11),(12,'Szekció 12','2023-11-06 15:00:00',12),(13,'Szekció 13','2023-11-07 10:00:00',13),(14,'Szekció 14','2023-11-07 14:00:00',14),(15,'Szekció 15','2023-11-08 09:00:00',15),(16,'Szekció 16','2023-11-08 13:00:00',16),(17,'Szekció 17','2023-11-09 11:00:00',17),(18,'Szekció 18','2023-11-09 15:00:00',18),(19,'Szekció 19','2023-11-10 10:00:00',19),(20,'Szekció 20','2023-11-10 14:00:00',20),(21,'Szekció 21','2023-11-11 09:00:00',21),(22,'Szekció 22','2023-11-11 13:00:00',22),(23,'Szekció 23','2023-11-12 11:00:00',23),(24,'Szekció 24','2023-11-12 15:00:00',24),(25,'Szekció 25','2023-11-13 10:00:00',25),(26,'Szekció 26','2023-11-13 14:00:00',26),(27,'Szekció 27','2023-11-14 09:00:00',27),(28,'Szekció 28','2023-11-14 13:00:00',28),(29,'Szekció 29','2023-11-15 11:00:00',29),(30,'Szekció 30','2023-11-15 15:00:00',30),(31,'Szekció 31','2023-11-16 10:00:00',31),(32,'Szekció 32','2023-11-16 14:00:00',32),(33,'Szekció 33','2023-11-17 09:00:00',33),(34,'Szekció 34','2023-11-17 13:00:00',34),(35,'Szekció 35','2023-11-18 11:00:00',35),(36,'Szekció 36','2023-11-18 15:00:00',36),(37,'Szekció 37','2023-11-19 10:00:00',37),(38,'Szekció 38','2023-11-19 14:00:00',38),(39,'Szekció 39','2023-11-20 09:00:00',39),(40,'Szekció 40','2023-11-20 13:00:00',40),(41,'Szekció 41','2023-11-21 11:00:00',41),(42,'Szekció 42','2023-11-21 15:00:00',42),(43,'Szekció 43','2023-11-22 10:00:00',43),(44,'Szekció 44','2023-11-22 14:00:00',44),(45,'Szekció 45','2023-11-23 09:00:00',45),(46,'Szekció 46','2023-11-23 13:00:00',46),(47,'Szekció 47','2023-11-24 11:00:00',47),(48,'Szekció 48','2023-11-24 15:00:00',48),(49,'Szekció 49','2023-11-25 10:00:00',49),(50,'Szekció 50','2023-11-25 14:00:00',50);
/*!40000 ALTER TABLE `szekciok` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed
