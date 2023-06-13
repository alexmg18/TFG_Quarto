import pygame
import Agentes
import Botones

# COLORES
BLANCO = (255, 255, 255)
VERDE = (55,100,65)
ROJO = (255, 0, 0)
AZUL = (30,144,255)
GRIS_CLARO = (225, 225, 225)
NARANJA = (241, 101, 9)
AMARILLO = (247, 255, 0)
 

# CARACTERISTICAS FICHAS
CARACTERISTICAS = ['forma', 'tamaño', 'color', 'relleno']


class Interfaz:
    def __init__(self, partida=None):
        # Inicializamos pygame
        pygame.init()
        pygame.font.init()

        if partida is not None:
            self.crearPartida(partida)

        # Establecemos el LARGO y ALTO de la pantalla
        self.ANCHO = pygame.display.Info().current_w
        self.ALTO = pygame.display.Info().current_h
        DIMENSION_VENTANA = [self.ANCHO, self.ALTO]
        self.pantalla = pygame.display.set_mode(DIMENSION_VENTANA, pygame.RESIZABLE)

        #Reajustamos el tamaño de la pantalla para que quede por encima de la barra de tareas inferior
        self.ANCHO = self.pantalla.get_width()
        self.ALTO = self.pantalla.get_height()

        DIMENSION_VENTANA = [self.ANCHO, self.ALTO]
        self.pantalla = pygame.display.set_mode(DIMENSION_VENTANA)
        
        self.medidas = Medidas(self.ANCHO, self.ALTO)

        # Diccionario para guardar las imagenes de las fichas
        self.imagenesFichas = dict()

        
        # Establecemos el título de la pantalla.
        pygame.display.set_caption("Quarto")

        #Crear Menu
        self.menu = Menu(self.medidas, self.pantalla)

        # Lo usamos para establecer cada cuanto se refresca la pantalla.
        self.reloj = pygame.time.Clock()
        self.reloj.tick(60)


    def getMedidas(self):
        return self.medidas

    def crearPartida(self, partida):
        self.partida = partida
        for ficha in self.partida.fichasSinJugar.listaFichasSinJugar:
            #Añadir las imagenes de las fichas al diccionario
            imagen = pygame.image.load(ficha.nombreFoto)
            imagen = pygame.transform.scale(imagen, (self.medidas.ANCHO_CELDAS_FICHA_JUGADOR, self.medidas.ALTO_CELDAS_FICHA_JUGADOR))
            self.imagenesFichas[ficha.nombreFoto] = imagen
        self.botonInicio = Botones.Boton(self.medidas.BOTON_MENU_X, self.medidas.BOTON_MENU_Y, self.medidas.BOTON_MENU_ANCHO, self.medidas.BOTON_MENU_ALTO, "Menú", BLANCO, NARANJA, self.pantalla)


    def mostrarJuego(self):
        self.pantalla.fill(VERDE)

        self.pintarTablero()
        self.pintarFichasTablero()
        self.pintarFichasSinJugar()
        self.pintarFichasJugadores()
        self.pintarTurno()
        self.pintarGanador()

        salir = not self.botonInicio.pintar()

        pygame.display.flip()
        
        return salir
        

    def pintarTablero(self):
        for fila in range(4):
            for columna in range(4):
                if self.partida.tablero.fichasGanadoras != None and self.partida.tablero.getFicha(fila, columna) in self.partida.tablero.fichasGanadoras:
                    color = AMARILLO
                else:
                    color = BLANCO
                pygame.draw.rect(self.pantalla,
                                color,
                                [(self.medidas.MARGEN_CELDAS + self.medidas.ANCHO_CELDAS) * columna + self.medidas.MARGENX_TABLERO,
                                (self.medidas.MARGEN_CELDAS + self.medidas.ALTO_CELDAS) * fila + self.medidas.MARGENY_TABLERO,
                                self.medidas.ANCHO_CELDAS,
                                self.medidas.ALTO_CELDAS])



    def pintarFichasTablero(self):
        for fila in range(4):
            for columna in range(4):
                if self.partida.tablero.fichasTablero[fila][columna] != None:
                    
                    self.pantalla.blit(self.imagenesFichas[self.partida.tablero.fichasTablero[fila][columna].nombreFoto],
                    [(self.medidas.MARGEN_CELDAS + self.medidas.ANCHO_CELDAS) * columna + self.medidas.MARGENX_TABLERO,
                    (self.medidas.MARGEN_CELDAS + self.medidas.ALTO_CELDAS) * fila + self.medidas.MARGENY_TABLERO])


    def pintarFichasSinJugar(self):
        for fila in range(4):
            for columna in range(4):
                if self.partida.fichasSinJugar.matrizFichasSinJugar[fila][columna] != None:

                    self.pantalla.blit(self.imagenesFichas[self.partida.fichasSinJugar.matrizFichasSinJugar[fila][columna].nombreFoto],
                    [(self.medidas.MARGEN_CELDAS + self.medidas.ANCHO_CELDAS_FICHASSINJUGAR) * columna + self.medidas.MARGENX_FICHASSINJUGAR,
                    (self.medidas.MARGEN_CELDAS + self.medidas.ALTO_CELDAS_FICHASSINJUGAR) * fila + self.medidas.MARGENY_FICHASSINJUGAR])

        
    def pintarFichasJugadores(self):
        if self.partida.jugador1.ficha != None:
            self.pantalla.blit(self.imagenesFichas[self.partida.jugador1.ficha.nombreFoto], [self.medidas.MARGENX_FICHAS_JUGADOR1, self.medidas.MARGENY_FICHA_JUGADOR1])

        if self.partida.jugador2.ficha != None:
            self.pantalla.blit(self.imagenesFichas[self.partida.jugador2.ficha.nombreFoto], [self.medidas.MARGENX_FICHAS_JUGADOR2, self.medidas.MARGENY_FICHA_JUGADOR2])


    def pintarTurno(self):
        if not self.partida.turno.bloqueado:
            font = pygame.font.Font(None, 60)
            text = font.render(str(self.partida.turno), 1,BLANCO)
            self.pantalla.blit(text, (self.medidas.MARGENX_TABLERO + self.medidas.ANCHO_TABLERO, self.medidas.MARGENY_TABLERO / 4))


    def pintarGanador(self):
        if self.partida.resultado in [0,1,2]:
            font = pygame.font.Font(None, 70)
            if self.partida.resultado == 0:
                textString = "Tablero completo, el resultado es empate"
            elif self.partida.resultado == 1:
                textString = "Ganador " + self.partida.jugador1.nombre
            elif self.partida.resultado == 2:
                textString = "Ganador " + self.partida.jugador2.nombre

            text = font.render(textString, 1, ROJO, BLANCO)
            self.pantalla.blit(text, (self.medidas.MARGENX_TABLERO , self.medidas.MARGENY_TABLERO / 3))


    def mostrarMenu(self):
        pygame.display.flip()
        self.pantalla.fill(VERDE)
        return self.menu.pintar()
    
    def pintarSalir(self):
        return self.menu.pintarSalir()
                    


