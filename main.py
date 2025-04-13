import pygame
import sys
from processing.objects import Planeta, Luna
from processing.calculations import calcular_fuerza, generar_planetas, generar_lunas, asignar
import yaml

def cargar_config(ruta="config.yaml"):
    with open(ruta, 'r') as archivo:
        return yaml.safe_load(archivo)

config = cargar_config()

pygame.init()


pantalla = pygame.display.set_mode(tuple(config["simulacion"]["resolucion"]))
pygame.display.set_caption("Simulación gravitacional")
reloj = pygame.time.Clock()

planetas = generar_planetas(config['simulacion']['cantidad.P'])

lunas=generar_lunas(config['simulacion']['cantidad.L'])

asignar(planetas,lunas)

cuerpos=planetas+lunas
# planetas.extend(lunas)


fuerza_cuerpos_x = [0.0]*len(cuerpos)
fuerza_cuerpos_y = [0.0]*len(cuerpos)




corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    pantalla.fill((0, 0, 20))  


    # Aplicar gravedad y actualizar
    for i in range(len(cuerpos)-1):
        for j in range(i+1,len(cuerpos)):
            fx,fy=calcular_fuerza(cuerpos[i],cuerpos[j])

            fuerza_cuerpos_x[i]+=fx
            fuerza_cuerpos_y[i]+=fy

            fuerza_cuerpos_x[j]-=fx
            fuerza_cuerpos_y[j]-=fy
    
    for i in range(len(cuerpos)):
        cuerpos[i].aplicar_fuerza(fuerza_cuerpos_x[i],fuerza_cuerpos_y[i],config['simulacion']['dt'])
       
    
    for i in range(len(cuerpos)):
        cuerpos[i].dibujar(pantalla)

    
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()