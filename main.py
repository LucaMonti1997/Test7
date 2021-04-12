# Explorar el tema de recursos y turnos
# Optimizar animaciones, estudiar un sistema que detecta cambios en posiciones/dimensiones y llama a actualizar la
# pantalla, ahorrando recursos

import pygame
import pygame_widgets
import random
from Constantes import *
from Clases import *
from Funciones import *

# Creamos la ventana donde se muestra tod0
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Test7')


# Mezcla las cartas
def shuffle():
    grupo_cartas.empty()
    # Generamos 8 cartas
    if narrador.player1_turn:
        for i in range(8):
            # Escojemos al azar entre dos tipos de cartas
            if random.choice([True, False]):
                carta_n = Carta([100 + i * (WIDTH - 100) / 8, HEIGHT - 150], [90, 100], NEGRO, 'LADRILLO1', LADRILLO1)
                carta_n.loadObject(texto_reparar)
            else:
                carta_n = Carta([100 + i * (WIDTH - 100) / 8, HEIGHT - 150], [90, 100], NEGRO, 'ESPADA1', ESPADA1)
                carta_n.loadObject(texto_daño)
            # Creamos y añadimos las animaciones a la carta creada
            expandir_carta_n = Animador(carta_n, 0.3, ['dimen', [150, 150]], 'expandir')
            encojer_carta_n = Animador(carta_n, 0.3, ['dimen', [50, 50]], 'encojer')
            carta_n.loadObject(expandir_carta_n, encojer_carta_n)
            grupo_cartas.add(carta_n)
    else:
        for i in range(8):
            carta_n = CartaTapada([100 + i * (WIDTH - 100) / 8, HEIGHT - 150], [90, 100], NEGRO, 'TAPADA1', TAPADA1)
            grupo_cartas.add(carta_n)


# "Pinta" la pantalla
def renderWindow():
    WIN.fill(VERDE_CLARO)

    # Mostramos las cartas
    grupo_cartas.update(WIN)
    grupo_cartas.draw(WIN)
    for carta in grupo_cartas:
        carta.redraw(WIN)

    # Mostramos los recursos
    grupo_recursos1.update(WIN)
    grupo_recursos1.draw(WIN)
    for carta_rec in grupo_recursos1:
        carta_rec.redraw(WIN)

    # Mostramos las bases y torres
    # grupo_base1.update(WIN)
    # grupo_base1.draw(WIN)
    # grupo_base2.update(WIN)
    # grupo_base2.draw(WIN)
    for base in bases:
        base.update(WIN)
        base.redraw(WIN)

    # Testeo. Mostramos los widgets
    for widget in lWidgets:
        widget.draw()

    # Se actualiza la ventana
    pygame.display.update()


# Gestiona la posición del raton respecto a otras entidades
def mouseHandler(pos):
    for carta in grupo_cartas:
        if carta.mouseOver(pos):
            cardHandler(carta.tipo)
            narrador.quiero_cambiar = True


# Gestiona las pulsaciones de teclas
def keyHandler(key):
    pass


# Gestiona la activación de botones y widgets
def botonHandler(tipo):
    if tipo == 1:
        if not bases[0].anim['resta hp'].busy:
            bases[0].anim['resta hp'].target = ['hp', clamp(bases[0].get('hp') - 25, 0, 100)]
            bases[0].anim['resta hp'].start()
    elif tipo == 2:
        if not bases[0].anim['resta hp_muro'].busy:
            bases[0].anim['resta hp_muro'].target = ['hp_muro', clamp(bases[0].get('hp_muro') - 25, 0, 100)]
            bases[0].anim['resta hp_muro'].start()


# Gestiona el uso de cartas
def cardHandler(tipo):
    if tipo == 'ESPADA1':
        if not bases[1].anim['resta hp'].busy:
            bases[1].anim['resta hp'].target = ['hp', clamp(bases[1].get('hp') - 25, 0, 100)]
            bases[1].anim['resta hp'].start()
    elif tipo == 'LADRILLO1':
        if not bases[0].anim['suma hp_muro'].busy:
            bases[0].anim['suma hp_muro'].target = ['hp_muro', clamp(bases[0].get('hp_muro') + 25, 0, 100)]
            bases[0].anim['suma hp_muro'].start()