class Medidas:
    def __init__(self, ancho, alto):
        self.ANCHO = ancho
        self.ALTO = alto

        self.MARGEN_CELDAS = 5

        #TABLERO
        self.MARGENY_TABLERO = self.ALTO / 5
        self.ALTO_TABLERO = self.ALTO * 3 / 5 
        self.ANCHO_TABLERO = self.ALTO_TABLERO
        self.MARGENX_TABLERO = ((self.ANCHO / 2) - self.ANCHO_TABLERO) * 3 / 4

        
        self.ALTO_CELDAS = (self.ALTO_TABLERO - 3 * self.MARGEN_CELDAS) / 4
        self.ANCHO_CELDAS = (self.ANCHO_TABLERO - 3 * self.MARGEN_CELDAS) / 4

        #FICHAS SIN JUGAR
        self.MARGENY_FICHASSINJUGAR = self.MARGENY_TABLERO
        self.ALTO_FICHASSINJUGAR = self.ALTO_TABLERO
        self.ANCHO_FICHASSINJUGAR = self.ANCHO_TABLERO

        MARGENX_FICHASSINJUGAR_RESPECTO_CENTRO = (self.ANCHO / 2) - self.MARGENX_TABLERO - self.ANCHO_TABLERO
        self.MARGENX_FICHASSINJUGAR = (self.ANCHO / 2) + MARGENX_FICHASSINJUGAR_RESPECTO_CENTRO


        self.ALTO_CELDAS_FICHASSINJUGAR = (self.ALTO_FICHASSINJUGAR - 3 * self.MARGEN_CELDAS) / 4
        self.ANCHO_CELDAS_FICHASSINJUGAR = (self.ANCHO_FICHASSINJUGAR - 3 * self.MARGEN_CELDAS) / 4

        #FICHAS JUGADORES
        self.ALTO_CELDAS_FICHA_JUGADOR = self.ALTO_CELDAS
        self.ANCHO_CELDAS_FICHA_JUGADOR = self.ANCHO_CELDAS
        self.MARGENY_FICHA_JUGADOR1 = self.MARGENY_TABLERO / 2 - (self.ALTO_CELDAS_FICHA_JUGADOR / 2)
        self.MARGENY_FICHA_JUGADOR2 = self.ALTO - (self.MARGENY_TABLERO / 2) - (self.ALTO_CELDAS_FICHA_JUGADOR / 2)
        self.MARGENX_FICHAS_JUGADOR1 = self.MARGENX_TABLERO + (self.ANCHO_TABLERO / 2) - (self.ANCHO_CELDAS_FICHA_JUGADOR / 2)
        self.MARGENX_FICHAS_JUGADOR2 = self.MARGENX_FICHAS_JUGADOR1

        
        self.BOTON_MENU_ANCHO = self.ANCHO / 8
        self.BOTON_MENU_ALTO = self.ALTO / 8
        self.BOTON_MENU_X = self.ANCHO - self.BOTON_MENU_ANCHO - 30
        self.BOTON_MENU_Y = 30

        #BOTONES MENU
        MARGEN_BOTONES = 50

        self.BOTON_INICIO_X = self.ANCHO * 7 / 16
        self.BOTON_INICIO_Y = self.ALTO * 3 / 4
        self.BOTON_INICIO_ANCHO = self.ANCHO / 8
        self.BOTON_INICIO_ALTO = self.ALTO / 8

        self.BOTON_SALIR_X = 30
        self.BOTON_SALIR_Y = self.BOTON_MENU_Y
        self.BOTON_SALIR_ANCHO = self.BOTON_INICIO_ANCHO * 3/4
        self.BOTON_SALIR_ALTO = self.BOTON_INICIO_ALTO * 3/4

        self.BOTON_JUGADOR1_X = self.ANCHO / 8
        self.BOTON_JUGADOR1_Y = self.ALTO / 4
        self.BOTON_JUGADOR1_ANCHO = self.ANCHO / 4
        self.BOTON_JUGADOR1_ALTO = self.ALTO / 6

        if self.ANCHO < 1800:
            self.BOTON_JUGADOR1_X -= 50
            self.BOTON_JUGADOR1_ANCHO += 100
            MARGEN_BOTONES = 35

        self.BOTON_CPU1_X = self.BOTON_JUGADOR1_X
        self.BOTON_CPU1_Y = self.BOTON_JUGADOR1_Y + self.BOTON_JUGADOR1_ALTO + MARGEN_BOTONES
        self.BOTON_CPU1_ANCHO = self.BOTON_JUGADOR1_ANCHO
        self.BOTON_CPU1_ALTO = self.BOTON_JUGADOR1_ALTO


        self.BOTON_GRUPO1_X = self.BOTON_JUGADOR1_X - MARGEN_BOTONES
        self.BOTON_GRUPO1_Y = self.BOTON_JUGADOR1_Y - MARGEN_BOTONES
        self.BOTON_GRUPO1_ANCHO = self.BOTON_CPU1_ANCHO + 2 * MARGEN_BOTONES
        self.BOTON_GRUPO1_ALTO = self.BOTON_JUGADOR1_ALTO * 2 + 3 * MARGEN_BOTONES



        self.BOTON_JUGADOR2_X = (self.ANCHO / 2) + (self.ANCHO / 2 - (self.BOTON_JUGADOR1_X + self.BOTON_JUGADOR1_ANCHO))
        self.BOTON_JUGADOR2_Y = self.BOTON_JUGADOR1_Y
        self.BOTON_JUGADOR2_ANCHO = self.BOTON_JUGADOR1_ANCHO
        self.BOTON_JUGADOR2_ALTO = self.BOTON_JUGADOR1_ALTO

        self.BOTON_CPU2_X = self.BOTON_JUGADOR2_X
        self.BOTON_CPU2_Y = self.BOTON_CPU1_Y
        self.BOTON_CPU2_ANCHO = self.BOTON_CPU1_ANCHO
        self.BOTON_CPU2_ALTO = self.BOTON_CPU1_ALTO

        
        self.BOTON_GRUPO2_X = self.BOTON_JUGADOR2_X - MARGEN_BOTONES
        self.BOTON_GRUPO2_Y = self.BOTON_GRUPO1_Y
        self.BOTON_GRUPO2_ANCHO = self.BOTON_GRUPO1_ANCHO
        self.BOTON_GRUPO2_ALTO = self.BOTON_GRUPO1_ALTO





