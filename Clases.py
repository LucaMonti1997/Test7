# Aquí se guardan todas las clases creadas

import pygame
import pygame_widgets
import random
from threading import Thread
import time
from Constantes import *
from Funciones import *


# Objeto animador
class Animador(object):
    stop_thread = False  # Flag que señala al thread de terminar

    def __init__(self, obj_anim, timeout, target, identificador):
        """
        Objeto que se encarga de realizar las animaciones.

        Lo que hace es actualizar un atributo del objeto al que pertenece. Según el temporizador establecido, su
        interpolación se adapta.

        Usa threads separadas para poder ejecutarse paralelamente al resto del codigo

        :param obj_anim: Objeto que se quiere animar, el que se escoja
        :param timeout: Tiempo que dura un loop de animación
        :param target: Lista [Parametro por modificar = Valor objetivo]
        :param identificador: ID que identifica el tipo de animación que es
        """
        self.obj_anim = obj_anim
        self.timeout = timeout
        self.target = target
        self.id = identificador  # ID podría ser palabra reservada. Posible BUG OJO!
        self.thread = Thread()  # Objeto Thread donde se ejecutará el loop de animación
        self.busy = False  # Será True mientras se ejecute el Thread

    # Asigna a thread la funcion loop y luego arranca el thread
    def start(self):
        if not self.busy:
            self.thread = Thread(target=self.loop)
            self.thread.start()

    # Bucle de animación
    def loop(self):
        # Evitamos multiples instancia del mismo thread
        if not self.busy:
            self.busy = True

            # Este clock limitará el numero de ejecuciones por segundo del calculo de la animación
            clock = pygame.time.Clock()

            # Comprobamos si estamos trabajando con un numero (valor individual), o un lista/tuple (secuencia)
            num_inicial = 'nada'
            tup_inicial = []

            if self.target[0] in ANIMABLES_NUM:
                num_inicial = self.obj_anim.get(self.target[0])
            elif self.target[0] in ANIMABLES_TUP:
                tup_inicial = self.obj_anim.get(self.target[0])

            # Nos guardamos el tiempo de inicio del bucle, para poder cumplir el timeout
            start_time = time.time()

            # Bucle de animacón en sí
            while time.time() - start_time < self.timeout:
                # Nº de calculos por segundo
                clock.tick(60)

                # Comprobamos si el flag nos indica que hay que parar
                if self.stop_thread:
                    self.stop_thread = False
                    self.busy = False
                    return

                # Decide la proporcionalidad del incremento/decremento
                step = round((time.time() - start_time) / self.timeout, 3)

                # Animación de un valor numerico
                if not num_inicial == 'nada':
                    new_value = num_inicial + step * (self.target[1] - num_inicial)
                    self.obj_anim.set(self.target[0], new_value)
                # Animación de un valor secuencial
                elif tup_inicial:
                    new_value = []
                    for i in range(len(tup_inicial)):
                        new_value.append(tup_inicial[i] + step * (self.target[1][i] - tup_inicial[i]))
                    self.obj_anim.set(self.target[0], new_value)
                if hasattr(self.obj_anim, 'dirty'):
                    self.obj_anim.dirty[self.target[0]] = True

            # Nos aseguramos que al acabar el valor es exactamente el que queriamos
            self.obj_anim.set(self.target[0], self.target[1])
            if hasattr(self.obj_anim, 'dirty'):
                self.obj_anim.dirty[self.target[0]] = True

        self.busy = False


