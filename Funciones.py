import pygame


# Restringe un numero entre un minimo y un maximo
def clamp(numero, minimo=0, maximo=100):
    return max(min(numero, maximo), minimo)


# Devuelve las coordenadas de un objeto respecto a otro, segun interese
def colocar(madre, hijo, pos_relativa='centro', x_off=0, y_off=0):
    """
    :param madre: Objeto madre. Nos interesa su coord y dimen.
    :param hijo: Objeto hijo. Nos interesa su dimen
    :param pos_relativa: String. Indicará donde colocamos el objeto hijo dentro del madre.
    Arriba, abajo, centro
    :param x_off: Numero. Porcentaje de offset en x aplicado después de calcular la pos_relativa.
    :param y_off: Numero. Porcentaje de offset en y aplicado después de calcular la pos_relativa.
    :return:
    """
    # Coordenadas y dimensiones objeto madre
    coord = madre.get('coord')
    dimen_m = madre.get('dimen')
    # Dimensiones objeto hijo. Solo objetos TextoColgado de momento. Por expandir.
    dimen_h = hijo.font.size(hijo.valor)
    # dimen_h = pygame.font.Font.size(hijo.font, hijo.valor)

    # Calculo valores de offset
    x_pro = clamp(1 - x_off, 0, 1)
    y_pro = clamp(1 - y_off, 0, 1)
    if pos_relativa == 'centro':
        return [coord_madre - dimen_hijo / 2 for coord_madre, dimen_hijo in
                zip(coord, dimen_h)]
    elif pos_relativa == 'arriba':
        return coord[0] - dimen_h[0] / 2, coord[1] - y_pro * dimen_m[1] / 2 - y_off * dimen_h[1] / 2
    elif pos_relativa == 'abajo':
        return coord[0] - dimen_h[0] / 2, coord[1] + y_pro * (dimen_m[1] / 2 - dimen_h[1]) - y_off * dimen_h[1] / 2
    elif pos_relativa == 'izq':
        return coord[0] - x_pro * (dimen_m[0] / 2) - x_off * dimen_h[0] / 2, coord[1] - dimen_h[1] / 2
    elif pos_relativa == 'der':
        return coord[0] + x_pro * (dimen_m[0] / 2 - dimen_h[0]) - x_off * dimen_h[0] / 2, coord[1] - dimen_h[1] / 2

    # CAJÓN DE FUNCIONES SIN UTILIZAR, PERO UTILES QUIZÁS
# Rutina que busca todo los atributos de tipo Torre
# for a in dir(self):
#     if hasattr(self, a):
#         if type(getattr(self, a)) == Torre:
#             b = getattr(self, a)
#             b.ancho = int(b.ancho_base * self.mult_ancho)
#             b.alto = int(b.alto_base * self.mult_alto)
