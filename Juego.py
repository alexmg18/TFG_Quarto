from time import time
import Agentes

CARACTERISTICAS = ['forma', 'tamaño', 'color', 'relleno']

class Tablero:
    def __init__(self):
        self.filas = [0,1,2,3]
        self.columnas = [0,1,2,3]
        self.diagonales = ["principal", "secundaria"]
        self.caracteristicas = ['forma', 'tamaño', 'color', 'relleno']
        self.fichasGanadoras = None

        self.fichasTablero = self.generarTableroVacio()
        self.contador = 0



    def generarTableroVacio(self):
        fichasTablero = []
        for fila in self.filas:
            fichasTablero.append([])
            for columna in self.columnas:
                fichasTablero[fila].append(None)

        return fichasTablero


    def colocarFicha(self, ficha, fila, columna):
        if self.fichasTablero[fila][columna] == None:
            self.fichasTablero[fila][columna] = ficha
            self.contador += 1

    def quitarFicha(self, fila, columna):
        if self.fichasTablero[fila][columna] != None:
            self.fichasTablero[fila][columna] = None
            self.contador -= 1

    def getFicha(self, fila, columna):
        return self.fichasTablero[fila][columna]


    def esGanador(self):
        resultado = False

        fichasLineas = self.fichasTodasLineas()

        for fichasLinea in fichasLineas:
            if self.comprobarLineaFichasGanadora(fichasLinea):
                self.fichasGanadoras = fichasLinea
                resultado = True

        return resultado
    



    def comprobarLineaFichasGanadora(self, fichasLinea):
        resultado = False

        if fichasLinea.count(None) == 0:
            for caracteristica in self.caracteristicas:
                if fichasLinea[0].caracteristicas[caracteristica] == fichasLinea[1].caracteristicas[caracteristica] == fichasLinea[2].caracteristicas[caracteristica] == fichasLinea[3].caracteristicas[caracteristica]:
                    resultado = True

        return resultado
    

    
    def estaCompleto(self):
        return self.contador == 16


    def fichasFila(self, fila):
        fichasFila = []

        for columna in self.columnas:
            fichasFila.append(self.fichasTablero[fila][columna])

        return fichasFila
    


    def fichasColumna(self, columna):
        fichasColumna = []

        for fila in self.filas:
            fichasColumna.append(self.fichasTablero[fila][columna])

        return fichasColumna
    

    def fichasDiagonal(self, diagonal):
        fichasDiagonal = []

        if diagonal == self.diagonales[0]: #principal
            for fila in self.filas:
                fichasDiagonal.append(self.fichasTablero[fila][fila])

        elif diagonal == self.diagonales[1]: #secundaria
            for fila in self.filas:
                fichasDiagonal.append(self.fichasTablero[fila][3-fila])

        return fichasDiagonal
    


    def fichasTodasFilas(self):
        fichasTodasFilas = []

        for fila in self.filas:
            fichasTodasFilas.append(self.fichasFila(fila))

        return fichasTodasFilas
    

    
    def fichasTodasColumnas(self):
        fichasTodasColumnas = []

        for columna in self.columnas:
            fichasTodasColumnas.append(self.fichasColumna(columna))

        return fichasTodasColumnas
    

    def fichasTodasDiagonales(self):
        fichasTodasDiagonales = []

        for diagonal in self.diagonales:
            fichasTodasDiagonales.append(self.fichasDiagonal(diagonal))

        return fichasTodasDiagonales
    

    def fichasTodasLineas(self, incluirPosicion=False):
        fichasTodasLineas = []

        fichasTodasLineas += self.fichasTodasFilas()
        fichasTodasLineas += self.fichasTodasColumnas()
        fichasTodasLineas += self.fichasTodasDiagonales()

        if incluirPosicion:
            posiciones = [("fila", 0), ("fila", 1), ("fila", 2), ("fila", 3), ("columna", 0), ("columna", 1), ("columna", 2), ("columna", 3),
                       ("diagonal", "principal"), ("diagonal", "secundaria")]
            return fichasTodasLineas, posiciones
        
        else:
            return fichasTodasLineas
    


    #Devuelve True si hay dos lineas de 3 fichas que compartan caracteristicas opuestas
    def esEscenarioDeNoVictoria(self):
        caracteristicasGanadoras = {}
        fichasTodasLineas = self.fichasTodasLineas()

        for fichasLinea in fichasTodasLineas:
            if fichasLinea.count(None) == 1: #comprobamos que haya 3 fichas en esa linea
                fichasLinea.remove(None) #quitamos el None de la lista
                for caracteristica in self.caracteristicas:
                    comparten = self.compartenCaracteristica(fichasLinea, caracteristica)
                    if comparten != False: #para cada caracteristica comprobamos si la comparten todas las fichas
                        if caracteristica in caracteristicasGanadoras:
                            if caracteristicasGanadoras[caracteristica] != comparten: #si esa caracteristica ya esta guardada con otro valor, es un escenario de No-Victoria
                                return True
                        else:
                            caracteristicasGanadoras[caracteristica] = comparten #si no tenemos esa caracteristica guardada, la guardamos


        return False


    def compartenCaracteristica(self, fichasLinea, caracteristica):
        valorCaracteristica = False

        if len(fichasLinea) > 0:
            valorCaracteristica = fichasLinea[0].caracteristicas[caracteristica]
            for ficha in fichasLinea:
                if ficha.caracteristicas[caracteristica] != valorCaracteristica:
                    valorCaracteristica = False
                    break

        return valorCaracteristica
    

        

