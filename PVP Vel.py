

import pyautogui
import time
import threading
import pygame
import os
from gtts import gTTS
import string
import sys
import math
import datetime

from pynput import mouse, keyboard
from threading import Timer
import ctypes, sys





start_time = time.time()
pygame.init()
pygame.mixer.init()
botones = {}
color = {}  # Color de referencia para el botón
#contador_botones = 0  # Contador para generar los nombres de las variables
contador_colores = 0  # Contador para generar los nombres de las variables de color
primera_pulsacion_mouse = True  # Control para el clic del mousef1
primera_pulsacion_tecla_g = True  # Control para la tecla 'g'
capturaletra2 = False

nombre_archivo_1 = "coordenadas1"
nombremastxt1 = nombre_archivo_1 + ".txt"
coordenadas1 = os.path.join(os.path.dirname(__file__), nombremastxt1)
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

nombre_archivo_2 = "coordenadas2"
nombremastxt2 = nombre_archivo_2 + ".txt"
coordenadas2 = os.path.join(os.path.dirname(__file__), nombremastxt2)

nombre_archivo_3 = "coordenadas3"
nombremastxt3 = nombre_archivo_3 + ".txt"
coordenadas3 = os.path.join(os.path.dirname(__file__), nombremastxt3)

archivo_actual = coordenadas1

nombre_archivo_4 = "Velocidades2yBucles2"
nombremastxt4 = nombre_archivo_4 + ".txt"
Velocidades2_y_Bucles2 = os.path.join(os.path.dirname(__file__), nombremastxt4)



nombre_archivo_5 = "Velocidades1yBucles1"
nombremastxt5 = nombre_archivo_5 + ".txt"
Velocidades1_y_Bucles1 = os.path.join(os.path.dirname(__file__), nombremastxt5)


is_paused = False  # Esta variable controlará el estado de pausa del programa

numero_exitos_confirmado = 0

botonescaptura = {}
colorcaptura = {}  # Color de referencia para el botón
exit_flag = False
keyboard_listener = None
mouse_listener = None
ejecutardecision = False
#ejecutarmain = True
establecerbotones = False
ejecutarmain = False
# Variables globales
archivo_actual = None
mouse_listener = None
keyboard_listener = None
velocidad = 1
cantidad_repeticiones_bucle = 1
contador_botones = 0




# a revisar cada ves que se ejecute
compararyrevisar = False

nombre_archivo_base = "Pokechange -" 
fecha_actual = datetime.datetime.now().strftime("(%d-%m-%Y)")
nombre_archivo_con_fecha = nombre_archivo_base + fecha_actual + ".txt"
ruta_completa = os.path.join(os.path.dirname(__file__), nombre_archivo_con_fecha)
try:
    with open(ruta_completa, 'r') as archivo:
        numero_de_veces_leidas = int(archivo.read())
except FileNotFoundError:
        numero_de_veces_leidas = 0
print("\nActualmente se han confirmado ", numero_de_veces_leidas, " casos de exito")










ejecutado1 = False
cont_errores = 0
contabilidad = 1

conta1 = 0
conta2 = 0
conta3 = 0
# pritnt
#--------------------------------------------------------------

def mostrar_tiempo_transcurrido():
    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - start_time
    horas, resto = divmod(tiempo_transcurrido, 3600)
    minutos, segundos = divmod(resto, 60)
    print(f"Tiempo transcurrido: {int(horas):02d}:{int(minutos):02d}:{int(segundos):02d}")

def decirtiempotranscurrido(): 
    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - start_time
    horas, resto = divmod(tiempo_transcurrido, 3600)
    minutos, segundos = divmod(resto, 60)
    textodesonido = f"se transcurrio: {int(horas):02d}:{int(minutos):02d}:{int(segundos):02d} tiempo"
    Sonido = limpiar_texto_para_nombre_archivo(textodesonido) + ".mp3"
    try:
        if '__file__' in globals():
            ruta_sonido = os.path.join(os.path.dirname(__file__), Sonido)
        else:
            ruta_sonido = os.path.join(os.getcwd(), Sonido)
        tts = gTTS(text=textodesonido, lang='es')
        tts.save(ruta_sonido)
        print(f"Archivo MP3 guardado exitosamente en: {ruta_sonido}")
        reproducir_sonido(ruta_sonido)
    except PermissionError as e:
        print(f"No se pudo guardar el archivo MP3: {e}")
    except Exception as e:
        print(f"Ocurrió un error al intentar guardar el archivo MP3: {e}")



def cargar_velocidades_y_bucles(nombre_archivo):
    velocidades = []
    bucles = []
    global existearchivo_velocidades_y_bucles
    existearchivo_velocidades_y_bucles = True
    try:
        with open(nombre_archivo, 'r') as archivo:
            contenido = archivo.read()
            # Asegurarse de que cada nueva entrada comience en una nueva línea
          
            contenido = contenido.replace('Bucle', '\nBucle').replace('Velocidad', '\nVelocidad')
            #print("Contenido del archivo procesado:\n", contenido)  # Línea de depuración
            lineas = contenido.split('\n')
            for linea in lineas:
                if linea.strip() == "":
                    continue
                #print("Procesando línea:", linea)  # Línea de depuración
                linea_limpia = linea.strip()
                partes = linea_limpia.split('= ')
                if len(partes) == 2:
                    clave, valor = partes[0], partes[1]
                    
                    if clave.startswith("Velocidad"):
                        velocidad = float(valor)
                        velocidades.append(velocidad)
                        #print(f"Velocidad agregada: {velocidad}")  # Línea de depuración
                    elif clave.startswith("Bucle"):
                        velocidad, repeticiones = map(int, valor.split(', '))
                        velocidad = float(velocidad)
                        bucles.append((velocidad, repeticiones))
                        #print(f"Velocidad de bucle: {velocidad}, Repeticiones: {repeticiones}")  # Línea de depuración
                        
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
        existearchivo_velocidades_y_bucles = False
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
    

    return velocidades, bucles


