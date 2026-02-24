import numpy as np

# ─────────────────────────────────────────────
# NODO DEL ÁRBOL
# ─────────────────────────────────────────────

class NodoTriki:
    def __init__(self, tablero, jugador, padre=None, movimiento=None, profundidad=0):
        self.tablero = tablero.copy()
        self.jugador = jugador
        self.padre = padre
        self.hijos = []
        self.movimiento = movimiento
        self.profundidad = profundidad
        self.resultado = None


# ─────────────────────────────────────────────
# LÓGICA DEL JUEGO
# ─────────────────────────────────────────────

def verificar_ganador(tablero):
    # Filas y columnas
    for i in range(3):
        if tablero[i,0] == tablero[i,1] == tablero[i,2] != ' ':
            return tablero[i,0]
        if tablero[0,i] == tablero[1,i] == tablero[2,i] != ' ':
            return tablero[0,i]

    # Diagonales
    if tablero[0,0] == tablero[1,1] == tablero[2,2] != ' ':
        return tablero[0,0]
    if tablero[0,2] == tablero[1,1] == tablero[2,0] != ' ':
        return tablero[0,2]

    return None


def casillas_vacias(tablero):
    return list(zip(*np.where(tablero == ' ')))


def siguiente_jugador(jugador):
    return 'O' if jugador == 'X' else 'X'


# ─────────────────────────────────────────────
# CONSTRUCCIÓN RECURSIVA DEL ÁRBOL
# ─────────────────────────────────────────────

def construir_arbol(nodo):
    ganador = verificar_ganador(nodo.tablero)

    if ganador:
        nodo.resultado = f"{ganador} gana"
        return

    vacias = casillas_vacias(nodo.tablero)

    if not vacias:
        nodo.resultado = "Empate"
        return

    for fila, col in vacias:
        nuevo_tablero = nodo.tablero.copy()
        nuevo_tablero[fila, col] = nodo.jugador

        hijo = NodoTriki(
            nuevo_tablero,
            siguiente_jugador(nodo.jugador),
            nodo,
            (fila, col),
            nodo.profundidad + 1
        )

        nodo.hijos.append(hijo)
        construir_arbol(hijo)


# ─────────────────────────────────────────────
# ESTADÍSTICAS
# ─────────────────────────────────────────────

def recolectar_hojas(nodo):
    if not nodo.hijos:
        return [nodo]
    hojas = []
    for hijo in nodo.hijos:
        hojas.extend(recolectar_hojas(hijo))
    return hojas


def calcular_estadisticas(raiz):
    hojas = recolectar_hojas(raiz)
    profundidades = [h.profundidad for h in hojas]

    return {
        "profundidad_minima": min(profundidades),
        "profundidad_maxima": max(profundidades),
        "victorias_x": sum(h.resultado == "X gana" for h in hojas),
        "victorias_o": sum(h.resultado == "O gana" for h in hojas),
        "empates": sum(h.resultado == "Empate" for h in hojas),
        "total_hojas": len(hojas),
        "hojas": hojas,
        "raiz": raiz
    }


# ─────────────────────────────────────────────
# VISUALIZACIÓN
# ─────────────────────────────────────────────

def imprimir_tablero(tablero):
    for i, fila in enumerate(tablero):
        print(" | ".join(fila))
        if i < 2:
            print("--+---+--")


def visualizar_estado_final(hoja):
    print("\nEstado Final:")
    imprimir_tablero(hoja.tablero)
    print("Resultado:", hoja.resultado)
    print("Profundidad:", hoja.profundidad)


def visualizar_recorrido(hoja):
    camino = []
    nodo = hoja

    while nodo:
        camino.append(nodo)
        nodo = nodo.padre

    camino.reverse()

    print("\nRecorrido completo:\n")

    for i, nodo in enumerate(camino):
        print(f"Paso {i}")
        imprimir_tablero(nodo.tablero)
        print()


# ─────────────────────────────────────────────
# PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────

def main():
    print("TRIKI – ÁRBOL DE ESTADOS")

    tablero_inicial = np.full((3,3), ' ')
    jugador_inicial = 'X'

    print("\nConstruyendo árbol...")
    raiz = NodoTriki(tablero_inicial, jugador_inicial)
    construir_arbol(raiz)
    print("Árbol construido.")

    stats = calcular_estadisticas(raiz)

    print("\nRESULTADOS:")
    print("Profundidad mínima:", stats["profundidad_minima"])
    print("Profundidad máxima:", stats["profundidad_maxima"])
    print("Victorias X:", stats["victorias_x"])
    print("Victorias O:", stats["victorias_o"])
    print("Empates:", stats["empates"])
    print("Total hojas:", stats["total_hojas"])

    # Mostrar ejemplo
    print("\nMostrando primera hoja generada (recorrido DFS):")
    hoja_ejemplo = stats["hojas"][0]
    # Se muestra la primera hoja como ejemplo verificable
    visualizar_estado_final(hoja_ejemplo)
    visualizar_recorrido(hoja_ejemplo)


if __name__ == "__main__":
    main()