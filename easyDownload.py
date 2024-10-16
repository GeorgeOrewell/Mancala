import os
import time
import logging
import shutil
import sys
from datetime import timedelta
import yt_dlp

# Logging einrichten
logging.basicConfig(filename="download_log.txt", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_message(message):
    """Gibt eine Nachricht aus und speichert sie im Log."""
    print(message)
    logging.info(message)

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

def input_urls():
    """Nimmt Nutzereingaben von URLs entgegen."""
    urls = []
    print("Gib die URLs zum Download ein. Bestätige jede URL mit Enter. Gib 'f' ein, um die Eingabe zu beenden.")
    while True:
        url = input("URL: ").strip()
        if url.lower() == 'f':
            break
        elif url:
            urls.append(url)
    if not urls:
        log_message("Keine URLs eingegeben.")
        return None
    log_message(f"{len(urls)} URLs eingegeben.")
    return urls

def download_videos_from_input(urls, downloaded_urls):
    """Lädt die eingegebenen URLs mit yt-dlp herunter."""
    if not urls:
        return None

    log_message(f"Starte den Download von {len(urls)} URLs...")
    downloaded_files = {}

    for idx, url in enumerate(urls):
        if url in downloaded_urls:
            log_message(f"({idx + 1}/{len(urls)}) URL bereits heruntergeladen: {url}. Überspringe...")
            continue

        log_message(f"({idx + 1}/{len(urls)}) Starte Download: {url}")
        try:
            ydl_opts = {
                'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',  # Bis 720p
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
                downloaded_files[url] = filename
                log_message(f"Download abgeschlossen: {filename}")
                log_message(f"Download abgeschlossen: {url}")

                downloaded_urls.add(url)
        except Exception as e:
            log_message(f"Fehler beim Download von {url}: {str(e)}")

    return downloaded_files

def move_downloaded_videos(target_directory, downloaded_files):
    """Bewegt alle heruntergeladenen Videos in das angegebene Verzeichnis."""
    log_message(f"Verschiebe heruntergeladene Dateien in das Verzeichnis: {target_directory}")

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        log_message(f"Verzeichnis {target_directory} erstellt.")

    for url, filename in downloaded_files.items():
        log_message(f"Verschiebe {filename} nach {target_directory}")
        shutil.move(filename, os.path.join(target_directory, filename))

    log_message("Alle Dateien wurden verschoben.")

def browse_directories(starting_directory='./storage/downloads/'):
    """Ermöglicht das Navigieren durch Verzeichnisse und wählt das Zielverzeichnis aus."""
    current_directory = os.path.abspath(starting_directory)

    while True:
        return current_directory

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

    # Eingabe der URLs durch den Benutzer
    urls = input_urls()

    if urls:
        downloaded_urls = load_downloaded_urls()
        downloaded_files = download_videos_from_input(urls, downloaded_urls)

        if downloaded_files:
            # Durch Verzeichnisse navigieren, um das Zielverzeichnis auszuwählen
            target_directory = browse_directories()
            # Heruntergeladene Dateien verschieben
            move_downloaded_videos(target_directory, downloaded_files)

    log_message("Alle Downloads abgeschlossen und Dateien verschoben.")

if __name__ == "__main__":
    main()