def cargar_coordenadas_desde_archivo(nombre_archivo):
    botones = []
    colores = []
    velocidades = []
    bucles = []

    try:
        with open(nombre_archivo, 'r') as archivo:
            contenido = archivo.read()
            # Asegurarse de que cada nueva entrada comience en una nueva línea
          
            contenido = contenido.replace('Bucle', '\nBucle').replace('Velocidad', '\nVelocidad').replace('Boton', '\nBoton').replace('Color', '\nColor')
            #print("Contenido del archivo procesado:\n", contenido)  # Línea de depuración
            lineas = contenido.split('\n')
            for linea in lineas:
                if linea.strip() == "":
                    continue
                #print("Procesando línea:", linea)  # Línea de depuración
                linea_limpia = linea.strip()
                partes = linea_limpia.split('= ')
                if len(partes) == 2:
                    clave, valor = partes[0], partes[1]
                    if clave.startswith('Boton'):
                        try:
                            x, y = map(int, valor.split(', '))
                            botones.append((x, y))
                            #print(f"Botón agregado: {(x, y)}")  # Línea de depuración
                        except ValueError:
                            print(f"Error procesando las coordenadas en la línea: {linea}")
                    elif clave.startswith('Color'):
                        try:
                            coordenadas_color = valor.strip('()')
                            color = tuple(map(int, coordenadas_color.split(', ')))
                            colores.append(color)
                            #print(f"Color agregado: {color}")  # Línea de depuración
                        except ValueError:
                            print(f"Error procesando el color en la línea: {linea}")
                    elif clave.startswith("Velocidad"):
                        velocidad = float(valor)
                        velocidades.append(velocidad)
                        #print(f"Velocidad agregada: {velocidad}")  # Línea de depuración
                    elif clave.startswith("Bucle"):
                        velocidad, repeticiones = map(int, valor.split(', '))
                        velocidad = float(velocidad)
                        cantidad_repeticiones_bucle = repeticiones
                        bucles.append((velocidad, repeticiones))
                        #print(f"Velocidad de bucle: {velocidad}, Repeticiones: {repeticiones}")  # Línea de depuración
                        
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
    

    return botones, colores, velocidades, bucles

# Ejemplo de uso
botones1, colores1, velocidades1, bucles1 = cargar_coordenadas_desde_archivo('coordenadas1.txt')






 
def cantidadbotones(botones, colores):
    #f2print(botones)
   
    return len(botones), len(colores)
    
    
    print("w")





botonescaptura1 = {}
botonescaptura2 = {}
botonescaptura3 = {}
colorcaptura1 = {}
colorcaptura2 = {}
colorcaptura3 = {}
def iniciar_mouse_listener():
    global mouse_listener
    if mouse_listener is None:
        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.start()    

def iniciar_keyboard_listener():
    global keyboard_listener
    if keyboard_listener is None:  # Solo inicia un nuevo listener si no hay uno activo
        print("Iniciando keyboard listener...")
        keyboard_listener = keyboard.Listener(on_press=on_press, daemon=True)
        keyboard_listener.start()

def reiniciar_programa():
    """
    Reinicia el script.
    """
    print("Reiniciando el programa...")
    # Obtener la ruta completa del script
    script = os.path.abspath(sys.argv[0])
    # Ejecutar el script
    os.execv(sys.executable, [sys.executable, f'"{script}"'] + sys.argv[1:])

def on_click(x, y, button, pressed):
        
    global botonescaptura1, botonescaptura2, botonescaptura3, colorcaptura1, colorcaptura2, colorcaptura3
    global primera_pulsacion_tecla_g, primera_pulsacion_mouse, velocidad_defecto
    global contador_botones, contador_colores, archivo_actual, nombre_bucle
    #iniciar_mouse_listener()
    
    
    if pressed and button == mouse.Button.left:
        contador_botones += 1
        

        nombre_boton = f"Boton{contador_botones}"
        pixelColor = pyautogui.screenshot().getpixel((x, y))
        nombre_color = f"Color{contador_botones}"
        nombre_velocidad = f"Velocidad{contador_botones}"
        nombre_bucle = f"Bucle{contador_botones}"

        if primera_pulsacion_tecla_g:
            guardar_coordenadasprimeras(x, y, nombre_boton, nombre_color, pixelColor,nombre_velocidad,velocidad, nombre_bucle)
            primera_pulsacion_tecla_g = False
        else:
            guardar_coordenadas_segundas(x,y, nombre_boton, nombre_color, pixelColor, nombre_velocidad, velocidad, nombre_bucle)
    #print(contador_botones)
    #detener_mouse_listener()
    



f_pressed_within_limit = False


