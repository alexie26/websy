# Webbasierte Systeme - Gruppe 07

Entwicklung einer Flask-Anwendung mit Datenbankanbindung

## Projektstruktur

Der Projektordner enthält standardmäßig folgende Dateien und Verzeichnisse:

* **db**:
  * **db_credentials.py**: enthält Verbindungsinformationen zur Datenbank
  * **db_schema.sql**: enthält SQL-Befehle zur Erzeugung der Datenbank
* **static**:
  * enthält alle statischen Dateien wie CSS-Dateien und Bilder
* **templates**:
  * enthält alle HTML-Templates
* **.gitignore**: enthält alle Dateien und Verzeichnisse, die nicht in die Versionskontrolle mit Git aufgenommen werden sollen
* **LICENSE**: enthält Lizenzbedingungen für das gesamte Projekt
* **README.md**: Diese Datei, enthält die Projektdokumentation im Markdown-Format
* **ss-2025-07.py**: enthält die eigentliche Flask-Anwendung

## Projektanforderungen

#Beauty Dienstleistungen

#Technology Stack
- **Backend**: Flask (Python)
- **Database**: MySQL with phpMyAdmin
- **Frontend**: HTML, CSS

### Mindestanforderungen
 ## Benutzerauthentifizierung & Verwaltung

 * [ ] Registrierung und Login für drei Benutzertypen: Anbieter, Nutzer und Admin
 * [ ] Admin-Bereich mit vollständiger Daten- und Nutzerverwaltung
 * [ ] Anbieter-Dashboard zur Verwaltung eigener Dienstleistungen und Termine
 * [ ] Nutzer-Bereich zur Verwaltung eigener Profildaten
 
 Rollenbasierte Zugriffssteuerung:
  * [ ] Nutzer:    Verwaltung eigener Daten und Buchungen
  * [ ] Anbieter:  Verwaltung eigener Dienstleistungen, Termine und Kundendaten
  * [ ] Admin:     Vollzugriff auf alle Systemdaten und Benutzer

# Daten Verwaltung
  * [ ] Einfuegen, Aendern und Loeschen von Daten nach berechtigung
  * [ ] Speicherung von Benutzer-, Termin- Bewertungsdaten in der Datenbank

# Homepage Anforderungen
  * [ ] Login-Bereich für alle Benutzertypen
  * [ ] Registrierungsmöglichkeit für Nutzer und Anbieter
  * [ ] Login/ Logout

### Optionale Anforderungen
* [ ] Benutzerdefinierte Theme-Umschaltung (Hell-/Dunkel-Modus)
* [ ] Verifizierung von Anbietern durch Admin
* [ ] Such und Filter Funktionen (Anbieter nach Kategorie, Standort, Verfugtbarkeit oder Bewertungen)
* [ ] Admin Dashboard