# Base de cada jugador. Donde está el castillo, la vida, etc.
# Maneja las torres, la muralla, textos y numeros
class Base(object):

    def __init__(self, coord, mult_ancho, mult_alto, hp=100, hp_muro=100):
        """
        Base de cada jugador. Donde está el castillo, la vida, etc.

        Maneja las torres, la muralla, textos y numeros

        :param coord: Lista. [x, y]
        :param mult_ancho: Multiplicador de anchura
        :param mult_alto: Multiplicador de altura
        :param hp: Numero .Marca la vida del castillo
        :param texto_hp: Objeto TextoColgado que representa hp
        :param hp_muro: Numero. Marca la vida de la muralla
        :param texto_hp_muro: Objeto TextoColgado que representa hp_muro
        """
        self.coord = coord
        self.mult_ancho = mult_ancho
        self.mult_alto = mult_alto

        self.hp = hp
        self.hp_muro = hp_muro

        self.torre = {}  # Diccionario con obetos Torre
        self.textos = {}  # Diccionario con objetos TextoColgado
        self.anim = {}  # Diccionario con objetos Animador

        self.dirty = {}  # Diciionario con una lista de referencia para saber si hay que actualizar algo

        for attr in ANIMABLES_NUM:
            self.dirty[attr] = True
        for attr in ANIMABLES_TUP:
            self.dirty[attr] = True

    def get(self, attr):
        if attr == 'hp':
            return self.hp
        elif attr == 'hp_muro':
            return self.hp_muro
        elif attr == 'coord':
            return self.coord

    def set(self, attr, value):
        if attr == 'hp':
            self.hp = value
        elif attr == 'hp_muro':
            self.hp_muro = value
        elif attr == 'coord':
            self.coord = value

    # Cuelga objetos sobre este objeto, para poder ser usado a traves de este objeto
    # Por ejemplo colgar distintos tipos de animaciones, torres, textos...
    def loadObject(self, *objetos):
        for objeto in objetos:
            if type(objeto) == Animador:
                self.anim[objeto.id] = objeto
            elif type(objeto) == TextoColgado:
                self.textos[objeto.id] = objeto
            elif type(objeto) == Torre:
                self.torre[objeto.id] = objeto

    # Actualiza las torres, si hace falta
    def update(self, win):
        if self.dirty['hp']:
            self.update_off('hp')
            self.add_off('hp')
            self.dirty['hp'] = False
        if self.dirty['hp_muro']:
            self.update_off('hp_muro')
            self.add_off('hp_muro')
            self.dirty['hp_muro'] = False
        if self.dirty['coord']:
            self.update_mult()
            self.add_off('coord')
            self.dirty['coord'] = False

        for llave in self.torre.keys():
            self.torre[llave].update(win)
        # Ponemos el suelo debajo, para esconder lo que se hunde.
        # Temporal, el suelo irá por separado (o no...)
        pygame.draw.rect(win, VERDE_CLARO,
                         (self.coord[0] - self.torre['mura'].ancho / 2 + self.torre['t_cen'].ancho / 2,
                          self.coord[1] + self.torre['t_cen'].alto - 1, self.torre['mura'].ancho,
                          self.torre['t_cen'].alto), 0)

    # Predispone las torres y muras del castillo
    def update_mult(self):
        for a in [self.torre['t_cen'], self.torre['t_der'], self.torre['t_izq'], self.torre['mura']]:
            a.ancho = int(a.ancho_base * self.mult_ancho)
            a.alto = int(a.alto_base * self.mult_alto)
            a.x = self.coord[0]
            a.y = self.coord[1]

    # ReCalcula el offset de las torres o muras
    def update_off(self, tipo):
        if tipo == 'hp':
            if self.hp >= 70:
                self.torre['t_izq'].y_off = 0
                self.torre['t_cen'].y_off = 0
                self.torre['t_der'].y_off = (self.torre['t_der'].alto * (100 - self.get('hp')) / 30)
            elif self.hp >= 40:
                self.torre['t_izq'].y_off = (self.torre['t_izq'].alto * (70 - self.get('hp')) / 30)
                self.torre['t_cen'].y_off = 0
                self.torre['t_der'].y_off = self.torre['t_der'].alto
            elif self.hp > 0:
                self.torre['t_izq'].y_off = self.torre['t_izq'].alto
                self.torre['t_cen'].y_off = (self.torre['t_cen'].alto * (40 - self.get('hp')) / 40)
                self.torre['t_der'].y_off = self.torre['t_der'].alto
            else:
                self.torre['t_izq'].y_off = self.torre['t_izq'].alto
                self.torre['t_cen'].y_off = self.torre['t_cen'].alto
                self.torre['t_der'].y_off = self.torre['t_der'].alto
        elif tipo == 'hp_muro':
            self.torre['mura'].y_off = (self.torre['mura'].alto * (100 - self.get('hp_muro')) / 100)

    # Obtiene la nueva posición teniendo en cuenta coordenadas y offset
    def add_off(self, tipo):
        if tipo == 'hp' or tipo == 'coord':
            self.torre['t_izq'].y = self.coord[1] + self.torre['t_cen'].alto - self.torre['t_izq'].alto + self.torre[
                't_izq'].y_off
            self.torre['t_izq'].x = self.coord[
                                        0] - self.torre['mura'].ancho / 2 + self.torre['t_cen'].ancho / 2 + self.torre[
                                        't_izq'].ancho
            self.torre['t_der'].y = self.coord[1] + self.torre['t_cen'].alto - self.torre['t_der'].alto + self.torre[
                't_der'].y_off
            self.torre['t_cen'].y = self.coord[1] + self.torre['t_cen'].y_off
            self.torre['t_der'].x = self.coord[
                                        0] + self.torre['mura'].ancho / 2 - self.torre['t_cen'].ancho / 2 - self.torre[
                                        't_der'].ancho * 2 / 3
        if tipo == 'hp_muro' or tipo == 'coord':
            self.torre['mura'].y = self.coord[1] + self.torre['t_cen'].alto - self.torre['mura'].alto + self.torre[
                'mura'].y_off
            self.torre['mura'].x = self.coord[0] - self.torre['mura'].ancho / 2 + self.torre['t_cen'].ancho / 2

    # Reescribe el texto
    def redraw(self, win):
        self.textos['hp'].valor = self.hp
        self.textos['hp_muro'].valor = self.hp_muro
        self.textos['hp'].renderSelf()
        self.textos['hp_muro'].renderSelf()
        win.blit(self.textos['hp'].texto, (self.coord[0], self.coord[1]))
        win.blit(self.textos['hp_muro'].texto, (self.coord[0] + 50, self.coord[1]))

    # Saber si el ratón se encuentra por encima
    def mouseOver(self, pos):
        pass  # LLamar mouseOver de otros objetos


