import Juego
import Agentes
from time import time
import pandas as pd


class Partida:
    def __init__(self, jugador1, jugador2):
        self.estado = None
        self.tablero = Juego.Tablero()
        self.fichasSinJugar = Juego.FichasSinJugar()
        self.jugador1 = Juego.Jugador(1, jugador1)
        self.jugador2 = Juego.Jugador(2, jugador2) 
        self.turno = Juego.Turno(self.jugador1, self.jugador2)
        self.resultado = None

        

class SimularPartida:
    def __init__(self, jugador1, jugador2, numeroPartidas, guardarResultadosEnCSV=True):
        self.numeroPartidas = numeroPartidas
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.resultados = {0: 0, 1: 0, 2: 0}
        self.dataframe = None
        self.tiempoIncial = time()

        #Tiempos
        self.tiempoTotalAgente1 = 0
        self.tiempoTotalEligeAgente1 = 0
        self.tiempoTotalColocaAgente1 = 0
        self.movimientosTotalesEligeAgente1 = 0
        self.movimientosTotalesColocaAgente1 = 0

        self.tiempoTotalAgente2 = 0
        self.tiempoTotalEligeAgente2 = 0
        self.tiempoTotalColocaAgente2 = 0
        self.movimientosTotalesEligeAgente2 = 0
        self.movimientosTotalesColocaAgente2 = 0

        
        self.guardarResultadosEnCSV = guardarResultadosEnCSV

        self.iniciarPartida()
        
        

    def iniciarPartida(self):
        PORCENTAJE_PROGRESO = 10
        porcentajeProgreso = self.numeroPartidas // PORCENTAJE_PROGRESO
        if porcentajeProgreso == 0:
            porcentajeProgreso = 1

        for i in range(self.numeroPartidas):
            partida = Partida(self.jugador1, self.jugador2)
            
            salir = False
            while not salir:
                partida.resultado = partida.turno.ejecutarTurno(partida, None)

                if partida.resultado != None:
                    salir = True
                    
                else:
                    partida.turno.siguienteTurno()
            if (i+1) % (porcentajeProgreso) == 0:
                print(str(i+1)+"/"+str(self.numeroPartidas))
            
            #Añadir resultado
            self.resultados[partida.resultado] += 1
            #Actualizar tiempos
            self.tiempoTotalAgente1 += partida.jugador1.agente.getTiempoTotal()
            self.tiempoTotalEligeAgente1 += partida.jugador1.agente.getTiempoElige()
            self.tiempoTotalColocaAgente1 += partida.jugador1.agente.getTiempoColoca()
            self.movimientosTotalesEligeAgente1 += partida.jugador1.agente.getMovimientosElige()
            self.movimientosTotalesColocaAgente1 += partida.jugador1.agente.getMovimientosColoca()

            self.tiempoTotalAgente2 += partida.jugador2.agente.getTiempoTotal()
            self.tiempoTotalEligeAgente2 += partida.jugador2.agente.getTiempoElige()
            self.tiempoTotalColocaAgente2 += partida.jugador2.agente.getTiempoColoca()
            self.movimientosTotalesEligeAgente2 += partida.jugador2.agente.getMovimientosElige()
            self.movimientosTotalesColocaAgente2 += partida.jugador2.agente.getMovimientosColoca()


        #SIMULACIÓN COMPLETADA

        #Calcular tiempos
        tiempoTotal = self.redondear(time()-self.tiempoIncial)
        tiempoPartida = self.redondear(float(tiempoTotal)/self.numeroPartidas)
        tiempoMedioPartida1 = self.redondear(self.tiempoTotalAgente1/self.numeroPartidas)
        tiempoMedioElige1 = self.redondear(self.tiempoTotalEligeAgente1/self.movimientosTotalesEligeAgente1)
        tiempoMedioColoca1 = self.redondear(self.tiempoTotalColocaAgente1/self.movimientosTotalesColocaAgente1)
        tiempoMedioPartida2 = self.redondear(self.tiempoTotalAgente2/self.numeroPartidas)
        tiempoMedioElige2 = self.redondear(self.tiempoTotalEligeAgente2/self.movimientosTotalesEligeAgente2)
        tiempoMedioColoca2 = self.redondear(self.tiempoTotalColocaAgente2/self.movimientosTotalesColocaAgente2)
        
        BOLD = '\033[1m'
        END = '\033[0m' 

        parametrosAgente1 = partida.jugador1.nombre
        expansion1, funcionEvaluacion1, tiempoSimulacion1 = "", "", ""
        if isinstance(partida.jugador1.agente, Agentes.MiniMax) or isinstance(partida.jugador1.agente, Agentes.AlphaBeta) or isinstance(partida.jugador1.agente, Agentes.MonteCarlo):
            expansion1 = partida.jugador1.agente.expansion
            parametrosAgente1 += " - Expansión: " + str(expansion1) + " niveles"
            if isinstance(partida.jugador1.agente, Agentes.MiniMax) or isinstance(partida.jugador1.agente, Agentes.AlphaBeta):
                funcionEvaluacion1 = partida.jugador1.agente.evaluador.tipo
                parametrosAgente1 += " - Función de evaluación: " + str(funcionEvaluacion1)
            if isinstance(partida.jugador1.agente, Agentes.MonteCarlo):
                tiempoSimulacion1 = partida.jugador1.agente.tiempoSimulacion
                parametrosAgente1 += " - Tiempo de simulación: " + str(tiempoSimulacion1) + "seg"
        
        parametrosAgente2 = partida.jugador2.nombre
        expansion2, funcionEvaluacion2, tiempoSimulacion2 = "", "", ""
        if isinstance(partida.jugador2.agente, Agentes.MiniMax) or isinstance(partida.jugador2.agente, Agentes.AlphaBeta) or isinstance(partida.jugador2.agente, Agentes.MonteCarlo):
            expansion2 = partida.jugador2.agente.expansion
            parametrosAgente2 += " - Expansión: " + str(expansion2) + " niveles"
            if isinstance(partida.jugador2.agente, Agentes.MiniMax) or isinstance(partida.jugador2.agente, Agentes.AlphaBeta):
                funcionEvaluacion2 = partida.jugador2.agente.evaluador.tipo
                parametrosAgente2 += " - Función de evaluación: " + str(funcionEvaluacion2)
            if isinstance(partida.jugador2.agente, Agentes.MonteCarlo):
                tiempoSimulacion2 = partida.jugador2.agente.tiempoSimulacion
                parametrosAgente2 += " - Tiempo de simulación: " + str(tiempoSimulacion2) + "seg."

        
        
        print("\n\n" + "-"*100)
        print(BOLD + "AGENTES" + END)
        print(parametrosAgente1)
        print(parametrosAgente2)


        print("\n\n" + BOLD + "RESULTADOS" + END +
                "\nGanador " + partida.jugador1.nombre + ": " + str(self.resultados[1]) + " -> {:.2f}%" .format(100*self.resultados[1]/self.numeroPartidas) +
                "\nGanador " + partida.jugador2.nombre + ": " + str(self.resultados[2]) + " -> {:.2f}%" .format(100*self.resultados[2]/self.numeroPartidas) + 
                "\nEmpates: " + str(self.resultados[0]) + " -> {:.2f}%" .format(100*self.resultados[0]/self.numeroPartidas))
        

        print("\n\n" + BOLD+ "ESTADÍSTICAS" + END)
        print("Tiempo total: " + str(tiempoTotal) + " segundos")
        print("Tiempo medio por partida: " + str(tiempoPartida) + " segundos")

        print("\nTiempo medio por partida " + partida.jugador1.nombre + ": " + str(tiempoMedioPartida1) + " segundos")
        print("Tiempo medio por movimiento 'Elige' " + partida.jugador1.nombre + ": " + str(tiempoMedioElige1) + " segundos")
        print("Tiempo medio por movimiento 'Coloca' " + partida.jugador1.nombre + ": " + str(tiempoMedioColoca1) + " segundos")
        
        print("\nTiempo medio por partida " + partida.jugador2.nombre + ": " + str(tiempoMedioPartida2) + " segundos")
        print("Tiempo medio por movimiento 'Elige' " + partida.jugador2.nombre + ": " + str(tiempoMedioElige2) + " segundos")
        print("Tiempo medio por movimiento 'Coloca' " + partida.jugador2.nombre + ": " + str(tiempoMedioColoca2) + " segundos")
        print("-"*100)

        if self.guardarResultadosEnCSV:
            self.leerCSV()
            self.añadirFila(partida.jugador1.nombre, expansion1, funcionEvaluacion1, tiempoSimulacion1, partida.jugador2.nombre, expansion2, funcionEvaluacion2, tiempoSimulacion2, self.numeroPartidas, self.resultados[1], self.resultados[2], self.resultados[0], tiempoTotal, tiempoPartida, tiempoMedioPartida1, tiempoMedioElige1, tiempoMedioColoca1, tiempoMedioPartida2, tiempoMedioColoca2, tiempoMedioColoca2)

    def leerCSV(self):
        try:
            self.dataframe = pd.read_csv("resultados_simulacion.csv", index_col=0)
        except:
            self.dataframe = pd.DataFrame(columns=["Jugador 1", "Expansión 1", "Tipo Función Ev. 1", "Tiempo simulación 1", "Jugador 2", "Expansión 2", "Tipo Función Ev. 2", "Tiempo simulación 2", "Partidas", "Victorias 1", "Victorias 2","Empates", "Tiempo total", "Tiempo por partida", "Tiempo medio por partida Jugador 1", "Tiempo por movimiento 'Elige' Jugador 1", "Tiempo por movimiento 'Coloca' Jugador 1", "Tiempo medio por partida Jugador 2",  "Tiempo por movimiento 'Elige' Jugador 2", "Tiempo por movimiento 'Coloca' Jugador 2"])
            self.dataframe.to_csv("./resultados_simulacion.csv")
        
    def añadirFila(self,j1, exp1, fEv1, tSim1, j2, exp2, fEv2, tSim2, partidas, victorias1, victorias2, empates, tiempoTotal, tiempoPartida, tiempoMedio1, tiempoElige1, tiempoColoca1, tiempoMedio2, tiempoElige2, tiempoColoca2):

        nueva_fila = {"Jugador 1": j1, "Expansión 1": exp1, "Tipo Función Ev. 1": fEv1, "Tiempo simulación 1": tSim1, "Jugador 2": j2, "Expansión 2": exp2, "Tipo Función Ev. 2": fEv2, "Tiempo simulación 2": tSim2, "Partidas": partidas, "Victorias 1": f"{victorias1}  ({round(100*victorias1/partidas, 2)}%)", "Victorias 2": f"{victorias2}  ({round(100*victorias2/partidas, 2)}%)", "Empates": f"{empates}  ({round(100*empates/partidas, 2)}%)", "Tiempo total": tiempoTotal, "Tiempo por partida": tiempoPartida, "Tiempo medio por partida Jugador 1": tiempoMedio1, "Tiempo por movimiento 'Elige' Jugador 1": tiempoElige1, "Tiempo por movimiento 'Coloca' Jugador 1": tiempoColoca1, "Tiempo medio por partida Jugador 2": tiempoMedio2,  "Tiempo por movimiento 'Elige' Jugador 2": tiempoElige2, "Tiempo por movimiento 'Coloca' Jugador 2": tiempoColoca2}
        dataframe_nueva_fila = pd.DataFrame(nueva_fila, index=[len(self.dataframe)])
        self.dataframe = pd.concat([self.dataframe, dataframe_nueva_fila])
        self.dataframe.to_csv("./resultados_simulacion.csv", index=True)

    def redondear(self, numero, decimales=5):
        if numero < 10**(-(decimales-1)):
            formato = "{:."+str(decimales)+"e}"
            return formato.format(numero)
        else:
            numero_redondeado = round(numero, decimales)
            formato = "{:."+str(decimales)+"f}"
            return  formato.format(numero_redondeado)

  


