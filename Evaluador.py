class Evaluador:
    def __init__(self, tipo):
        self.tipo = tipo

    def funcionEvaluacion(self, tablero, listaFichasSinJugar, nodoOponente):
        if self.tipo == 1:
            return self.funcionEvaluacionSimple(tablero, listaFichasSinJugar, nodoOponente)
        elif self.tipo == 2:
            return self.funcionEvaluacionCompleja(tablero, listaFichasSinJugar, nodoOponente, restarLineasDe2=True)
        elif self.tipo == 3:
            return self.funcionEvaluacionCompleja(tablero, listaFichasSinJugar, nodoOponente, restarLineasDe2=False)
        

    #Solo asigna puntos si el tablero es ganador o perdedor
    def funcionEvaluacionSimple(self, tablero, listaFichasSinJugar, nodoOponente):
        puntuacion = 0
        if tablero.esGanador():
            puntuacion = 1
        elif tablero.estaCompleto():
            puntuacion = 0
        elif tablero.esEscenarioDeNoVictoria():
            puntuacion = -1
        
        if nodoOponente:
            puntuacion = -puntuacion
        return puntuacion
    

    #Tambien asigna puntos por tener lineas de 3 o 2 fichas prometedoras, teniendo en cuenta las fichas que quedan por colocar
    def funcionEvaluacionCompleja(self, tablero, listaFichasSinJugar, nodoOponente, restarLineasDe2):
        puntuacion = 0
        if tablero.esGanador():
            puntuacion = 10000
        elif tablero.estaCompleto():
            puntuacion = 0
        elif tablero.esEscenarioDeNoVictoria():
            puntuacion = -10000
        else:
            #3 en la misma linea
            fichasLineas = tablero.fichasTodasLineas()
            for fichasLinea in fichasLineas:
                if fichasLinea.count(None) == 1: #comprobamos que haya 3 fichas en esa linea
                    fichasLinea.remove(None) #quitamos el None de la lista
                    for caracteristica in tablero.caracteristicas:
                        comparten = tablero.compartenCaracteristica(fichasLinea, caracteristica)
                        if comparten != False: #para cada caracteristica comprobamos si la comparten todas las fichas
                            for fichaSinJugar in listaFichasSinJugar:
                                if fichaSinJugar.caracteristicas[caracteristica] == comparten: #Comprobamos si hay alguna ficha sin jugar con la caracteristica común
                                    puntuacion -= 41
                                    break
            #2 en la misma linea
            fichasLineas = tablero.fichasTodasLineas()
            for fichasLinea in fichasLineas:
                if fichasLinea.count(None) == 2: #comprobamos que haya 2 fichas en esa linea
                    fichasLinea.remove(None)
                    fichasLinea.remove(None) #quitamos los 2 None de la lista
                    for caracteristica in tablero.caracteristicas:
                        comparten = tablero.compartenCaracteristica(fichasLinea, caracteristica)
                        if comparten != False: #para cada caracteristica comprobamos si la comparten todas las fichas
                            for fichaSinJugar in listaFichasSinJugar:
                                if fichaSinJugar.caracteristicas[caracteristica] == comparten: #Comprobamos si hay alguna ficha sin jugar con la caracteristica común
                                    if restarLineasDe2:
                                        puntuacion -= 1
                                    else:
                                        puntuacion += 1
                                    break
        
        if nodoOponente:
            puntuacion = -puntuacion

        return puntuacion
    

    