import pygame
import random
import numpy as np


class Figura():
    def __init__(self, masa):
        self.masa = masa
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        self.tipo_figura = random.choice(["circulo", "rectangulo", "triangulo"])
        # self.radio_base = 5
        self.radio = np.log(self.masa)*0.5


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
