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

![Adressierungs-Sequenz](https://kroki.io/plantuml/svg/eNp90bEKgzAQBuA9T3G4lg65bA5FSZbSQgsinVOTIWCtaPT5a6opaaqdAvf_3BeSrLeys8OjJu10msq0srGQcN3YTtZQNsYmIHvg5XdB6NFUGug7FHQ1xDnE1ZDNISOEl7A_TEAK16Gu4U4RzpfbMhY0hSNyKNw1YQe5Up3ue0hoQmRlzSitdr6gvl3YZ6d9b5m75W5Lzk--iRGndLjO67ihY6gjEejbkY4_-txkf3T86GxDZ6HOiGC-Heks1kNmevlMN8p9_QvzcZM1)

### Geräte-Identifikatoren
Die Identifikation des Befehlstyps erfolgt über die Bits 5, 6 und 7 der Geräteadresse. Die eigentliche Geräteadresse (0-15) liegt in den Bits 1-4. Bit 0 ist meist 0.

| Typ | Bit 7 | Bit 6 | Bit 5 | Binär-Format |
| :--- | :---: | :---: | :---: | :--- |
| Zentraleinheit | 1 | 1 | 1 | `1111 1110` |
| Lokomotivbefehl | 0 | 0 | 0 | `000X XXX0` |
| Magnetartikelbefehl | 0 | 0 | 1 | `001X XXX0` |
| Zusatzfunktionen (f1-f4) | 0 | 1 | 0 | `010X XXX0` |

### Adress-Byte Struktur
![Adress-Byte](https://kroki.io/wavedrom/svg/eNqrVlAqSk1XslKI5lJQqFbKS8xNBXKUDJR0FJSSMkuKgRxDIDOxpKQIJB6UWpxaVJaaolSrg6LeMSWlKLW4WEHDJ9hJT8832EkTyQATJANcUssyk1MVYOoN9PQMTdEN83RB0myMpNnAwEDBFqY3My9dqZYrFiidnJ-XlgnyQzVMkwVQNCcxLxXs_NpaLgA8tz9J)

## Protokoll-Spezifikation und Befehlssätze

### Kommunikationsfluss
Befehle werden in Paketen von 3 bis 4 Bytes übertragen. Da es sich um ein Multi-Master-System handelt, übernimmt das sendende Gerät temporär die Master-Rolle.

![Kommunikationsfluss](https://kroki.io/plantuml/svg/eNp9klFLwzAUhd_zKy57amEO1D31Qba1gsMNh6H4HNPbLpglJb2d7N9701VxIntKuDnf6elJFh2pQP3BipZXo02rHMFEoqswQCKtOiKoDraqIwzpJO7lpTZHR0FZKJ0hSM7CQRbZM5GXQjhPCP7IZ3LKgwzWlUWQpHicyHwzBVks4ck0-1RIuHkAmcGut3YYb17eWBSjjofRYHVi9DaDV-QohlPAsqoCdh0keZmKvBxdlvnzH-gug_EPf4gCj0bjVeo-g0KRggRnzQwK1P7b4So2v8Bki1j9p-e9JN_CylCM4_v3oR6e1J47OzmdihGL1rvgdQy-dh2FXpPx7pep_nD-02LV4CH2smWlarjn-RCpS8-3EbhsAl8Pho967yF-iW-kj761FwsuKb6NL4gFpQI=)

### Lokomotivbefehle (Standard H0-Modus)
Wird verwendet für Standard-Motorola-Decoder (MM1).

* **Paketlänge:** 4 Bytes (Empfänger, Sender, Decoder-Adresse, Datenbyte)
* **Adressbereich:** 00 bis 79 (Adresse 80 wird als 00 übertragen)

![Lokbefehl H0](https://kroki.io/wavedrom/svg/eNpdj8sKwjAQRff9iiErCyE2PkCELCzSlYpYd-Ii1rEGNaltKkjpv5sWhOhuXvfcOw2QEnMyh0MA0BAtH-gakhaI5-HWVDBYpTFj6zQOCQVyUrZy-4krpbVldxqJ1JqCAhdLVVIYMcanoteTlv5AE4_APUJS68wqo52Xyq82_Nft3wV60rFvHkVih88aK-sScC42mEurXgiL7Eba4OhuM6Mvqnux-RJmbnqXGvsgbRt8AHspSKQ=)

### Lokomotivbefehle (Erweitertes Motorola-Format / MM2)
Unterstützt absolute Fahrtrichtung und erzwungene Adressübernahme.

![Lokbefehl MM2](https://kroki.io/wavedrom/svg/eNpdkE2LwjAQhu_9FUNOLYSaqAuLkEOL9KSybPcgyB5iOtagJlqzyFL63526LFRP8_28L9MCa7BmM9hEAC1z-oRUsPKMWI0-_BXiRZmn6bLME8aBbW240nxKqQ6h6VeFmqOujt4cOEg1tw2HcZrKN_VgsI4_gYsBRQ4oxY8zwXpHerbeh-T17uv3jIPTydCAkOoTL6Qu1oosZ-YA8XomVK7_PBW3KqEohVphnfU9QXnhG4Osi74JZbzb2f4L7b_AO3WP2uHDZ9dFd-YyUWM=)

### Zusatzfunktionen (f1 bis f4)
Befehle zur Steuerung der Sonderfunktionen.

![Funktionsbefehl](https://kroki.io/wavedrom/svg/eNqrVlAqSk1XslKI5lJQqFbKS8xNBXKU0gyVdBSUkjJLioE8w1odVEkjfJLG-CRN8EiG5pUWp6YgKTABMhNLSopAko455YmVxQoGSrVcsUDh5Py8tEyQs6thii2AojmJeakQk2u5AALGOdw=)

### Magnetartikelbefehle (Weichen/Signale)
* **Paketlänge:** 3 Bytes
* **Datenbyte:** Enthält Ausgangsnummer (Bit 1-2), Richtung (Bit 0), Power (Bit 3) und Sektionsadresse (Bit 4-5).

![Magnetartikelbefehl](https://kroki.io/wavedrom/svg/eNp1kM0KgkAQgO8-xTBnEa1LBB4EoeNG0Sk6bO4YC7rG7oqE7Ls3BoH9eJu_b75hRkBLN9zCOQIY0ciWOMFSW4wBr9o7TjMOpfd26qT5gVQMWb6zRAZD_MGJ3s-41YwrqeoUWeCJe-8hTZL1N7wflqWiriep-DEeqVowcsfrzkChlCXn_ipPpnekFhYUzSAfzGGILlyuOlPr6VXje3jD1UYaep0bQvQEMkhb2w==)

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
