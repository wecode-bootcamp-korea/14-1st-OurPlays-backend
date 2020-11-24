INSERT INTO `categories` VALUES (9,'그 외 장소'),(3,'빌라'),(2,'사무실'),(7,'스튜디오'),(4,'아파트'),(5,'옥상'),(1,'원룸'),(6,'주택'),(8,'카페식당'),(10,'펜션');

INSERT INTO `django_content_type` VALUES (1,'contenttypes','contenttype'),(5,'place','category'),(6,'place','inavilablebookingday'),(7,'place','place'),(8,'place','placeimage'),(10,'place','rating'),(9,'place','tag'),(4,'reservation','reservation'),(3,'reservation','reservationstatus'),(2,'sessions','session'),(11,'user','placemark'),(14,'user','signupmotive'),(12,'user','user'),(13,'user','usertag');

INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-11-18 11:23:40.506305'),(2,'contenttypes','0002_remove_content_type_name','2020-11-18 11:23:40.669285'),(3,'place','0001_initial','2020-11-18 11:23:40.969402'),(4,'user','0001_initial','2020-11-18 11:23:41.512403'),(5,'place','0002_auto_20201118_1123','2020-11-18 11:23:42.717021'),(6,'reservation','0001_initial','2020-11-18 11:23:42.872179'),(7,'sessions','0001_initial','2020-11-18 11:23:43.179598'),(8,'place','0003_auto_20201119_0426','2020-11-19 04:26:48.347634'),(9,'place','0004_auto_20201119_0739','2020-11-19 07:40:12.063277');

INSERT INTO `place_images` VALUES (8,'https://i.ibb.co/VgZ36PP/IMG-0650.jpg',7),(9,'https://i.ibb.co/VgZ36PP/IMG-0649.jpg',7),(10,'https://i.ibb.co/VgZ36PP/IMG-0647.jpg',7),(11,'https://i.ibb.co/VgZ36PP/IMG-0648.jpg',7),(12,'https://i.ibb.co/VgZ36PP/IMG-0644.jpg',7),(13,'https://i.ibb.co/VgZ36PP/IMG-0645.jpg',7),(14,'https://i.ibb.co/VgZ36PP/IMG-0642.jpg',7),(15,'https://i.ibb.co/VgZ36PP/IMG-0643.jpg',7),(16,'https://i.ibb.co/VgZ36PP/IMG-0650.jpg',7),(17,'https://i.ibb.co/VgZ36PP/IMG-0649.jpg',7),(18,'https://i.ibb.co/VgZ36PP/IMG-0647.jpg',7),(19,'https://i.ibb.co/VgZ36PP/IMG-0648.jpg',7),(20,'https://i.ibb.co/VgZ36PP/IMG-0650.jpg',7),(21,'https://i.ibb.co/VgZ36PP/IMG-0649.jpg',7),(22,'https://i.ibb.co/VgZ36PP/IMG-0647.jpg',7),(23,'https://i.ibb.co/VgZ36PP/IMG-0648.jpg',7),(24,'https://i.ibb.co/VgZ36PP/IMG-0650.jpg',7),(25,'https://i.ibb.co/VgZ36PP/IMG-0649.jpg',7),(26,'https://i.ibb.co/VgZ36PP/IMG-0647.jpg',7),(27,'https://i.ibb.co/VgZ36PP/IMG-0648.jpg',7);

INSERT INTO `places` VALUES (7,'선릉 테헤란로 427',20000,65,10,0,33,'선릉역에 위치한 공유사무실1','사용 후 정리정돈 확실히1','선릉역에서 5분거리 위치, 주변에 밥집 많음1',4,'https://i.ibb.co/VgZ36PP/IMG-0649.jpg',2,1,1);

INSERT INTO `tags` VALUES (1,'공유','2020-11-18 12:54:27.173423'),(2,'favorit','2020-11-19 05:28:18.653811'),(3,'sweet place','2020-11-19 05:28:18.659587');

INSERT INTO `users` VALUES (1,'백승진',0,'jinybear@example.com','1234','Hi',0,0,'','2020-11-18 21:35:20.000000');
