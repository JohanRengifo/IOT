import cv2
import pytesseract
import re

# Variables
cuadro = 100
doc = 0

# Inicializar la cámara utilizando un enlace HTTP
cap = cv2.VideoCapture('http://172.16.1.101:8080/video')

# Funciones
def configurar_tesseract():
    # Configurar la ruta al ejecutable de Tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def reconocer_texto(imagen):
    global doc

    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral adaptativo
    umbral = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)

    # Configuración de OCR
    config = "--psm 1"
    texto = pytesseract.image_to_string(umbral, config=config)

    # Palabras clave
    seccol = r'COLOMBIA'
    seccol2 = r'IDENTIFICACION'

    busqueda_col = re.search(seccol, texto, re.IGNORECASE)
    busqueda_col2 = re.search(seccol2, texto, re.IGNORECASE)

    print(texto)

    # Si se encuentra "COLOMBIA" e "IDENTIFICACION" en el texto
    if busqueda_col and busqueda_col2:
        doc = 1

def main():
    configurar_tesseract()

    while True:
        # Lectura de la Videocaptura
        ret, frame = cap.read()

        # Interfaz
        cv2.putText(frame, 'Ubique el Documento de Identidad', (458, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 255, 0), 2)
        cv2.rectangle(frame, (cuadro, cuadro), (1280 - cuadro, 720 - cuadro), (0, 255, 0), 2)

        if doc == 0:
            cv2.putText(frame, 'Presiona S para Identificar', (458, 750 - cuadro), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 255, 0), 2)
        elif doc == 1:
            cv2.putText(frame, 'Identificación Colombiana', (458, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 255, 0), 2)

        # Leer la tecla presionada
        key = cv2.waitKey(1)

        if key == 83 or key == 115:  # Letra 'S' o 's'
            reconocer_texto(frame)

        if key == 27:  # Tecla Esc para salir
            break

        # Mostrar la ventana
        cv2.imshow("Reconocimiento", frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()