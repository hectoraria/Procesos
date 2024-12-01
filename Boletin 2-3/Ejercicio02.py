import multiprocessing
import random

def generar_ips(conexion_salida):

    for _ in range(10):
        ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        conexion_salida.send(ip)
    conexion_salida.close()

def filtrar_clases(conexion_entrada, conexion_salida):
    """Proceso 2: Filtra las IPs que pertenecen a las clases A, B o C y las reenvía."""
    while True:
        try:
            ip = conexion_entrada.recv()
            octeto1 = int(ip.split('.')[0])
            if 1 <= octeto1 <= 126:
                clase = "A"
            elif 128 <= octeto1 <= 191:
                clase = "B"
            elif 192 <= octeto1 <= 223:
                clase = "C"
            else:
                continue
            conexion_salida.send((ip, clase))  # Envía la IP y la clase al Proceso 3
        except EOFError:  # Cuando se cierra la conexión, salir del bucle
            break
    conexion_salida.close()

def imprimir_ips(conexion_entrada):
    """Proceso 3: Recibe las IPs con su clase y las imprime por consola."""
    while True:
        try:
            ip, clase = conexion_entrada.recv()  # Recibe una tupla (IP, Clase)
            print(f"Dirección IP: {ip} - Clase: {clase}")
        except EOFError:  # Cuando se cierra la conexión, salir del bucle
            break

if __name__ == "__main__":
    # Crear pipes para comunicación entre procesos
    pipe1_salida, pipe1_entrada = multiprocessing.Pipe()
    pipe2_salida, pipe2_entrada = multiprocessing.Pipe()

    # Crear los procesos
    proceso1 = multiprocessing.Process(target=generar_ips, args=(pipe1_entrada,))
    proceso2 = multiprocessing.Process(target=filtrar_clases, args=(pipe1_salida, pipe2_entrada))
    proceso3 = multiprocessing.Process(target=imprimir_ips, args=(pipe2_salida,))

    # Iniciar los procesos
    proceso1.start()
    proceso2.start()
    proceso3.start()

    # Esperar a que terminen los procesos
    proceso1.join()
    pipe1_salida.close()  # Cerrar el extremo de lectura del pipe1
    proceso2.join()
    pipe2_salida.close()  # Cerrar el extremo de lectura del pipe2
    proceso3.join()

