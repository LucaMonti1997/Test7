import pygame


# Restringe un numero entre un minimo y un maximo
def clamp(numero, minimo=0, maximo=100):
    return max(min(numero, maximo), minimo)


# Devuelve las coordenadas de un objeto respecto a otro, segun interese
def colocar(madre, hijo, pos_relativa='nada', off='nada'):
    """
    :param madre: Objeto madre. Nos interesa su coord y dimen.
    :param hijo: Objeto hijo. Nos interesa su dimen
    :param pos_relativa: Lista. [String x, String y]. Indicará donde colocamos el objeto hijo dentro del madre.
    top, bot, mid, left, right
    :param off: Lista. [numero x, numero y] Porcentaje de offset aplicado después de calcular la pos_relativa.
    """
    if pos_relativa == 'nada':
        pos_relativa = ['mid', 'mid']
    if off == 'nada':
        off = [0, 0]

    # Coordenadas y dimensiones objeto madre
    coord = madre.get('coord')
    dimen_m = madre.get('dimen')
    # Dimensiones objeto hijo. Solo objetos TextoColgado de momento. Por expandir.
    dimen_h = hijo.font.size(str(hijo.valor))
    # dimen_h = pygame.font.Font.size(hijo.font, hijo.valor)

    # Calculo valores de offset
    pro = [0, 0]
    pro[0] = clamp(1 - off[0], 0, 1)
    pro[1] = clamp(1 - off[1], 0, 1)

    resultado = ['', '']

    for i in range(2):
        if pos_relativa[i] == 'left' or pos_relativa[i] == 'top':
            resultado[i] = coord[i] - pro[i] * (dimen_m[i] / 2) - off[i] * dimen_h[i] / 2
        elif pos_relativa[i] == 'mid':
            resultado[i] = coord[i] - dimen_h[i] / 2
        elif pos_relativa[i] == 'right' or pos_relativa[i] == 'bot':
            resultado[i] = coord[i] + pro[i] * (dimen_m[i] / 2 - dimen_h[i]) - off[i] * dimen_h[i] / 2

    return resultado

    # CAJÓN DE FUNCIONES SIN UTILIZAR, PERO UTILES QUIZÁS
# Rutina que busca todo los atributos de tipo Torre
# for a in dir(self):
#     if hasattr(self, a):
#         if type(getattr(self, a)) == Torre:
#             b = getattr(self, a)
#             b.ancho = int(b.ancho_base * self.mult_ancho)
#             b.alto = int(b.alto_base * self.mult_alto)
