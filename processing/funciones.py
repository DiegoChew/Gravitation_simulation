import random
from .objectos import Planeta,Luna
import yaml
from pathlib import Path
import numpy as np

def cargar_config():
    ruta_config = Path(__file__).parent.parent / "config.yaml"
    
    with open(ruta_config, 'r') as archivo:
        return yaml.safe_load(archivo) 
config = cargar_config()
class Generar_cuerpos ():

    def __init__(self,cantidad_planetas,cantidad_lunas):
        self.cantidad_planetas=cantidad_planetas
        self.cantidad_lunas=cantidad_lunas
        self.planetas=self.generar_planetas()
        self.lunas=self.generar_lunas()


#De una constante 'cantidad' se crea una lista con esa cantidad de planetas
    def coor_pos (self):
        min_x=config['objetos']['posicion_x']['min']
        max_x=config['objetos']['posicion_x']['max']
        min_y=config['objetos']['posicion_y']['min']
        max_y=config['objetos']['posicion_y']['max']

        min_v=config['objetos']['velocidad']['min']
        max_v=config['objetos']['velocidad']['max']
        
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        vx = random.uniform(min_v, max_v)
        vy = random.uniform(min_v, max_v)

        return (x,y,vx,vy)
    
    def generar_planetas(self):
        planetas = []
        for _ in range(self.cantidad_planetas):
            mu_m = config['objetos']['masa.P']['mu']
            m = config['objetos']['masa.P']['sigma']
            masa = random.gauss(mu_m, m)

            coord_pos=self.coor_pos()
            x = coord_pos[0]
            y = coord_pos[1]
            vx = coord_pos[2]
            vy = coord_pos[3]

            planeta = Planeta(masa=masa, posicion=[x,y], velocidad=[vx,vy])
            planetas.append(planeta)
        
        return planetas

#Lo mismo pero para lunas
    def generar_lunas(self):
        lunas = []
        for _ in range(self.cantidad_lunas):
            mu_m = config['objetos']['masa.L']['mu']
            m = config['objetos']['masa.L']['sigma']
            masa = random.gauss(mu_m, m)

            coord_pos=self.coor_pos()
            x = coord_pos[0]
            y = coord_pos[1]
            vx = coord_pos[2]
            vy = coord_pos[3]
            
            luna = Luna(masa=masa, posicion=[x,y], velocidad=[vx,vy])
            lunas.append(luna)
        
        return lunas
    
#calcula la fuerza entre dos planetas
def calcular_fuerza(par_planeta):
    planeta_a,planeta_b=par_planeta
    G=6.674e-11
    e=1e-30

    #vector distancia
    dx=planeta_a.posicion_x - planeta_b.posicion_x
    dy=planeta_a.posicion_y - planeta_b.posicion_y

    r = np.sqrt(dx**2+dy**2+e)#e=1e-30 evita division entre 0
    
    A = config['objetos']['escalado_a']
    B = config['objetos']['escalado_b']
    C = config['objetos']['escalado_c']

    distancia = (B*np.arctan(planeta_a.masa)*planeta_b.masa**A+ C)*2
    
    if r <= distancia:
        return "FUSION"
    
    __fuerza = -G*planeta_a.masa*planeta_b.masa/(r**2) #F=-G(m1*m2)/r^2

    fx = __fuerza * dx / r #componente en x de F
    fy = __fuerza * dy / r #componente en y de F

    return fx, fy

#asigna de manera "aleatoria", ya que de por si planetas y lunas lo son.
def asignar(planetas,lunas):

    P=len(planetas)
    L=len(lunas)
    n=0
    i=0
    if P!=0:

        while n < L:
            planetas[i].agregar_luna(lunas[n])
            if i == L-1:
                break
            elif i == P-1:
                i=0
                n=n+1
            else:
                i=i+1
                n=n+1
    else:
        pass            

#une los cuerpos muy cercanos y forma un nuevo cuerpo

def fusionar (*cuerpos):

    if len(cuerpos) == 1:
        cuerpo_a,cuerpo_b = cuerpos[0]
    else:
        cuerpo_a,cuerpo_b = cuerpos[:2]

    masa_total = cuerpo_a.masa + cuerpo_b.masa

    x = (cuerpo_a.posicion_x * cuerpo_a.masa + cuerpo_b.posicion_x * cuerpo_b.masa) / masa_total
    y = (cuerpo_a.posicion_y * cuerpo_a.masa + cuerpo_b.posicion_y * cuerpo_b.masa) / masa_total
    
    # Conservación del momento lineal (velocidad promedio ponderada)
    vx = (cuerpo_a.velocidad_x * cuerpo_a.masa + cuerpo_b.velocidad_x * cuerpo_b.masa) / masa_total
    vy = (cuerpo_a.velocidad_y * cuerpo_a.masa + cuerpo_b.velocidad_y * cuerpo_b.masa) / masa_total
    
    if masa_total <= 1.5*config["objetos"]["masa.P"]["mu"]:
        cuerpo = Luna(masa=masa_total, posicion=[x, y], velocidad=[vx, vy])
    else:
        cuerpo = Planeta(masa=masa_total, posicion=[x, y], velocidad=[vx, vy])

    return cuerpo
