# Datasheet: Märklin Digital I2C-Bus (MM1 & MM2)

## Übersicht
Dieses Dokument spezifiziert die Datenkommunikation der Märklin Digital-Eingabegeräte über den I2C-Bus. Das System nutzt eine Multi-Master-Architektur, bei der Steuergeräte (z. B. Control 80f) aktiv Befehle an die Zentraleinheit senden und Rückmeldungen empfangen.

## Physikalische Schicht

### Schnittstellenbelegung
Die Kommunikation erfolgt über die seitlichen Kontaktleisten der Zentraleinheiten (6020/6021).

| Signal | Pin (Rechts) | Pin (Links) | Beschreibung |
| :--- | :--- | :--- | :--- |
| **SDA** | b2 | b16 | Serielle Datenleitung (bi-direktional) |
| **SCL** | b4 | b14 | Serieller Takt (gesteuert durch den jeweiligen Master) |
| **b12** | b12 | - | Adress-Chain-Leitung zur Software-Adressierung |

### Bus-Regeln
* **Ruhezustand:** Beide Leitungen (SDA, SCL) liegen auf logisch HIGH Potential.
* **Pegelwechsel:** Daten auf der SDA-Leitung dürfen sich nur ändern, wenn SCL auf LOW liegt.
* **Datengültigkeit:** Wenn SCL auf HIGH liegt, muss der Pegel auf SDA stabil bleiben.
* **Start-Bedingung:** Ein Master zieht SDA auf LOW, während SCL auf HIGH liegt.
* **Acknowledge (Q):** Nach jedem Byte (8 Bit) sendet der Empfänger ein LOW-Bit als Bestätigung. Fehlt dieses, wird ein Stop-Signal generiert.
* **Stop-Bedingung:** Übergang von SDA von LOW auf HIGH, während SCL auf HIGH liegt. In diesem System werden oft zwei Stop-Bits zur Synchronisation beim Wechsel der Master/Slave-Rollen verwendet.

## Adressierung und Identifikation

### Software-Adressierung (Chain-Verfahren)
Nach dem Einschalten oder einem RESET müssen Geräte auf der rechten Seite (Control 80, Interface, etc.) adressiert werden. Dies geschieht über eine Kettenleitung an Pin b12.

1. Die Zentrale zieht b12 für das erste Gerät auf LOW.
2. Das Gerät empfängt seine Adresse über I2C, quittiert diese und zieht b12 für das nächste Gerät in der Kette auf LOW.
3. Dieser Prozess setzt sich fort, bis alle Geräte adressiert sind.

![Adressierungs-Sequenz](diagrams/addressing_sequence.puml)

### Geräte-Identifikatoren
Die Identifikation des Befehlstyps erfolgt über die Bits 5, 6 und 7 der Geräteadresse. Die eigentliche Geräteadresse (0-15) liegt in den Bits 1-4. Bit 0 ist meist 0.

| Typ | Bit 7 | Bit 6 | Bit 5 | Binär-Format |
| :--- | :---: | :---: | :---: | :--- |
| Zentraleinheit | 1 | 1 | 1 | `1111 1110` |
| Lokomotivbefehl | 0 | 0 | 0 | `000X XXX0` |
| Magnetartikelbefehl | 0 | 0 | 1 | `001X XXX0` |
| Zusatzfunktionen (f1-f4) | 0 | 1 | 0 | `010X XXX0` |

### Adress-Byte Struktur
![Adress-Byte](diagrams/addressing_bytes.json)

## Protokoll-Spezifikation und Befehlssätze

### Kommunikationsfluss
Befehle werden in Paketen von 3 bis 4 Bytes übertragen. Da es sich um ein Multi-Master-System handelt, übernimmt das sendende Gerät temporär die Master-Rolle.

![Kommunikationsfluss](diagrams/communication_flow.puml)

### Lokomotivbefehle (Standard H0-Modus)
Wird verwendet für Standard-Motorola-Decoder (MM1).

* **Paketlänge:** 4 Bytes (Empfänger, Sender, Decoder-Adresse, Datenbyte)
* **Adressbereich:** 00 bis 79 (Adresse 80 wird als 00 übertragen)

![Lokbefehl H0](diagrams/loco_command_h0.json)

### Lokomotivbefehle (Erweitertes Motorola-Format / MM2)
Unterstützt absolute Fahrtrichtung und erzwungene Adressübernahme.

![Lokbefehl MM2](diagrams/loco_command_ext.json)

### Zusatzfunktionen (f1 bis f4)
Befehle zur Steuerung der Sonderfunktionen.

![Funktionsbefehl](diagrams/function_command.json)

### Magnetartikelbefehle (Weichen/Signale)
* **Paketlänge:** 3 Bytes
* **Datenbyte:** Enthält Ausgangsnummer (Bit 1-2), Richtung (Bit 0), Power (Bit 3) und Sektionsadresse (Bit 4-5).

![Magnetartikelbefehl](diagrams/switch_command.json)

## Systemverhalten und Spezialfunktionen

### Unterschiede Central Unit (6020) vs. Control Unit (6021)
* **Zentraleinheit 6020:** Im STOP-Modus wird der Bus nach dem ersten Byte blockiert (SCL/SDA auf LOW), bis wieder in den GO-Modus gewechselt wird.
* **Zentraleinheit 6021:** Nutzt das erweiterte Motorola-Format (MM2) bei entsprechender DIP-Schalter-Einstellung.

### Undokumentierte Funktionen (6021)
Diese Funktionen sind über die Adresseingabe am Steuergerät zugänglich (nur im MM2-Format):

* **91 + 93:** Löschen des Refresh-Speichers und Setzen aller Richtungen auf "Vorwärts".
* **92 + 93:** Alle 80 Lokadressen in den Refresh-Zyklus aufnehmen.
* **94 + 93:** Software-Versionstest (LED blinkt).
* **97 + 93:** Wiederherstellung des letzten Betriebszustands (Recall).
