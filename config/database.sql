-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 06 déc. 2022 à 18:55
-- Version du serveur : 5.7.36
-- Version de PHP : 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+2:00";

--
-- Base de données : `web_scraping_project`
--
CREATE DATABASE IF NOT EXISTS `web_scraping_project` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `web_scraping_project`;

-- --------------------------------------------------------

--
-- Structure de la table `jobs_offers`
--

DROP TABLE IF EXISTS `jobs_offers`;
CREATE TABLE IF NOT EXISTS `jobs_offers` (
  `job_offer_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `description` text,
  `location` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `company_url` varchar(800) DEFAULT NULL,
  `criteria` json DEFAULT NULL,
  `date_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `technologies` json DEFAULT NULL,
  `jobboard` varchar(255) NOT NULL,
  PRIMARY KEY (`job_offer_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
COMMIT;
