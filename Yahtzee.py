import random
import csv

class Dados:
    def __init__(self):
        self.dados = [0] * 5

    def lanzar(self):
        self.dados = [random.randint(1, 6) for _ in range(5)]

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntuacion = {f"{i}": None for i in range(1, 7)}
        self.puntuacion.update({
            "Tres iguales": None,
            "Cuatro iguales": None,
            "Full House": None,
            "Escalera pequeña": None,
            "Escalera grande": None,
            "Chance": None,
            "Yahtzee": None
        })
        self.bono_superior = 0
        self.total_puntuacion = 0
    
    def actualizar_puntuacion(self, categoria, puntos):
        if self.puntuacion[categoria] is None:
            self.puntuacion[categoria] = puntos
            if categoria in map(str, range(1, 7)):
                self.calcular_bono_superior()
            self.total_puntuacion += puntos
    
    def calcular_bono_superior(self):
        subtotal = sum(v for k, v in self.puntuacion.items() if k in map(str, range(1, 7)) and v is not None)
        if subtotal >= 63:
            self.bono_superior = 35
        else:
            self.bono_superior = 0

def calcular_puntuacion(dados, categoria):
    if categoria in map(str, range(1, 7)):
        numero = int(categoria)
        return dados.count(numero) * numero
    elif categoria == "Tres iguales":
        return sum(dados) if any(dados.count(i) >= 3 for i in set(dados)) else 0
    elif categoria == "Cuatro iguales":
        return sum(dados) if any(dados.count(i) >= 4 for i in set(dados)) else 0
    elif categoria == "Full House":
        unique_counts = set(dados.count(i) for i in set(dados))
        return 25 if unique_counts == {2, 3} else 0
    elif categoria == "Escalera pequeña":
        escaleras_pequeñas = [set(range(i, i+4)) for i in range(1, 4)]
        return 30 if any(set(dados).issuperset(esc) for esc in escaleras_pequeñas) else 0
    elif categoria == "Escalera grande":
        return 40 if set(dados) in [set(range(1, 6)), set(range(2, 7))] else 0
    elif categoria == "Chance":
        return sum(dados)
    elif categoria == "Yahtzee":
        return 50 if len(set(dados)) == 1 else 0

def mostrar_posibles_puntuaciones(dados, puntuaciones):
    posibles_puntuaciones = {}
    for categoria in puntuaciones:
        if puntuaciones[categoria] is None:
            puntos = calcular_puntuacion(dados, categoria)
            posibles_puntuaciones[categoria] = puntos
            print(f"{categoria}: {puntos} puntos")
    return posibles_puntuaciones

def mejor_categoria(posibles_puntuaciones):
    mejor_cat = max(posibles_puntuaciones, key=posibles_puntuaciones.get)
    mejor_punt = posibles_puntuaciones[mejor_cat]
    return mejor_cat, mejor_punt

def mostrar_tablero(jugador1, jugador2):
    print(f"\nPuntuaciones de {jugador1.nombre}:")
    for k, v in jugador1.puntuacion.items():
        print(f"{k}: {v if v is not None else '-'}")
    print(f"Bono Superior: {jugador1.bono_superior}")
    print(f"Total: {jugador1.total_puntuacion + jugador1.bono_superior}")

    print(f"\nPuntuaciones de {jugador2.nombre}:")
    for k, v in jugador2.puntuacion.items():
        print(f"{k}: {v if v is not None else '-'}")
    print(f"Bono Superior: {jugador2.bono_superior}")
    print(f"Total: {jugador2.total_puntuacion + jugador2.bono_superior}")

def determinar_ganador(jugador1, jugador2):
    puntuacion_final1 = jugador1.total_puntuacion + jugador1.bono_superior
    puntuacion_final2 = jugador2.total_puntuacion + jugador2.bono_superior

    if puntuacion_final1 > puntuacion_final2:
        ganador = jugador1.nombre
        puntos_ganador = puntuacion_final1
        perdedor = jugador2.nombre
        puntos_perdedor = puntuacion_final2
        print(f"\nEl ganador es {jugador1.nombre} con {puntuacion_final1} puntos.")
    elif puntuacion_final2 > puntuacion_final1:
        ganador = jugador2.nombre
        puntos_ganador = puntuacion_final2
        perdedor = jugador1.nombre
        puntos_perdedor = puntuacion_final1
        print(f"\nEl ganador es {jugador2.nombre} con {puntuacion_final2} puntos.")
    else:
        ganador = "Empate"
        puntos_ganador = puntuacion_final1
        perdedor = "Empate"
        puntos_perdedor = puntuacion_final2
        print(f"\nEl juego es un empate con {puntuacion_final1} puntos cada uno.")
    
    return ganador, puntos_ganador, perdedor, puntos_perdedor

# Juego Principal
def jugar_yahtzee():
    jugador1 = Jugador(input("Ingresa Nombre del Jugador 1: "))
    jugador2 = Jugador(input("Ingresa Nombre del Jugador 2: "))
    num_rondas = int(input("¿Cuántas rondas deseas jugar?: "))

    dados = Dados()
    jugadores = [jugador1, jugador2]
    resultados = []

    for ronda in range(num_rondas):
        for jugador in jugadores:
            input(f"\nPresiona Enter para el turno de {jugador.nombre} - Ronda {ronda + 1}")
            
            for lanzamiento in range(3):
                dados.lanzar()
                print(f"Lanzamiento {lanzamiento + 1}: {dados.dados}")
                if lanzamiento == 2:
                    print("Puntuaciones posibles:")
                    posibles_puntuaciones = mostrar_posibles_puntuaciones(dados.dados, jugador.puntuacion)
                    mejor_cat, mejor_punt = mejor_categoria(posibles_puntuaciones)
                    print(f"Categoría seleccionada automáticamente: {mejor_cat} con {mejor_punt} puntos.")
                    jugador.actualizar_puntuacion(mejor_cat, mejor_punt)
                    resultados.append([jugador.nombre, ronda + 1, lanzamiento + 1, dados.dados.copy(), mejor_cat, mejor_punt])
                else:
                    resultados.append([jugador.nombre, ronda + 1, lanzamiento + 1, dados.dados.copy()])
                    input("Presiona Enter para el siguiente lanzamiento...")

            mostrar_tablero(jugador1, jugador2)

    ganador, puntos_ganador, perdedor, puntos_perdedor = determinar_ganador(jugador1, jugador2)

    # Guardar resultados en un archivo CSV
    with open('resultados_yahtzee.csv', mode='w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow([])
        writer.writerow(["Ganador : " , ganador])
        writer.writerow(["Puntos: "  , puntos_ganador])
        writer.writerow(["Perdedor: " , perdedor ])
        writer.writerow(["Puntos: " ,   puntos_perdedor])

# Ejecutar el juego
jugar_yahtzee()