def eliminar_ultimo_boton_color(nombre_archivo, contador_botones):
    try:
        # Leer el contenido del archivo
        with open(nombre_archivo, "r") as file:
            lineas = file.readlines()

        # Verificar si hay líneas para eliminar
        if len(lineas) >= 4:
            # Guardar la información del último botón y color
            
            ultimo_boton = lineas[-4].strip()
            ultimo_color = lineas[-3].strip()
            ultimo_velocidad = lineas[-2].strip()
            ultimo_bucle = lineas[-1].strip()
            
            # Eliminar las últimas dos líneas (botón y color)
            lineas = lineas[:-4]

            # Reescribir el archivo sin las últimas dos líneas
            with open(nombre_archivo, "w") as file:
                file.writelines(lineas)

            # Imprimir la información del botón y color eliminados
            print(f"Último botón eliminado: {ultimo_boton}")
            #print(f"Último color eliminado: {ultimo_color}")
            print(f"Total de botones ahora: {contador_botones}")
        else:
            print("No hay suficientes líneas en el archivo para eliminar.")
    except Exception as e:
        print(f"Error al eliminar el último botón: {e}")




def mostrarcantidadbotonesycolores():
    botones1, colores1 = cargar_coordenadas_desde_archivo(coordenadas1)
    botones2, colores2 = cargar_coordenadas_desde_archivo(coordenadas2)
    botones3, colores3 = cargar_coordenadas_desde_archivo(coordenadas3)
    cantidad_botones1, cantidad_colores1 = cantidadbotones(botones1, colores1) 
    cantidad_botones2, cantidad_colores2 = cantidadbotones(botones2, colores2)
    cantidad_botones3, cantidad_colores3 = cantidadbotones(botones3, colores3)
    print(f"la cantidad de botones1 es de {cantidad_botones1}")
    print(f"la cantidad de botones2 es de {cantidad_botones2}")
    print(f"la cantidad de botones3 es de {cantidad_botones3}")


