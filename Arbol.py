import Juego
import random
import copy

class Arbol:
    def __init__(self, padre, profundidad, turno, tablero, ficha, listaFichasSinJugar):
        self.padre = padre
        self.hijos = []
        self.profundidad = profundidad
        if padre is None:
            self.turno = self.copiarTurno(turno)
            self.tablero = self.copiarTablero(tablero)
            self.listaFichasSinJugar = self.copiarListaFichasSinJugar(listaFichasSinJugar)
        else:
            self.turno = turno
            self.tablero = tablero
            self.listaFichasSinJugar = listaFichasSinJugar
        self.ficha = ficha
        

    def expandirArbol(self, niveles):
        nodosAExpandir = [self]
        profundidadActual = 0
        profundidadLimite = niveles
        
        #EXPANDIR N NIVELES
        while profundidadActual < profundidadLimite:
            for nodoPadre in nodosAExpandir:
                if nodoPadre.turno.accion == "Coloca":
                    for fila in range(4):
                        for columna in range(4):
                            if nodoPadre.tablero.getFicha(fila, columna) == None:
                                tableroHijo = self.copiarTablero(nodoPadre.tablero)
                                tableroHijo.colocarFicha(nodoPadre.ficha, fila, columna)
                                turnoHijo = self.copiarTurno(nodoPadre.turno)
                                turnoHijo.siguienteTurno()
                                nodoPadre.hijos.append(self.crearHijo(nodoPadre, nodoPadre.profundidad+1, turnoHijo, tableroHijo, None, self.copiarListaFichasSinJugar(nodoPadre.listaFichasSinJugar)))

                elif nodoPadre.turno.accion == "Elige":
                    if not nodoPadre.tablero.esGanador():
                        for fichaSinJugar in nodoPadre.listaFichasSinJugar:
                            listaFichasSinJugarHijo = self.copiarListaFichasSinJugar(nodoPadre.listaFichasSinJugar)
                            listaFichasSinJugarHijo.remove(fichaSinJugar)
                            turnoHijo = self.copiarTurno(nodoPadre.turno)
                            turnoHijo.siguienteTurno()
                            nodoPadre.hijos.append(self.crearHijo(nodoPadre, nodoPadre.profundidad+1, turnoHijo, self.copiarTablero(nodoPadre.tablero), fichaSinJugar, listaFichasSinJugarHijo))
                            
            if len(nodosAExpandir) > 0:
                profundidadActual = nodosAExpandir[0].profundidad
                nuevosNodosAExpandir = []
                for nodoPadre in nodosAExpandir:
                    nuevosNodosAExpandir += nodoPadre.hijos
                nodosAExpandir = nuevosNodosAExpandir
            else:
                break

    def crearHijo(self, padre, profundidad, turno, tablero, ficha, listaFichasSinJugar):
        return Arbol(padre, profundidad, turno, tablero, ficha, listaFichasSinJugar)


    def buscarNodoPorTablero(self, tablero):
        if self.tablero.fichasTablero == tablero.fichasTablero:
            return self
        else:
            if len(self.hijos) == 0:
                return None
            else:
                for hijo in self.hijos:
                    resultado = hijo.buscarNodoPorTablero(tablero)
                    if resultado != None:
                        return resultado
                    
    def copiarTablero(self, tablero):
        nuevoTablero = Juego.Tablero()
        nuevoTablero.fichasTablero = [[c for c in f] for f in tablero.fichasTablero]
        nuevoTablero.contador = tablero.contador
        return nuevoTablero

    def copiarListaFichasSinJugar(self, listaFichasSinJugar):
        nuevaLista = []
        nuevaLista = [ficha for ficha in listaFichasSinJugar]
        return nuevaLista
    
    def copiarTurno(self, turno):
        return copy.copy(turno)  
                    
    

class ArbolMinimax(Arbol):
    def __init__(self, padre, profundidad, turno, tablero, ficha, listaFichasSinJugar):
        super().__init__(padre, profundidad, turno, tablero, ficha, listaFichasSinJugar)
        self.puntuacion = 0

    def crearHijo(self, padre, profundidad, turno, tablero, ficha, listaFichasSinJugar):
        return ArbolMinimax(padre, profundidad, turno, tablero, ficha, listaFichasSinJugar)
    