class PartidaConInterfaz(Partida):
    def __init__(self):
        self.ESTADOS = ["Menu", "EnJuego", "Finalizado"]
        self.estado = self.ESTADOS[0]
        self.medidas = None

        self.iniciarPartida()

    def iniciarPartida(self):
        import pygame
        import Interfaz
        interfaz = Interfaz.Interfaz()
        self.medidas = interfaz.getMedidas()
        salir = False
        while not salir:
            if self.estado == self.ESTADOS[0]:
                if not interfaz.mostrarMenu():
                    jugador1, jugador2 = interfaz.menu.obtenerJugadores()
                    super().__init__(jugador1, jugador2)
                    interfaz.crearPartida(self)
                    self.estado = self.ESTADOS[1]
                salir = not interfaz.pintarSalir()

                for evento in pygame.event.get(): 
                    if evento.type == pygame.QUIT: 
                        salir = True
                
            elif self.estado == self.ESTADOS[1]:
                if not interfaz.mostrarJuego():
                    self.estado = self.ESTADOS[0]
                else:
                    posicionRaton = None

                    for evento in pygame.event.get(): 
                        if evento.type == pygame.QUIT: 
                            salir = True
                        if evento.type == pygame.MOUSEBUTTONDOWN:
                            posicionRaton = pygame.mouse.get_pos()

                    if self.turno.jugador.cpu or posicionRaton != None:
                        self.resultado = self.turno.ejecutarTurno(self, posicionRaton)

                        if self.resultado != "No ejecutado":
                            if self.resultado != None:
                                self.estado = self.ESTADOS[2]
                            else:
                                self.turno.siguienteTurno()

            elif self.estado == self.ESTADOS[2]:
                if not interfaz.mostrarJuego():
                    self.estado = self.ESTADOS[0]
                
                for evento in pygame.event.get(): 
                    if evento.type == pygame.QUIT: 
                        salir = True