import os
import logging
from datetime import datetime
from PIL import Image

import threading
import sys

def clean_frames(image):
    grayscale_img = image.convert("L")
    cleaned_img = grayscale_img.point(lambda p: 0 if p < 65 else 255)
    cleaned_img = cleaned_img.convert("RGB")
    logging.info(f"Oczyszczono klatkę")
    return cleaned_img

def is_green(pixel, tolerance=50, target_color=(3, 254, 0)):
    return all(abs(pixel[i] - target_color[i]) < tolerance for i in range(3))

def overlap(x1, y1, w1, h1, x2, y2, w2, h2):
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

def crop_green_frames(image_path, output_dir, max_frames=2, frame_size=(930, 930), tolerance=50, suffix="", lock=None):
    img = Image.open(image_path)
    width, height = img.size

    frame_count = 0
    saved_frames = []

    # Współrzędne prawej krawędzi pierwszej znalezionej ramki
    right_edge_x = None

    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))

            if is_green(pixel, tolerance):
                # Sprawdź, czy obszar o wymiarach frame_size jest w granicach obrazu
                if x + frame_size[0] <= width and y + frame_size[1] <= height:
                    # Jeśli nie ustalono jeszcze współrzędnej prawej krawędzi, to ustaw ją
                    if right_edge_x is None:
                        right_edge_x = x + frame_size[0]

                    # Wytnij obszar o rozmiarze frame_size
                    cropped_img = img.crop((x, y, x + frame_size[0], y + frame_size[1]))

                    # Sprawdź, czy nowa ramka nachodzi na już zapisane ramki
                    overlap_flag = False
                    for frame in saved_frames:
                        if overlap(x, y, frame_size[0], frame_size[1], *frame):
                            overlap_flag = True
                            break

                    if not overlap_flag:
                        # Zapisz wytnięty obszar
                        frame_count += 1
                        output_path = os.path.join(output_dir, f"frame_{frame_count}{suffix}.jpg")
                        
                        cleaned_img = clean_frames(cropped_img)
                        cleaned_img.save(output_path)

                        # Zapisz współrzędne nowej ramki do listy zapisanych ramek
                        saved_frames.append((x, y, frame_size[0], frame_size[1]))

                        logging.info(f"Znaleziono klatkę {frame_count} w {image_path}")

                        if frame_count == max_frames:
                            break

    if frame_count == 0:
        logging.warning(f"Brak zielonych klatek w {image_path}")
    else:
        logging.info(f"Znaleziono i zapisano {frame_count} zielonych klatek w {image_path}")

def process_survey_folder_parallel(folder_path):
    for survey_folder in os.listdir(folder_path):
        survey_folder_path = os.path.join(folder_path, survey_folder)

        if os.path.isdir(survey_folder_path):
            current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_directory = "D:/Magisterka/Wyniki ankiet/Skany"
            log_filename = f"log_{current_datetime}.txt"
            log_path = os.path.join(log_directory, log_filename)

            output_directory = os.path.join(survey_folder_path, f'wyniki_ankiety_{survey_folder}')
            os.makedirs(output_directory, exist_ok=True)

            logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

            logging.info(f"Przetwarzanie folderu z ankietą: {survey_folder}")
            logging.info(f"Katalog wyjściowy: {output_directory}")

            # Dodanie pliku tekstowego o strukturze "Label x.txt"
            label_filename = f"Label {survey_folder}.txt"
            label_path = os.path.join(survey_folder_path, label_filename)

            with open(label_path, 'w') as label_file:
                label_file.write("Ankieta 1\nWiek - \nPłeć - \nMiejsce zamieszkania - \nWykształcenie - ")

            logging.info(f"Dodano plik z etykietą: {label_filename}")

            image_path_a = os.path.join(survey_folder_path, f"{survey_folder}a.jpg")
            image_path_b = os.path.join(survey_folder_path, f"{survey_folder}b.jpg")

            if os.path.exists(image_path_a) and os.path.exists(image_path_b):
                logging.info(f"Ścieżka obrazu A: {image_path_a}")
                logging.info(f"Ścieżka obrazu B: {image_path_b}")

                # Wykorzystaj threading.Lock() do synchronizacji wątków
                lock = threading.Lock()

                # Przekazanie lock do funkcji crop_green_frames
                # Przekazanie lock do funkcji crop_green_frames
                thread_a = threading.Thread(target=crop_green_frames,
                                            args=(image_path_a, output_directory, 2, (960, 960), 50, "_a", lock))
                thread_b = threading.Thread(target=crop_green_frames,
                                            args=(image_path_b, output_directory, 2, (960, 960), 50, "_b", lock))
                thread_a.start()
                thread_b.start()

                # Oczekiwanie na zakończenie obu wątków przed kontynuacją
                thread_a.join()
                thread_b.join()

            elif os.path.exists(image_path_a):
                logging.warning("Brak obrazu B dla folderu z ankietą. Pomijanie przetwarzania.")
            elif os.path.exists(image_path_b):
                logging.warning("Brak obrazu A dla folderu z ankietą. Pomijanie przetwarzania.")
            else:
                logging.error("Brak obu plików obrazów dla folderu z ankietą. Pomijanie przetwarzania.")

    logging.info("Zakończono przetwarzanie wszystkich ankiet")
    sys.exit()

if __name__ == "__main__":
    surveys_path = "D:/Magisterka/Wyniki ankiet/Skany"
    process_survey_folder_parallel(surveys_path)
