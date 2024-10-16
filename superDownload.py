import os
import time
import logging
import shutil
import sys
from datetime import datetime, timedelta
import yt_dlp

# Logging einrichten
logging.basicConfig(filename="download_log.txt", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_message(message):
    """Gibt eine Nachricht aus und speichert sie im Log."""
    print(message)
    logging.info(message)

def find_files():
    """Sucht nach .dl, .lst, .txt und .yt Dateien im aktuellen Verzeichnis."""
    log_message("Suche nach passenden Dateien im Verzeichnis...")
    valid_extensions = ['.dl', '.lst', '.txt', '.yt']
    files = [f for f in os.listdir() if os.path.isfile(f) and any(f.endswith(ext) for ext in valid_extensions)]
    if not files:
        log_message("Keine Dateien mit URLs gefunden.")
        return None
    log_message(f"{len(files)} Dateien gefunden: {files}")
    return files

def select_file(files):
    """Lässt den Benutzer eine Datei aus der Liste auswählen."""
    log_message("Bitte wähle eine Datei aus:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")
    choice = int(input("Gib die Zahl der Datei ein, die du verwenden möchtest: ")) - 1
    selected_file = files[choice]
    log_message(f"Ausgewählte Datei: {selected_file}")
    return selected_file

def load_downloaded_urls():
    """Lädt bereits heruntergeladene URLs aus der Logdatei."""
    downloaded_urls = set()
    if os.path.exists("download_log.txt"):
        with open("download_log.txt", 'r') as log_file:
            for line in log_file:
                if "Download abgeschlossen:" in line:
                    url = line.split("Download abgeschlossen: ")[-1].strip()
                    downloaded_urls.add(url)
    return downloaded_urls

def format_time(seconds):
    """Wandelt Sekunden in das Format xxh xxm xxs um."""
    seconds = round(seconds)  # Auf ganze Sekunden runden
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"

def clear_line():
    """Löscht die aktuelle Zeile im Terminal."""
    sys.stdout.write('\r')
    sys.stdout.flush()

def progress_hook(d):
    """Hook für den Fortschritt von yt-dlp."""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').strip()
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('eta', None)

        if eta is not None:
            eta = format_time(eta)
        else:
            eta = "Unbekannt"

        clear_line()
        print(f"Fortschritt: {percent} | {speed} | Restzeit: {eta}", end='')
    elif d['status'] == 'finished':
        clear_line()
        log_message("Download abgeschlossen, Verarbeitung...")

def download_videos_from_file(file, downloaded_urls):
    """Liest URLs aus der Datei und lädt sie mit yt-dlp herunter."""
    with open(file, 'r') as f:
        lines = f.readlines()

    url_categories = {}
    current_category = None

    for line in lines:
        line = line.strip()
        if line.startswith('#'):  # Kommentarzeilen als Kategorien erkennen
            current_category = line[1:].strip()  # Kategorie ist der Text nach '#'
            if current_category not in url_categories:
                url_categories[current_category] = []
        elif line and current_category:
            url_categories[current_category].append(line)

    if not url_categories:
        log_message(f"Keine URLs in {file} gefunden.")
        return None

    log_message(f"URLs in {len(url_categories)} Kategorien gefunden. Starte den Download...")

    downloaded_files = {}  # Dictionary, um URLs mit Dateinamen zu verknüpfen
    for category, urls in url_categories.items():
        log_message(f"\nKategorie: {category} - {len(urls)} URLs")
        for idx, url in enumerate(urls):
            if url in downloaded_urls:
                log_message(f"({idx + 1}/{len(urls)}) URL bereits heruntergeladen: {url}. Überspringe...")
                continue

            log_message(f"({idx + 1}/{len(urls)}) Starte Download: {url}")
            try:
                ydl_opts = {
                    'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',  # Bis 720p, aber nichts unter 380p
                    'noplaylist': True,
                    'ignoreerrors': True,
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',  # Optionale Konvertierung zu MP4
                    }],
                    'outtmpl': '%(title)s.%(ext)s',  # Speichern als Titel der Datei
                    'logger': logging.getLogger(),
                    'progress_hooks': [progress_hook]  # Hook für Fortschritt
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info_dict)
                    downloaded_files[url] = filename  # URL mit Dateinamen verknüpfen
                    log_message(f"Download abgeschlossen: {filename}")
                    log_message(f"Download abgeschlossen: {url}")

                    downloaded_urls.add(url)  # URL zu den heruntergeladenen hinzufügen
            except Exception as e:
                log_message(f"Fehler beim Download von {url}: {str(e)}")

    return url_categories, downloaded_files

def move_downloaded_videos(target_directory, url_categories, downloaded_files):
    """Bewegt alle heruntergeladenen Videos in das angegebene Verzeichnis und erstellt Kategorieordner."""
    log_message(f"Verschiebe heruntergeladene Dateien in das Verzeichnis: {target_directory}")

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        log_message(f"Verzeichnis {target_directory} erstellt.")

    for category, urls in url_categories.items():
        category_dir = os.path.join(target_directory, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
            log_message(f"Kategorieordner {category_dir} erstellt.")

        for url in urls:
            if url in downloaded_files:
                filename = downloaded_files[url]
                log_message(f"Verschiebe {filename} nach {category_dir}")
                shutil.move(filename, os.path.join(category_dir, filename))

    log_message("Alle Dateien wurden verschoben.")


def browse_directories(starting_directory='./storage/downloads/'):
    """Ermöglicht das Navigieren durch Verzeichnisse und wählt das Zielverzeichnis aus."""
    current_directory = os.path.abspath(starting_directory)

    while True:
        print(f"\nAktuelles Verzeichnis: {current_directory}")
        directories = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d))]
        directories.insert(0, '..')  # Option zum Zurücknavigieren

        print("\nVerzeichnisse:")
        for idx, directory in enumerate(directories):
            print(f"{idx}: {directory}")

        choice = input("\nWähle ein Verzeichnis (Nummer eingeben) oder 'f' zum Bestätigen: ").strip()

        if choice == 'f':
            return current_directory
        elif choice.isdigit() and 0 <= int(choice) < len(directories):
            current_directory = os.path.join(current_directory, directories[int(choice)])
        else:
            print("Ungültige Eingabe, bitte versuche es erneut.")

def main():
    """Hauptfunktion des Skripts."""
    log_message("Skript gestartet...")

    #files = find_files()
    #if not files:
    #    return

    #selected_file = select_file(files)
    selected_file = "download.lst"

    downloaded_urls = load_downloaded_urls()

    if not os.path.exists('download.lst'):
        with open('download.lst', 'w') as f:
            pass  # Leere Datei erstellen, wenn sie nicht existiert

    os.system('nano download.lst')

    url_categories, downloaded_files = download_videos_from_file(selected_file, downloaded_urls)

    if url_categories and downloaded_files:
        # Durch Verzeichnisse navigieren, um das Zielverzeichnis auszuwählen
        target_directory = browse_directories()
        # Hier wird `downloaded_files` zusätzlich übergeben
        move_downloaded_videos(target_directory, url_categories, downloaded_files)

    log_message("Alle Downloads abgeschlossen und Dateien verschoben.")

if __name__ == "__main__":
    main()