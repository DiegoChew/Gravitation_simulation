import pygame
import sys
# from processing.objects import Planeta, Luna
from processing.funciones import calcular_fuerza, generar_planetas, generar_lunas, asignar, fusion, union_fuerza	
import yaml
import multiprocessing as mp

def cargar_config(ruta="config.yaml"):
    with open(ruta, 'r') as archivo:
        return yaml.safe_load(archivo)

config = cargar_config()



if __name__ == '__main__':
    
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
    # cuerpos2=cuerpos.copy()

    

    num_procesos= mp.cpu_count()
    pool = mp.Pool(processes=num_procesos)
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        pantalla.fill((0, 0, 20))
    
        nuevos_cuerpos = cuerpos[:]
        fusiones_pendientes = []
        pares_validos = []

        for i in range(len(cuerpos) - 1):
            for j in range(i + 1, len(cuerpos)):
                resultado = calcular_fuerza(cuerpos[i], cuerpos[j])
                if resultado == "FUSION":
                    fusiones_pendientes.append((cuerpos[i], cuerpos[j]))
                else:

                    pares_validos.append((cuerpos[i], cuerpos[j]))
            
        for cuerpo1, cuerpo2 in fusiones_pendientes:
            if cuerpo1 in nuevos_cuerpos and cuerpo2 in nuevos_cuerpos:
                nuevos_cuerpos.remove(cuerpo1)
                nuevos_cuerpos.remove(cuerpo2)
                fusionado = fusion(cuerpo1, cuerpo2)
                nuevos_cuerpos.append(fusionado)
        cuerpos = nuevos_cuerpos

        pares_validos = [(c1, c2) for c1, c2 in pares_validos if c1 in cuerpos and c2 in cuerpos]

        fuerza = pool.map(union_fuerza, pares_validos)
#lista para fuerza de cuerpos
        fuerza_cuerpos_x = [0.0]*len(cuerpos)
        fuerza_cuerpos_y = [0.0]*len(cuerpos)
        
        for a, (cuerpo1, cuerpo2) in enumerate(pares_validos):
            resultado = fuerza[a]
            fx, fy = resultado
            i = cuerpos.index(cuerpo1)
            j = cuerpos.index(cuerpo2)
            fuerza_cuerpos_x[i] += fx
            fuerza_cuerpos_y[i] += fy
            fuerza_cuerpos_x[j] -= fx
            fuerza_cuerpos_y[j] -= fy

        for i in range(len(cuerpos)):
            cuerpos[i].aplicar_fuerza(fuerza_cuerpos_x[i],fuerza_cuerpos_y[i],config['simulacion']['dt'])
            cuerpos[i].dibujar(pantalla)

    
        pygame.display.flip()
        reloj.tick(460)

pygame.quit()
sys.exit()







  

   


#     fusion_ocurrida = False
#     # sumatoria de cada cuerpo respecto de los demás
#     for i in range(len(cuerpos)-1):
#         for j in range(i+1,len(cuerpos)):
#             a=calcular_fuerza(cuerpos[i],cuerpos[j])
#             if a == "FUSION":
#                 cuerpos.append(fusion(cuerpos[i],cuerpos[j]))
#                 del cuerpos[j]
#                 del cuerpos[i]
#                 fusion_ocurrida = True
#                 break
#             else:
#                 fx,fy=a
#                 fuerza_cuerpos_x[i]+=fx
#                 fuerza_cuerpos_y[i]+=fy

#                 fuerza_cuerpos_x[j]-=fx
#                 fuerza_cuerpos_y[j]-=fy
#         if fusion_ocurrida:
#             break  # Sale del for i




#     #aplicar las fuerzas resultantes
#     for i in range(len(cuerpos)):
#         cuerpos[i].aplicar_fuerza(fuerza_cuerpos_x[i],fuerza_cuerpos_y[i],config['simulacion']['dt'])
       
#     #mostrar en pantalla
#     for i in range(len(cuerpos)):
#         cuerpos[i].dibujar(pantalla)
    
#     pygame.display.flip()
#     reloj.tick(60)

# pygame.quit()
# sys.exit()