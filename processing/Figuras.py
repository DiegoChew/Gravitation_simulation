import pygame
import random
import numpy as np
import yaml
from pathlib import Path

def cargar_config():
    ruta_config = Path(__file__).parent.parent / "config.yaml"
    
    with open(ruta_config, 'r') as archivo:
        return yaml.safe_load(archivo) 
config = cargar_config()

#Asigna una forma y color aleatorio
class Figura():
    def __init__(self, masa):
        self.masa = masa
        #color aleatorio
        self.__color = ( 
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        #figura aleatoria
        self.__tipo_figura = random.choice(["circulo", "rectangulo", "triangulo"])

        A = config['objetos']['escalado_a']
        B = config['objetos']['escalado_b']
        C = config['objetos']['escalado_c']

        self.__r = B*np.arctan(self.masa)*self.masa**A + C#tamaño en relación a la masa
        # self.radio = self.masa*config['objetos']['escalado']

    def dibujar_figura(self, pantalla,x,y):
        if self.__tipo_figura == "circulo":
            pygame.draw.circle(
                pantalla,
                self.__color,
                (int(x), int(y)),
                int(self.__r)
            )
        elif self.__tipo_figura == "rectangulo":
            rect = pygame.Rect(
                x - self.__r,
                y - self.__r,
                self.__r * 2,
                self.__r * 2
            )
            pygame.draw.rect(pantalla, self.__color, rect)
        elif self.__tipo_figura == "triangulo":
            puntos = [
                (x- self.__r, y - self.__r),
                (x + self.__r, y - self.__r),
                (x, y + self.__r)
            ]
            pygame.draw.polygon(pantalla, self.__color, puntos)
