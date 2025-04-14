from abc import ABC, abstractmethod
from processing.Figuras import Figura
import numpy as np
import random

#clase padre
class CuerpoCeleste(ABC):
    
    @abstractmethod
    def __init__(self,posicion=[0,0],velocidad=[0,0]):
        self.posicion_x=posicion[0]
        self.posicion_y=posicion[1]
        self.velocidad_x=velocidad[0]
        self.velocidad_y=velocidad[1]

    #Cambia la posicion del cuerpo según la fuerza ejercida en el
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


#clase para lunas
class Luna (CuerpoCeleste, Figura):
    def __init__ (self, masa):
        Figura.__init__(self,masa)
        CuerpoCeleste.__init__(self)
#clase para planetas
class Planeta (CuerpoCeleste,Figura):
    def __init__ (self,masa,posicion,velocidad):
        CuerpoCeleste.__init__(self,posicion,velocidad)
        Figura.__init__(self,masa)
        
    def agregar_luna (self,luna_a):
        G=6.6746e-11
        e=1e-30

        #asigna a "luna" una posición cernana al planeta asignado
        luna_a.posicion_x=self.posicion_x+random.uniform(-50,50)
        luna_a.posicion_y=self.posicion_y+random.uniform(-50,50)

        dx= luna_a.posicion_x-self.posicion_x
        dy= luna_a.posicion_y-self.posicion_y

        r=np.sqrt(dx**2+dy**2+e) #e=1e-30 evita division entre 0
        
        #velocidad orbital circular
        VT = np.sqrt(G * self.masa / r)

        #asigna a "luna" su velocidad inicial → v_orbital+v_inicial_planeta
        luna_a.velocidad_x=-VT*(dy/r)+self.velocidad_x
        luna_a.velocidad_y=VT*(dx/r)+self.velocidad_y