class ArbolAlphaBeta(Arbol):
    def __init__(self, padre, profundidad, turno, tablero, ficha, listaFichasSinJugar):
        super().__init__(padre, profundidad, turno, tablero, ficha, listaFichasSinJugar)
        self.alphabeta = None

    def crearHijo(self, padre, profundidad, turno, tablero, ficha, listaFichasSinJugar):
        return ArbolAlphaBeta(padre, profundidad, turno, tablero, ficha, listaFichasSinJugar)




class ArbolMCTS(Arbol):
    def __init__(self, padre, profundidad, turno, tablero, ficha, listaFichasSinJugar):
        super().__init__(padre, profundidad, turno, tablero, ficha, listaFichasSinJugar)
        self.numeroVisitas = 0
        self.numeroVictorias = 0

    def crearHijo(self, padre, profundidad, turno, tablero, ficha, listaFichasSinJugar):
        return ArbolMCTS(padre, profundidad, turno, tablero, ficha, listaFichasSinJugar)


    def seleccion(self):
        if len(self.hijos) == 0:
            return self
        else:
            hijoSeleccionado = random.choice(self.hijos)
            return hijoSeleccionado.seleccion()
        
    def turnoAleatorio(self, nodo, returnNodo=False, returnResultado=False):

        turnoCopia = self.copiarTurno(nodo.turno)
        tableroCopia = self.copiarTablero(nodo.tablero)
        listaFichasSinJugarCopia = self.copiarListaFichasSinJugar(nodo.listaFichasSinJugar)
        resultado = None

        if turnoCopia.accion == "Coloca":
            celdasVacias = []
            for fila in range(4):
                for columna in range(4):
                    if tableroCopia.fichasTablero[fila][columna] == None:
                        celdasVacias.append((fila, columna))
            fila, columna = random.choice(celdasVacias)
            tableroCopia.colocarFicha(nodo.ficha, fila, columna)
            if tableroCopia.esGanador():
                resultado = turnoCopia.jugador.numero
            elif tableroCopia.estaCompleto():
                resultado = 0
            fichaCopia = None
            turnoCopia.siguienteTurno()
        else: #Elige
            fichaCopia = random.choice(listaFichasSinJugarCopia)
            listaFichasSinJugarCopia.remove(fichaCopia)
            turnoCopia.siguienteTurno()

        if returnNodo and not returnResultado:
            return ArbolMCTS(nodo, nodo.profundidad+1, turnoCopia, tableroCopia, fichaCopia, listaFichasSinJugarCopia)
        elif not returnNodo and returnResultado:
            return resultado
        elif returnNodo and returnResultado:
            return ArbolMCTS(nodo, nodo.profundidad+1, turnoCopia, tableroCopia, fichaCopia, listaFichasSinJugarCopia), resultado

        
    def expansion(self):
        return self.turnoAleatorio(self, returnNodo=True)

    def simulacion(self, miNumeroJugador):
        if self.tablero.esGanador():
            ganador = self.turno.jugador.numero
            if ganador == miNumeroJugador:
                resultado = 1
            else:
                resultado = 0
        elif self.tablero.estaCompleto():
            resultado = 0
        else:
            terminada = False
            nodo = self
            while not terminada:
                nodo, ganador = self.turnoAleatorio(nodo, returnNodo=True, returnResultado=True)
                if ganador != None:
                    terminada = True
            
            if miNumeroJugador == ganador:
                resultado = 1
            else:
                resultado = 0
        return resultado

    def retropropagacion(self, resultado):
        self.numeroVisitas += 1
        self.numeroVictorias += resultado

        if not self.padre == None:
            self.padre.retropropagacion(resultado)

    def hijoConMejorRatio(self):
        mejorRatio = 0
        mejorHijo = self.hijos[0]

        for hijo in self.hijos:
            if hijo.numeroVisitas > 0:
                ratio = hijo.numeroVictorias / hijo.numeroVisitas
                if ratio >= mejorRatio:
                    mejorRatio = ratio
                    mejorHijo = hijo
        return mejorHijo 
    
    
                


     