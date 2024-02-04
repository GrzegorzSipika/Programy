import cv2
import numpy as np

def znajdz_granice_kolumn(img):
    # Zamień obraz na odcienie szarości
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Zastosuj binaryzację, aby wyostrzyć czarne obszary
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Znajdź krawędzie pionowe
    krawedzie_pionowe = cv2.Sobel(binary, cv2.CV_64F, 1, 0, ksize=5)

    # Znajdź kontury
    kontury, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Znajdź współrzędne linii pionowych
    granice_kolumn = [0]
    for kontur in kontury:
        x, _, _, _ = cv2.boundingRect(kontur)
        granice_kolumn.append(x)

    granice_kolumn.sort()

    return granice_kolumn

def odczytaj_komorki_z_X(img_path):
    # Wczytaj obraz
    img = cv2.imread(img_path)

    # Dodaj margines do obrazu
    margines = 10
    img = cv2.copyMakeBorder(img, margines, margines, margines, margines, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    # Znajdź granice kolumn
    granice_kolumn = znajdz_granice_kolumn(img)

    # Dla ułatwienia przyjmujemy, że tabela ma 12 kolumn
    if len(granice_kolumn) == 13:
        for i in range(12):
            kolumna_poczatek = granice_kolumn[i]
            kolumna_koniec = granice_kolumn[i + 1]

            # Wytnij obszar kolumny z marginesem
            kolumna = img[:, kolumna_poczatek:kolumna_koniec]

            # Zamień na odcienie szarości
            gray_kolumna = cv2.cvtColor(kolumna, cv2.COLOR_BGR2GRAY)

            # Zastosuj binaryzację, aby wyostrzyć czarne obszary
            _, binary_kolumna = cv2.threshold(gray_kolumna, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Sprawdź, czy w kolumnie jest znak X
            if np.any(binary_kolumna == 0):  # Sprawdzamy, czy istnieje czarny piksel (znak X)
                print(f"Znak X znaleziony w kolumnie {i + 1}")
            else:
                print(f"Brak znaku X w kolumnie {i + 1}")
    else:
        print("Nie udało się odnaleźć 12 kolumn. Sprawdź obraz.")

if __name__ == "__main__":
    # Ścieżka do pliku jpg
    sciezka_do_pliku = "D:/Magisterka/Wyniki ankiet/Wycieta_tabela.jpg"

    # Wywołaj funkcję odczytującą komórki z X
    odczytaj_komorki_z_X(sciezka_do_pliku)
