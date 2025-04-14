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
        self.color = ( 
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        #figura aleatoria
        self.tipo_figura = random.choice(["circulo", "rectangulo", "triangulo"])

        self.radio = np.log(self.masa)**config['objetos']['escalado'] #tamaño en relación a la masa
        # self.radio = self.masa*config['objetos']['escalado']

    def dibujar(self, pantalla):
        x = self.posicion_x
        y = self.posicion_y 
        if self.tipo_figura == "circulo":
            pygame.draw.circle(
                pantalla,
                self.color,
                (int(x), int(y)),
                int(self.radio)
            )
        elif self.tipo_figura == "rectangulo":
            rect = pygame.Rect(
                x - self.radio,
                y - self.radio,
                self.radio * 2,
                self.radio * 2
            )
            pygame.draw.rect(pantalla, self.color, rect)
        elif self.tipo_figura == "triangulo":
            puntos = [
                (x- self.radio, y - self.radio),
                (x + self.radio, y - self.radio),
                (x, y + self.radio)
            ]
            pygame.draw.polygon(pantalla, self.color, puntos)
