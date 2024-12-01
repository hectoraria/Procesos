import multiprocessing

def contar_vocal(fichero, vocal):
    with open(fichero, 'r', encoding='utf-8') as f:
        texto = f.read().lower()  
        return texto.count(vocal)


def proceso_contar_vocales(fichero):

    vocales = ['a', 'e', 'i', 'o', 'u']
    procesos = []
    resultados = []

    # Crear un proceso por cada vocal
    with multiprocessing.Pool(len(vocales)) as pool:
        resultados = pool.starmap(contar_vocal, [(fichero, vocal) for vocal in vocales])

    # Mostrar los resultados
    for vocal, resultado in zip(vocales, resultados):
        print(f"La vocal '{vocal}' aparece {resultado} veces.")

# Ejemplo de uso
if __name__ == "__main__":
    fichero = "vocales.txt"
    proceso_contar_vocales(fichero)