class Turno:
    def __init__(self, jugador1, jugador2):
        self.jugadores = [jugador1, jugador2]
        
        self.jugador = self.jugadores[0]
        self.accion = "Elige"
        self.bloqueado = False


    def cambiarAccion(self):
        if self.accion == "Elige":
            self.accion = "Coloca"
        else:
            self.accion = "Elige"

    def cambiarJugador(self):
        if self.jugador == self.jugadores[0]: #jugador1
            self.jugador = self.jugadores[1] #jugador2
        else:
            self.jugador = self.jugadores[0] #jugador1

    def siguienteTurno(self):
        if self.accion == "Elige":
            self.cambiarJugador()
        self.cambiarAccion()

    def ejecutarTurno(self, partida, posicionRaton):
        if self.accion == "Elige":
            if self.jugador.turnoElige(partida, posicionRaton):
                return None
            else:
                return "No ejecutado"
        elif self.accion == "Coloca":
            return self.jugador.turnoColoca(partida, posicionRaton)
            

    def bloquearTurno(self):
        self.bloqueado = True

    def __str__(self) :
        return (self.accion + " " + str(self.jugador.nombre))


class Jugador:
    def __init__(self, numero, agente):
        self.ficha = None
        self.numero = numero


        if isinstance(agente, Agentes.Persona):
            self.cpu = False
            self.agente = agente
            self.nombre = "Jugador " + str(self.numero)

        else:
            self.cpu = True
            if isinstance(agente, Agentes.Aleatorio):
                self.agente = Agentes.Aleatorio()
                self.nombre = "Agente Aleatorio " + str(self.numero)
            elif isinstance(agente, Agentes.ReglasSimples):
                self.agente = Agentes.ReglasSimples()
                self.nombre = "Agente Reglas Simples " + str(self.numero)
            elif isinstance(agente, Agentes.ReglasComplejas):
                self.agente = Agentes.ReglasComplejas()
                self.nombre = "Agente Reglas Complejas " + str(self.numero)
            elif isinstance(agente, Agentes.MiniMax):
                self.agente = Agentes.MiniMax(agente.turnosExpandidos, agente.evaluador.tipo)
                self.nombre = "Agente MiniMax " + str(self.numero)
            elif isinstance(agente, Agentes.AlphaBeta):
                self.agente = Agentes.AlphaBeta(agente.turnosExpandidos, agente.evaluador.tipo)
                self.nombre = "Agente AlphaBeta " + str(self.numero)
            elif isinstance(agente, Agentes.MonteCarlo):
                self.agente = Agentes.MonteCarlo(agente.turnosExpandidos, agente.tiempoSimulacion)
                self.nombre = "Agente Monte Carlo " + str(self.numero)
            
        
    def turnoElige(self, partida, posicionRaton):
        tiempoInicial = time()
        fichaElegida = self.agente.turnoElige(partida, posicionRaton)
        tiempoMovimiento = time() - tiempoInicial
        self.agente.movimientosElige += 1
        self.agente.tiempoElige += tiempoMovimiento

        if fichaElegida != None:
            if self.numero == 1:
                partida.jugador2.ficha = fichaElegida
            elif self.numero == 2:
                partida.jugador1.ficha = fichaElegida

            partida.fichasSinJugar.eliminarFicha(fichaElegida)

            return True
        else:
            return False

        

    def turnoColoca(self, partida, posicionRaton):
        tiempoInicial = time()
        fila, columna = self.agente.turnoColoca(partida, posicionRaton, self.ficha, self.numero)
        tiempoMovimiento = time() - tiempoInicial
        self.agente.movimientosColoca += 1
        self.agente.tiempoColoca += tiempoMovimiento
        
        
        if fila != None and columna != None:
            partida.tablero.colocarFicha(self.ficha, fila, columna)
            self.ficha = None

            if partida.tablero.esGanador():
                partida.turno.bloquearTurno()
                return self.numero
            elif partida.tablero.estaCompleto():
                partida.turno.bloquearTurno()
                return 0
            else:
                return None
        else:
            return "No ejecutado"
        
        


class Ficha:
    def __init__(self, forma, tamaño, color, relleno):
        self.caracteristicas = {'forma': forma, 'tamaño': tamaño, 'color': color, 'relleno': relleno}
        self.nombreFoto = "fichas/"+ forma[0]+ tamaño[0]+ color[0]+ relleno[0]+".png"
        

 

class FichasSinJugar:
    def __init__(self):
        self.listaFichasSinJugar = self.crearFichas()
        self.matrizFichasSinJugar = []
        for i in range(4):
            self.matrizFichasSinJugar.append([])
            for j in range(4):
                self.matrizFichasSinJugar[i].append(self.listaFichasSinJugar[i*4 + j])


    
    def crearFichas(self):
        fichas = []

        FORMA = ["redonda", "cuadrada"]
        TAMAÑO = ["grande", "pequeño"]
        COLOR = ["rojo", "azul"]
        RELLENO = ["si", "no"]

        for forma in FORMA:
            for tamaño in TAMAÑO:
                for color in COLOR:
                    for relleno in RELLENO:
                        fichas.append(Ficha(forma, tamaño, color, relleno))
        
        return fichas



    def eliminarFicha(self, ficha):
        self.listaFichasSinJugar.remove(ficha)
        for i in range(len(self.matrizFichasSinJugar)):
            for j in range(len(self.matrizFichasSinJugar[i])):
                if self.matrizFichasSinJugar[i][j] == ficha:
                    self.matrizFichasSinJugar[i][j] = None
                    

    