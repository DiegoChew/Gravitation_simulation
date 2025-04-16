import pygame
import sys
from processing.funciones import calcular_fuerza, generar_planetas, generar_lunas, asignar, fusion, union_fuerza	
import yaml
import multiprocessing as mp

# Necesario para usar valores en el .yaml
def cargar_config(ruta="config.yaml"):
    with open(ruta, 'r') as archivo:
        return yaml.safe_load(archivo)

config = cargar_config()



if __name__ == '__main__':

#inicia la simulación    
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


    
#nucleos dependiendo el sistma que lo ejecute
    num_procesos= mp.cpu_count()
    pool = mp.Pool(processes=num_procesos)
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        pantalla.fill((0, 0, 20))

# listas necesarias, quedan vacias en cada ciclo - cuerpos 
        nuevos_cuerpos = cuerpos[:] #copia cuerpos
        fusiones_pendientes = []
        pares_validos = []

# Filtra en dos listas cuerpos para fusion y cuerpos para seguir simulando, en tuplas de cuerpos que van a interactuar
# Notar que no se están creando todos los casos, reduce a la mitad el proceso

        for i in range(len(cuerpos) - 1):
            for j in range(i + 1, len(cuerpos)):
                resultado = calcular_fuerza(cuerpos[i], cuerpos[j])
                if resultado == "FUSION":
                    fusiones_pendientes.append((cuerpos[i], cuerpos[j]))
                else:
                    pares_validos.append((cuerpos[i], cuerpos[j]))

# En la lista de cuerpos para fusion, los elimina y crea un nuevo cuerpo y lo agrega a lista nuevos cuerpos
        for cuerpo1, cuerpo2 in fusiones_pendientes:
            if cuerpo1 in nuevos_cuerpos and cuerpo2 in nuevos_cuerpos:
                nuevos_cuerpos.remove(cuerpo1)
                nuevos_cuerpos.remove(cuerpo2)
                fusionado = fusion(cuerpo1, cuerpo2)
                nuevos_cuerpos.append(fusionado)
        cuerpos = nuevos_cuerpos #lista de cuerpos ya fusionados y los pares validos, se usa en la siguiente iteración

# Me identifica en tupla los cuerpos validos para calcular la fuerza entre ellos con pool de multiprocessing
        pares_validos = [(cuerpo1, cuerpo2) for cuerpo1, cuerpo2 in pares_validos if cuerpo1 in cuerpos and cuerpo2 in cuerpos]

# Calcula la fuerza de los cuerpos

        fuerza = pool.map(union_fuerza, pares_validos)

# lista para fuerza de cuerpos
        fuerza_cuerpos_x = [0.0]*len(cuerpos)
        fuerza_cuerpos_y = [0.0]*len(cuerpos)

# suma las fuerzas a cada cuerpo
# aqui se aplica que la fuerza de uno es el negativo del otro por lo que reduce a la mitad los calculos 

        for a, (cuerpo1, cuerpo2) in enumerate(pares_validos):
            resultado = fuerza[a]
            fx, fy = resultado
            i = cuerpos.index(cuerpo1)
            j = cuerpos.index(cuerpo2)
            fuerza_cuerpos_x[i] += fx
            fuerza_cuerpos_y[i] += fy
            fuerza_cuerpos_x[j] -= fx
            fuerza_cuerpos_y[j] -= fy

# actualiza las posiciones de los cuerpos y los muestra en pantalla
        for i in range(len(cuerpos)):
            cuerpos[i].aplicar_fuerza(fuerza_cuerpos_x[i],fuerza_cuerpos_y[i],config['simulacion']['dt'])
            cuerpos[i].dibujar(pantalla)

    
        pygame.display.flip()
        reloj.tick(60)

pygame.quit()
sys.exit()

# Estamos calculando 2 veces la fuerza, pero es necesario para poder usar multiprocessing y a su vez poder filtrar los cuerpos
# a fusionar y cuerpos a calcular fuerza.
