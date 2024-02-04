from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import messagebox

def jest_zielony(pixel, prog=100):
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
    for survey_folder in os.listdir(folder_path):
        survey_folder_path = os.path.join(folder_path, survey_folder)

        if os.path.isdir(survey_folder_path):
            for image_filename in os.listdir(survey_folder_path):
                if image_filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(survey_folder_path, image_filename)

                    try:
                        obraz = Image.open(image_path)
                        obraz_z_zielonym = zamien_na_idealny_zielony(obraz)
                        obraz_z_zielonym.save(image_path)
                    except Exception as e:
                        print(f"Error processing image {image_filename}: {str(e)}")

    messagebox.showinfo("Zakończono", "Przetwarzanie zakończone!")

if __name__ == "__main__":
    surveys_path = "D:/Magisterka/Wyniki ankiet/Skany"
    process_survey_folder(surveys_path)
