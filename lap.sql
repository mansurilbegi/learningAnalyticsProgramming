-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1:5999
-- Üretim Zamanı: 14 Haz 2023, 10:45:45
-- Sunucu sürümü: 10.4.27-MariaDB
-- PHP Sürümü: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `lap`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `attendance`
--

CREATE TABLE `attendance` (
  `moduleID` int(11) NOT NULL,
  `username` varchar(25) NOT NULL,
  `attended` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `attendance`
--

INSERT INTO `attendance` (`moduleID`, `username`, `attended`) VALUES
(1, 'akinmakin', 1),
(1, 'bayblau', 1),
(1, 'dschawid', 0),
(1, 'naazkaaya', 0),
(1, 'oguzhan', 1),
(1, 'saripirens', 1);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `course`
--

CREATE TABLE `course` (
  `courseID` int(11) NOT NULL,
  `courseCode` varchar(10) NOT NULL,
  `instructorUsername` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `course`
--

INSERT INTO `course` (`courseID`, `courseCode`, `instructorUsername`) VALUES
(1, 'CNG 111', 'mansursio'),
(2, 'CNG 140', 'mansursio'),
(4, 'CNG 111', 'celines'),
(6, 'CNG 223', 'mansursio');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `exception`
--

CREATE TABLE `exception` (
  `exceptionID` int(11) NOT NULL,
  `exceptionName` varchar(30) NOT NULL,
  `count` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `exception`
--

INSERT INTO `exception` (`exceptionID`, `exceptionName`, `count`) VALUES
(1, 'AssertionError', 0),
(2, 'AttributeError', 0),
(3, 'FloatingPointError', 0),
(4, 'GeneratorExit', 0),
(5, 'ImportError', 0),
(6, 'IndexError', 0),
(7, 'KeyError', 0),
(8, 'KeyboardInterrupt', 0),
(9, 'MemoryError', 0),
(10, 'NameError', 0),
(11, 'NotImplementedError', 0),
(12, 'OSError', 0),
(13, 'OverflowError', 0),
(14, 'ReferenceError', 0),
(15, 'RuntimeError', 0),
(16, 'StopIteration', 0),
(17, 'SyntaxError', 0),
(18, 'IndentationError', 0),
(19, 'TabError', 0),
(20, 'SystemError', 0),
(21, 'SystemExit', 0),
(22, 'TypeError', 0),
(23, 'UnboundLocalError', 0),
(24, 'UnicodeError', 0),
(25, 'UnicodeEncodeError', 0),
(26, 'UnicodeDecodeError', 0),
(27, 'UnicodeTranslateError', 0),
(28, 'ValueError', 0),
(29, 'ZeroDivisionError', 0);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `instructor`
--

CREATE TABLE `instructor` (
  `username` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `instructor`
--

INSERT INTO `instructor` (`username`) VALUES
('celines'),
('mansursio');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `module`
--

CREATE TABLE `module` (
  `moduleID` int(11) NOT NULL,
  `moduleName` varchar(10) NOT NULL,
  `deadline` date NOT NULL,
  `courseID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `module`
--

INSERT INTO `module` (`moduleID`, `moduleName`, `deadline`, `courseID`) VALUES
(1, 'Module 1', '2023-06-08', 1),
(2, 'Module 2', '2023-06-25', 1),
(3, 'Module 1', '2023-06-25', 2),
(4, 'Module 2', '2023-06-25', 2),
(8, 'Module 4', '2023-06-25', 1),
(9, 'Module 3', '2023-06-25', 2),
(10, 'Module 3', '2023-06-04', 1);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `question`
--

CREATE TABLE `question` (
  `questionID` int(11) NOT NULL,
  `questionNo` int(11) NOT NULL,
  `question` text NOT NULL,
  `moduleID` int(11) NOT NULL,
  `questionContent` varchar(500) DEFAULT NULL,
  `questionStatus` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `question`
--

INSERT INTO `question` (`questionID`, `questionNo`, `question`, `moduleID`, `questionContent`, `questionStatus`) VALUES
(45, 1, 'Write a python function that takes 2 numbers(a,b) and does addition operation between a and b, then initializes c with the result of this addition, finally function returns c.', 1, 'def add(a,b):\r\n    #Your Code will be here\r\n    return()', 1),
(46, 2, 'Write a function in Python that takes an array as input and returns the sum of all elements in the array.', 1, 'def array_sum(arr):\r\n   #Your Code will be here\r\n    return()', 1),
(47, 1, 'Write a Python function that takes a string as an argument and returns the number of vowels in that string.', 2, 'def count_vowels(s):\r\n    #your code will be here\r\n    return ()', 1),
(48, 1, 'Write a Python program to calculate the factorial of a given number.', 3, 'def factorial(n):\r\n    #your code will be here\r\n    return ()', 1);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `registration`
--

CREATE TABLE `registration` (
  `username` varchar(25) NOT NULL,
  `courseID` int(11) NOT NULL,
  `evaluation` int(11) NOT NULL,
  `evaluationText` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `registration`
--

INSERT INTO `registration` (`username`, `courseID`, `evaluation`, `evaluationText`) VALUES
('akinmakin', 1, 0, 'null'),
('bayblau', 1, 0, 'null'),
('bayblau', 2, 0, 'null'),
('dschawid', 1, 0, 'null'),
('dschawid', 2, 0, 'null'),
('dschawid', 6, 0, 'null'),
('naazkaaya', 1, 0, 'null'),
('naazkaaya', 2, 0, 'null'),
('naazkaaya', 6, 0, 'null'),
('oguzhan', 1, 0, 'null'),
('oguzhan', 2, 0, 'null'),
('oguzhan', 6, 0, 'null'),
('pinarsio', 2, 0, 'null'),
('saripirens', 1, 0, 'null'),
('saripirens', 2, 0, 'null');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `solution`
--

CREATE TABLE `solution` (
  `questionID` int(11) NOT NULL,
  `username` varchar(25) NOT NULL,
  `isSolved` tinyint(1) NOT NULL,
  `attempts` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `solution`
--

INSERT INTO `solution` (`questionID`, `username`, `isSolved`, `attempts`) VALUES
(45, 'akinmakin', 1, 6),
(45, 'bayblau', 1, 3),
(45, 'dschawid', 0, 2),
(45, 'oguzhan', 0, 1),
(45, 'saripirens', 1, 12);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `solutionexception`
--

CREATE TABLE `solutionexception` (
  `questionID` int(11) NOT NULL,
  `username` varchar(25) NOT NULL,
  `exceptionID` int(11) NOT NULL,
  `count` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `solutionexception`
--

INSERT INTO `solutionexception` (`questionID`, `username`, `exceptionID`, `count`) VALUES
(45, 'akinmakin', 10, 3),
(45, 'akinmakin', 29, 2),
(45, 'bayblau', 10, 1),
(45, 'bayblau', 29, 1),
(45, 'dschawid', 29, 2),
(45, 'oguzhan', 29, 1),
(45, 'saripirens', 10, 4),
(45, 'saripirens', 17, 1),
(45, 'saripirens', 18, 2),
(45, 'saripirens', 29, 1);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `student`
--

CREATE TABLE `student` (
  `username` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `student`
--

INSERT INTO `student` (`username`) VALUES
('akinmakin'),
('bayblau'),
('daisy'),
('dschawid'),
('naazkaaya'),
('oguzhan'),
('pinarsio'),
('saripirens');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `testcases`
--

CREATE TABLE `testcases` (
  `questionID` int(11) NOT NULL,
  `testCase` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `testcases`
--

INSERT INTO `testcases` (`questionID`, `testCase`) VALUES
(45, '(add,1,1,2),(add,2,2,4)'),
(46, '(array_sum,1,2,3,4,5,6,21),(array_sum,1,2,3,4,10)'),
(47, '(count_vowels,\"abcdefg\",2),(count_vowels,\"mansuryavas\",4)'),
(48, '(factorial,5,120),(factorial,6,720)');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `user`
--

CREATE TABLE `user` (
  `username` varchar(25) NOT NULL,
  `password` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `surname` varchar(20) NOT NULL,
  `userType` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `user`
--

INSERT INTO `user` (`username`, `password`, `name`, `surname`, `userType`) VALUES
('akinmakin', 'a123', 'Akin', 'Bur', 2),
('bayblau', 'b123', 'Batuhan', 'Karay', 2),
('celines', 'c123', 'Celine', 'Sezer', 1),
('daisy', 'd123', 'Daisy', 'Sezer', 2),
('dschawid', 'j123', 'Javid', 'Babayev', 2),
('mansursio', 'm123', 'Mansur', 'Ilbegi', 1),
('naazkaaya', 'N.azey9B', 'Zeynep Naz', 'Kaya', 2),
('oguzhan', '123456', 'oguzhan', 'alperturk', 2),
('pinarsio', 'p123', 'Pinar', 'Sari', 2),
('saripirens', 'e123', 'Ekrem', 'Karay', 2);

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`moduleID`,`username`),
  ADD KEY `attendanceStudent_fk` (`username`);

--
-- Tablo için indeksler `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`courseID`),
  ADD KEY `instructorCourse_fk` (`instructorUsername`);

--
-- Tablo için indeksler `exception`
--
ALTER TABLE `exception`
  ADD PRIMARY KEY (`exceptionID`);

--
-- Tablo için indeksler `instructor`
--
ALTER TABLE `instructor`
  ADD PRIMARY KEY (`username`);

--
-- Tablo için indeksler `module`
--
ALTER TABLE `module`
  ADD PRIMARY KEY (`moduleID`),
  ADD KEY `courseModule_fk` (`courseID`);

--
-- Tablo için indeksler `question`
--
ALTER TABLE `question`
  ADD PRIMARY KEY (`questionID`),
  ADD KEY `questionModule_fk` (`moduleID`);

--
-- Tablo için indeksler `registration`
--
ALTER TABLE `registration`
  ADD PRIMARY KEY (`username`,`courseID`),
  ADD KEY `courseRegistration_fk` (`courseID`);

--
-- Tablo için indeksler `solution`
--
ALTER TABLE `solution`
  ADD PRIMARY KEY (`questionID`,`username`),
  ADD KEY `usernameSolution_fk` (`username`);

--
-- Tablo için indeksler `solutionexception`
--
ALTER TABLE `solutionexception`
  ADD PRIMARY KEY (`questionID`,`username`,`exceptionID`),
  ADD KEY `solutionExceptions_fk` (`exceptionID`);

--
-- Tablo için indeksler `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`username`);

--
-- Tablo için indeksler `testcases`
--
ALTER TABLE `testcases`
  ADD PRIMARY KEY (`questionID`);

--
-- Tablo için indeksler `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `course`
--
ALTER TABLE `course`
  MODIFY `courseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Tablo için AUTO_INCREMENT değeri `exception`
--
ALTER TABLE `exception`
  MODIFY `exceptionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- Tablo için AUTO_INCREMENT değeri `module`
--
ALTER TABLE `module`
  MODIFY `moduleID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Tablo için AUTO_INCREMENT değeri `question`
--
ALTER TABLE `question`
  MODIFY `questionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- Dökümü yapılmış tablolar için kısıtlamalar
--

--
-- Tablo kısıtlamaları `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendanceModule_fk` FOREIGN KEY (`moduleID`) REFERENCES `module` (`moduleID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `attendanceStudent_fk` FOREIGN KEY (`username`) REFERENCES `student` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Tablo kısıtlamaları `course`
--
ALTER TABLE `course`
  ADD CONSTRAINT `instructorCourse_fk` FOREIGN KEY (`instructorUsername`) REFERENCES `instructor` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Tablo kısıtlamaları `instructor`
--
ALTER TABLE `instructor`
  ADD CONSTRAINT `instructorUsername_fk` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Tablo kısıtlamaları `module`
--
ALTER TABLE `module`
  ADD CONSTRAINT `courseModule_fk` FOREIGN KEY (`courseID`) REFERENCES `course` (`courseID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Tablo kısıtlamaları `question`
--
ALTER TABLE `question`
  ADD CONSTRAINT `questionModule_fk` FOREIGN KEY (`moduleID`) REFERENCES `module` (`moduleID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Tablo kısıtlamaları `registration`
--
ALTER TABLE `registration`
  ADD CONSTRAINT `courseRegistration_fk` FOREIGN KEY (`courseID`) REFERENCES `course` (`courseID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `studentRegistration_fk` FOREIGN KEY (`username`) REFERENCES `student` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Tablo kısıtlamaları `solution`
--
ALTER TABLE `solution`
  ADD CONSTRAINT `questionSolution_fk` FOREIGN KEY (`questionID`) REFERENCES `question` (`questionID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `solutionException_fk` FOREIGN KEY (`questionID`) REFERENCES `question` (`questionID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `studentSolution_fk` FOREIGN KEY (`username`) REFERENCES `student` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `usernameSolution_fk` FOREIGN KEY (`username`) REFERENCES `student` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Tablo kısıtlamaları `solutionexception`
--
ALTER TABLE `solutionexception`
  ADD CONSTRAINT `questionID_fk` FOREIGN KEY (`questionID`) REFERENCES `question` (`questionID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `solutionExceptions_fk` FOREIGN KEY (`exceptionID`) REFERENCES `exception` (`exceptionID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Tablo kısıtlamaları `student`
--
ALTER TABLE `student`
  ADD CONSTRAINT `studentUsername_fk` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Tablo kısıtlamaları `testcases`
--
ALTER TABLE `testcases`
  ADD CONSTRAINT `questionTestCase_fk` FOREIGN KEY (`questionID`) REFERENCES `question` (`questionID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
