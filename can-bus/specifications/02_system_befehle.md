# 2 System-Befehle

Systembefehle betreffen den Gleis Format Prozessor direkt und bestimmen die Funktionsweise, bzw. die
Zustände.
Des weiteren werden Zustände des Gleis Format Prozessor weitergemeldet.
Die Befehle enthalten, neben einer UID, auch ein Kommandobyte. Dieses dient zur Kennzeichnung des
auszuführenden Systembefehls.
## 2.1 Befehl: System Stopp
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
System Stopp (0x00)
Format:
Beschreibung:
Gleis Format Prozessor stoppt den Betrieb auf Haupt- und Programmiergleis. Es wird keine elektrische
Energie mehr geliefert. Alle Fahrstufen/Funktionswerte und Einstellungen werden behalten.
Als Sonderform muss auf einen generellen Stopp Befehl, welcher alle Gleis Format Prozessoren betrifft,
geachtet werden. Hierzu wird eine spezielle Ziel Geräte UID verwendet (0x0000)
Beispiel:
00004711 5 00 00 00 00 00 Stopp an alle
00004711 5 43 53 32 08 00 Stopp an bestimmten Teilnehmer (CS2 mit SNr. 08)
Antwort:
Ursprünglicher Befehl mit gesetztem Response Bit
Besonderheiten:
Stopp wird immer von Graphical User Interface Prozessor ausgelöst.
Es wird keine Fahrstufe 0 oder Nothalt gesendet. Nach System Go fahren alle Lokomotiven wieder mit
der alten Einstellung weiter oder bleiben stehen. Dieses Verhalten wird durch den Decoder bestimmt.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 0\\\|1 |  | 5 | Ziel Geräte-UID |  |  |  | Sub-CMD Stopp |  |  |  |
|  |  |  |  |  | High |  |  | Low |  |  |  |  |

## 2.2 Befehl: System Go
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
System Go (0x01)
Format:
Beschreibung:
Der Gleis Format Prozessor aktiviert den Betrieb und liefert elektrische Energie. Es werden alle evtl.
noch vorhandenen bzw. gespeicherten Geschwindigkeitsstufen/Funktionen wieder gesendet.
Als Sonderform muss auf einen generellen Go Befehl, welcher alle Gleis Format Prozessor betrifft,
geachtet werden. Hierzu wird eine spezielle Ziel Geräte UID verwendet (0x0000) .
Beispiel:
00004711 5 00 00 00 00 01 Go an alle
00004711 5 43 53 32 08 01 Go an bestimmten Teilnehmer (CS2 mit SNr. 04)
Antwort:
Ursprünglicher Befehl mit gesetztem Response Bit.
Besonderheiten:
Go wird immer von Graphical User Interface Prozessor ausgelöst.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 0\\\|1 |  | 5 | Ziel Geräte-UID |  |  |  | Sub-CMD Go |  |  |  |
|  |  |  |  |  | High |  |  | Low |  |  |  |  |

## 2.3 Befehl: System Halt
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
System Halt (0x02)
Format:
Beschreibung:
Allen Lokomotiven wird befohlen, inklusive ABV, anzuhalten (Fahrstufe 0). Digitalsignal weiterhin auf
Gleis, danach werden keine weiteren Kommandos auf das Gleis gesendet. Elektrische Energie steht
weiterhin zur Verfügung. Sinnvoll zum definierten Herunterfahren der Anlage.
Als Sonderform muss auf einen generellen System Halt Befehl, welcher alle Gleis Format Prozessor
betrifft, geachtet werden. Hierzu wird eine spezielle Ziel Geräte UID verwendet (0x0000)
Beispiel:
00004711 5 00 00 00 00 02 Halt an alle
00004711 5 43 53 32 08 02 Halt an bestimmten Teilnehmer (CS2 mit SNr. 04)
Antwort:
Ursprünglicher Befehl mit gesetztem Response Bit.
Besonderheiten:
Halt wird immer von Graphical User Interface Prozessor ausgelöst.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 0\\\|1 |  | 5 | Ziel Geräte-UID |  |  |  | Sub-CMD Halt |  |  |  |
|  |  |  |  |  | High |  |  | Low |  |  |  |  |

