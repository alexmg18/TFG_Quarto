import random
import copy
import Juego
import sys
from time import time
from Arbol import ArbolMinimax, ArbolAlphaBeta, ArbolMCTS
from Evaluador import Evaluador

class Agente:
    def __init__(self):
        self.tiempoElige = 0
        self.tiempoColoca = 0
        self.movimientosElige = 0
        self.movimientosColoca = 0

    def getTiempoTotal(self):
        return self.tiempoElige + self.tiempoColoca
    def getTiempoElige(self):
        return self.tiempoElige
    def getTiempoColoca(self):
        return self.tiempoColoca
    def getMovimientosElige(self):
        return self.movimientosElige
    def getMovimientosColoca(self):
        return self.movimientosColoca

class Persona(Agente):
    def __init__(self):
        super().__init__()

    def turnoElige(self, partida, posicionRaton):
        columna = int((posicionRaton[0] - partida.medidas.MARGENX_FICHASSINJUGAR) // (partida.medidas.ANCHO_CELDAS_FICHASSINJUGAR + partida.medidas.MARGEN_CELDAS))
        fila = int((posicionRaton[1] - partida.medidas.MARGENY_FICHASSINJUGAR) // (partida.medidas.ALTO_CELDAS_FICHASSINJUGAR + partida.medidas.MARGEN_CELDAS))

        if columna <4 and columna>=0 and fila<4 and fila>=0 and partida.fichasSinJugar.matrizFichasSinJugar[fila][columna] != None:
            return partida.fichasSinJugar.matrizFichasSinJugar[fila][columna]
        else:
            return None

    def turnoColoca(self, partida, posicionRaton, ficha, miNumeroJugador):
        columna = int((posicionRaton[0] - partida.medidas.MARGENX_TABLERO) // (partida.medidas.ANCHO_CELDAS + partida.medidas.MARGEN_CELDAS))
        fila = int((posicionRaton[1] - partida.medidas.MARGENY_TABLERO) // (partida.medidas.ALTO_CELDAS + partida.medidas.MARGEN_CELDAS))

        if columna<4 and columna>=0 and fila<4 and fila>=0 and partida.tablero.fichasTablero[fila][columna] == None:
            return fila, columna
        else:
            return None, None
        



class Aleatorio(Agente):
    def __init__(self):
        super().__init__()

    def turnoElige(self, partida, posicionRaton):
        return random.choice(partida.fichasSinJugar.listaFichasSinJugar)
        

    def turnoColoca(self, partida, posicionRaton, ficha, miNumeroJugador):
        celdasVacias = []
        for fila in range(4):
            for columna in range(4):
                if partida.tablero.fichasTablero[fila][columna] == None:
                    celdasVacias.append((fila, columna))
        return random.choice(celdasVacias)






class ReglasSimples(Agente):
    def __init__(self):
        super().__init__()
        
    def turnoElige(self, partida, posicionRaton):
        caracteristicasGanadoras = {}

        fichasLineas = partida.tablero.fichasTodasLineas()
        for fichasLinea in fichasLineas:
            if fichasLinea.count(None) == 1:
                fichasLinea.remove(None)
                for caracteristica in Juego.CARACTERISTICAS:
                    comparten = partida.tablero.compartenCaracteristica(fichasLinea, caracteristica) 
                    if comparten != False:
                        if caracteristica in caracteristicasGanadoras:
                            return random.choice(partida.fichasSinJugar.listaFichasSinJugar) #RANDOM, no hay opcion de que no sea ganadora
                        else:
                            caracteristicasGanadoras[caracteristica] = comparten



        if len(caracteristicasGanadoras) == 0:
            return random.choice(partida.fichasSinJugar.listaFichasSinJugar) #RANDOM, ninguna es ganadora

        fichasNoGanadoras = []
        for ficha in partida.fichasSinJugar.listaFichasSinJugar:
            valida = True
            for caracteristica in caracteristicasGanadoras:
                if ficha.caracteristicas[caracteristica] == caracteristicasGanadoras[caracteristica]:
                    valida = False
            if valida:
                fichasNoGanadoras.append(ficha)

        if len(fichasNoGanadoras) == 0:
            return random.choice(partida.fichasSinJugar.listaFichasSinJugar) #RANDOM, no hay fichas que no tengan ninguna de las caracteristicas ganadoras

        return random.choice(fichasNoGanadoras) #Devolvemos una ficha que no sea ganadora


    def turnoColoca(self, partida, posicionRaton, ficha, miNumeroJugador):
        #Comprobar si la ficha es ganadora
        fichasLineas, posiciones = partida.tablero.fichasTodasLineas(True)
        for fichasLinea, (linea, posicion) in zip(fichasLineas, posiciones):
            auxFichasLinea = copy.copy(fichasLinea)
            if fichasLinea.count(None) == 1:
                fichasLinea.remove(None)
                fichasLinea.append(ficha)
                for caracteristica in Juego.CARACTERISTICAS:
                    if partida.tablero.compartenCaracteristica(fichasLinea, caracteristica) != False:
                        if linea == "fila":
                            fila = posicion
                            columna = auxFichasLinea.index(None)
                        elif linea == "columna":
                            fila = auxFichasLinea.index(None)
                            columna = posicion
                        elif linea == "diagonal":
                            fila = auxFichasLinea.index(None)
                            if posicion == "principal":
                                columna = fila
                            elif posicion == "secundaria":
                                columna = 3-fila
                        return fila, columna

        #Elegir random
        celdasVacias = []
        for fila in range(4):
            for columna in range(4):
                if partida.tablero.fichasTablero[fila][columna] == None:
                    celdasVacias.append((fila, columna))
        return random.choice(celdasVacias)





class ReglasComplejas(Agente):
    def __init__(self):
        super().__init__()

    def turnoElige(self, partida, posicionRaton):
        caracteristicasGanadoras = {}
        fichasLineas = partida.tablero.fichasTodasLineas()
        for fichasLinea in fichasLineas:
            if fichasLinea.count(None) == 1:
                fichasLinea.remove(None)
                for caracteristica in Juego.CARACTERISTICAS:
                    comparten = partida.tablero.compartenCaracteristica(fichasLinea, caracteristica) 
                    if comparten != False:
                        if caracteristica in caracteristicasGanadoras:
                            return random.choice(partida.fichasSinJugar.listaFichasSinJugar) #RANDOM, no hay opcion de que no sea ganadora
                        else:
                            caracteristicasGanadoras[caracteristica] = comparten
        

        if len(caracteristicasGanadoras) == 0:
            return random.choice(partida.fichasSinJugar.listaFichasSinJugar) #RANDOM, ninguna es ganadora

        fichasNoGanadoras = []
        for ficha in partida.fichasSinJugar.listaFichasSinJugar:
            valida = True
            for caracteristica in caracteristicasGanadoras:
                if ficha.caracteristicas[caracteristica] == caracteristicasGanadoras[caracteristica]:
                    valida = False
            if valida:
                fichasNoGanadoras.append(ficha)

        if len(fichasNoGanadoras) == 0:
            return random.choice(partida.fichasSinJugar.listaFichasSinJugar) #RANDOM, no hay fichas que no tengan ninguna de las caracteristicas ganadoras

        return random.choice(fichasNoGanadoras) #Devolvemos una ficha que no sea ganadora


    def turnoColoca(self, partida, posicionRaton, ficha, miNumeroJugador):
        #Comprobar si la ficha es ganadora
        fichasLineas, posiciones = partida.tablero.fichasTodasLineas(True)
        for fichasLinea, (linea, posicion) in zip(fichasLineas, posiciones):
            auxFichasLinea = copy.copy(fichasLinea)
            if fichasLinea.count(None) == 1:
                fichasLinea.remove(None)
                fichasLinea.append(ficha)
                for caracteristica in Juego.CARACTERISTICAS:
                    if partida.tablero.compartenCaracteristica(fichasLinea, caracteristica) != False:
                        if linea == "fila":
                            fila = posicion
                            columna = auxFichasLinea.index(None)
                        elif linea == "columna":
                            fila = auxFichasLinea.index(None)
                            columna = posicion
                        elif linea == "diagonal":
                            fila = auxFichasLinea.index(None)
                            if posicion == "principal":
                                columna = fila
                            elif posicion == "secundaria":
                                columna = 3-fila
                        return fila, columna

        
    

        #Buscar una linea que comparta caracteristicas
        celdasConCaracteristicasCompartidasEnLaLinea = []

        fichasLineas, posiciones = partida.tablero.fichasTodasLineas(True)
        for fichasLinea, (linea, posicion) in zip(fichasLineas, posiciones):
            auxFichasLinea = copy.copy(fichasLinea)
            while(None in fichasLinea):
                fichasLinea.remove(None)
            if len(fichasLinea) > 0:
                fichasLinea.append(ficha)
                for caracteristica in Juego.CARACTERISTICAS:
                    if partida.tablero.compartenCaracteristica(fichasLinea, caracteristica) != False:
                        celdasVacias = []
                        for celda in range(len(auxFichasLinea)):
                            if auxFichasLinea[celda] == None:
                                if linea == "fila":
                                    fila = posicion
                                    columna = celda
                                elif linea == "columna":
                                    fila = celda
                                    columna = posicion
                                elif linea == "diagonal":
                                    fila = celda
                                    if posicion == "principal":
                                        columna = fila
                                    elif posicion == "secundaria":
                                        columna = 3-fila 
                                celdasVacias.append((fila, columna))
                        for (fila, columna) in celdasVacias:
                            if (fila, columna) not in celdasConCaracteristicasCompartidasEnLaLinea:
                                partida.tablero.colocarFicha(partida.turno.jugador.ficha, fila, columna)
                                if not partida.tablero.esEscenarioDeNoVictoria(): #no es escenario de no-victoria
                                    celdasConCaracteristicasCompartidasEnLaLinea.append((fila, columna))
                                partida.tablero.quitarFicha(fila, columna)

                 
       
        if len(celdasConCaracteristicasCompartidasEnLaLinea) > 0:
            return random.choice(celdasConCaracteristicasCompartidasEnLaLinea)
            
        #Elegir random
        celdasVacias = []
        for fila in range(4):
            for columna in range(4):
                if partida.tablero.fichasTablero[fila][columna] == None:
                    celdasVacias.append((fila, columna))
        return random.choice(celdasVacias)





class MiniMax(Agente):
    def __init__(self, turnosExpandidos=1, funcionEvaluacion=1):
        super().__init__()
        self.arbol = None
        self.turnosExpandidos = turnosExpandidos
        self.expansion = turnosExpandidos*2 #x2 porque cada turno está compuesto de dos acciones
        self.evaluador = Evaluador(funcionEvaluacion)

    def turnoElige(self, partida, posicionRaton):

        if self.arbol == None:
            return random.choice(partida.fichasSinJugar.listaFichasSinJugar)

        nodoActual = self.arbol.buscarNodoPorTablero(partida.tablero)
        for hijo in nodoActual.hijos:
            if hijo.puntuacion == nodoActual.puntuacion:
                nodoMovimiento = hijo
                break

        return nodoMovimiento.ficha

        


    def turnoColoca(self, partida, posicionRaton, ficha, miNumeroJugador):
        self.arbol = ArbolMinimax(None, 0, partida.turno, partida.tablero, ficha, partida.fichasSinJugar.listaFichasSinJugar)
        self.arbol.expandirArbol(self.expansion)
        nodoActual = self.arbol


        self.minimax(nodoActual, miNumeroJugador)
        for hijo in nodoActual.hijos:
            if hijo.puntuacion == nodoActual.puntuacion:
                nodoMovimiento = hijo
                break
        
        for fila in range(4):
            for columna in range(4):
                if nodoMovimiento.tablero.getFicha(fila, columna) == ficha:
                    return fila, columna
                
        

    def minimax(self, nodo, miNumeroJugador):
        if len(nodo.hijos) == 0:
            nodoOponente = nodo.turno.jugador.numero != miNumeroJugador
            nodo.puntuacion = self.evaluador.funcionEvaluacion(nodo.tablero, nodo.listaFichasSinJugar, nodoOponente)
        else:
            if miNumeroJugador == nodo.turno.jugador.numero:
                maximizar = True
                puntuacion = -sys.maxsize #-infinito
            else:
                maximizar = False
                puntuacion = sys.maxsize #infinito

            for hijo in nodo.hijos:
                self.minimax(hijo, miNumeroJugador)
                puntuacionHijo = hijo.puntuacion
                if maximizar:
                    if puntuacionHijo > puntuacion:
                        puntuacion = puntuacionHijo
                else:
                    if puntuacionHijo < puntuacion:
                        puntuacion = puntuacionHijo

            nodo.puntuacion = puntuacion 






class AlphaBeta(Agente):
    def __init__(self, turnosExpandidos=1, funcionEvaluacion=1):
        super().__init__()
        self.arbol = None
        self.turnosExpandidos = turnosExpandidos
        self.expansion = turnosExpandidos*2 #x2 porque cada turno está compuesto de dos acciones
        self.evaluador = Evaluador(funcionEvaluacion)

    def turnoElige(self, partida, posicionRaton):
        if self.arbol == None:
            return random.choice(partida.fichasSinJugar.listaFichasSinJugar)
            
        nodoActual = self.arbol.buscarNodoPorTablero(partida.tablero)
        for hijo in nodoActual.hijos:
            if hijo.puntuacion == nodoActual.puntuacion:
                nodoMovimiento = hijo
                break
        
        return nodoMovimiento.ficha
    

    
    def turnoColoca(self, partida, posicionRaton, ficha, miNumeroJugador):

        self.arbol = ArbolAlphaBeta(None, 0, partida.turno, partida.tablero, ficha, partida.fichasSinJugar.listaFichasSinJugar)
        self.arbol.expandirArbol(self.expansion)

        self.alphaBeta(self.arbol, -sys.maxsize, sys.maxsize, miNumeroJugador)
        for hijo in self.arbol.hijos:
            if hijo.puntuacion == self.arbol.puntuacion:
                nodoMovimiento = hijo
                break
        
        for fila in range(4):
            for columna in range(4):
                if nodoMovimiento.tablero.getFicha(fila, columna) == ficha:
                    return fila, columna


    
    def alphaBeta(self, nodo, alpha, beta, miNumeroJugador):
        if len(nodo.hijos) == 0:
            nodoOponente = nodo.turno.jugador.numero != miNumeroJugador
            nodo.puntuacion = self.evaluador.funcionEvaluacion(nodo.tablero, nodo.listaFichasSinJugar, nodoOponente)
            return
        
        if miNumeroJugador == nodo.turno.jugador.numero: #maximizar
            mejorValor = -sys.maxsize

            for hijo in nodo.hijos:
                self.alphaBeta(hijo, alpha, beta, miNumeroJugador)
                valor = hijo.puntuacion
                mejorValor = max(mejorValor, valor)
                alpha = max(alpha, mejorValor)
                if beta <= alpha:
                    break
            nodo.puntuacion = mejorValor
            return
        else: #minimizar
            mejorValor = sys.maxsize
            
            for hijo in nodo.hijos:
                self.alphaBeta(hijo, alpha, beta, miNumeroJugador)
                valor = hijo.puntuacion
                mejorValor = min(mejorValor, valor)
                beta = min (beta, mejorValor)
                if beta <= alpha:
                    break
            nodo.puntuacion = mejorValor
            return
            




                

class MonteCarlo(Agente):
    def __init__(self, turnosExpandidos=1, tiempoSimulacion=1):
        super().__init__()
        self.arbol = None
        self.turnosExpandidos = turnosExpandidos
        self.expansion = turnosExpandidos*2 #x2 porque cada turno está compuesto de dos acciones
        self.tiempoSimulacion = tiempoSimulacion
        
    def turnoElige(self, partida, posicionRaton):
        if self.arbol == None:
            return random.choice(partida.fichasSinJugar.listaFichasSinJugar)

        nodoActual = self.arbol.buscarNodoPorTablero(partida.tablero)
        nodoMovimiento = nodoActual.hijoConMejorRatio()
        
        return nodoMovimiento.ficha
        


    def turnoColoca(self, partida, posicionRaton, ficha, miNumeroJugador):
        self.arbol = ArbolMCTS(None, 0, partida.turno, partida.tablero, ficha, partida.fichasSinJugar.listaFichasSinJugar)
        self.arbol.expandirArbol(self.expansion)
        
        tiempoInicial = time()
        while (time()-tiempoInicial) < self.tiempoSimulacion:
            nodoSeleccionado = self.arbol.seleccion()
            if nodoSeleccionado.tablero.esGanador():
                ganador = nodoSeleccionado.turno.jugador.numero
                if ganador == miNumeroJugador:
                    resultado = 1
                else:
                    resultado = 0
            elif nodoSeleccionado.tablero.estaCompleto():
                resultado = 0
            else:
                nodoExpandido = nodoSeleccionado.expansion()
                resultado = nodoExpandido.simulacion(miNumeroJugador)
            nodoSeleccionado.retropropagacion(resultado)
        
        nodoMovimiento = self.arbol.hijoConMejorRatio()
             
        for fila in range(4):
            for columna in range(4):
                fichaAux = nodoMovimiento.tablero.getFicha(fila, columna)
                if fichaAux != None and fichaAux.caracteristicas == ficha.caracteristicas:
                    return fila, columna

    
    
        


