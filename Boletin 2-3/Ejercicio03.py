import random
import multiprocessing

# Proceso 1: Generar 6 notas aleatorias entre 1 y 10 y escribirlas en el fichero
def generar6_numero(fichero):
    notas = []
    for _ in range(6):
        nota = round(random.uniform(1, 10), 2)  # Generar notas aleatorias con dos decimales
        notas.append(nota)

    # Escribir las notas en el fichero
    with open(fichero, 'w', encoding='utf-8') as f:
        for nota in notas:
            f.write(str(nota) + '\n')

    print(f"Notas generadas en {fichero}: {notas}")
    return fichero  # Devolver el nombre del fichero para el proceso siguiente


# Proceso 2: Leer las notas desde el fichero y calcular la media, luego guardarla
def leer_fichero(fichero, alumno):
    with open(fichero, 'r', encoding='utf-8') as f:
        notas = [float(linea.strip()) for linea in f]  # Leer y convertir a flotante las notas

    media = sum(notas) / len(notas)  # Calcular la media
    media = round(media, 2)  # Redondear a dos decimales

    # Escribir la media en media.txt (modo 'a' para no sobrescribir)
    with open("media.txt", 'a', encoding='utf-8') as f:
        f.write(f"{alumno} {media}\n")

    print(f"Media para {alumno}: {media}")
    return media


# Proceso 3: Leer las medias desde el fichero y obtener la máxima
def leer_medias():
    nota_maxima = -1
    alumno_maxima = ""
    with open("media.txt", 'r', encoding='utf-8') as f:
        for linea in f:
            partes = linea.strip().split(" ", 1)  # Divide en nombre y media
            if len(partes) == 2:
                try:
                    nota = float(partes[1])  # Intentar convertir la media a número
                    nombre = partes[0]

                    if nota > nota_maxima:  # Comparar para encontrar la máxima
                        nota_maxima = nota
                        alumno_maxima = nombre
                except ValueError:
                    pass  # Si no se puede convertir, ignorar la línea

    print(f"Alumno con la nota máxima: {alumno_maxima}: {nota_maxima}")
    return alumno_maxima, nota_maxima


# Función principal para lanzar todos los procesos
def main():
    fichero = "ficheroejer3.txt"  # El fichero único donde se almacenan las notas de los alumnos
    alumnos = ["Hector", "Marco", "Jorge", "Eduardo", "Pablo", "Raul", "JoseMamu", "Dani", "Ezeki", "Tonio"]

    # Paso 1: Generar notas para cada alumno y guardar en el fichero
    for alumno in alumnos:
        with multiprocessing.Pool() as pool:
            # Usamos 'starmap' para pasar los parámetros correctamente (fichero, alumno)
            pool.starmap(generar6_numero, [(fichero,)])  # Generamos el fichero de notas solo una vez
            pool.starmap(leer_fichero, [(fichero, alumno)] )  # Llamamos al proceso para cada alumno

    # Paso 3: Leer las medias y encontrar la máxima
    leer_medias()  # Este paso no se hace de manera concurrente ya que solo es una operación finala


if __name__ == '__main__':
    main()
