import datetime
import multiprocessing


def peliculas_año(fichero, año, queue):
    peliculas_filtradas = []

    # Leer el fichero y filtrar las películas por el año de estreno
    with open(fichero, 'r', encoding='utf-8') as f:
        for linea in f:
            # Dividir la línea por el separador ";" para obtener nombre y año
            partes = linea.strip().split(";")
            if len(partes) == 2:
                nombre_pelicula = partes[0]
                año_estreno = int(partes[1])

                if año_estreno == año:  # Verificar si coincide con el año dado
                    peliculas_filtradas.append(nombre_pelicula)

    # Enviar las películas filtradas al proceso que las escribirá
    queue.put(peliculas_filtradas)
    print(f"Películas del año {año}:")
    for pelicula in peliculas_filtradas:
        print(pelicula)


def escribir_pelis(queue, año):
    # Esperar a que se reciban las películas desde la cola
    peliculas = queue.get()

    fichero = f"peliculas_{año}.txt"
    with open(fichero, 'a', encoding='utf-8') as f:
        for pelicula in peliculas:
            f.write(f"{pelicula}\n")
    print(f"Películas del año {año} escritas en {fichero}")


if __name__ == '__main__':
    fichero = "pelis.txt"

    # Pedir al usuario que introduzca el año
    año = int(input("Introduce un año:"))

    # Comprobar si el año es válido (no mayor al actual)
    if año <= datetime.datetime.now().year:
        # Crear una cola para comunicar los procesos
        queue = multiprocessing.Queue()

        # Crear un proceso para filtrar las películas por el año
        proceso_filtrar = multiprocessing.Process(target=peliculas_año, args=(fichero, año, queue))

        # Crear un proceso para escribir las películas filtradas en el archivo
        proceso_escribir = multiprocessing.Process(target=escribir_pelis, args=(queue, año))

        # Iniciar ambos procesos
        proceso_filtrar.start()
        proceso_escribir.start()

        # Esperar a que ambos procesos terminen
        proceso_filtrar.join()
        proceso_escribir.join()

    else:
        print("Año incorrecto. No puede ser mayor que el año actual.")
