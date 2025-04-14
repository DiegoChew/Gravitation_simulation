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
    G=6.674e-11
    e=1e-30

    #vector distancia
    dx=planeta_a.posicion_x - planeta_b.posicion_x
    dy=planeta_a.posicion_y - planeta_b.posicion_y

    r = np.sqrt(dx**2+dy**2+e)#e=1e-30 evita division entre 0
    if r <= np.log(planeta_a.masa):
        return "FUSION"
    fuerza = -G*planeta_a.masa*planeta_b.masa/(r**2) #F=-G(m1*m2)/r^2

    fx = fuerza * dx / r #componente en x de F
    fy = fuerza * dy / r #componente en y de F

    return fx, fy

#De una constante 'cantidad' se crea una lista con esa cantidad de planetas
def generar_planetas(cantidad):
    planetas = []
    for _ in range(cantidad):
        masa = random.gauss(config['objetos']['masa.P']['mu'], config['objetos']['masa.P']['sigma'])
        # masa = random.gauss(1e20, config['objetos']['masa.P']['sigma'])
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
   
    if L < P:
        for i in range(L):
            planetas[i].agregar_luna(lunas[i])
    else:
        n=0
        while n < L:
            for i in range(P):
                planetas[i].agregar_luna(lunas[n])
                n=n+1
                if n == L:
                    break

def fusion (cuerpo_a,cuerpo_b):
    masa_total = cuerpo_a.masa + cuerpo_b.masa
    
    x = (cuerpo_a.posicion_x * cuerpo_a.masa + cuerpo_b.posicion_x * cuerpo_b.masa) / masa_total
    y = (cuerpo_a.posicion_y * cuerpo_a.masa + cuerpo_b.posicion_y * cuerpo_b.masa) / masa_total
    
    # Conservación del momento lineal (velocidad promedio ponderada)
    vx = (cuerpo_a.velocidad_x * cuerpo_a.masa + cuerpo_b.velocidad_x * cuerpo_b.masa) / masa_total
    vy = (cuerpo_a.velocidad_y * cuerpo_a.masa + cuerpo_b.velocidad_y * cuerpo_b.masa) / masa_total

    # vx = cuerpo_a.velocidad_x + cuerpo_b.velocidad_x
    # vy = cuerpo_a.velocidad_y + cuerpo_b.velocidad_y

    cuerpo = Planeta(masa=masa_total, posicion=[x, y], velocidad=[vx, vy])

    return cuerpo
    # lista_n = [i for i in range(n)]

    # lista_m = [i for i in range(m)]
