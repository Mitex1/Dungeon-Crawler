✨ Key Features

    Grafische Benutzeroberfläche: Ein eigenständiges Spielfenster, erstellt mit Python's tkinter.
    Endloser Dungeon: Erkunde prozedural generierte Etagen. Kein Spieldurchlauf ist wie der andere!
    RPG-System: Sammle Erfahrungspunkte, steige im Level auf, verteile Attributspunkte und lerne neue, mächtige Fähigkeiten.
    Drei spielbare Klassen: Wähle zwischen dem standhaften Krieger, dem mächtigen Magier und dem agilen Dieb.
    Umfangreiches Beutesystem: Finde Waffen und Rüstungen in verschiedenen Seltenheitsstufen (Gewöhnlich, Selten, Episch, Legendär), um deinen Charakter zu verbessern.
    Taktische Kämpfe: Tritt gegen vielfältige Gegner an, die über einzigartige Spezialfähigkeiten wie Heilen, Vergiften oder Rüstungsbruch verfügen.
    Zufällige Ereignisse: Entdecke auf deiner Reise nützliche Händler oder riskiere alles an mysteriösen Schreinen, die Segen oder Flüche gewähren können.
    Epischer Bosskampf: Stelle dich der ultimativen Herausforderung auf der letzten Etage.
    Speichern & Laden: Dein Fortschritt kann jederzeit gesichert und später fortgesetzt werden.

⚙️ Systemanforderungen

    Python 3.x

Das ist alles! Es werden keine externen Bibliotheken benötigt. Alle notwendigen Module (Tkinter, random, json, os) sind Teil der Standard-Python-Installation.
🚀 Wie man das Spiel startet

    Stelle sicher, dass du Python 3 auf deinem System installiert hast.
    Speichere den gesamten Spielcode in einer Datei namens dungeon_crawler.py.
    Öffne ein Terminal (oder eine Kommandozeile/PowerShell).
    Navigiere mit dem Befehl cd in das Verzeichnis, in dem du die Datei gespeichert hast. Zum Beispiel:
    Bash

cd C:\Users\DeinName\Documents\PythonGames

Führe das Spiel mit dem folgenden Befehl aus:
Bash

    python dungeon_crawler.py

    Das Spielfenster sollte sich öffnen. Viel Spaß!

🎮 Spielanleitung
Ziel des Spiels

Das Ziel ist es, durch die Etagen des Dungeons abzusteigen, den mächtigen Drachenlord auf Etage 5 zu finden und ihn im Kampf zu besiegen.
Steuerung

    Bewegung: Pfeiltasten (Hoch, Runter, Links, Rechts)
    Heiltrank benutzen: H-Taste
    Manatrank benutzen: M-Taste
    Interaktionen (Kämpfe, Menüs): Mausklicks auf die entsprechenden Buttons.

Das Interface

    Karte (links): Zeigt deine Umgebung. Deine Position ist blau. Unentdeckte Räume sind dunkelgrau, besuchte hellgrau. Besondere Orte (Händler, Treppen, Boss) sind farblich markiert.
    Info-Fenster (rechts oben): Hier siehst du deine Charakterwerte, dein Level, Leben/Mana, Gold und deine aktuell ausgerüsteten Gegenstände.
    Aktions-Fenster (rechts unten): Das Log-Fenster zeigt alle Ereignisse und Kampfnachrichten. Darunter erscheinen kontextabhängige Buttons für Kämpfe, Interaktionen oder Menüs.

Gameplay-Elemente

    Leveln: Besiege Monster, um XP zu erhalten. Bei einem Levelaufstieg werden dein Leben und Mana vollständig aufgefüllt und du erhältst Attributspunkte, die du im Info-Fenster verteilen kannst, sobald die [+]-Buttons erscheinen. Auf Level 5 kannst du zudem eine neue, mächtige Fähigkeit lernen.
    Ausrüstung: Waffen und Rüstungen haben verschiedene Seltenheitsstufen, die farblich im Log markiert sind:
        &lt;span style="color:gray;">Gewöhnlich&lt;/span>
        &lt;span style="color:#3399FF;">Selten&lt;/span>
        &lt;span style="color:#9933FF;">Episch&lt;/span>
        &lt;span style="color:#FF9900;">Legendär&lt;/span>
    Statuseffekte: Achte im Kampf auf Statuseffekte! Gift zieht dir jede Runde Leben ab, während Rüstungsbruch dich anfälliger für Schaden macht.# Dungeon-Crawler
