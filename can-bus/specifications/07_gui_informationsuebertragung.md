# 7 GUI Informationsübertragung

Konfigurationsabgleich mehrerer Graphical User Interface Prozessors.
## 7.1 Befehl: Anfordern Config Data
Kennung:
Anfordern Config Data (0x20, in CAN-ID: 0x40)
Format:
Beschreibung:
Anfordern einer Configdatei. Darin enthalten ist ein 8 Byte Dateiname.
Bestätigen der Anforderung mit gesetztem Resp. Bit.
Die folgenden Dateinamen werden von der CS2 unterstützt:

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | Konfig Data |  | Hash | 8 | Byte 0 | Byte 1 | Byte 2 | Byte 3 | Byte 4 | Byte 5 | Byte 6 | Byte 7 |


| Dateiname | Ab- sender | Bedeutung | Folge-Info | Stream-Datenformat |
| --- | --- | --- | --- | --- |
| "lokinfo" | MS2 | Daten einer Lok | Anfang des Lok-Namens 2 Pakete mit zusammen max. 16 Zeichen | Text (Ausschnitt aus "lokomotive.cs2") |
| "loknamen" | MS2 | Namen von n Loks und Gesamtzahl | 1 Datagram mit Nr. der ersten Lok und Anzahl durch Leerzeichen getrennt | Text: Lok-Nr, Lok-Name und Gesamtanzahl der Loks im .cs2-Format. |
| "maginfo" | MS2 | Daten von n Magnetartikeln | 1 Datagram mit Adresse des ersten Magnet- artikels und Anzahl durch Leerzeichen getrennt | Text (Ausschnitt aus "magnetartikel.cs2") |
| "lokdb" | MS2 | Lokdatenbank | - | Binär (MS2-Lokdb-Format) |
| „lang“ | MS2 | Sprachendatei | - | Binär (MS2-Sprachen-Format) |
| „ldbver“ | MS2 | Versionsinfo der Lokdatenbank | - | Text: Versionsnummer, Monat, Jahr, Anzahl der Einträge im .cs2-Format |
| „langver“ | MS2 | Versionsinfo der Sprachendatei | - | Text: Versionsnummer und Größe der Sprachendatei im .cs2-Format |
| „loks“ | CS2 (Slave) | Komplette Lokliste | - | Konfigurationsdatei „lokomotive.cs2“ Zlib-komprimiert |
| „mags“ | CS2 (Slave) | Komplette Magnetartikel- konfiguration | - | Konfigurationsdatei „magnetartikel.cs2“ Zlib-komprimiert |
| „gbs“ | CS2 (Slave) | Komplette Gleisbildgrund- konfiguration | - | Konfigurationsdatei „gleisbild.cs2“ Zlib-komprimiert |
| „gbs-#“ | CS2 | Konfiguration einer | - | Konfigurationsdatei einer |

Wenn in der Spalte Folge-Info etwas angegeben ist, erwartet die Master-CS2 nach der Quittung
eine(?) weitere Config-Data-Anfrage, in der die erste Anfrage weiter qualifiziert wird.
Besonderheiten:
Kann vom PC auch angefordert werden (für Datensicherung).

|  | (Slave) | Gleisbildseite |  | Gleisbildseite Zlib-komprimiert |
| --- | --- | --- | --- | --- |
| „fs“ | CS2 (Slave) | Komplette Fahrstraßen- konfiguration | - | Konfigurationsdatei „fahrstrassen.cs2“ Zlib-komprimiert |
| „lokstat" | CS2 (Slave) | Aktueller Zustand der Loks | - | Statusdatei „lokomotive.sr2“ Zlib-komprimiert |
| „magstat“ | CS2 (Slave) | Aktueller Zustand der Magnetartikel | - | Statusdatei „magnetartikel.sr2“ Zlib-komprimiert |
| „gbsstat“ | CS2 (Slave) | Aktueller Zustand einer Gleisbildseite | - | Statusdatei „gleisbild.sr2“ Zlib-komprimiert |
| fsstat | CS2 (Slave) | Reserve für Fahrstrassen | - | Nicht implementiert |