# Las imagenes de las torres/muras
class Torre(pygame.sprite.Sprite):

    def __init__(self, enlace, identificador, x=1, y=1, ancho=1, alto=1):
        """
        Las imagenes de las torres/muras.

        Falta cambiar el sistema de coordenadas y dimensiones como listas en lugar de numeros separados. Ya lo he
        intentado, pero se bugueaba por algún motivo.

        :param enlace: String. Ruta a la imagen de la imagen
        :param identificador: ID que identifica el tipo de torre que es
        :param coord: Lista. Coordenadas [x,y]. Por acabar de hacer
        :param dimen_base: Lista. Dimensiones base [ancho, alto]. Por acabar de hacer
        """
        super().__init__()
        self.x = x
        self.x_off = 0
        self.y = y
        self.y_off = 0
        self.ancho = ancho
        self.ancho_base = ancho
        self.alto = alto
        self.alto_base = alto
        self.enlace = enlace
        self.id = identificador
        self.icono = pygame.image.load(enlace).convert()
        self.image = pygame.Surface([1, 1])
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    # Actualiza posición, escala, etc. Y vuelve a "pintar" el icono
    def update(self, win):
        self.rect.midbottom = [self.x, self.y]
        self.icono = pygame.image.load(self.enlace)
        self.icono = pygame.transform.scale(self.icono, (self.ancho, self.alto))

        # Escalar el "cuadrado" del sprite. Para DEBUG
        # self.image = pygame.transform.scale(self.image, (int(self.ancho / 1), int(self.alto / 1)))

        win.blit(self.icono, self.rect)


