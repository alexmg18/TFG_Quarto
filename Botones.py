import pygame
class Boton():
    def __init__(self, x, y, ancho, alto, texto, colorTexto, colorBoton, pantalla):
        self.pantalla = pantalla
        self.colorTexto = colorTexto
        self.colorBoton = colorBoton

        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        
        self.rectanguloBoton = pygame.Rect(x, y, ancho, alto)
        self.fuente = pygame.font.Font(None, 50)
        self.texto = self.fuente.render(texto, True, colorTexto)
        self.rectanguloTexto = self.texto.get_rect()
        self.rectanguloTexto.centerx = self.rectanguloBoton.centerx
        self.rectanguloTexto.centery = self.rectanguloBoton.centery

        self.clicked = False
        

    def pintar(self):
        pygame.draw.rect(self.pantalla, self.colorBoton, self.rectanguloBoton)
        self.pantalla.blit(self.texto, self.rectanguloTexto)

        return self.comprobarClick()

    def comprobarClick(self):
        if self.rectanguloBoton.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                return True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return False
        


        



class BotonSeleccionable(Boton):
    def __init__(self, x, y, ancho, alto, texto, colorTexto, colorBotonSeleccionado, colorBotonNoSeleccionado, pantalla, seleccionado=False):
        super().__init__(x, y, ancho, alto, texto, colorTexto, colorBotonSeleccionado, pantalla)
        
        self.colorBotonNoSeleccionado = colorBotonNoSeleccionado
        self.seleccionado = seleccionado
        
        
    def pintar(self):
        if self.seleccionado:
            pygame.draw.rect(self.pantalla, self.colorBoton, self.rectanguloBoton)
        else:
            pygame.draw.rect(self.pantalla, self.colorBotonNoSeleccionado, self.rectanguloBoton)
        self.pantalla.blit(self.texto, self.rectanguloTexto)

        return self.comprobarClick()

    def comprobarClick(self):
        if self.rectanguloBoton.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.seleccionado = True
                return True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return False







class BotonFlechasSeleccionable(BotonSeleccionable):
    def __init__(self, x, y, ancho, alto, listaTexto, colorTexto, colorBotonSeleccionado, colorBotonNoSeleccionado, pantalla, seleccionado=False):
        super().__init__(x, y, ancho, alto, listaTexto[0], colorTexto, colorBotonSeleccionado, colorBotonNoSeleccionado, pantalla, seleccionado)
        
        self.listaTexto = listaTexto
        self.indiceTexto = 0
        
        self.textoDividido = False
        

    def pintar(self):
        
        
        if self.seleccionado:
            pygame.draw.rect(self.pantalla, self.colorBoton, self.rectanguloBoton)
        else:
            pygame.draw.rect(self.pantalla, self.colorBotonNoSeleccionado, self.rectanguloBoton)
        self.flechaIzquierda = pygame.draw.polygon(self.pantalla, self.colorTexto, [(self.x+20, self.y+self.alto//2), (self.x+70, self.y+self.alto//4), (self.x+70, self.y+self.alto*3//4)])
        self.flechaDerecha = pygame.draw.polygon(self.pantalla, self.colorTexto, [(self.x+self.ancho-20, self.y+self.alto//2), (self.x+self.ancho-70, self.y+self.alto//4), (self.x+self.ancho-70, self.y+self.alto*3//4)])
        self.texto = self.fuente.render(self.listaTexto[self.indiceTexto], True, self.colorTexto)
        
        if not self.textoDividido:
            self.pantalla.blit(self.texto, self.rectanguloTexto)
        else:
            self.pantalla.blit(self.texto1, self.rectanguloTexto1)
            self.pantalla.blit(self.texto2, self.rectanguloTexto2)

        
        
        return self.comprobarClick()
    

    def cambiarTexto(self, texto):
        self.texto = self.fuente.render(texto, True, self.colorTexto)
        self.rectanguloTexto = self.texto.get_rect()
        self.rectanguloTexto.centerx = self.rectanguloBoton.centerx
        self.rectanguloTexto.centery = self.rectanguloBoton.centery

        self.textoDividido = False

        distanciaEntreFlechas = self.flechaDerecha.x - (self.flechaIzquierda.x + self.flechaIzquierda.width)
        if self.rectanguloTexto.width >= distanciaEntreFlechas:
            textos = texto.split(maxsplit=1)
            if len(textos) > 1:
                self.textoDividido = True

                self.texto1 = self.fuente.render(textos[0], True, self.colorTexto)
                self.rectanguloTexto1 = self.texto1.get_rect()
                self.rectanguloTexto1.centerx = self.rectanguloBoton.centerx
                self.rectanguloTexto1.y = self.rectanguloBoton.centery - self.rectanguloTexto1.height

                self.texto2 = self.fuente.render(textos[1], True, self.colorTexto)
                self.rectanguloTexto2 = self.texto2.get_rect()
                self.rectanguloTexto2.centerx = self.rectanguloBoton.centerx
                self.rectanguloTexto2.y = self.rectanguloBoton.centery

                self.rectanguloTexto.x = min(self.rectanguloTexto1.x, self.rectanguloTexto2.x)
                self.rectanguloTexto.y = self.rectanguloTexto1.y
                self.rectanguloTexto.width = max(self.rectanguloTexto1.width, self.rectanguloTexto2.width)
                self.rectanguloTexto.height = self.rectanguloTexto1.height + self.rectanguloTexto2.height

                
    
    def comprobarClick(self):
        posicion = pygame.mouse.get_pos()
        if self.rectanguloBoton.collidepoint(posicion):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                if self.seleccionado:
                    if self.flechaIzquierda.collidepoint(posicion):
                        self.indiceTexto = (self.indiceTexto-1) % len(self.listaTexto)
                        self.cambiarTexto(self.listaTexto[self.indiceTexto])
                    if self.flechaDerecha.collidepoint(posicion):
                        self.indiceTexto = (self.indiceTexto+1) % len(self.listaTexto)
                        self.cambiarTexto(self.listaTexto[self.indiceTexto])
                else:
                    self.seleccionado = True
                return True
            
        if not pygame.mouse.get_pressed()[0]:
             self.clicked = False

        return False
    


class GrupoBotones:
    def __init__(self, x, y, ancho, alto, colorRectangulo, boton1, boton2, pantalla, botonSeleccionado=1):
        self.pantalla = pantalla
        self.colorRectangulo = colorRectangulo

        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        
        self.rectanguloBotones = pygame.Rect(x, y, ancho, alto)
        self.boton1 = boton1
        self.boton2 = boton2

        if botonSeleccionado == 1:
            self.boton1.seleccionado = True
            self.boton2.seleccionado = False
        else:
            self.boton1.seleccionado = False
            self.boton2.seleccionado = True

        
    def pintar(self):
        pygame.draw.rect(self.pantalla, self.colorRectangulo, self.rectanguloBotones)
        if self.boton1.pintar():
            self.boton2.seleccionado = False

        if self.boton2.pintar():
            self.boton1.seleccionado = False