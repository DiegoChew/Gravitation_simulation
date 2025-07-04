from processing.funciones import calcular_fuerza,Generar_cuerpos, asignar
from processing.objectos import Planeta
import numpy as np
import random 
import yaml
from pathlib import Path

def cargar_config():
    ruta_config = Path(__file__).parent.parent / "config.yaml"
    
    with open(ruta_config, 'r') as archivo:
        return yaml.safe_load(archivo) 
config = cargar_config()

masa=1e20
x_1=(config['objetos']['escalado_b']*np.arctan(masa)*masa**config['objetos']['escalado_a']+ config['objetos']['escalado_c'])*2.5
x_2=(config['objetos']['escalado_b']*np.arctan(masa)*masa**config['objetos']['escalado_a']+ config['objetos']['escalado_c'])*1.5
x=[x_1,x_2]

for i in x:
    planeta1 = Planeta(masa, posicion=[0, 0], velocidad=[0, 0])
    planeta2 = Planeta(masa, posicion=[i, 0], velocidad=[0, 0])
    resultado = calcular_fuerza((planeta1, planeta2))
    if i == x[0] and len(resultado) == 2 :
        print("✅ Test calcular_fuerza: pasó")
    elif i == x[1] and resultado == "FUSION" :
        print("✅ Test fusion: pasó")
    else:
        print("❌ Test calcular_fuerza: falló. Resultado:", resultado)


cantidad=random.randint(0,50)
cuerpos_celestes = Generar_cuerpos(cantidad_planetas=cantidad,cantidad_lunas=cantidad)
planetas = cuerpos_celestes.planetas

if len(planetas) == cantidad:
    print("✅ Test generacion aleatoria de planetas: pasó")
else:
    print("❌ Test generacion aleatoria de planetas: falló, no genera la cantidad de planetas esperado")

lunas = cuerpos_celestes.lunas

if len(lunas) == cantidad:
    print("✅ Test generacion aleatoria de lunas: pasó")
else:
    print("❌ Test generacion aleatoria de lunas: falló, no genera la cantidad de lunas esperado")

n=0

asignar(planetas,lunas)

for i in range(cantidad):
    fuerza = calcular_fuerza((planetas[i],lunas[i]))
    if fuerza == "FUSION":
        pass
    else:
        n=n+1

if n==cantidad:
    print("✅ Test asignación de coordenadas para luna asignada: pasó")
else:
     print("❌ Test asignación de coordenadas para luna asignada: falló, luna asignada se encuentra muy cerca de planeta asignado")

m=0

for i in range(cantidad):
    producto_escalar=planetas[i].velocidad_x*lunas[i].velocidad_x+planetas[i].velocidad_y*lunas[i].velocidad_y
    # print(producto_escalar)
    if producto_escalar <= 20:
        m=m+1
    else:
        pass
# print(m,cantidad)
if m==cantidad:
    print("✅ Test asignacion de velocidad orbital para luna asignada: pasó")
else:
     print("❌ Test asignacion de velocidad orbital para luna asignada: falló, luna asignada no tiene una velocidad para orbitar en planeta asignado")