# Plantilla para carta, rectangulos y cosas por el estilo
# Tendrán un icono, texto y posibles animaciones asociadas
class PlantillaCarta(pygame.sprite.Sprite):
    _overed = False  # Indica si está siendo sobrevolada por el raton

    def __init__(self, coord, dimen, color, link_icono):
        """
        Plantilla para carta, rectangulos y cosas por el estilo

        Tendrán un icono, texto y posibles animaciones asociadas

        :param coord: Lista. Coordenadas [x,y]
        :param dimen: Lista. Dimensiones [ancho,alto]
        :param color: Color de fondo
        :param link_icono: String. Ruta a la imagen del icono
        """
        super().__init__()
        self._coord = coord
        self._dimen = dimen
        self._color = color
        self._icono = pygame.image.load(link_icono).convert()
        self._link_icono = link_icono
        self._image = pygame.Surface(dimen)
        self._rect = self._image.get_rect()
        self._rect.center = coord
        self._link_icono = link_icono
        self.anim = {}  # Diccionario con objetos Animador
        self.textos = {}  # Diccionario con objetos TextoColgado

    def get(self, attr):
        if attr == 'coord':
            return self._coord
        elif attr == 'dimen':
            return self._dimen
        elif attr == 'color':
            return self._color

    def set(self, attr, value):
        if attr == 'coord':
            self._coord = value
        elif attr == 'dimen':
            self._dimen = value
        elif attr == 'color':
            self._color = value

    # Detecta si el ratón está por encima del objeto
    def mouseOver(self, pos):
        return self.rect.collidepoint(pos)

    # Actualiza graficamente el objeto
    def update(self, win):
        self.image = pygame.Surface(self._dimen)
        self.image.fill(self._color)
        self.rect = self.image.get_rect()
        self.rect.center = [self._coord[0], self._coord[1]]
        self._icono = pygame.image.load(self._link_icono)
        self._icono = pygame.transform.scale(self._icono, [int(self._dimen[0]), int(self._dimen[1])])

        self._overed = self.rect.collidepoint(pygame.mouse.get_pos())

    # Actualiza graficamente el icono. Lo coloca en el centro del objeto
    def redraw(self, win):
        win.blit(self._icono, (self._coord[0] - self._dimen[0] / 2, self._coord[1] - self._dimen[1] / 2))

    # Cuelga objetos sobre este objeto, para poder ser usado a traves de este objeto
    # Por ejemplo colgar distintos tipos de animaciones
    def loadObject(self, *objetos):
        for objeto in objetos:
            if type(objeto) == Animador:
                self.anim[objeto.id] = objeto
            elif type(objeto) == TextoColgado:
                self.textos[objeto.id] = objeto


# Las cartas en sí
class Carta(PlantillaCarta):
    expanding = True  # Indica si la carta se está expandiendo
    shrinking = True  # Indica si la carta se está encojiendo

    def __init__(self, coord, dimen, color, tipo, link_icono):
        """
        Las cartas en sí. Puedes hacer click en ellas y hacen cosas.

        Autogestiona sus animaciones.

        :param coord: Lista. Coordenadas [x,y]
        :param dimen: Lista. Dimensiones [ancho,alto]
        :param color: Color de fondo
        :param tipo: String. Tipo de carta. Identificador de algun tipo
        :param link_icono: String. Ruta a la imagen del icono
        """
        super().__init__(coord, dimen, color, link_icono)
        self.tipo = tipo

    # Actualiza graficamente el objeto
    def update(self, win):
        super().update(win)
        self.animSelf()

    # Actualiza graficamente los iconos y textos del objeto
    def redraw(self, win):
        super().redraw(win)
        self.textos['descr'].renderSelf()
        win.blit(self.textos['descr'].texto, colocar(self, self.textos['descr'], ['left', 'top']))

    # Gestiona animaciones de forma pasiva y automatica
    def animSelf(self):
        if self._overed:
            if not self.expanding:
                self.expanding = True
                self.shrinking = False
                self.anim['encojer'].stop_thread = True
                self.anim['expandir'].stop_thread = False
                self.anim['expandir'].start()
        else:
            if self.expanding:
                self.expanding = False
                self.shrinking = True
                self.anim['expandir'].stop_thread = True
                self.anim['encojer'].stop_thread = False
                self.anim['encojer'].start()


class CartaTapada(PlantillaCarta):
    def __init__(self, coord, dimen, color, tipo, link_icono):
        """
        Carta tapada. No hace nada

        :param coord: Lista. Coordenadas [x,y]
        :param dimen: Lista. Dimensiones [ancho,alto]
        :param color: Color de fondo
        :param tipo: String. Tipo de carta. Identificador de algun tipo
        :param link_icono: String. Ruta a la imagen del icono
        """
        super().__init__(coord, dimen, color, link_icono)
        self.tipo = tipo


