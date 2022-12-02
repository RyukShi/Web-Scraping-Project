-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : ven. 02 déc. 2022 à 11:37
-- Version du serveur : 5.7.36
-- Version de PHP : 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+2:00";

--
-- Base de données : `web_scraping_project`
--

-- --------------------------------------------------------

--
-- Structure de la table `jobs_offers`
--

DROP TABLE IF EXISTS `jobs_offers`;
CREATE TABLE IF NOT EXISTS `jobs_offers` (
  `jobs_offer_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4,
  `location` varchar(255) DEFAULT NULL,
  `jobs_offer_url` varchar(500) NOT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `company_url` varchar(500) DEFAULT NULL,
  `posted_at` varchar(255) DEFAULT NULL,
  `criteria` json DEFAULT NULL,
  `date_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`jobs_offer_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
COMMIT;
