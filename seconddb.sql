-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 12, 2023 at 08:49 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `seconddb`
--

-- --------------------------------------------------------

--
-- Table structure for table `borrowtab`
--

CREATE TABLE `borrowtab` (
  `borrowno` int(11) NOT NULL,
  `studentdetails` varchar(50) NOT NULL,
  `equipment` varchar(50) NOT NULL,
  `status` varchar(45) NOT NULL,
  `time_start` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `time_end` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ordertab`
--

CREATE TABLE `ordertab` (
  `ID` int(11) NOT NULL,
  `studentdetails` varchar(45) NOT NULL,
  `tssize` varchar(45) NOT NULL,
  `tsquantity` int(11) NOT NULL,
  `pantssize` varchar(45) NOT NULL,
  `pantsquantity` int(11) NOT NULL,
  `totalprice` float NOT NULL,
  `status` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `password`
--

CREATE TABLE `password` (
  `idpassword` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `password`
--

INSERT INTO `password` (`idpassword`) VALUES
('s');

-- --------------------------------------------------------

--
-- Table structure for table `pricetab`
--

CREATE TABLE `pricetab` (
  `tshirt_size_and_pants_size` varchar(45) NOT NULL,
  `prices` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reservetab`
--

CREATE TABLE `reservetab` (
  `reserve_no` int(11) NOT NULL,
  `event_name` varchar(45) NOT NULL,
  `org_name` varchar(45) NOT NULL,
  `date` date NOT NULL,
  `time_start` time NOT NULL,
  `time_end` time NOT NULL,
  `status` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `borrowtab`
--
ALTER TABLE `borrowtab`
  ADD PRIMARY KEY (`borrowno`);

--
-- Indexes for table `ordertab`
--
ALTER TABLE `ordertab`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `tssize_idx` (`tssize`),
  ADD KEY `pantssize_idx` (`pantssize`);

--
-- Indexes for table `password`
--
ALTER TABLE `password`
  ADD PRIMARY KEY (`idpassword`);

--
-- Indexes for table `pricetab`
--
ALTER TABLE `pricetab`
  ADD PRIMARY KEY (`tshirt_size_and_pants_size`);

--
-- Indexes for table `reservetab`
--
ALTER TABLE `reservetab`
  ADD PRIMARY KEY (`reserve_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `borrowtab`
--
ALTER TABLE `borrowtab`
  MODIFY `borrowno` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ordertab`
--
ALTER TABLE `ordertab`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reservetab`
--
ALTER TABLE `reservetab`
  MODIFY `reserve_no` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ordertab`
--
ALTER TABLE `ordertab`
  ADD CONSTRAINT `pantssize` FOREIGN KEY (`pantssize`) REFERENCES `pricetab` (`tshirt_size_and_pants_size`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tssize` FOREIGN KEY (`tssize`) REFERENCES `pricetab` (`tshirt_size_and_pants_size`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