## 2.4 Befehl: Lok Nothalt
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
Lok Nothalt (0x03)
Format:
Beschreibung:
Nothalt bzw. Soforthalt der Lokomotive, je nach Gleisprotokoll. Es muss eine Lokomotive angegeben
werden, die schon durch ein Kommando angesprochen wurde. Ist diese Lok nicht im Zyklus, wird diese
dadurch nicht aufgenommen.
Beispiel:
00004711 5 00 00 00 48 03 Lok Nothalt MM2 72
00004711 5 00 00 C0 03 03 Lok Nothalt DCC Adr. 3
00004711 5 00 00 40 05 03 Lok Nothalt MFX SID 5
Antwort:
Ursprünglicher Befehl mit gesetztem Response Bit.
Besonderheiten:
Nothalt ist nicht als Fahrstufe implementiert, damit keine Fehlinterpretation bei verschiedenen
Protokollen geschieht.
Nothalt wird immer von Graphical User Interface Prozessor ausgelöst.
Erster Befehl nimmt Lok in den Zyklus auf, Nothalt wird gesendet.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 0\\\|1 |  | 5 | Loc-ID |  |  |  | Sub-CMD Lok Halt |  |  |  |
|  |  |  |  |  | High |  |  | Low |  |  |  |  |

## 2.5 Befehl: Lok Zyklus beenden
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
Lok Zyklus Stopp (0x04)
Format:
Beschreibung:
Lok aus Verwaltungsliste des Gleis Format Prozessor löschen.
Lok erhält keine Befehle mehr (kein Refreshzyklus).
Erst wieder bei Setzen einer Fahrstufe oder Ansprechen mittels Funktionen wird Lok wieder
angesprochen und mit Gleistelegrammen versorgt.
Beispiel:
00004711 5 00 00 00 48 04 Zyklus Ende MM2 72
00004711 5 00 00 C0 03 04 Zyklus Ende DCC Adr. 3
00004711 5 00 00 40 05 04 Zyklus Ende MFX SID 5
00004711 5 43 53 32 08 04 Zyklus Ende alle Loks im Gleis Format Prozessor mit UID=43 53 32 08
00004711 5 00 00 00 00 04 Zyklus Ende alle Loks auf allen Gleis Format Prozessoren
(UID 00 00 00 00 Broadcast an alle)
Antwort:
Ursprünglicher Befehl mit gesetztem Response Bit.
Besonderheiten:
Wird immer von Graphical User Interface Prozessor ausgelöst.
Entspricht die Loc-ID der UID des Gleis Format Prozessor, so wird die gesamte Lokverwaltungstabelle
gelöscht.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 0\\\|1 |  | 5 | Loc-ID |  |  |  | Sub-CMD Zyklus |  |  |  |
|  |  |  |  |  | High |  |  | Low |  |  |  |  |

## 2.6 Befehl: Lok Datenprotokoll
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
Lok Datenprotokoll (0x05)
Format:
Beschreibung:
Gleisunterprotokoll ändern bzw. abweichend vom Defaultwert wählen, aber nicht das grundsätzliche
Gleisprotokoll, da sonst Änderung der Loc-ID.
Also DCC bleibt DCC, MM2 bleibt MM2, ....
Folgende Gleisunterprotokolländerungen sind möglich (Werte für Parameter Gleisprotokoll):
Bei MM2:
0: MM2 2040, Ansteuerung Loks mit 20kHz und FDEC mit 40 kHz
1: MM2_LOK_20, Nur Ansteuerung Loks mit 20 kHz.
2: MM2_FKT_40, Nur Ansteuerung FDEC mit 40 kHz.
Bei DCC:
0: DCC Kurze Adresse, 28 Fahrstufen [=DCC-FS-Default],
1: DCC Kurze Adresse, 14 Fahrstufen
2: DCC Kurze Adresse, 126 Fahrstufen
3: DCC Lange Adresse, 28 Fahrstufen
4: DCC Lange Adresse, 126 Fahrstufen
Beispiel:
00004711 6 00 00 C0 03 05 02 DCC Adr 03 mit 126 Fahrstufen ansteuern
Antwort:
Ursprünglicher Befehl mit gesetztem Response Bit.
Bei ungültiger Loc-ID (nicht DCC nicht MM2) wird keine Antwort gesendet.
Besonderheiten:
Wird immer von Graphical User Interface Prozessor ausgelöst.
Erster Befehl nimmt Lok/Funktionsdecoder in Zyklus auf.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 0\\\|1 |  | 6 | Loc-ID |  |  |  | Sub-CMD Protokoll | Gleis- protokoll |  |  |
|  |  |  |  |  | High |  |  | Low |  |  |  |  |

