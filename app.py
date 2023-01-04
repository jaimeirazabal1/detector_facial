import cv2  # Importamos OpenCV
import sqlite3  # Importamos SQLite
import os
import pyttsx3


def crear_tabla():
    # Conectamos a la base de datos
    conn = sqlite3.connect("basededatos.db")
    # Creamos el cursor
    c = conn.cursor()
    
    # Verificamos si la tabla existe
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rostros'")
    # Obtenemos el resultado de la consulta
    resultado = c.fetchone()
    
    # Si el resultado es None, la tabla no existe
    if resultado is None:
        # Creamos la tabla
        c.execute("CREATE TABLE rostros (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, cara BLOB)")
        # Mostramos un mensaje
        print("Tabla creada con éxito")
    else:
        # Mostramos un mensaje
        print("La tabla ya existe")
    
    # Confirmamos los cambios
    conn.commit()
    # Cerramos la conexión
    conn.close()

def insertar_registro(nombre, cara):
    # Conectamos a la base de datos
    conn = sqlite3.connect("basededatos.db")
    # Creamos el cursor
    c = conn.cursor()
    # Insertamos el registro
    c.execute("INSERT INTO rostros (nombre, cara) VALUES (?, ?)", (nombre, cara))
    # Confirmamos los cambios
    conn.commit()
    # Cerramos la conexión
    conn.close()

def hablar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

# Iniciamos la cámara
camara = cv2.VideoCapture(0)
crear_tabla()
# Creamos el detector de rostro
detector_rostros = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Creamos una lista para almacenar los nombres de las personas reconocidas
nombres_reconocidos = []
print("entrando en el ciclo")
while True:
    # Leemos el frame de la cámara
    _, frame = camara.read()
    
    # Convertimos el frame a gris
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectamos los rostros en el frame
    rostros = detector_rostros.detectMultiScale(frame_gris, 1.3, 5)
    
    # Dibujamos un rectángulo alrededor de los rostros detectados
    for (x, y, w, h) in rostros:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Mostramos el frame en la pantalla
    cv2.imshow("Rostros", frame)
    
    # Si se detecta un rostro
    if len(rostros) > 0:
        # Preguntamos el nombre de la persona
        nombre = input("Ingresa el nombre de la persona: ")
        
        # Si el nombre no ha sido reconocido antes
        if nombre not in nombres_reconocidos:
            # Añadimos el nombre a la lista de nombres reconocidos
            nombres_reconocidos.append(nombre)
            # Guardamos la imagen del rostro en un archivo
            cv2.imwrite("rostros/" + nombre + ".jpg", frame_gris[y:y+h, x:x+w])
            

            # Insertamos el registro en la base de datos
            insertar_registro(nombre, "rostros/" + nombre + ".jpg")

            # Mostramos un mensaje de éxito
            print("Registro insertado con éxito")

            # Hacemos que la aplicación hable para avisar que se ha añadido un nuevo rostro
            hablar("Rostro añadido con éxito")

    # Si presionamos la tecla q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Liberamos la cámara y destruimos las ventanas
camara.release()
cv2.destroyAllWindows()

