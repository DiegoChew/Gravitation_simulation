import random
from .objects import Planeta,Luna
import yaml
from pathlib import Path
import numpy as np

def cargar_config():
    ruta_config = Path(__file__).parent.parent / "config.yaml"
    
    with open(ruta_config, 'r') as archivo:
        return yaml.safe_load(archivo) 
config = cargar_config()


#calcula la fuerza entre dos planetas
def calcular_fuerza(planeta_a, planeta_b):
    G=6.6746e-11
    e=1e-30

    #vector distancia
    dx=planeta_a.posicion_x - planeta_b.posicion_x
    dy=planeta_a.posicion_y - planeta_b.posicion_y

    r = np.sqrt(dx**2+dy**2+e)#e=1e-30 evita division entre 0

    fuerza = -G*planeta_a.masa*planeta_b.masa/(r**2) #F=-G(m1*m2)/r^2

    fx = fuerza * dx / r #componente en x de F
    fy = fuerza * dy / r #componente en y de F

    return fx, fy

#De una constante 'cantidad' se crea una lista con esa cantidad de planetas
def generar_planetas(cantidad):
    planetas = []
    for _ in range(cantidad):
        masa = random.gauss(config['objetos']['masa.P']['mu'], config['objetos']['masa.P']['sigma'])
        x = random.uniform(config['objetos']['posicion_x']['min'], config['objetos']['posicion_x']['max'])
        y = random.uniform(config['objetos']['posicion_y']['min'], config['objetos']['posicion_y']['max'])
        vx = random.uniform(config['objetos']['velocidad']['min'], config['objetos']['velocidad']['max'])
        vy = random.uniform(config['objetos']['velocidad']['min'], config['objetos']['velocidad']['max'])
        
        planeta = Planeta(masa=masa, posicion=[x, y], velocidad=[vx, vy])
        planetas.append(planeta)
    
    return planetas

#Lo mismo pero para lunas
def generar_lunas(cantidad):
    lunas = []
    for _ in range(cantidad):
        masa = random.gauss(config['objetos']['masa.L']['mu'], config['objetos']['masa.L']['sigma'])
        
        luna = Luna(masa)
        lunas.append(luna)
    
    return lunas

#asigna de manera "aleatoria", ya que de por si planetas y lunas lo sn, lunas a planetas.
def asignar(planetas,lunas):

    P=len(planetas)
    L=len(lunas)
    
    if P>=L:
        for j in range(L):
            planetas[j].agregar_luna(lunas[j])
    else:
        n=0
        while n < L:
             for i in range(P):
                planetas[i].agregar_luna(lunas[n])
                n=n+1

    # lista_n = [i for i in range(n)]

    # lista_m = [i for i in range(m)]