## 7.2 Befehl: Config Data Stream
Kennung:
Config Data Stream (0x21, in CAN-ID: 0x42)
Format:
Beschreibung:
Überträgt den Datenstrom einer Konfigurationsdatei.
Folgt unmittelbar auf das (letzte) Antwortframe der "Config Data Anforderung" oder zum Mitteilen einer
Konfigurationsänderung per Broadcast. Durch die DLC wird der Inhalt unterschieden:
DLC = 6:
Ist das erste Paket im Datenstrom. Es definiert den Datenstrom als Antwort auf eine Config Data
Anfrage. Es enthält die Dateilänge in Bytes, sowie die CRC der zu übertragenden Bytes.
Bei diesem Typ des Datenstroms wird zur Kollisionsauflösung der Hash des Empfängers verwendet.
Erweiterung: Dies kann auch die Antwort auf eine "blokinfo" Frage sein. Dieser Text wird zu einem
Rückmeldekontakt / Block dargestellt. Bietet somit die Möglichkeit einer freien Textdarstellung im
Gleisbild.
DLC = 7:
Ist das erste Paket im Datenstrom. Es definiert den Datenstrom als Broadcast einer Konfigänderung. Es
enthält die Dateilänge in Bytes, sowie die CRC der zu übertragenden Bytes, sowie einem reservierten
Byte. Der Datenstrom ist bei dieser Übertragungsform immer(?) Zlib-Komprimiert.
Bei diesem Typ des Datenstroms wird zur Kollisionsauflösung der Hash des Senders verwendet.
DLC = 8:
Datenpaket: Es enthält immer 8 Byte an Daten. Stehen weniger Daten zur Verfügung, so wird mit 0x00
gepaddet. Wird immer ab dem 2.ten Datenpaket gesendet. Hash richtet sich nach obiger Systematik.
Alle anderen DLC-Längen:
Tritt im Datenstrom eine andere Länge auf, so ist der Empfang abzubrechen bzw. zu beenden.
Besonderheiten:
Pakete werden nicht bestätigt und werden mit niedriger Prio im CAN übertragen.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | CFG Data Stream |  |  | 6 | Dateilänge / Streamlänge in Bytes |  |  |  | CRC |  |  |  |
|  |  |  |  |  | High |  |  | Low | High | Low |  |  |
| Message Prio | CFG Data Stream |  |  | 7 | Dateilänge / Streamlänge in Bytes |  |  |  | CRC |  | Byte 6 |  |
|  |  |  |  |  | High |  |  | Low | High | Low |  |  |
| Message Prio | CFG Data Stream |  |  | 8 | Byte 0 | Byte 1 | Byte 2 | Byte 3 | Byte 4 | Byte 5 | Byte 6 | Byte 7 |

Der CRC ist ein 16-Bit-CRC mit dem Startwert 0xFFFF und dem Polynom 0x1021, der nach folgendem
Algorithmus berechnet wird.

```cpp
u16 CtDataSender::updateCRC (u16 CRC_acc, u8 CRC_input)
{
#define POLY 0x1021
// Create the CRC "dividend" for polynomial arithmetic (binary arithmetic with no carries)
CRC_acc = CRC_acc ^ (CRC_input << 8);
// "Divide" the poly into the dividend using CRC XOR subtraction CRC_acc holds the
// "remainder" of each divide. Only complete this division for 8 bits since input is 1 byte
for (int i = 0; i < 8; i++) {
// Check if the MSB is set (if MSB is 1, then the POLY can "divide" into the "dividend")
if ((CRC_acc & 0x8000) == 0x8000) {
// if so, shift the CRC value, and XOR "subtract" the poly
CRC_acc = CRC_acc << 1;
CRC_acc ^= POLY;
}

else {
// if not, just shift the CRC value
CRC_acc = CRC_acc << 1;
}
}
// Return the final remainder (CRC value)
return CRC_acc;
}
```