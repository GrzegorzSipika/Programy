import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os

class MonitorFolderHandler(FileSystemEventHandler):
    def __init__(self, source_folder, destination_folder):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.counter = self.znajdz_najwiekszy_numer() + 1  # Zaczynamy od największego numeru + 1
        self.current_folder_count = 0

    def znajdz_najwiekszy_numer(self):
        existing_folders = [name for name in os.listdir(self.destination_folder) if os.path.isdir(os.path.join(self.destination_folder, name))]
        existing_numbers = [int(name) for name in existing_folders if name.isdigit()]
        return max(existing_numbers, default=0)

    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.lower().endswith(".jpg"):
            print(f"Nowy plik JPG: {event.src_path}")
            self.przenies_do_docelowej_lokalizacji(event.src_path)

    def przenies_do_docelowej_lokalizacji(self, source_path):
        file_name = os.path.basename(source_path)
        folder_name = str(self.counter)
        destination_folder_path = os.path.join(self.destination_folder, folder_name)
        
        # Unikalna nazwa pliku na podstawie rodzaju zdjęcia
        if self.current_folder_count == 0:
            destination_path = os.path.join(destination_folder_path, f"{folder_name}_a.jpg")
        else:
            destination_path = os.path.join(destination_folder_path, f"{folder_name}_b.jpg")

        try:
            if not os.path.exists(destination_folder_path):
                os.makedirs(destination_folder_path)

            shutil.move(source_path, destination_path)
            print(f"Przeniesiono plik do: {destination_path}")

            self.current_folder_count += 1

            # Sprawdzanie czy dodano już 2 pliki do bieżącego folderu
            if self.current_folder_count == 2:
                # Zwiększ licznik dla następnego folderu
                self.counter += 1
                self.current_folder_count = 0
        except Exception as e:
            print(f"Błąd podczas przenoszenia pliku: {e}")

def monitoruj_folder(source_folder, destination_folder):
    event_handler = MonitorFolderHandler(source_folder, destination_folder)
    observer = Observer()
    observer.schedule(event_handler, path=source_folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    source_folder = "D:/Magisterka/Wyniki ankiet/a"
    destination_folder = "D:/Magisterka/Wyniki ankiet/b"

    if not os.path.exists(source_folder):
        print(f"Podana ścieżka do źródłowego folderu nie istnieje: {source_folder}")
    elif not os.path.exists(destination_folder):
        print(f"Podana ścieżka do docelowego folderu nie istnieje: {destination_folder}")
    else:
        monitoruj_folder(source_folder, destination_folder)