## 2.7 Befehl: Schaltzeit Zubehördecoder festlegen
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
Schaltzeit (0x06)
Format:
Beschreibung:
Defaultzeit zum Schalten von Zubehör festlegen.
Zeit kann auch beim Schaltbefehl mit angegeben werden.
Zeit in 10 ms Schritten, maximal 163 Sekunden rund 2:45 min, Wert 0 ist wieder Dafaultschaltzeit.
Beispiel:
00004711 7 00 00 00 00 06 0A Schaltzeit 100 ms festlegen
Antwort:
Ursprünglicher Befehl mit gesetztem Response Bit.
Besonderheiten:
Wird immer von Graphical User Interface Prozessor ausgelöst.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 1 |  | 7 | Ziel Geräte-UID |  |  |  | Sub-CMD Schaltzeit | <Zeit> |  |  |
|  |  |  |  |  | High |  |  | Low |  | High | Low |  |

## 2.8 Befehl: Fast Read für mfx SID - Adresse
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
Fast Read (0x07)
Format:
Beschreibung:
Ab GFP Version 2 wird für diese MFX SID die Wartezeit zwischen den Lesebefehlen unterdrückt.
Fast Read ist nur mit Decodern der neueren Generation möglich. Mfx - Decoder der ersten Generation
sind hierfür nicht ausgelegt und werden dadurch zerstört.
Fast Read kann erst nach einer Plausibilitätsprüfung durch den GFP aktiviert werden. Die UID zu dieser
SID muss aus dem Märklin mfx Decoderbereich sein. (Beginnend mit 0x7F). Dies wird durch ein mfx
Verify erreicht. Dieser Verify muss vor diesem Befehl ausgeführt werden und positiv beantwortet
werden.
Antwort:
Immer: Ursprünglicher Befehl mit gesetztem Response Bit.
Besonderheiten:
In V1.0 wird Befehl verworfen.
Wird immer von Graphical User Interface Prozessor ausgelöst.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 0\\\|1 |  | 7 | Absender Geräte-UID |  |  |  | Sub-CMD Fast Read | MFX-SID |  |  |
|  |  |  |  |  | High |  |  | Low |  | High | Low |  |

## 2.9 Befehl: Gleisprotokoll Frei Schalten
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
Gleis Protokoll (0x08)
Format:
Beschreibung:
Aktiviert oder sperrt entsprechende Protokolle auf dem Gleis. Parameter gibt Bitkodiert die
entsprechenden Gleisprotokolle frei.
Ein gesetztes Bit gibt das entsprechende Protokoll frei, ein Gelöschtes unterdrückt es. Nach dem Reset
werden alle Protokolle frei gegeben.
Antwort:
Ursprünglicher Befehl mit gesetztem Response Bit
Besonderheiten:
GFP beherrscht nur MM2, mfx und DCC.
Bei abgeschaltetem mfx werden keine mfx-Loks mehr gesucht.
Ein Speichern der Einstellung findet im Gleis Format Prozessor nicht statt. Bei jedem Start ist dieser
Parameter neu zu setzen.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 0\\\|1 |  | 6 | Ziel Geräte-UID |  |  |  | Sub-CMD GleisProt | Param |  |  |
|  |  |  |  |  | High |  |  | Low |  |  |  |  |


