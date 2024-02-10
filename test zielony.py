from PIL import Image
import os
import tkinter as tk
from tkinter import messagebox

def jest_zielony(pixel, prog=140):
    return pixel[1] - pixel[0] > prog and pixel[1] - pixel[2] > prog

def zamien_na_idealny_zielony(img):
    szerokosc, wysokosc = img.size
    idealny_zielony = (0, 255, 0)  # RGB dla koloru zielonego
    prog_zielony = 50  # Próg dla zbliżenia do koloru zielonego

    for x in range(szerokosc):
        for y in range(wysokosc):
            pixel = img.getpixel((x, y))
            if jest_zielony(pixel, prog_zielony):
                img.putpixel((x, y), idealny_zielony)

    return img

def process_survey_folder(folder_path):
    survey_folders = os.listdir(folder_path)
    # Sortowanie folderów numerycznie na podstawie ich nazwy
    survey_folders_sorted = sorted(survey_folders, key=lambda x: int(x.split(' ')[-1]))

    for survey_folder in survey_folders_sorted:
        survey_folder_path = os.path.join(folder_path, survey_folder)

        if os.path.isdir(survey_folder_path):
            print(f"Otwieranie folderu: {survey_folder_path}")  # Informacja o otwieranym folderze
            for image_filename in os.listdir(survey_folder_path):
                if image_filename.lower().endswith(('.jpg', '.jpeg')):
                    image_path = os.path.join(survey_folder_path, image_filename)
                    print(f"Przetwarzanie obrazu: {image_filename}")  # Informacja o przetwarzanym obrazie

                    try:
                        obraz = Image.open(image_path)
                        obraz_z_zielonym = zamien_na_idealny_zielony(obraz)
                        obraz_z_zielonym.save(image_path)
                    except Exception as e:
                        print(f"Błąd przetwarzania obrazu {image_filename}: {str(e)}")

def main():
    root = tk.Tk()
    root.withdraw()  # Ukrycie głównego okna Tkinter
    surveys_path = "D:/Magisterka/Wyniki ankiet/Skany"
    process_survey_folder(surveys_path)
    messagebox.showinfo("Zakończono", "Przetwarzanie zakończone!")
    root.destroy()  # Usunięcie okna po zakończeniu

if __name__ == "__main__":
    main()
