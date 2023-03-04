# firebird

## Voraussetungen!
Firebird muss bei euch lokal installiert sein.  
Außerdem müsst ihr bei der Erstellung der Datenbank die default Werte aus der Anleitung angegeben haben.  
Der Benutzername muss also "SYSDBA" und das Passwort "masterkey" sein.

## Erstellen eines 32bit Python virtual envs (mit Conda)

Da wir mit einer 32bit Version von Firebird arbeiten, brauchen wir auch eine 32bit Python Version.
Hierfür müsst ihr zunächst euer Anaconda Prompt öffnen. Als nächstes legen wir eine temporäre Umgebungsvariable an.  
Mithilfe dieser weiß Anaconda, dass wir eine 32bit Umgebung erstellen wollen. Hierfür folgendes Kommando ausführen:

```bash
set CONDA_FORCE_32BIT=1
```

Diese Umgebungsvariable ist nur solange gültig, wie die Konsole geöffnet ist.  
D.h. wenn die Konsole geschlossen und dann neu geöffnet wird, werden wieder 64bit Umgebungen erstellt.  
Nun erstellen wir eine neue 32bit Umgebung mit folgendem Befehl:

```bash
conda create -n env_32bit python=3.9
```

Der Name ist hierbei lediglich so gewählt, dass man die 32bit Umgebung erkennt. Ihr könnt die Umgebung aber auch beliebig anders benennen.  
Zum Schluss aktivieren wir die Umgebung mit folgendem Befehl:

```bash
conda activate env_32bit
```

## Installation

Navigiert in euer gewünschtes Verzeichnis und klont anschließend das Projekt mit folgendem Befehl:

```bash
git clone
```

Navigiert in den Projektordner.

```bash
cd firebird
```

Installiert die wheel Datei im dist Ordner.

```bash
pip install dist/firebird-0.0.1-py3-none-any.whl
```

## Anwendung

Um das Paket nutzen zu können müsst ihr wissen wo eure Datenbank-Datei (.FDB) und euer Client (fbclient.dll) liegen.  
Bei mir lag die Client Datei z.B. direkt im Installationsordner von Firebird_4_0.  
Den Pfad für die .FDB solltet ihr beim Erstellen der Datenbank selbst ausgewählt haben.  
Achtet bitte darauf, wenn ihr Pfade mit Backslashes benutzt, daraus einen Raw-String zu machen um mögliche Probleme zu vermeiden.  
Die Grundlage bildet die Firebird_Engine Klasse. Wir müssen eine Instanz davon erstellen um eine Verbindung mit der Datenbank herzustellen.  

```python
from firebird import Firebird_Engine

# Beispiel für eine Instanz der Klasse Firebird_Engine
engine = Firebird_Engine(db_path="D:/Dateien/Firebase/FAHRZEUGE.FDB", client_path=r"D:\Programme\Firebird_4_0\fbclient.dll")
```
Wenn ihr das ausführt solltet ihr bei einer erfolgreichen Verbindung "Successfully connected to database" ausgegeben bekommen.  
Derzeit gibt es drei Hauptfunktionen im Paket, die im Folgenden näher erläutert werden.  
In den nachfolgenden Beispielen wird die Instanz "engine" verwendet, die im ersten Beispiel erstellt wurde.  

### DataFrame

Mit der DataFrame Methode können Datenbankabfragen als Pandas DataFrames zurückgegeben werden.  
Dabei wird die query als String übergeben.  

```python

# Beispiel für eine Datenbankabfrage
table = engine.DataFrame("SELECT * FROM Kunde")
```

### drop_all

Mit der drop_all Methode kann eine Datenbank schnell bereinigt werden.  
Dabei werden alle erstellten Tabellen und Domains entfernt.  

```python

# Beispiel für Bereinigung der Datenbank
engine.drop_all()
```

### run_query

Die run_query Methode ermöglicht es SQL-Skripte laufen zu lassen, die auf die Datenbank schreiben wollen.  
Bspw. kann damit das gesamte Skript für die zweite Aufgabe aus unserer Vorlesung ausgeführt werden. Auch hier wird die query als String übergeben.  
Es ist außerdem möglich das SQL-Skript in einer seperaten .sql Datei abzuspeichern und dann im Nachgang als String einzulesen.

```python

# Pfad zum Skript übergeben
with open('fahrzeuge.sql', 'r') as text:
    query = text.read()

engine.run_query(query)
```