def es_admin():
    """
    Verifica si el script se está ejecutando con privilegios de administrador.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def reiniciar_con_privilegios_de_admin():
    """
    Reinicia el script con privilegios de administrador.
    """
    if not es_admin():
        print("Reiniciando el programa con privilegios de administrador...")
        # Obtener la ruta completa del script
        script = os.path.abspath(sys.argv[0])
        # Ejecutar el script con privilegios de administrador
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 1)
        sys.exit()
mostrar_tiempo_transcurrido()



def on_press(key):
    global archivo_actual, botonescaptura1, botonescaptura2, botonescaptura3, colorcaptura1
    global colorcaptura2, colorcaptura3, primera_pulsacion_tecla_g, contador_botones, exit_flag, ejecutardecision, keyboard_listener, contador_botones, start_time
    global f_pressed_within_limit, start_time, is_paused, numero_exitos_confirmado
    print(f"Key event: {key}")

    if hasattr(key, 'char') and key.char == 'f':
        if not f_pressed_within_limit:  # Check if 'f' wasn't already pressed
            f_pressed_within_limit = True
            ejecutardecision = True
            print("Tecla 'f' presionada, ejecutardecision es True.")
            mostrar_tiempo_transcurrido()
            # Do not stop the listener here if you want to capture another key press.

    # Check for other key presses after 'f' has been pressed
    elif f_pressed_within_limit:
        if key == keyboard.KeyCode(char='1'):
           
            print("Se presionó la tecla '1' después de 'f'.")
            # Call your desired function or set a flag here.
            # For example:
            # decision1()
            # To prevent further key processing, you can stop the listener:
            keyboard_listener.stop()

    try:
            # Verifica si la tecla presionada es 'f'
        if key.char == 'r':
            keyboard_listener.stop()

            limpiar_pantalla()
            reiniciar_programa()
            return False
    except AttributeError:
            pass
    if key == keyboard.KeyCode(char='0'):
        ("\n se termino")
        exit_flag = True
        end_time = time.time()
        if start_time is not None:
            total_time = end_time - start_time
        print(f"Tiempo total de ejecución: {total_time:.2f} segundos")
        detener_mouse_listener()
        keyboard_listener.stop()    
        if keyboard_listener is not None:
            keyboard_listener.stop()
        print("Finalizando el programa...")
        reiniciar_con_privilegios_de_admin()
        return False  # Detiene el listener
    if key == keyboard.KeyCode(char='p'):
        is_paused = not is_paused
        if is_paused:
            print("Programa pausado. Presione 'P' nuevamente para reanudar.")
            detener_mouse_listener()
        else:
            print("Programa reanudado.")
            iniciar_mouse_listener()

    if key == keyboard.KeyCode(char='1'):
        if ejecutardecision:
            decision1()
            #decision1()

        else:
            detener_mouse_listener()
            contador_botones = 0
            primera_pulsacion_tecla_g = True
            archivo_actual = coordenadas1
        
            print("Captura de clics activada. Guardando en coordenadas1.txt")
        
            iniciar_mouse_listener()
    if key == keyboard.KeyCode(char='c'):
        if ejecutardecision:
            coord1 = "coordenadas1.txt"
            coord2 = "coordenadas2.txt"
            velocidaybucle2 = "Velocidades2yBucles2.txt"
            velocidadybucle1 = "Velocidades1yBucles1.txt"
            copiar_velocidad_bucle(coord2,velocidaybucle2)
            copiar_velocidad_bucle(coord1,velocidadybucle1)
    if key == keyboard.KeyCode(char='2'):
        if ejecutardecision:
            detener_mouse_listener()
            decision2()
            #decision2()
        else:
            detener_mouse_listener()
            contador_botones = 0
            primera_pulsacion_tecla_g = True
            archivo_actual = coordenadas2
            print("Captura de clics activada. Guardando en coordenadas2.txt")
            iniciar_mouse_listener()   

    if key == keyboard.KeyCode(char='3'):
        if ejecutardecision:
            decision3()
            #decision3()
        else:
            detener_mouse_listener()
            contador_botones = 0
            primera_pulsacion_tecla_g = True
            archivo_actual = coordenadas3
            print("Captura de clics activada. Guardando en coordenadas3.txt")
            iniciar_mouse_listener()
    
    if key == keyboard.KeyCode(char='4'):
        detener_mouse_listener()
        botones1, colores1 = cargar_coordenadas_desde_archivo(coordenadas1)
        botones2, colores2 = cargar_coordenadas_desde_archivo(coordenadas2)
        decision1()
    if key == keyboard.Key.enter:
        mostrarcantidadbotonesycolores()

    if key == keyboard.Key.backspace:
        # Verificar si hay botones para eliminar
        
        if contador_botones > 0:
            # Disminuir el contador de botones
            contador_botones -= 1

            # Eliminar el último botón y color del archivo
            eliminar_ultimo_boton_color(archivo_actual, contador_botones)
        else:
            print("No hay botones para eliminar.")
    if key == keyboard.Key.esc:
        exit_flag = True
        print("Finalizando el programa...")
        detener_mouse_listener()
        if keyboard_listener is not None:
            keyboard_listener.stop()
        sys.exit()
        
    elif key == keyboard.Key.space:
        limpiar_pantalla()
    
    


import os

def copiar_velocidad_bucle(nombre_archivo_coord, velocidadybucle):
    # Nombre del nuevo archivo
    

    try:
        # Abrir el archivo original para lectura
        with open(nombre_archivo_coord, 'r') as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo_coord}' no se encontró.")
        return

    # Lista para almacenar las líneas que contienen Velocidad y Bucle
    lineas_filtradas = []

    # Filtrar las líneas que contienen Velocidad y Bucle
    for linea in lineas:
        if "Velocidad" in linea or "Bucle" in linea:
            lineas_filtradas.append(linea.strip() + '\n')

    # Obtener el directorio del script actual
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Ruta completa del nuevo archivo en la misma carpeta
    ruta_nuevo_archivo = os.path.join(directorio_actual, velocidadybucle)

    # Escribir las líneas filtradas en el nuevo archivo (modo 'w' para sobreescribir si ya existe)
    with open(ruta_nuevo_archivo, 'w') as nuevo_archivo:
        nuevo_archivo.writelines(lineas_filtradas)

    print(f"Las líneas se han copiado a {ruta_nuevo_archivo}")

# Llamar a la función con el nombre del archivo original






def espera_tecla_f():
    # Crea un listener de teclado que utiliza la función de callback 'on_press'
    with keyboard.Listener(on_press=on_press) as listener:
        # Espera hasta que el listener se detenga (cuando se presione 'f' o pase el timeout)
        listener.join()
        
    # Si el listener aún está corriendo después del timeout, lo detiene
    if listener.is_alive():
        listener.stop()


def guardar_coordenadasprimeras(x, y, nombre_boton, nombre_color, pixelColor, nombre_velocidad,velocidad, nombre_bucle):
    # Comprueba si hay un archivo actual y guarda las coordenadas y colores
    global archivo_actual
    if archivo_actual is not None:
        with open(f"{archivo_actual}", "w") as file:
            file.write(f"{nombre_boton}= {x}, {y}\n")
            file.write(f"{nombre_color}= {pixelColor}\n")
            file.write(f"{nombre_velocidad}= {velocidad}\n")
            file.write(f"{nombre_bucle}= {velocidad}, {cantidad_repeticiones_bucle}\n")
            print(f"{nombre_boton}= {x}, {y}")
def guardar_coordenadas_segundas(x, y, nombre_boton, nombre_color, pixelColor, nombre_velocidad, velocidad, nombre_bucle):
    # Comprueba si hay un archivo actual y guarda las coordenadas, colores y velocidad
    global archivo_actual
    if archivo_actual is not None:
        with open(f"{archivo_actual}", "a") as file:
            file.write(f"{nombre_boton}= {x}, {y}\n")
            file.write(f"{nombre_color}= {pixelColor}\n")
            file.write(f"{nombre_velocidad}= {velocidad}\n")
            file.write(f"{nombre_bucle}= {velocidad}, {cantidad_repeticiones_bucle}\n")
            print(f"{nombre_boton}= {x}, {y}")
def limpiar_pantalla():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def detener_mouse_listener():
    global mouse_listener
    if mouse_listener is not None:
        mouse_listener.stop()
        mouse_listener = None

def capturar():
    iniciar_mouse_listener()
    detener_mouse_listener()


def reiniciar_variables_para_captura():
    global contador_botones, contador_colores, botones, color, primera_pulsacion_mouse

    # Reiniciar los contadores
    contador_botones = 0
    contador_colores = 0

    # Reiniciar los diccionarios de botones y colores
    botones = {}
    color = {}

    # Asegurarse de que la próxima pulsación del mouse sea considerada la primera
    primera_pulsacion_mouse = True


#print(botones1)



if compararyrevisar:
    dur = 3
    cantidad_errores_maxima = 5
    hacerclick = False
    numero_de_veces = 2
    esperarentrebucle = False
    
    porcentnotificaciones = (2, 40, 90)
    notificaciones_pendientes = list(porcentnotificaciones)
else:
    cantidad_errores_maxima = 7
    dur = 1
    hacerclick = True
    cantidadobjetivoatenerexitos = 105
    numero_de_veces = cantidadobjetivoatenerexitos - numero_de_veces_leidas
    #numero_de_veces = 10
    print("El número recomendado para el bucle es de " + str(numero_de_veces))
    esperarentrebucle = True

    porcentnotificaciones = (10,20,30, 70, 90, 100)
    notificaciones_pendientes = list(porcentnotificaciones)



botones1, colores1, velocidades1, bucles1 = cargar_coordenadas_desde_archivo(coordenadas1)
botones2, colores2, velocidades2, bucles2 = cargar_coordenadas_desde_archivo(coordenadas2)
botones3, colores3, velocidades3, bucles3 = cargar_coordenadas_desde_archivo(coordenadas3)
cantidad_botones1, cantidad_colores1 = cantidadbotones(botones1, colores1) 
cantidad_botones2, cantidad_colores2 = cantidadbotones(botones2, colores2)
cantidad_botones3, cantidad_colores3 = cantidadbotones(botones3, colores3)

print(f"la cantidad de botones1 es de {cantidad_botones1}")
print(f"la cantidad de botones2 es de {cantidad_botones2}")
print(f"la cantidad de botones3 es de {cantidad_botones3}"+"\n")
print("Si desea establecer los botones encontes presione el numero de la coordenada")
print("SI desea ejecutar alguna decision entonces presione f y luego el numero de la decision")

#print(bucles1)
def limpiar_texto_para_nombre_archivo(texto, longitud_maxima=50):
        # Remover caracteres no deseados y limitar la longitud4
        texto_limpio = "".join(c for c in texto if c in string.ascii_letters + string.digits + " ")
        return texto_limpio[:longitud_maxima]









def guardarnumero_exitos_confirmados(numero_exitos_confirmado):
        
        global numero_de_veces_leidas
        numero_de_veces_leidas += 1
        with open(ruta_completa, 'w') as archivo:
            archivo.write(str(numero_de_veces_leidas))
        #generararchivosonido("El bucle se completo exitosamente", numero_exitos_confirmado, "veces")    
        #generararchivosonido("El intercambio se actualizo a", numero_de_veces_leidas, "veces")
        #decirtiempotranscurrido()
        #sys.exit()

def registrarprogreso():
    global numero_de_veces_leidas
    numero_de_veces_leidas += 1
    with open(ruta_completa, 'w') as archivo:
        archivo.write(str(numero_de_veces_leidas))
def reproducir_sonido(nombre_archivo):
    # Inicializar pygame para reproducción de audio
    pygame.mixer.init()
    
    # Cargar y reproducir el archivo de sonido
    pygame.mixer.music.load(nombre_archivo)
    pygame.mixer.music.play()
    
    # Esperar a que termine la reproducción
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def limpiar_texto_para_nombre_archivo(texto):
    # Implementa la lógica para limpiar el texto y convertirlo en un nombre de archivo válido
    # Por ejemplo, podrías eliminar caracteres especiales o reemplazarlos con "_"
    texto_limpio = texto.replace(" ", "_")  # Ejemplo simple: reemplazar espacios con "_"
    return texto_limpio


def generararchivosonido(texto):
    try:
        SonidoNotificacion = limpiar_texto_para_nombre_archivo(texto) + ".mp3"
        tts = gTTS(text=texto, lang='es')
        ruta_sonido_notificacion = os.path.join(os.path.dirname(__file__), SonidoNotificacion)
        tts.save(ruta_sonido_notificacion)
        print(f"Archivo MP3 guardado exitosamente en: {ruta_sonido_notificacion}")
        return ruta_sonido_notificacion
    except Exception as e:
        print("Ocurrió un error:", e)
        return None

def generar_y_reproducir(texto):
    archivo_sonido = generararchivosonido(texto)
    if archivo_sonido:
        reproducir_sonido(archivo_sonido)




        

def notificacionpor(contabilidad, numporcent, notificaciones_pendientes):
    if contabilidad / numero_de_veces * 100 >= numporcent and numero_de_veces > 3:
        textonotificacion1 = f"El script ha completado el {numporcent}% de su ejecución."
        SonidoNotificacion = limpiar_texto_para_nombre_archivo(textonotificacion1) + ".mp3"
        print(f"El script ha completado el {numporcent}% de su ejecución.")
        try:
            tts = gTTS(text=textonotificacion1, lang='es')
            ruta_sonido_notificacion = os.path.join(os.path.dirname(__file__), SonidoNotificacion)
            tts.save(ruta_sonido_notificacion)
            print(f"Archivo MP3 guardado exitosamente en: {ruta_sonido_notificacion}")
            reproducir_sonido(ruta_sonido_notificacion)
            notificaciones_pendientes.remove(numporcent)  # Eliminar el porcentaje ya notificado
        except Exception as e:
            print("Ocurrió un error:", e)





def extraer_repeticiones(bucle):

    if isinstance(bucle, tuple) and len(bucle) == 2:
        try:
            repeticiones = int(bucle[1])
            return repeticiones
        except ValueError:
            print(f"Error al convertir las repeticiones: {bucle[1]}")
    return None

def extraer_velocidades_bucle(bucle):
    
    if isinstance(bucle, tuple) and len(bucle) == 2:
        try:
            primero = int(bucle[0])
            return primero
        except ValueError:
            print(f"Error al convertir el primer elemento: {bucle[0]}")
    return None


def realizar_click2(boton2, velocidad2, velocidades_bucle2, repeticiones2):
    
    
    
    global conta2, colores2, cont_errores, numero_exitos_confirmado, contabilidad, ejecutado1,cantidad_errores_maxima
    global dur_temporal
    boton_primero = botones2[0]
    conta2 += 1
    contador_boton_a_presionar_unicamente = 0
    primera_vez = True
    for _ in range(repeticiones2):
        if exit_flag:
            break
        contador_boton_a_presionar_unicamente += 1
       
        #dur_temporal = velocidad2
        if primera_vez:
            dur_temporal = velocidad2
            primera_vez = False
        else:
            dur_temporal = velocidades_bucle2
        color_actual = pyautogui.screenshot().getpixel(boton2)
        if conta2 != repeticiones2: 
            mostrar_tiempo_transcurrido() 
        if repeticiones2 != 1:
            print(f"Botón {conta2} presionado {repeticiones2}/{contador_boton_a_presionar_unicamente} veces, dur_temporal={dur_temporal}")
        print("(", numero_de_veces, "/", contabilidad, "),(", cantidad_botones2, "/", conta2, ")", boton2, ", dur_temporal=", dur_temporal)
        
        pyautogui.moveTo(boton2, duration=dur_temporal)
        
        

       
        
        if repeticiones2 == 1:
            if conta2 <= len(colores2):
                if color_actual == colores2[conta2 - 1]:
                    cont_errores = 0
                    print("es verdad")
                else:
                    cont_errores += 1
                    print(f"Se han cometido {cont_errores} errores")
                    if cont_errores % cantidad_errores_maxima == 0:
                        #reproducir_sonido("Se cometieron {cont_errores} errores, se debe reiniciar el programa")
                        
                        print(f"Se cometieron {cont_errores} errores, se debe reiniciar el programa")
                        generar_y_reproducir(f"Se han cometido {cont_errores} errores, se debe reiniciar el programa")
            else:
                print("Índice fuera de rango para colores2")
        
        if hacerclick:
            pyautogui.click()
            
            time.sleep(0)
        else:
            time.sleep(0)        
    

def realizar_click1(boton1, velocidad1, velocidades_bucle1, repeticiones1):
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    global conta1, colores1,contabilidad, ejecutado1,cantidad_errores_maxima, cont_errores, numero_exitos_confirmado
    
    
    boton_primero = botones2[0]
    conta1 += 1
    
    contador_boton_a_presionar_unicamente = 0
    primera_vez = True
    for _ in range(repeticiones1):
        contador_boton_a_presionar_unicamente += 1
        #dur_temporal = velocidad2
        if primera_vez:
            dur_temporal = velocidad1
            primera_vez = False
        else:
            dur_temporal = velocidades_bucle1
        color_actual = pyautogui.screenshot().getpixel(boton1)
        if conta2 != repeticiones1: 
            mostrar_tiempo_transcurrido() 
        if repeticiones1 != 1:
            print(f"Botón {conta1} presionado {repeticiones1}/{contador_boton_a_presionar_unicamente} veces, dur_temporal={dur_temporal}")
        print("(", numero_de_veces, "/", contabilidad, "),(", cantidad_botones1, "/", conta1, ")", boton1)
        
        pyautogui.moveTo(boton1, duration=dur_temporal)
        
        

       
        
        if repeticiones1 == 1:
            if conta1 <= len(colores2):
                if color_actual == colores1[conta1 - 1]:
                    cont_errores = 0
                    print("es verdad")
                else:
                    cont_errores += 1
                    print(f"Se han cometido {cont_errores} errores")
                    if cont_errores == cantidad_errores_maxima:
                        print(f"Se cometieron {cont_errores} errores, se debe reiniciar el programa")
            else:
                print("Índice fuera de rango para colores2")
        
        if hacerclick:
            pyautogui.click()
            
            time.sleep(0)
        else:
            time.sleep(0)        
    


def ejecutar2():
    print("se esta ejecutando 2")
    global botonabucle
    global coordenadas1, coordenadas2, coordenadas3, botones1
    global colores1, botones2, colores2, ejecutado1
    global cantidad_botones1, cantidad_botones2, cantidad_botones3
    global numero_de_veces_leidas, exit_flag, notificaciones_pendientes, cont_errores, conta2
    global ejecutado1, numero_exitos_confirmado, contabilidad, primera_ejecucion

    botonabucle = 1
    primera_ejecucion = True
    presionar_boton = 3  # Número de veces que se debe presionar el botón 3
    contador_boton_a_presionar_unicamente = 0  # Contador de veces que se ha presionado el botón 3
    
    botones1, colores1, velocidades1, bucles1 = cargar_coordenadas_desde_archivo(coordenadas1)
    
    botones2, colores2, vel2, buc2 = cargar_coordenadas_desde_archivo(coordenadas2)

    vel2opcional, buc2opcional = cargar_velocidades_y_bucles(Velocidades2_y_Bucles2)


    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    if existearchivo_velocidades_y_bucles == True:
        velocidades2 = vel2opcional
        bucles2 = buc2opcional
    if existearchivo_velocidades_y_bucles == False:
        velocidades2 = vel2
        bucles2 = buc2
   
    tiempo_estimado_total = numero_de_veces * 10
    pygame.mixer.init()
     # Espera 4 segundos antes de empezar

    #keyboard_listener = keyboard.Listener(on_press=on_press)
    #keyboard_listener.start()
    
    conta2 = 0

    
    for _ in range(numero_de_veces):
        if exit_flag:
            break
        if is_paused:
            continue 
        while not exit_flag and contabilidad <= numero_de_veces:
            if is_paused:
                continue 
            conta2 = 0
        
            for boton2, velocidad2, bucle2 in zip(botones2, velocidades2, bucles2):
                if exit_flag:
                    break
                
                velocidad2 = velocidades2[conta2]
                bucle2 = bucles2[conta2]
                repeticiones1 = extraer_repeticiones(bucle2)
                velocidades_bucle2 = extraer_velocidades_bucle(bucle2)
                
                if primera_ejecucion:
                    time.sleep(4)
                    velocidad2 = 1
                    print("Es la primera ejecución")
                    primera_ejecucion = False
                
                realizar_click2(boton2, velocidad2, velocidades_bucle2, repeticiones1)
                if exit_flag:
                    break
            registrarprogreso()
            contabilidad += 1
            time.sleep(0)
               # while contador_boton_a_presionar_unicamente < re
                   # numero_exitos_confirmado = realizar_click(boton2, velopeticiones:
                    #if exit_flag:
                    #    breakcidad2, repeticiones)
                    #contador_boton_a_presionar_unicamente += 1
                   # print(f"Botón {botonabucle} presionado {contador_boton_a_presionar_unicamente}/{presionar_boton} veces, dur_temporal={dur_temporal}")
                
            for porcentaje in notificaciones_pendientes:
                notificacionpor(contabilidad, porcentaje, notificaciones_pendientes)
            if exit_flag:
                break
        
        
    if exit_flag:
        print("El programa ha sido detenido por el usuario.")
        sys.exit()

    keyboard_listener.stop()


def ejecutar1():
    print("se esta ejecutando 1")
    global botonabucle
    global coordenadas1, coordenadas2, coordenadas3, botones1
    global colores1, botones2, colores2, ejecutado1
    global cantidad_botones1, cantidad_botones2, cantidad_botones3
    global numero_de_veces_leidas, exit_flag, notificaciones_pendientes, cont_errores, conta1
    global ejecutado1, numero_exitos_confirmado, contabilidad

    botonabucle = 1
    
   
    botones1, colores1, vel1, buc1 = cargar_coordenadas_desde_archivo(coordenadas1)

    vel1opcional, buc1opcional = cargar_velocidades_y_bucles(Velocidades1_y_Bucles1)


    if existearchivo_velocidades_y_bucles == True:
        velocidades1 = vel1opcional
        bucles1 = buc1opcional
    if existearchivo_velocidades_y_bucles == False:
        velocidades1 = vel1
        bucles1 = buc1

   
    pygame.mixer.init()
    time.sleep(0)  # Espera 5 segundos antes de empezar

    #keyboard_listener = keyboard.Listener(on_press=on_press)
    #keyboard_listener.start()
    
    conta1 = 0

    
    for _ in range(numero_de_veces):
       
        if exit_flag:
            break
        if is_paused:
            continue 
        while not exit_flag and contabilidad <= 1:
            if is_paused:
                continue 
            conta1 = 0
            
            for boton1, velocidad1, bucle1 in zip(botones1, velocidades1, bucles1):
                
                if exit_flag:
                    break
                velocidad1 = velocidades1[conta1]
                bucle1 = bucles1[conta1]
                repeticiones1 = extraer_repeticiones(bucle1)
                velocidades_bucle1 = extraer_velocidades_bucle(bucle1)
                realizar_click1(boton1, velocidad1, velocidades_bucle1, repeticiones1)
            contabilidad += 1
               # while contador_boton_a_presionar_unicamente < re
                   # numero_exitos_confirmado = realizar_click(boton2, velopeticiones:
                    #if exit_flag:
                    #    breakcidad2, repeticiones)
                    #contador_boton_a_presionar_unicamente += 1
                   # print(f"Botón {botonabucle} presionado {contador_boton_a_presionar_unicamente}/{presionar_boton} veces, dur_temporal={dur_temporal}")
                
            """for porcentaje in notificaciones_pendientes:
                notificacionpor(contabilidad, porcentaje, notificaciones_pendientes)
            else:
                numero_exitos_confirmado = realizar_click(boton2)"""
                    
            
            """print("#--------------------------------------------------------------")
            caso_de_error(numero_exitos_confirmado)
            contabilidad += 1    
            if esperarentrebucle:
                time.sleep(0)
            """    
        
       

    if exit_flag:
        print("El programa ha sido detenido por el usuario.")
        sys.exit()

    #keyboard_listener.stop()







def ejecutar3():
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    print("se está ejecutando 3")
   
    global conta3, cont_errores, numero_exitos_confirmado, contabilidad, botones3, colores3, cantidad_botones3, cantidad_errores_maxima, coordenadas3
    global exit_flag
    botones3, colores3 = cargar_coordenadas_desde_archivo(coordenadas3)
    cantidad_botones3, cantidad_colores3 = cantidadbotones(botones3, colores3)
    dur = 0.1
    conta3 = 0
    while not exit_flag and conta3 < cantidad_botones3:
        if is_paused:
            continue
        boton3 = botones3[conta3]
        conta3 += 1
        try:
            x, y = boton3
            color_actual = pyautogui.screenshot().getpixel((x, y))
            print ("(", cantidad_botones3, "/", conta3, "),", boton3,)
            pyautogui.moveTo(boton3, duration=dur)

            if color_actual == colores3[conta3-1]:
                print("Es verdad")
                cont_errores = 0
                if conta3 == cantidad_botones3:
                    numero_exitos_confirmado = contabilidad
                print("casos de éxito confirmados:", numero_exitos_confirmado)
            else:
                cont_errores += 1
                print(f"Se han cometido {cont_errores} errores")
                if cont_errores == cantidad_errores_maxima:
                    if conta3 == cantidad_botones3:
                        numero_exitos_confirmado = contabilidad
                    print("casos de éxito confirmados:", numero_exitos_confirmado)
            if hacerclick:
               pyautogui.click()
               print("click")
            if compararyrevisar:
                time.sleep(0)
            else:
                time.sleep(0)
        except Exception as e:
            print("Error ejecutando la tercera coordenada:", e)

# Continúa con el resto del código como estaba



def decision3():
    global establecerbotones, exit_flag, coordenadas1, coordenadas2, coordenadas3
    global botones1, colores1, botones2, colores2, botones3, colores3

    botones1, colores1 = cargar_coordenadas_desde_archivo(coordenadas1)
    botones2, colores2 = cargar_coordenadas_desde_archivo(coordenadas2)
    botones3, colores3 = cargar_coordenadas_desde_archivo(coordenadas3)

    if not establecerbotones:
        print("Iniciando el bucle para ejecutar3...")
        ejecutar3()  # Llama directamente a ejecutar3
       

# El resto del código continúa como estaba


def decision2():
    
    global establecerbotones, exit_flag, coordenadas2
    global ejecutado1
    global start_time
    start_time = time.time()
    #print("iniciando tiempo2")
    ejecutado1 = False
    #1print(botones2)
    if not establecerbotones:
        #print("Iniciando el bucle...")
        ejecutar2()
        time.sleep(10)
        ejecutar3()
    

def decision1():
    global ejecutado1
    ejecutado1 = True
    global establecerbotones, exit_flag, coordenadas1, botones1, colores1, botones2, colores2, botones3, colores3, velocidades1, velocidades2, velocidades3, numero_exitos_confirmado, contabilidad

    botones1, colores1, velocidades1, bucles1 = cargar_coordenadas_desde_archivo(coordenadas1)
    botones2, colores2, velocidades2, bucles2 = cargar_coordenadas_desde_archivo(coordenadas2)
    botones3, colores3, velocidades3, bucles3 = cargar_coordenadas_desde_archivo(coordenadas3)

    if not establecerbotones:
        iniciar_keyboard_listener()
        print("Iniciando el bucle...")
        ejecutar1()  # Pasa los botones, colores y velocidades a ejecutar1
        numero_exitos_confirmado = 2
        contabilidad = 3
        time.sleep(12)
        ejecutar2()  # Pasa los botones, colores y velocidades a ejecutar2
        #ejecutar3()  # Pasa los botones, colores y velocidades a ejecutar3

# Mas definiciones--------------------------------------------------








def set_ejecutardecision_false():
    global ejecutardecision
    """if not ejecutardecision:
        print("No se presionó ninguna tecla 'f' en 5 segundos.")"""

def main():
    global keyboard_listener, f_pressed_within_limit

    # Set the flag to False initially
    f_pressed_within_limit = False

    # Start a timer to reset the flag after 5 seconds
    timer = Timer(5.0, set_ejecutardecision_false)
    timer.start()

    # Start the keyboard listener
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    # Wait indefinitely for the listener to stop (on 'esc' key press or after processing 'f' and another key)
    keyboard_listener.join()

    # If the timer is still running, cancel it and print the message
    if timer.is_alive():
        timer.cancel()
        """ if not ejecutardecision:
            print("No se presionó ninguna tecla 'f' en 5 segundos.")"""

# ... (other code)

if __name__ == "__main__":
    main()






    """if conta2 <= len(colores2):
            if color_actual == colores2[conta2 - 1]:
                cont_errores = 0
            else:
                cont_errores += 1
                print(f"Se han cometido {cont_errores} errores")
                if cont_errores == cantidad_errores_maxima:
                    
                    if conta2 == cantidad_botones2:
                        if ejecutado1:
                            numero_exitos_confirmado = int((((contabilidad + 1) * cantidad_botones2) - cont_errores) / cantidad_botones2)
                        if not ejecutado1:
                            numero_exitos_confirmado = int((((contabilidad + 1) * cantidad_botones2) - cont_errores) / cantidad_botones2)
                    print("Se cometieron {cont_errores} errores, se debe reiniciar el programaa")
                    #agregar en la linea anterior una definicion para notificar que la cantidad de erorres maxikma ya fue alcanzada
        else:
            print("Índice fuera de rango para colores2")"""