import cv2
import numpy as np

def wyciagnij_tabele(sciezka_wejsciowa, sciezka_wyjsciowa):
    # Wczytaj obraz
    obraz = cv2.imread(sciezka_wejsciowa)

    # Przekształć obraz na przestrzeń kolorów HSV
    hsv = cv2.cvtColor(obraz, cv2.COLOR_BGR2HSV)

    # Zdefiniuj zakres kolorów niebieskich w przestrzeni kolorów HSV
    dolny_niebieski = np.array([90, 50, 50])
    gorny_niebieski = np.array([130, 255, 255])

    # Stwórz maskę kolorów niebieskich
    maska = cv2.inRange(hsv, dolny_niebieski, gorny_niebieski)

    # Zastosuj maskę na oryginalnym obrazie
    wynikowy_obraz = cv2.bitwise_and(obraz, obraz, mask=maska)

    # Znajdź kontury w wynikowym obrazie
    kontury, _ = cv2.findContours(maska, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Wybierz największy kontur (zakładając, że tabela jest największym obiektem)
    najwiekszy_kontur = max(kontury, key=cv2.contourArea)

    # Znajdź bounding box wokół konturu
    x, y, w, h = cv2.boundingRect(najwiekszy_kontur)

    # Wyciągnij tabelę na podstawie bounding box
    tabela = obraz[y:y+h, x:x+w]

    # Zapisz wyciętą tabelę w nowym pliku jpg
    cv2.imwrite(sciezka_wyjsciowa, tabela)

if __name__ == "__main__":
    sciezka_wejsciowa = "D:/Magisterka/Wyniki ankiet/Ankieta1.jpg"
    sciezka_wyjsciowa = "D:/Magisterka/Wyniki ankiet/Wycieta_tabela.jpg"

    wyciagnij_tabele(sciezka_wejsciowa, sciezka_wyjsciowa)
