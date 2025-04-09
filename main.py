import pygame
import sys
from processing.objects import Planeta
from processing.calculations import calcular_fuerza, generar_planetas
import yaml

def cargar_config(ruta="config.yaml"):
    with open(ruta, 'r') as archivo:
        return yaml.safe_load(archivo)

config = cargar_config()

pygame.init()


pantalla = pygame.display.set_mode(tuple(config["simulacion"]["resolucion"]))
pygame.display.set_caption("Simulación gravitacional")
reloj = pygame.time.Clock()



planetas = generar_planetas(config['simulacion']['cantidad'])

fuerza_planetas_x = [0.0]*len(planetas)
fuerza_planetas_y = [0.0]*len(planetas)


corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    pantalla.fill((0, 0, 20))  

    # Aplicar gravedad y actualizar
    for i in range(len(planetas)-1):
        for j in range(i+1,len(planetas)):
            fx,fy=calcular_fuerza(planetas[i],planetas[j])

            fuerza_planetas_x[i]+=fx
            fuerza_planetas_y[i]+=fy

            fuerza_planetas_x[j]-=fx
            fuerza_planetas_y[j]-=fy
    
    # print([fuerza_planetas_x])
    # print(fuerza_planetas_y)
    
    for i in range(len(planetas)):
        planetas[i].aplicar_fuerza(fuerza_planetas_x[i],fuerza_planetas_y[i],config['simulacion']['dt'])
        
    for i in range(len(planetas)):
        planetas[i].dibujar(pantalla)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()