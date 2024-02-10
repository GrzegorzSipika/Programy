import os
import logging
from datetime import datetime
from PIL import Image
import cv2
import threading
import sys
import numpy as np

def setup_logging():
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_directory = "D:/Magisterka/Wyniki ankiet/Skany"
    log_filename = f"log_{current_datetime}.txt"
    log_path = os.path.join(log_directory, log_filename)
    logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_green(pixel, tolerance=30, target_color=(3, 254, 0)):
    return all(abs(int(pixel[i]) - target_color[i]) < tolerance for i in range(3) if isinstance(pixel[i], (int, float)))

def overlap(x1, y1, w1, h1, x2, y2, w2, h2):
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)


def clean_frames(image):
    # Konwersja do skali szarości i czyszczenie obrazu mogą być różne w zależności od potrzeb
    grayscale_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, cleaned_img = cv2.threshold(grayscale_img, 85, 255, cv2.THRESH_BINARY)
    return cleaned_img

def find_green_frames(image_path, output_dir, target_frame_count=4, frame_size=(930, 930), suffix=""):
    img = cv2.imread(image_path)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([36, 25, 25])
    upper_green = np.array([86, 255, 255])

    mask = cv2.inRange(hsv_img, lower_green, upper_green)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) < target_frame_count:
        logging.warning(f"Found less than {target_frame_count} contours, some frames might be missed.")
        return

    # Sortuj kontury według ich powierzchni (od największych do najmniejszych) i ogranicz do pierwszych 4
    contours_sorted_by_area = sorted(contours, key=cv2.contourArea, reverse=True)[:target_frame_count]

    # Określ pozycje konturów
    positions = [(cv2.boundingRect(cnt)[0], cv2.boundingRect(cnt)[1]) for cnt in contours_sorted_by_area]

    # Sortuj kontury na podstawie ich pozycji, aby uzyskać kolejność: lewa górna, prawa górna, lewa dolna, prawa dolna
    contours_sorted = sorted(contours_sorted_by_area, key=lambda cnt: (cv2.boundingRect(cnt)[1], cv2.boundingRect(cnt)[0]))

    # Określ środkową linię podziału pomiędzy górnymi a dolnymi ramkami
    median_y = np.median([pos[1] for pos in positions])

    # Podziel kontury na górne i dolne
    top_contours = [cnt for cnt in contours_sorted if cv2.boundingRect(cnt)[1] < median_y]
    bottom_contours = [cnt for cnt in contours_sorted if cv2.boundingRect(cnt)[1] >= median_y]

    # Sortuj górne i dolne kontury niezależnie według osi X
    top_sorted = sorted(top_contours, key=lambda cnt: cv2.boundingRect(cnt)[0])
    bottom_sorted = sorted(bottom_contours, key=lambda cnt: cv2.boundingRect(cnt)[0])

    # Połącz posortowane kontury w końcową kolejność
    final_sorted_contours = top_sorted + bottom_sorted

    frame_count = 0
    for cnt in final_sorted_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cropped_img = img[y:y+h, x:x+w]
        output_path = os.path.join(output_dir, f"frame_{frame_count+1}{suffix}.jpg")
        cv2.imwrite(output_path, clean_frames(cropped_img))
        frame_count += 1

    logging.info(f"Found and saved {frame_count} green frames in {image_path}")


def process_single_folder(folder_path, survey_folder):
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
            label_file.write("\nKLASA:  \n\n\nWiek - \nPłeć - \nMiejsce zamieszkania - \nWykształcenie - \nZatrudnienie - \n\nIlość uzyskanych punktów - ")

        logging.info(f"Dodano plik z etykietą: {label_filename}")

        image_path_a = os.path.join(survey_folder_path, f"{survey_folder}_a.jpg")
        image_path_b = os.path.join(survey_folder_path, f"{survey_folder}_b.jpg")

        if os.path.exists(image_path_a) and os.path.exists(image_path_b):
            logging.info(f"Ścieżka obrazu A: {image_path_a}")
            logging.info(f"Ścieżka obrazu B: {image_path_b}")

            # Wykorzystaj threading.Lock() do synchronizacji wątków
            lock = threading.Lock()

            # Przekazanie lock do funkcji crop_green_frames
            # Przekazanie lock do funkcji crop_green_frames
            thread_a = threading.Thread(target=find_green_frames,
                                        args=(image_path_a, output_directory, 4, (950, 950),  "_a"))
            thread_b = threading.Thread(target=find_green_frames,
                                        args=(image_path_b, output_directory, 4, (950, 950),  "_b"))
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

def process_survey_folder_parallel(folder_path):
    setup_logging()  # Konfiguracja loggingu na początku
    threads = []

    for survey_folder in os.listdir(folder_path):
        survey_folder_path = os.path.join(folder_path, survey_folder)
        if os.path.isdir(survey_folder_path):
            thread = threading.Thread(target=process_single_folder, args=(folder_path, survey_folder))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    logging.info("Zakończono przetwarzanie wszystkich ankiet")
    sys.exit()

if __name__ == "__main__":
    surveys_path = "D:/Magisterka/Wyniki ankiet/Skany"
    process_survey_folder_parallel(surveys_path)