-- MySQL dump 10.13  Distrib 8.0.25, for Linux (x86_64)
--
-- Host: 0710160.mysql.pythonanywhere-services.com    Database: 0710160$ggicn
-- ------------------------------------------------------
-- Server version	5.7.34-log

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('d3718a1c30bd');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `article`
--

DROP TABLE IF EXISTS `article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL,
  `subtitle` varchar(256) DEFAULT NULL,
  `body` text NOT NULL,
  `date` varchar(256) DEFAULT NULL,
  `img_name` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article`
--

LOCK TABLES `article` WRITE;
/*!40000 ALTER TABLE `article` DISABLE KEYS */;
INSERT INTO `article` VALUES (1,'Building Connections Through Kai','','<p>Greater Green Island Community Network believe it is more important than ever to be connected with neighbours. The &ldquo;Reach Out, Look Out and Help Out&rdquo; messaging from&nbsp;Neighbourhood Support highlights what GGICN want to see happening in Greater Green Island as we learn what the Traffic Light System means for life going forward.&nbsp;</p>\n\n<p><br>\nWith the recent move into Red, it is a timely reminder to check in with your neighbours and others on your street to make sure they are okay. The more people who do this the higher the chance we do not miss or overlook someone who needs support. We have vulnerable people in the community who might need someone to drop off shopping for them at this time. It is great to hear this is already happening in some areas of Greater Green Island.&nbsp;</p>\n\n<p><br>\nIf you are worried about yourself or someone else in your community please get in touch and we can connect you or them with someone who can help.&nbsp;If you would like to volunteer to drop off food to your neighbours, please get in touch. GGICN are in the process of setting up an informal food delivery plan.</p>\n\n<p>Neighbours Day Aotearoa 2022, which runs from 18th - 27th March, is all about Kai Connections, a great excuse to connect with neighbours, whether you know everyone or no one, over food. In 2022 to keep gatherings safe and small we want to help you plan Neighbours Day for your neighbourhood. We would love see streets across Greater Green Island have small get-togethers to build relationships and celebrate their strength and resilience.&nbsp;</p>\n\n<p>Some ideas that might interest your street include: having a Food Truck park up for an evening, a picnic with lawn games, a neighbourhood recipe swap.</p>\n\n<p><br>\nGGICN can help you plan, access funding and help you align with the Traffic Light System rules. If your street or neighbourhood would like to hold a get together this year, you or someone you know needs support during Red or you would like to help support vulnerable neighbours please get in touch with the GGICN team at <a href=\"mailto:events@greatergreenisland.nz\">events@greatergreenisland.nz</a> or call 0212286934.</p>\n','01-02-2022','informer8.png'),(2,'12 Days of Christmas a Huge Success','','<p>The Christmas spirit took on an element of mystery last year, when the Greater Green Island team planned a successful treasure hunt over the 12 days before Christmas.</p>\n\n<p>Thirteen letters were hidden in 12 places around Greater Green Island, between Emerson Street Playground in Concord to the Brighton Domain.&nbsp; With daily clues released on Facebook, Instagram and our website, the community response was fantastic.</p>\n\n<p>Community worker Ben McKenzie said the purpose of the &lsquo;12 Days of Christmas&rsquo; activity was to provide a no cost family friendly event that could be done in the lead up to Christmas.</p>\n\n<p>&ldquo;It was exciting to receive all the photos of families who had the letters. We were stoked about all the photos we received of families with the letters, we are satisfied we facilitated an event that brought families closer together while exploring.&quot;</p>\n\n<p>There were prizes for the first to send a photo of each letter, spot prizes for guesses of the secret phrase and for those who photographed all 12 letters.</p>\n\n<p>With the Green Island Christmas Market cancelled due to Covid, GGICN wanted to keep positivity alight.</p>\n\n<p>&ldquo;We understand the necessity of being creative in the way we structure events while we live with Covid-19. The 12 Days of Christmas was a great solution to offering a community wide event while protecting the health of the community,&rdquo; Mr McKenzie said.</p>\n\n<p>The activity was also a way to draw awareness to some of the amazing spots in the Greater Green Island community. Many of the letters were in parks, but some were placed in areas of community initiative such as the Green Island Community Garden and the Ocean View Mosaic Wall.</p>\n\n<p>Once a letter&rsquo;s clue was revealed, it was in place until Christmas.</p>\n\n<p>Mr McKenzie said the event was an opportunity for GGI locals to get out of their suburb and discover hidden gems in other parts of the Greater Green Island Community.</p>\n\n<p>&ldquo;The feedback from families who joined in was very positive. It was a hit with children and adults alike. People liked the challenge of solving the clues to figure out where they needed to head to find the letters,&rdquo; he said.</p>\n\n<p>Congratulations to everyone who got a prize over the 12 days. We are thankful for the generous donations from Royal Albatross and Fort Taiaroa, Biggies Pizza, Beachlands Speedway, Leap Dunedin, Olveston Historic Home, Dunedin Gasworks Museum and Escape Dunedin that meant we were able to give away close to $500 worth of prizes.</p>\n','01-02-2022','informer9.png'),(3,'Waldronville\'s Delta Drive Walkway to Get a Facelift','','<p>Take a wander down Waldronville&rsquo;s Delta Drive walkway, and it may appear a little drab&mdash;but not for long. Enter the inspiration of community-minded Vianney Santagati?</p>\n\n<p>Ms Santagati who is the colour behind a few mosaic murals in Dunedin, including the mosaic wall in Ocean View&rsquo;s Bennett Path, was approached by a neighbouring resident of the walkway about a possible artwork lining one of the walls. A passionate creative, Ms Santagati agreed, and now with resource consent recently received from the Dunedin City Council, she is looking for some keen community-minded helpers.</p>\n\n<p>Ms Santagati is hoping to attract interest&nbsp; for the project, and will be holding mosaic workshops from March.</p>\n\n<p>&ldquo;People with no experience will be welcome. We&rsquo;ll have some spare tools for them to use and will show them how to do it,&rdquo; Ms Santagati said.</p>\n\n<p>With 20 years of experience in the craft, the Ocean View resident said there were a couple of reasons why she enjoyed the craft.</p>\n\n<p>&ldquo;It&rsquo;s making something out of something that&rsquo;s discarded. You don&rsquo;t have to draw well to do a good mosaic or creative a work of art. You get to know a lot of nice people in the community and it&rsquo;s nice for people to get to know their neighbours.&rdquo;</p>\n\n<p>Ms Santagati said wall projects were a great way to get the community together&nbsp; &ldquo;and to help them feel part of the community&rdquo;.</p>\n\n<p>The theme of the Waldronville mosaic would consist of the surrounding local environment such as the estuary and plane in the local playground, along with street names, Island Park Golf Course and Beachlands Speedway.</p>\n\n<p>The project would cost thousands, and Ms Santagati said she would be applying for grants from the council.</p>\n\n<p>&ldquo;The first stage will be to get things made to put on the walls, and then get the walls cleaned and prep them. There&rsquo;s a few cracks and holes in the walls.</p>\n\n<p>&ldquo;I would hope that by next summer we would have a lot of it done. It would depend on how many people turn up,&rdquo; she said.</p>\n\n<p>The Ocean View Hall will be used on Monday nights for the workshops, from 7 to 9pm, starting March 7th. Vaccination passes required.</p>\n\n<p>For more information, please see advert below or call Vianney on 021 246 0472.</p>\n','01-02-2022','informer10.png');
/*!40000 ALTER TABLE `article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL,
  `subtitle` varchar(256) DEFAULT NULL,
  `body` text NOT NULL,
  `date` varchar(256) DEFAULT NULL,
  `img_name` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,'Test event','This is a subtitle','<p>##TODO: comment SQLlite, uncomment MySQL, Migrate(app, db) and flask_migrate import before publishing (COUNT 4 THINGS)</p>\n','27-01-2022','event1.jpg');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mailing_list`
--

DROP TABLE IF EXISTS `mailing_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mailing_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `email` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mailing_list`
--

LOCK TABLES `mailing_list` WRITE;
/*!40000 ALTER TABLE `mailing_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `mailing_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(256) NOT NULL,
  `password` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','pbkdf2:sha256:260000$pglygJSq$60104b2f944484ca13692f93faa274723c4199c756b1606afea331e08f06e0cd');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-10 21:50:02
