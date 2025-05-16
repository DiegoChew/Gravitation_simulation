# Simulación Gravitacional de Multiples Cuerpos

Simula la interacción gravitacional de múltiples objetos creados de forma aleatoria meditante la fuerza de gravitación de Newton, considerando el choque entre cuerpos como una colisión perfectamente inelástica.



> Todas las propiedades en **negrita** se encuentran definidas en el archivo .yaml.

## Como iniciar la simulación

Es necesario tener instalada la apt que permite la creación de entornos virtuales, en caso de no tenerla instalada ejecute en su terminal:

`apt install python3.10-venv`

Para la primera ejecución de la simulación ejecute:

`make build`

Para iniciar simulaciones posteriores ejecute:

`make run`

Para ejecutar tests:

`make test`

Para ejecutar chequeos estáticos:

`make typecheck`


## Estructura del Proyecto


 - main.py  - (Archivo principal)
 - processing/
    - Figuras.py - (Creación de características visuales)
    - funciones.py - (Funciónes auxiliares)
    - objetos.py - (Creación de los objetos)
- tests/
    - tests_funciones_objetos.py
- config.yaml - (Características de objetos y simulación)
- README.md
- requirements.txt - (Paquetes necesarios)



## Creación de cuerpos

Los cuerpos tomados en la simulación son planetas y lunas.

### Planetas 

Características principales:

- **Masa aleatoria** dada por una Distribución Gaussiana.
- **Velocidad y posición inicial** dadas de forma aleatoria. 
- Forma circular, curadrada o triangular de forma aleatoria.
- Color aleatorio.

### Lunas

Características principales:

- **Masa aleatoria** dada por una Distribución Gaussiana.
- **Velocidad y posición inicial** definidas tal que una luna asignada a un planeta tenga una orbita estable (Ver apartado de Física). 
- Forma circular, curadrada o triangular de forma aleatoria.
- Color aleatorio.

### Visualización

Tanto los planetas como lunas comparten que su dimensiones son proporcionales a su masa dada por la siguiente relación:

$$d=B\cdot\arctan(m)\cdot m^{A}+C$$

Donde A, B, C, **constantes de propocionalidad** y $m$ masa del cuerpo.

$A \propto $ Tasa de crecimiento

$B \propto $ Escala 

$C \propto $ Tamaño minímo

## Fisica de la Simulación

### Simulación 

El metodo usado: simulación por tiempo discreto.

Para dicho método se usa la recursión:

$$v_{n+1}=v_{n}+a\cdot\Delta t\qquad  \qquad x_{n+1}=x_{n}+v_{n+1}\cdot \Delta t$$ 

$\Delta t $ **intervalo de itempo** y $\textbf{a}=\frac{\textbf{F}}{m}$.

### Fuerza Gravitacional

La única fuerza de interacción entre los cuerpos, definida como:

$$\textbf{F}=-G\frac{m_1\cdot m_2}{r^2} \hat{r}$$

$G=6.674e-11$ constante de gravitación.

### Velocidad Orbital

Es la velocidad míníma para que un objeto tenga una órbita estable.

La velocidad orbital es una velocidad normal al vector distancia, $\hat{r}\perp \hat{a}$.

$$\textbf{v}_{orb}=\sqrt{\frac{GM}{r}} \hat{a}$$

Dicha velocidad se le asigna a cada luna dependiendo el planeta al que esté asignada y la distiancia a la que se encuentre del mismo (elegida aleatoreamente).