| Bit# | Protokoll |
| --- | --- |
| 0 | MM2 |
| 1 | MFX |
| 2 | DCC |
| 3 | Res |
| 4 | Res |
| 5 | Res |
| 6 | Res |
| 7 | Res |

## 2.10 Befehl: System MFX Neuanmeldezähler setzen
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
Neuanmeldezähler (0x09)
Format:
Beschreibung:
Neuanmeldezähler des Gleis Format Prozessor verändern. Für MFX Subsystem.
Beispiel:
00004711 7 43 53 32 08 09 00 02 Setzen Neuanmeldezähler auf 2.
Antwort:
Ursprünglicher Befehl mit gesetztem Response Bit.
Besonderheiten:
Wird immer von Graphical User Interface Prozessor ausgelöst.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 1 |  | 7 | Ziel Geräte-UID |  |  |  | Sub-CMD MFX NAZ | Neuanmeldezähler |  |  |
|  |  |  |  |  | High |  |  | Low |  | High | Low |  |

## 2.11 Befehl: System Überlast
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
Überlast (0x0A)
Format:
Beschreibung:
Ein Teilnehmer meldet hiermit die Überschreitung der im Betrieb zulässigen Werte. In Kanalnummer
steht der Verursacher.
Die Kanalnummern sind pro Gerät eindeutig festgelegt. Mittels des Befehls "Statusdaten Konfiguration"
kann die Bedeutung des Kanals festgestellt werden. Kanalnummer wird bei der Abfrage mitgeteilt.
Beispiel:
00004711 6 43 53 32 08 0A 01 Kanalnummer 1 meldet Überlast.
Antwort:
Dieses "Kommando" wird nur als Antwort gesendet.
Besonderheiten:
Wird immer von dem Gleis Format Prozessor ausgelöst.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 1 |  | 6 | Absender Geräte-UID (Gleis Format |  |  |  | Sub-CMD Überlast | Kanal- nummer |  |  |
|  |  |  |  |  | PHrigohze ssor) |  |  | Low |  |  |  |  |

## 2.12 Befehl: System Status
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
Status (0x0B)
Format:
Beschreibung:
Anfrage zu den aktuellen Verbrauchswerten des Gleis Format Prozessor. Gezielte Anfrage von einem
Bediengerät. Nur der Gleis Format Prozessor, dessen UID im Frame ist, meldet seinen Wert.
Die Kanalnummer sind pro Gerät eindeutig festgelegt. Mittels des Befehls "Statusdaten Konfiguration"
kann Anzahl Kanäle, Bedeutung und Konfiguration des Kanals festgestellt werden.
Auslösen der Anfrage durch DLC = 6 und fehlendem Messwert & Resp. Bit.
Antwort mit DLC = 8 und Messwert, sowie gesetztem Resp. Bit.
Geräte UID bestimmt das gefragte Gerät.
Dieser Befehl wird dazu verwendet, den Status eines Teilnehmers darzustellen. Diese Abfragen sollten
nur dann stattfinden, wenn die Daten wirklich benötigt und angezeigt werden. Zyklische Abfragen,
welche nicht zur grafischen Darstellung benötigt werden, sollten in einem Zeitabstand <10s erfolgen.
Setzen eines Konfigurationswertes des Gleis Format Prozessor. Welche Werte gesetzt werden können,
ist mittels des Befehls "Statusdaten Konfiguration" feststellbar. Erfolgreiches setzen eines Wertes wird
mit einer Antwort quittiert.
Die Antwort auf Setzen eines Konfigurationswerts ist mit DLC = 7. Im Antwortbyte steht das Ergebniss
der Operation: Bei Gültig wird mit TRUE (0x01), bei ungültig mit FALSE (0x00) geantwortet.
Beispiel:
00004711 6 43 53 32 08 0B 01 Abfrage des Messwertes Kanalnummer 1
00014711 8 43 53 32 08 0B 01 00 03 Antwort mit Messwert
Besonderheiten:
Ist die Kanalnummer nicht vorhanden, so wird die originale Anfrage mit DLC=6 und fehlendem Messwert
bestätigt.
Abfrage mittels der Bradcastadresse 0x00 00 00 00 ist möglich, liefert aber keine Zuordenbarkeit zum
Endgerät. Befehl wird mit ursprünglicher Anfrageadresse bestätigt.
Wird immer von Graphical User Interface Prozessor ausgelöst.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 0 |  | 6 | Ziel Geräte-UID |  |  |  | Sub-CMD Status | Kanal- nummer |  |  |
|  |  |  |  |  | High |  |  | Low |  |  |  |  |
| Message Prio | System- befehl | 0 |  | 8 | Absender Geräte-UID |  |  |  | Sub-CMD Status | Kanal- nummer | Konfigurationswert |  |
|  |  |  |  |  | High |  |  | Low |  |  | High | Low |
| Message Prio | System- befehl | 1 |  | 7 | Ziel Geräte-UID |  |  |  | Sub-CMD Status | Kanal- nummer | TRUE / |  |
|  |  |  |  |  | High |  |  | Low |  |  | FALSE |  |
| Message Prio | System- befehl | 1 |  | 8 | Absender Geräte-UID |  |  |  | Sub-CMD Status | Kanal- nummer | Messwert |  |
|  |  |  |  |  | High |  |  | Low |  |  | High | Low |

