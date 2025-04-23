import pygame
import sys
from processing.funciones import calcular_fuerza, asignar,fusionar, Generar_cuerpos
# from processing.objectos import Planeta
import yaml
import multiprocessing as mp

# Necesario para usar valores en el .yaml
def cargar_config(ruta="config.yaml"):
    with open(ruta, 'r') as archivo:
        return yaml.safe_load(archivo)

config = cargar_config()



if __name__ == '__main__':

    pygame.init()
    pantalla = pygame.display.set_mode(tuple(config["simulacion"]["resolucion"]))
    pygame.display.set_caption("Simulación gravitacional")
    reloj = pygame.time.Clock()

#generación de cuerpos

    Cplanetas = config['simulacion']['cantidad.P']
    Clunas = config['simulacion']['cantidad.L']

    cuerpos_celestes = Generar_cuerpos(cantidad_planetas=Cplanetas,cantidad_lunas=Clunas)
    
    asignar(cuerpos_celestes.planetas,cuerpos_celestes.lunas)

    cuerpos=cuerpos_celestes.planetas+cuerpos_celestes.lunas

#cantidad de nucleos usados
    num_procesos= mp.cpu_count()-2
    pool = mp.Pool(processes=num_procesos)
    
#inicia la simulación 
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        pantalla.fill((0, 0, 20))

#crea una tupla por cada combinación de cuerpos, sin repetición 
        pares = [(cuerpos[i], cuerpos[j]) for i in range(len(cuerpos)) for j in range(i+1, len(cuerpos))]
        
# Calcula la fuerza de los cuerpos con multiprocessing
        fuerza = pool.map(calcular_fuerza, pares)
        # print(fuerza)
# lista para fuerza de cuerpos
        fuerza_cuerpos_x = [0.0]*len(cuerpos)
        fuerza_cuerpos_y = [0.0]*len(cuerpos)
#lista de cuerpos a fusionar
        fusiones_pendientes = []
#filtra los cuerpos a fusionar y lo agrega a funsiones pendientes y suma las fuerzas por componentes
        for a, (cuerpo1, cuerpo2) in enumerate(pares):
            i = cuerpos.index(cuerpo1)
            j = cuerpos.index(cuerpo2)

            if fuerza[a] == "FUSION":
                fusiones_pendientes.append((cuerpos[i], cuerpos[j]))

            else:
                resultado = fuerza[a]
                fx, fy = resultado
                fuerza_cuerpos_x[i] += fx
                fuerza_cuerpos_y[i] += fy
                fuerza_cuerpos_x[j] -= fx
                fuerza_cuerpos_y[j] -= fy

# actualiza las posiciones de los cuerpos y los muestra en pantalla
        for i in range(len(cuerpos)):
            cuerpos[i].aplicar_fuerza(fuerza_cuerpos_x[i],fuerza_cuerpos_y[i])
            cuerpos[i].dibujar(pantalla)

#fusiona los cuerpos y los elimina de la lista cuerpos
        for cuerpo1, cuerpo2 in fusiones_pendientes:
            if cuerpo1 in cuerpos and cuerpo2 in cuerpos:
                cuerpos.remove(cuerpo1)
                cuerpos.remove(cuerpo2)
                fusionado = fusionar(cuerpo1, cuerpo2)
                cuerpos.append(fusionado)

        pygame.display.flip()
        reloj.tick(60)

pygame.quit()
sys.exit()


