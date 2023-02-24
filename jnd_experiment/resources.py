import glob
import csv

# instructions
pitch_FL_text = """
Bitte hör ganz genau hin.
Du wirst nun dreimal denselben Namen hören.
Ein Name ist immer anders als die beiden anderen.
Manchmal ist der erste Name (1) anders.
Manchmal ist der dritte Name (3) anders.
Wenn du denkst, der erste Name ist anders, als die beiden anderen, drücke '<- 1' (links).
Wenn du denkst, der dritte Name ist anders, als die beiden anderen, drücke '3 ->' (rechts).
Drücken Sie auf den weiter-Button, sobald Sie bereit sind
"""

pause_text = """
Bitte hör ganz genau hin."
Du wirst nun dreimal eine Wortgruppe hören.
Eine Wortgruppe ist immer anders als die beiden anderen.
Manchmal ist die erste Wortgruppe (1) anders.
Manchmal ist die dritte Wortgruppe (3) anders.
Wenn du denkst, die erste Wortgruppe ist anders, als die beiden anderen, drücke '<- 1' (links).
Wenn du denkst, die dritte Wortgruppe ist anders, als die beiden anderen, drücke '3 ->' (rechts).
Drücken Sie auf den weiter-Button, sobald Sie bereit sind
"""

