from abc import ABC, abstractmethod
import random 
import pygame
import numpy as np

class CuerpoCeleste(ABC):
    
    @abstractmethod
    def __init__(self,posicion=[0,0],velocidad=[0,0]):
        self.posicion_x=posicion[0]
        self.posicion_y=posicion[1]
        self.velocidad_x=velocidad[0]
        self.velocidad_y=velocidad[1]
    
class Figura(ABC):
    def __init__(self, masa):
        self.masa = masa
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        self.tipo_figura = random.choice(["circulo", "rectangulo", "triangulo"])
        # self.radio_base = 5
        self.radio = np.log(self.masa)+self.masa*0.00001


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


class Planeta (CuerpoCeleste,Figura):
    def __init__ (self,masa,posicion,velocidad):
        CuerpoCeleste.__init__(self,posicion,velocidad)
        Figura.__init__(self,masa)

    def aplicar_fuerza(self, fuerza_x, fuerza_y, delta_time):
        # F = m*a → a = F/m
        aceleracion_x = fuerza_x / self.masa
        aceleracion_y = fuerza_y / self.masa
        
        # Actualizar velocidad (v = v0 + a*t)
        self.velocidad_x += aceleracion_x * delta_time
        self.velocidad_y += aceleracion_y * delta_time
        
        # Actualizar posición (x = x0 + v*t)
        self.posicion_x += self.velocidad_x * delta_time
        self.posicion_y += self.velocidad_y * delta_time


