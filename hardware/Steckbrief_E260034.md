# Steckbrief: Märklin E260034 mtc21 Trägerleiterplatte

Die **Märklin E260034** ist eine Trägerleiterplatte mit einer 21-poligen Schnittstelle (mtc21), die in modernen Märklin-Lokomotiven zur Aufnahme von Digital-Decodern dient.

## Technische Daten

| Merkmal | Spezifikation |
| :--- | :--- |
| **Typ** | Trägerleiterplatte (Adapterplatine) |
| **Schnittstelle** | 21-polig mtc (NEM 660 / VHDM Standard) |
| **Teilenummer** | E260034 (Ersatzteilnummer) |
| **PCB-Kennung** | SE150602A |
| **Anwendung** | Einbau in H0-Lokomotiven zur Umrüstung oder als Ersatz |
| **Anschlüsse** | Lötpads für Motor, Gleis, Licht und Zusatzfunktionen (AUX), SUSI-Schnittstelle, Lautsprecher |

## Pinbelegung (mtc21 Standard)

Die Platine folgt der standardmäßigen 21-poligen Belegung für mtc-Schnittstellen:

1.  **Motor rechts** (Anschluss zum Motor)
2.  **Motor links** (Anschluss zum Motor)
3.  **Gleis links / Masse** (Radschleifer)
4.  **Gleis rechts / Mittelschleifer** (Schleifer)
5.  **Licht vorne** (AUX 0 f)
6.  **Licht hinten** (AUX 0 r)
7.  **AUX 1** (Zusatzfunktion 1)
8.  **AUX 2** (Zusatzfunktion 2)
9.  **V+ (Decoder)** (Gemeinsamer Rückleiter für Funktionen)
10. **GND (Decoder)**
11. **Hall-Sensor / Index-Pin** (Meist zur mechanischen Kodierung)
12. **Speaker +** (Lautsprecheranschluss)
13. **Speaker -** (Lautsprecheranschluss)
14. **AUX 3** (Verstärkt oder unverstärkt, modellabhängig)
15. **AUX 4** (Verstärkt oder unverstärkt, modellabhängig)
... (weitere Pins gemäß NEM 660)

## Details zur Variante SE150602A

Diese spezifische Ausführung der E260034 zeichnet sich durch zusätzliche Steckverbinder und eine klare Beschriftung der Lötpads aus.

![Märklin E260034 SE150602A](https://github.com/user-attachments/assets/7669dbc4-10a3-449d-ac80-4da6803cfa5e)

### Steckverbinder
*   **Lautsprecher (Lautsprecher-Symbol):** 2-poliger Miniatur-Steckverbinder (JST SH 1.0mm oder ähnlich) oben links.
*   **SUSI:** 4-poliger Miniatur-Steckverbinder (oben mittig) für Sound-Erweiterungsmodule.

### Lötpad-Belegung

Die folgende Tabelle beschreibt die Lötpads und die standardmäßig verwendeten Kabelfarben gemäß der Abbildung:

| Pad-Label | Kabelfarbe | Funktion | Beschreibung |
| :--- | :--- | :--- | :--- |
| **B/GR** | Rot | Bahn / Mittelschleifer | Stromabnahme (Mittelschleifer) |
| **0/GL** | Braun | 0 / Masse | Rückleitung über Schienen (Radschleifer) |
| **MV-** | Grau | Motor (-) | Motoranschluss |
| **MR+** | Blau | Motor (+) | Motoranschluss |
| **+Ub** | Orange | Decoder V+ (U+) | Gemeinsamer Rückleiter für Funktionen |
| **LV-** | Weiß | Licht Vorne | Lichtausgang vorne (geschaltete Masse) |
| **LR** | Gelb | Licht Hinten | Lichtausgang hinten (geschaltete Masse) |
| **+Ub** | Orange | Decoder V+ (U+) | Zweiter Anschlusspunkt für Rückleiter |
| **+Uli** | - | Licht V+ | (Zusatzversorgung Licht) |
| **AUX1** | Grün | Funktion 1 | Zusatzfunktion 1 |
| **AUX2** | Violett | Funktion 2 | Zusatzfunktion 2 |
| **AUX3** | - | Funktion 3 | Zusatzfunktion 3 |
| **AUX4** | - | Funktion 4 | Zusatzfunktion 4 |
| **GND** | Braun | Masse (Decoder) | Gemeinsames Bezugspotenzial (Elektronik-Masse) |
| **+5V** | - | 5V DC | Niederspannungsversorgung für Peripherie |
| **IN1, IN2, IN3** | - | Eingänge | Sensor-Eingänge (z.B. Radsynchroner Sound), oben rechts |

## Besonderheiten der E260034

*   **Bauform:** Kompakte Ausführung, optimiert für den Bauraum in spezifischen Märklin-Modellen.
*   **Bestückung:** Mit Lötpads und zusätzlichen Steckverbindern (SUSI, Speaker) für eine flexible Verdrahtung.
*   **Kompatibilität:** Geeignet für alle Märklin mLD, mLD3, mSD und mSD3 Decoder sowie mtc21-Decoder anderer Hersteller (ESU, Zimo etc.).

## Montagehinweise

*   Die Platine wird mechanisch im Lokchassis befestigt.
*   Der Decoder wird auf die 21-polige Stiftleiste aufgesteckt.
*   Es ist auf die korrekte Ausrichtung des Decoders zu achten (Index-Pin auf Position 11).
