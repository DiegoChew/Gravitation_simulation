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

def calcular_fuerza(planeta_a, planeta_b):
    G=6.6746e-11
    dx=planeta_a.posicion_x - planeta_b.posicion_x
    dy=planeta_a.posicion_y - planeta_b.posicion_y
    distancia = np.sqrt(dx**2+dy**2)
        
    if distancia == 0:
        return 0, 0

    fuerza = -G*planeta_a.masa*planeta_b.masa/(distancia**2)
    fx = fuerza * dx / distancia
    fy = fuerza * dy / distancia
    return fx, fy

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

def generar_lunas(cantidad):
    lunas = []
    for _ in range(cantidad):
        masa = random.gauss(config['objetos']['masa.L']['mu'], config['objetos']['masa.L']['sigma'])
        
        luna = Luna(masa)
        lunas.append(luna)
    
    return lunas

def asignar(planetas,lunas):

    P=len(planetas)
    L=len(lunas)
    
    if P>=L:
        for j in range(L):
            planetas[j].agregar_luna(lunas[j])
    else:
        for i in range(P):
            planetas[i].agregar_luna(lunas[i])
            if i < (L-P):
                planetas[i].agregar_luna(lunas[-i])

    # lista_n = [i for i in range(n)]

    # lista_m = [i for i in range(m)]
