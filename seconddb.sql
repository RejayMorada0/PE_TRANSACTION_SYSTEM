-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 12, 2023 at 09:05 AM
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

--
-- Dumping data for table `borrowtab`
--

INSERT INTO `borrowtab` (`borrowno`, `studentdetails`, `equipment`, `status`, `time_start`, `time_end`) VALUES
(3, 'GFNBNHMVJHKJ ', 'BASKETBALL', 'RETURNED', '2023-07-12 07:02:58', '2023-07-12 07:02:58');

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

--
-- Dumping data for table `ordertab`
--

INSERT INTO `ordertab` (`ID`, `studentdetails`, `tssize`, `tsquantity`, `pantssize`, `pantsquantity`, `totalprice`, `status`) VALUES
(1, 'FGFHBVNBMNB,', 'T-SHIRT - L', 1, 'PANTS - M', 1, 200, 'RECIEVED ORDER');

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

--
-- Dumping data for table `pricetab`
--

INSERT INTO `pricetab` (`tshirt_size_and_pants_size`, `prices`) VALUES
('NOT AVAIL', 0),
('PANTS - L', 100),
('PANTS - M', 100),
('PANTS - S', 100),
('PANTS - XL', 100),
('PANTS - XS', 100),
('PANTS - XXL', 100),
('T-SHIRT - L', 100),
('T-SHIRT - M', 100),
('T-SHIRT - S', 100),
('T-SHIRT - XL', 100),
('T-SHIRT - XS', 100),
('T-SHIRT - XXL', 100);

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
  MODIFY `borrowno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `ordertab`
--
ALTER TABLE `ordertab`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `reservetab`
--
ALTER TABLE `reservetab`
  MODIFY `reserve_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