class Menu:
    def __init__(self, medidas: Medidas, pantalla):
        self.DICT_CPU = {"Aleatorio": Agentes.Aleatorio(), "Reglas Simples": Agentes.ReglasSimples(), "Reglas Complejas": Agentes.ReglasComplejas(), "MiniMax": Agentes.MiniMax(),
                     "AlphaBeta": Agentes.AlphaBeta(), "Monte Carlo": Agentes.MonteCarlo()}
        LISTA_CPU = list(self.DICT_CPU.keys())
        self.botonInicio = Botones.Boton(medidas.BOTON_INICIO_X, medidas.BOTON_INICIO_Y, medidas.BOTON_INICIO_ANCHO, medidas.BOTON_INICIO_ALTO, "Iniciar", BLANCO, NARANJA, pantalla)

        self.botonSalir = Botones.Boton(medidas.BOTON_SALIR_X, medidas.BOTON_SALIR_Y, medidas.BOTON_SALIR_ANCHO, medidas.BOTON_SALIR_ALTO, "Salir", BLANCO, ROJO, pantalla)

        self.botonJugador1 = Botones.BotonSeleccionable(medidas.BOTON_JUGADOR1_X, medidas.BOTON_JUGADOR1_Y, medidas.BOTON_JUGADOR1_ANCHO, medidas.BOTON_JUGADOR1_ALTO, "Jugador 1", BLANCO, VERDE, GRIS_CLARO, pantalla, True)
        self.botonCPU1 = Botones.BotonFlechasSeleccionable(medidas.BOTON_CPU1_X, medidas.BOTON_CPU1_Y, medidas.BOTON_CPU1_ANCHO, medidas.BOTON_CPU1_ALTO, LISTA_CPU, BLANCO, VERDE, GRIS_CLARO, pantalla, False)
        self.grupoBotones1 = Botones.GrupoBotones(medidas.BOTON_GRUPO1_X, medidas.BOTON_GRUPO1_Y, medidas.BOTON_GRUPO1_ANCHO, medidas.BOTON_GRUPO1_ALTO, BLANCO, self.botonJugador1, self.botonCPU1, pantalla, 1)
        
        self.botonJugador2 = Botones.BotonSeleccionable(medidas.BOTON_JUGADOR2_X, medidas.BOTON_JUGADOR2_Y, medidas.BOTON_JUGADOR2_ANCHO, medidas.BOTON_JUGADOR2_ALTO, "Jugador 2", BLANCO, VERDE, GRIS_CLARO, pantalla, True)
        self.botonCPU2 = Botones.BotonFlechasSeleccionable(medidas.BOTON_CPU2_X, medidas.BOTON_CPU2_Y, medidas.BOTON_CPU2_ANCHO, medidas.BOTON_CPU2_ALTO, LISTA_CPU, BLANCO, VERDE, GRIS_CLARO, pantalla, False)
        self.grupoBotones2 = Botones.GrupoBotones(medidas.BOTON_GRUPO2_X, medidas.BOTON_GRUPO2_Y, medidas.BOTON_GRUPO2_ANCHO, medidas.BOTON_GRUPO2_ALTO, BLANCO, self.botonJugador2, self.botonCPU2, pantalla, 1)
        
        self.pantalla = pantalla
        self.medidas = medidas

    def pintar(self):
        self.grupoBotones1.pintar()
        self.grupoBotones2.pintar()
        return not self.botonInicio.pintar()
    
    def pintarSalir(self):
        return not self.botonSalir.pintar()
        
        
    
    def obtenerJugadores(self):
        if self.grupoBotones1.boton1.seleccionado:
            jugador1 = Agentes.Persona()
        elif self.grupoBotones1.boton2.seleccionado:
            jugador1 = self.DICT_CPU[self.grupoBotones1.boton2.listaTexto[self.grupoBotones1.boton2.indiceTexto]]

        if self.grupoBotones2.boton1.seleccionado:
            jugador2 = Agentes.Persona()
        elif self.grupoBotones2.boton2.seleccionado:
            jugador2 = self.DICT_CPU[self.grupoBotones2.boton2.listaTexto[self.grupoBotones2.boton2.indiceTexto]]

        return jugador1, jugador2



