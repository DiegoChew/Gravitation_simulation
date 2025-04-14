import pygame
import sys
# from processing.objects import Planeta, Luna
from processing.funciones import calcular_fuerza, generar_planetas, generar_lunas, asignar, fusion
import yaml

def cargar_config(ruta="config.yaml"):
    with open(ruta, 'r') as archivo:
        return yaml.safe_load(archivo)

config = cargar_config()

pygame.init()


pantalla = pygame.display.set_mode(tuple(config["simulacion"]["resolucion"]))
pygame.display.set_caption("Simulación gravitacional")
reloj = pygame.time.Clock()

#lista de objetos "planeta"
planetas = generar_planetas(config['simulacion']['cantidad.P'])

#lista de objetos "luna"
lunas=generar_lunas(config['simulacion']['cantidad.L'])

#asignar luna a planeta
asignar(planetas,lunas)

#lista con planetas y lunas
cuerpos=lunas+planetas


#lista para fuerza de cuerpos
fuerza_cuerpos_x = [0.0]*len(cuerpos)
fuerza_cuerpos_y = [0.0]*len(cuerpos)




corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    pantalla.fill((0, 0, 20))  

    fusion_ocurrida = False
    # sumatoria de cada cuerpo respecto de los demás
    for i in range(len(cuerpos)-1):
        for j in range(i+1,len(cuerpos)):
            a=calcular_fuerza(cuerpos[i],cuerpos[j])
            if a == "FUSION":
                cuerpos.append(fusion(cuerpos[i],cuerpos[j]))
                del cuerpos[j]
                del cuerpos[i]
                fusion_ocurrida = True
                break
            else:
                fx,fy=a
                fuerza_cuerpos_x[i]+=fx
                fuerza_cuerpos_y[i]+=fy

                fuerza_cuerpos_x[j]-=fx
                fuerza_cuerpos_y[j]-=fy
        if fusion_ocurrida:
            break  # Sale del for i




    #aplicar las fuerzas resultantes
    for i in range(len(cuerpos)):
        cuerpos[i].aplicar_fuerza(fuerza_cuerpos_x[i],fuerza_cuerpos_y[i],config['simulacion']['dt'])
       
    #mostrar en pantalla
    for i in range(len(cuerpos)):
        cuerpos[i].dibujar(pantalla)
    
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()