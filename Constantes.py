# Aquí se guardan todo la información que sera constante, como definiciones de colores, fonts,
# rutas a archivos y otros valores
import pygame

# COLORES
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
ROJO_CLARO = (255, 80, 80)
VERDE = (0, 255, 0)
VERDE_CLARO = (120, 255, 0)
AZUL = (0, 0, 255)
AZUL_CLARO = (0, 255, 255)
COLORES = (BLANCO, NEGRO, ROJO, VERDE, VERDE_CLARO, AZUL, AZUL_CLARO)

# CARACTERISTICAS PANTALLA
WIDTH, HEIGHT = 1200, 700

# RUTAS ASSETS
ESPADA1 = 'Assets/TestAssets/Espada1.png'
REC_ESPADA1 = 'Assets/TestAssets/RecursoEspada1.png'
LADRILLO1 = 'Assets/TestAssets/Ladrillo1.png'
TAPADA1 = 'Assets/TestAssets/Tapada1.png'
TORRE1 = 'Assets/TestAssets/Torre1.png'
TORRE2 = 'Assets/TestAssets/Torre2.png'
TORRESENCILLA1 = 'Assets/TestAssets/Castillo1/TorreSencilla1.png'
TORRESENCILLA2 = 'Assets/TestAssets/Castillo1/TorreSencilla2.png'
MURALLA1 = 'Assets/TestAssets/Castillo1/Muralla1.png'
MURALLA2 = 'Assets/TestAssets/Castillo1/Muralla2.png'

# FONTS
pygame.font.init()

TEST_FONT = pygame.font.SysFont('Comicsans', 40)
TEST_FONT_DESCR = pygame.font.SysFont('Comicsans', 20)

CALIBRI = pygame.font.SysFont('Calibri', 40)
TIMESNR = pygame.font.SysFont('Times new roman', 40)
ARIAL = pygame.font.SysFont('Arial', 40)

# LISTA PARAMETROS ANIMABLES
# Los NUM son parametros de un numero
# Los TUP son tuples, listas, conjuntos varios...
ANIMABLES_NUM = ['hp', 'hp_muro']
ANIMABLES_TUP = ['coord', 'dimen', 'color']
