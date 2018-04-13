# ADS Testing Framework

Primitives Testframework

## Usage

* Es gibt 3 Ordner
	* `framework`: Hier den Ordner reinpacken, den Studenten runterladen. Wichtig ist das `E[0-9]` am Ende des Namens
	* `solution`: Hier den Ordner mit korrekten Lösungen reinpacken. Sollte auch auf `E[0-9]` enden
	* `submission`: Hier einen Ordner mit den `matrNr.java`Files reinpacken. Ordnername sollte ebenfalls auf `E[0-9]` enden. 

Anschließend mit `./python tester.py E1` starten. `E1` ist optional - wenn man keines angibt, sollte das Programm nachfragen.

Ausgabe ist dann für jeden Studenten ca. so:

```1231.java (123ms): Identical: [korrekte Inst. ], Mismatch: [falsche Inst.], Not found: [nicht gefundene Inst.]```


