# Librerias
import cv2
import pytesseract
import re

# variables
cuadro = 100
doc=0

cap = cv2.VideoCapture('https://172.16.1.101:8080/')
cap.set(3, 1280)
cap.set(4, 720)


# Funciones
def texto(image):
    global doc
    # Variables
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # escala de Grises
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #umbral
    umbral = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)
    # Configuracion OCR
    config = "--psm 1"
    texto = pytesseract.image_to_string(umbral, config=config)
    
    #palabras claves
    seccol = r'COLOMBIA'
    seccol2 = r'IDENTIFICACION'

    buscecol= re.findall(seccol, texto)
    buscecol2 = re.findall(seccol2, texto)
    
    print(texto)
    
    # Si es Colombia
    if len(buscecol)!=0 and len(buscecol2)!=0:
        doc=1

while True:
    # Lectura de la Videocaptura
    ret, frame = cap.read()
    
    # Interfaz
    cv2.putText(frame, 'ubique el Docuemnto de identidad', (458, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 255, 0), 2) 
    cv2.rectangle(frame, (cuadro, cuadro), (1280 - cuadro, 720 - cuadro), (0, 255, 0), 2)
    
    if doc==0:
        cv2.putText(frame, 'Presiona S para Identificar', (458, 750 - cuadro), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 255, 0), 2)
    elif doc==1:
        cv2.putText(frame, 'Identificacion Colombiana', (458, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.71, (0, 255, 0), 2)
    
    # Si la letra es s o S
    t = cv2.waitKey(1)
    if t == 83 or t == 115:
        texto(frame)
        
    if t == 27:
        break
    
    # Lanza la Ventana
    cv2.imshow("Reconocimiento", frame)

    # Cierre la ventana
    t = cv2.waitKey(1)
    if t == 27:
        break

cap.release()
cv2.destroyAllWindows()