## 2.13 Befehl: Gerätekennung
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
Kennung (0x0C)
Format:
Beschreibung:
Für Geräte mit S88 Bus / Rückmeldebus und Automatisierungsmodule:
Setzen oder Mitteilen einer 16 Bit Kennung zur Bildung eindeutiger Automatik-UID.
Wird der Befehl mit fehlendem Gerätekenner gesendet, so wird nach einer gültigen Kennung gefragt.
Wird der Befehl mit Gerätekenner gesendet, so setzt dieser Befehl die Kennung.
Die Master - Zentrale weist den Endgeräten die Geräte - Kennung beim Systemstart jeweis zu. Eine
Resetfeste Speicherung findet in den Geräten nicht statt.
Der Master -Zentrale speichert sich eine Liste mit allen bekannten Geräten im System, sowie deren
NickNames als .cs2 Konfigurationsdatei.
Besonderheiten:
Systemkenner mit dem Wert "0" oder 0xFFFF" sind ungültig und sollten in dem Graphical User Interface
Prozessor zu einer Meldung zur Eingabe einer gültigen Kennung führen.
Weiteres siehe Erläuterung der „Automatik-UID“.

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 0 |  | 5 | Ziel Geräte-UID |  |  |  | Sub-CMD Kennung |  |  |  |
|  |  |  |  |  | High |  |  | Low |  |  |  |  |
| Message Prio | System- befehl | 0 |  | 7 | Ziel Geräte-UID |  |  |  | Sub-CMD Kennung | System - Kenner |  |  |
|  |  |  |  |  | High |  |  | Low |  | High | Low |  |
| Message Prio | System- befehl | 1 |  | 7 | Ziel Geräte-UID |  |  |  | Sub-CMD Kennung | System - Kenner |  |  |
|  |  |  |  |  | High |  |  | Low |  | High | Low |  |

## 2.14 Befehl: System Reset
Kennung:
Systembefehl (0x00, in CAN-ID: 0x00)
Sub-CMD:
Set UID (0x80)
Format:
Beschreibung:
Zurücksetzen des Gerätes.
Besonderheiten:

| Prio | Command | Resp. | Hash | DLC | D-Byte 0 | D-Byte 1 | D-Byte 2 | D-Byte 3 | D-Byte 4 | D-Byte 5 | D-Byte 6 | D-Byte 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2+2 Bit | 8 Bit | 1 Bit | 16 Bit | 4 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit | 8 Bit |
| Message Prio | System- befehl | 0\\\|1 |  | 6 | Ziel Geräte-UID |  |  |  | Sub-CMD Reset | Reset-Ziel |  |  |
|  |  |  |  |  | High |  |  | Low |  |  |  |  |