# Los recuadros donde se muestran cada recurso
class CartaRecurso(PlantillaCarta):

    def __init__(self, coord, dimen, color, link_icono, recurso):
        """
        Los recuadros donde se muestran cada recurso.

        :param coord: Lista. Coordenadas [x,y]
        :param dimen: Lista. Dimensiones [ancho,alto]
        :param color: Color de fondo
        :param link_icono: String. Ruta a la imagen del icono
        :param recurso: Recurso. El recurso que esta carta representa
        """
        super().__init__(coord, dimen, color, link_icono)
        self.recurso = recurso

    # Actualiza graficamente los iconos y textos del objeto
    def redraw(self, win):
        super().redraw(win)
        self.textos['espadas'].renderSelf()
        self.textos['cantidad espadas'].renderSelf()
        self.textos['herreros'].renderSelf()
        self.textos['cantidad herreros'].renderSelf()
        win.blit(self.textos['espadas'].texto,
                 colocar(self, self.textos['espadas'], ['left', 'top']))
        win.blit(self.textos['cantidad espadas'].texto,
                 colocar(self, self.textos['cantidad espadas'], ['left', 'top'], [0.3, 0.2]))
        win.blit(self.textos['herreros'].texto,
                 colocar(self, self.textos['herreros'], ['right', 'top']))
        win.blit(self.textos['cantidad herreros'].texto,
                 colocar(self, self.textos['cantidad herreros'], ['right', 'top'], [0.3, 0.2]))


# Cada tipo de recurso
class Recurso(object):
    def __init__(self, tipo, cantidad, generador):
        """
        Cada tipo de recurso. Tendrá metodos que permitan gestionar el gasto y la generación automaticamente.

        :param tipo: String. Tipo de recurso
        :param cantidad. Numero. Cantidad del recurso inicail y a lo largo de la partida
        :param generador. Numero. Cantidad de recurso que se genera por turno
        """
        self._tipo = tipo
        self._cantidad = cantidad
        self._generador = generador

    def get(self, attr):
        """
        :param attr: Tipo de atributo que se quiere acceder. Puede ser 'tipo','cantidad','generador'
        """
        if attr == 'tipo':
            return self._tipo
        elif attr == 'cantidad':
            return self._cantidad
        elif attr == '_generador':
            return self._generador

    def set(self, attr, value):
        """
        :param attr: Tipo de atributo que se quiere acceder. Puede ser 'tipo','cantidad','generador'
        :param value: Valor que se queire asociar
        """
        if attr == 'tipo':
            self._tipo = value
        elif attr == 'cantidad':
            self._cantidad = value
        elif attr == 'generador':
            self._generador = value

    # Calcula el nuevo valor de cantidad
    def reCalcula(self, value):
        self._cantidad = clamp(self._cantidad + value)


# Texto extra de otros objetos. Titulos, descripciones, etc.
# "Colgado" porque su posición será relativa al objeto del que se cuelgue
# Hay que ampliar sus capacidades, de momento solo acepta numeros o solo texto
# Y al acceder a self.valor no se sabe que tipo se saca.
# Quizás conviene crear clases mas especificas
class TextoColgado(object):
    texto = ''

    def __init__(self, valor, font, color, identificaor='nada'):
        """
        Texto extra de otros objetos. Titulos, descripciones, etc.

        "Colgado" porque su posición será relativa al objeto del que se cuelgue.

        Hay que ampliar sus capacidades, de momento solo acepta numeros o solo texto.

        Y al acceder a self.valor no se sabe que tipo se saca.

        Quizás conviene crear clases mas especificas.

        :param valor: Mixto. Lo que se muestra en el texto
        :param font: Font. Font que usa el texto
        :param color: Lista. Color del texto
        :param identificaor: ID que identifica el tipo de texto que es
        """
        self.valor = valor
        self.font = font
        self.color = color
        self.id = identificaor

    def renderSelf(self):
        self.texto = self.font.render(str(self.valor), 1, self.color)


class Narrador(object):
    def __init__(self):
        """
        Se encarga de "dirigir" la partida. Reparte las cartas, gestiona los turnos, generación de recursos, eventos
        aleatorios, etc.
        """
        self.player1_turn = random.choice([True, False])
        self.player2_turn = not self.player1_turn
        self.quiero_cambiar = True  # Indica si el narrador quiere cambiar turno

    def PasarTurno(self):
        self.player1_turn = not self.player1_turn
        self.player2_turn = not self.player1_turn
        self.quiero_cambiar = False
