-- Tabellenstruktur für Tabelle `Nutzer`
--

CREATE TABLE `Nutzer` (
  `Nutzer_ID` int(11) NOT NULL,
  `Vorname` varchar(100) NOT NULL,
  `Nachname` varchar(100) NOT NULL,
  `EMail` varchar(100) NOT NULL,
  `Strasse` text NOT NULL,
  `Hausnummer` varchar(10) NOT NULL,
  `PLZ` varchar(100) NOT NULL,
  `ORT` text NOT NULL,
  `ProfilBild` varchar(100) DEFAULT NULL,
  `Telefon` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `Nutzer`
--

INSERT INTO `Nutzer` (`Nutzer_ID`, `Vorname`, `Nachname`, `EMail`, `Strasse`, `Hausnummer`, `PLZ`, `ORT`, `ProfilBild`, `Telefon`) VALUES
(1, 'Anna', 'Meier', 'anna.meier@gmail.com', 'Hauptstrasse', '12', '10827', 'Berlin', 'Anier', '01739825982'),
(2, 'Peter', 'Schmidt', 'schmidtpeter@gmail.com', 'Bahnhofstrasse', '7A', '44623', 'Herne', 'UPeidt', '01517164853'),
(3, 'Alexandra', 'Sidiropoulou', 'sidir.alexandra@gmail.com', 'Paulinenstrasse', '23', '74076', 'Heilbronn', 'asidiropou', '01796625662'),
(4, 'Biwar', 'sifo', 'biwar1998@yahoo.com', 'Hindenburgstr', '89', '71638', 'Ludwigsburg', 'bsaifo', '01743841173'),
(5, 'Ghazal', 'Al Kudsy', 'wq.76@hotmail.com', 'Falltorstr', '11', '74172', 'Neckarsulm', 'galkudsy', '01639204750');
(6, 'Alexandra', 'Rosu', 'mariaalexandrarosu9@gmail.com', 'Klostermuehlstr', '2', '93194', 'Walderbach', 'mrosu', '015562740042');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `Nutzer`
--
ALTER TABLE `Nutzer`
  ADD PRIMARY KEY (`Nutzer_ID`),
  ADD UNIQUE KEY `EMail` (`EMail`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `Nutzer`
--
ALTER TABLE `Nutzer`
  MODIFY `Nutzer_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

-- Tabellenstruktur für Tabelle `Login`
--

CREATE TABLE `Login` (
  `Login_ID` int(11) NOT NULL,
  `Benutzername` varchar(100) NOT NULL,
  `Passwort` varchar(255) NOT NULL,
  `Rolle` enum('Nutzer','Anbieter','Admin') NOT NULL,
  `FK_Nutzer_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `Login`
--

INSERT INTO `Login` (`Login_ID`, `Benutzername`, `Passwort`, `Rolle`, `FK_Nutzer_ID`) VALUES
(1, 'aneir', '12345annameier', 'Nutzer', 1),
(2, 'peidt', '987654schmidt', 'Anbieter', 2),
(3, 'asidiropou', '270903asidiropou', 'Admin', 3),
(4, 'bsaifo', '200199bsaifo', 'Admin', 4),
(5, 'galkudsy', '010103galkudsy', 'Admin', 5);
(6, 'mrosu', '260903mrosu', 'Admin', 6);
--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `Login`
--
ALTER TABLE `Login`
  ADD PRIMARY KEY (`Login_ID`),
  ADD UNIQUE KEY `Benutzername` (`Benutzername`),
  ADD KEY `FK_Nutzer_ID` (`FK_Nutzer_ID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `Login`
--
ALTER TABLE `Login`
  MODIFY `Login_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `Login`
--
ALTER TABLE `Login`
  ADD CONSTRAINT `Login_ibfk_1` FOREIGN KEY (`FK_Nutzer_ID`) REFERENCES `Nutzer` (`Nutzer_ID`);
COMMIT;

-- Tabellenstruktur für Tabelle `Dienstleistungen`
--

CREATE TABLE `Dienstleistungen` (
  `Dienstleistung_ID` int(11) NOT NULL,
  `Titel` varchar(200) NOT NULL,
  `Beschreibung` text NOT NULL,
  `Dauer` tinytext NOT NULL,
  `Preise` double(10,2) NOT NULL,
  `Bild` varchar(100) NOT NULL,
  `FK_Login_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `Dienstleistungen`
--

INSERT INTO `Dienstleistungen` (`Dienstleistung_ID`, `Titel`, `Beschreibung`, `Dauer`, `Preise`, `Bild`, `FK_Login_ID`) VALUES
(2, 'Aqua Facial', '- Entfernung von Mitessern und Komedonen\r\n- Minderung von Akne und oberflächlichen Narben möglich\r\n- Möglichkeit zur Reduzierung der fettigen Haut hin zum normalen Hautzustand\r\n- Anwendung auch auf empfindlicher Haut möglich\r\n- kann gut mit anderen Behandlungen kombiniert werden', '60 Min', 129.00, 'BeautyPointAquaFacial', 2);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `Dienstleistungen`
--
ALTER TABLE `Dienstleistungen`
  ADD PRIMARY KEY (`Dienstleistung_ID`),
  ADD KEY `FK_Login_ID` (`FK_Login_ID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `Dienstleistungen`
--
ALTER TABLE `Dienstleistungen`
  MODIFY `Dienstleistung_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
  MODIFY `Dauer` INT;
--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `Dienstleistungen`
--
ALTER TABLE `Dienstleistungen`
  ADD CONSTRAINT `Dienstleistungen_ibfk_1` FOREIGN KEY (`FK_Login_ID`) REFERENCES `Login` (`Login_ID`);
COMMIT;

-- Tabellenstruktur für Tabelle `Unternehmensprofil`
--

CREATE TABLE `Unternehmensprofil` (
  `Profil_ID` int(11) NOT NULL,
  `Titel` varchar(150) NOT NULL,
  `Beschreibung` text DEFAULT NULL,
  `EMail` varchar(100) DEFAULT NULL,
  `Telefonnummer` varchar(30) DEFAULT NULL,
  `Adresse` text DEFAULT NULL,
  `Hausnummer` varchar(10) DEFAULT NULL,
  `PLZ` int(5) DEFAULT NULL,
  `Ort` varchar(100) DEFAULT NULL,
  `FK_Login_ID` int(11) DEFAULT NULL,
  `FK_Dienstleistung_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `Unternehmensprofil`
--

INSERT INTO `Unternehmensprofil` (`Profil_ID`, `Titel`, `Beschreibung`, `EMail`, `Telefonnummer`, `Adresse`, `Hausnummer`, `PLZ`, `Ort`, `FK_Login_ID`, `FK_Dienstleistung_ID`) VALUES
(1, 'BEAUTY POINT', 'In ruhiger Lage und stilvollem Ambiente erwartet Sie ein Team aus fünf erfahrenen Expertinnen – spezialisiert auf Behandlungen rund um Ihre Schönheit von Kopf bis Fuß.', 'infobeautypoint@gmail.com', '01517164853', ' Lautenbacher Straße', '51', 74172, 'Neckarsulm', 2, 2);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `Unternehmensprofil`
--
ALTER TABLE `Unternehmensprofil`
  ADD PRIMARY KEY (`Profil_ID`),
  ADD KEY `FK_Login_ID` (`FK_Login_ID`),
  ADD KEY `FK_Dienstleistung_ID` (`FK_Dienstleistung_ID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `Unternehmensprofil`
--
ALTER TABLE `Unternehmensprofil`
  MODIFY `Profil_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `Unternehmensprofil`
--
ALTER TABLE `Unternehmensprofil`
  ADD CONSTRAINT `Unternehmensprofil_ibfk_1` FOREIGN KEY (`FK_Login_ID`) REFERENCES `Login` (`Login_ID`),
  ADD CONSTRAINT `Unternehmensprofil_ibfk_2` FOREIGN KEY (`FK_Dienstleistung_ID`) REFERENCES `Dienstleistungen` (`Dienstleistung_ID`);
COMMIT;

-- Tabellenstruktur für Tabelle `Termin`
--

CREATE TABLE `Termin` (
  `Termin_ID` int(11) NOT NULL,
  `Status` enum('gebucht','abgeschlossen','storniert') DEFAULT NULL,
  `Uhrzeit` time NOT NULL,
  `Datum` date NOT NULL,
  `FK_Nutzer_ID` int(11) DEFAULT NULL,
  `FK_Dienstleistung_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `Termin`
--

INSERT INTO `Termin` (`Termin_ID`, `Status`, `Uhrzeit`, `Datum`, `FK_Nutzer_ID`, `FK_Dienstleistung_ID`) VALUES
(1, 'gebucht', '10:00:00', '2025-05-25', 1, 2);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `Termin`
--
ALTER TABLE `Termin`
  ADD PRIMARY KEY (`Termin_ID`),
  ADD KEY `FK_Nutzer_ID` (`FK_Nutzer_ID`),
  ADD KEY `FK_Dienstleistung_ID` (`FK_Dienstleistung_ID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `Termin`
--
ALTER TABLE `Termin`
  MODIFY `Termin_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `Termin`
--
ALTER TABLE `Termin`
  ADD CONSTRAINT `Termin_ibfk_1` FOREIGN KEY (`FK_Nutzer_ID`) REFERENCES `Nutzer` (`Nutzer_ID`),
  ADD CONSTRAINT `Termin_ibfk_2` FOREIGN KEY (`FK_Dienstleistung_ID`) REFERENCES `Dienstleistungen` (`Dienstleistung_ID`);
COMMIT;

-- Tabellenstruktur für Tabelle `Bewertung`
--

CREATE TABLE `Bewertung` (
  `Bewertung_ID` int(11) NOT NULL,
  `Bewertung` int(11) DEFAULT NULL CHECK (`Bewertung` between 1 and 5),
  `Kommentieren` text DEFAULT NULL,
  `FK_Termin_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `Bewertung`
--

INSERT INTO `Bewertung` (`Bewertung_ID`, `Bewertung`, `Kommentieren`, `FK_Termin_ID`) VALUES
(1, 5, 'Sehr freundliche Behandlung, gerne wieder!', 1);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `Bewertung`
--
ALTER TABLE `Bewertung`
  ADD PRIMARY KEY (`Bewertung_ID`),
  ADD UNIQUE KEY `FK_Termin_ID` (`FK_Termin_ID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `Bewertung`
--
ALTER TABLE `Bewertung`
  MODIFY `Bewertung_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `Bewertung`
--
ALTER TABLE `Bewertung`
  ADD CONSTRAINT `Bewertung_ibfk_1` FOREIGN KEY (`FK_Termin_ID`) REFERENCES `Termin` (`Termin_ID`);
COMMIT;