# Genera los castillos al principio
def generaCastillos():
    for i in range(2):
        torrel = Torre(TORRESENCILLA2, 't_izq', 1, 1, 25, 125)
        torrer = Torre(TORRESENCILLA2, 't_der', 1, 1, 25, 125)
        torrec = Torre(TORRESENCILLA2, 't_cen', 1, 1, 30, 150)
        muralla = Torre(MURALLA2, 'mura', 1, 1, 175, 55)

        hp_texto = TextoColgado(100, TEST_FONT_DESCR, AZUL, 'hp')
        hp_muro_texto = TextoColgado(100, TEST_FONT_DESCR, ROJO, 'hp_muro')

        base = Base((225 + i * (WIDTH - 450), 150), 1, 1)
        bases.append(base)

        anim_base1 = Animador(bases[i], 1.2, ['hp', bases[i].get('hp') - 5], 'resta hp')
        anim_base2 = Animador(bases[i], 1.2, ['hp', bases[i].get('hp') + 5], 'suma hp')
        anim_mura1 = Animador(bases[i], 1.2, ['hp_muro', bases[i].get('hp_muro') - 5], 'resta hp_muro')
        anim_mura2 = Animador(bases[i], 1.2, ['hp_muro', bases[i].get('hp_muro') + 5], 'suma hp_muro')

        base.loadObject(torrel, torrer, torrec, muralla, hp_texto, hp_muro_texto, anim_base1, anim_base2, anim_mura1,
                        anim_mura2)


# Genera los recursos al principio
def generaRecursos():
    grupo_recursos1.empty()
    texto_espadas = TextoColgado('Espadas', TEST_FONT_DESCR, VERDE, 'espadas')
    numero_espadas = TextoColgado(5, TEST_FONT_DESCR, VERDE_CLARO, 'cantidad espadas')
    texto_herreros = TextoColgado('Herreros', TEST_FONT_DESCR, ROJO, 'herreros')
    numero_herreros = TextoColgado(2, TEST_FONT_DESCR, ROJO_CLARO, 'cantidad herreros')
    recurso1 = Recurso('espadas', 5, 3)
    carta_recurso1 = CartaRecurso((100, 100), (150, 150), NEGRO, REC_ESPADA1, recurso1)
    carta_recurso1.loadObject(texto_espadas)
    carta_recurso1.loadObject(numero_espadas)
    carta_recurso1.loadObject(texto_herreros)
    carta_recurso1.loadObject(numero_herreros)
    grupo_recursos1.add(carta_recurso1)


def cambiarTurno():
    narrador.quiero_cambiar = True


# Creamos el narrador
narrador = Narrador()

# Grupo para las dos bases
bases = []
# Grupo de sprites para las cartas
grupo_cartas = pygame.sprite.Group()
# Grupo de sprites para los recursos
grupo_recursos1 = pygame.sprite.Group()
# Texto para las cartas
texto_daño = TextoColgado('Daño', TEST_FONT_DESCR, ROJO, 'descr')
texto_reparar = TextoColgado('Reparar', TEST_FONT_DESCR, AZUL, 'descr')

# Barajamos las cartas una primera vez, y creamos los castillos
shuffle()
generaCastillos()
generaRecursos()

# Widget para testear
boton_damage = pygame_widgets.Button(WIN, 250, 300, 125, 40, text='Dañar castillo', onClick=botonHandler,
                                     onClickParams=[1])
boton_damage_muro = pygame_widgets.Button(WIN, 250, 350, 125, 40, text='Dañar muras', onClick=botonHandler,
                                          onClickParams=[2])
boton_shuffle = pygame_widgets.Button(WIN, 450, 325, 125, 40, text='Cambiar turno', onClick=cambiarTurno)

lWidgets = [boton_damage, boton_damage_muro, boton_shuffle]


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        # Comprobamos que eventos han ocurrido y actuamos respecto a ellos
        if narrador.quiero_cambiar:
            narrador.PasarTurno()
            shuffle()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseHandler(pygame.mouse.get_pos())
        keyHandler(pygame.key.get_pressed())

        # Testeo
        for boton in lWidgets:
            boton.listen(events)

        renderWindow()
    pygame.quit()


if __name__ == '__main__':
    main()
