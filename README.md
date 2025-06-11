# Magia

Autor: Fabio Santiago Echeverria Perpetua

Universidad: Universidad Nacional de Córdoba

Carrera/Programa: Licenciatura en Ciencias de la Computación

Director/a: Pedro R. D'Argenio

Año: 2025

## Abstract

*Este trabajo aborda la aplicación de técnicas de aprendizaje en entornos modelados como juegos estocásticos de dos jugadores. Se estudia en particular la combinación del algoritmo Q-learning y Smart Sampling, con el objetivo de evaluar la eficacia de ambas técnicas. Para esto utilizamos una semantica particular para definir los juegos estocásticos de dos jugadores y luego se interpreta mediante un simulador que integra los algoritmos propuestos. **Los resultados sobre distintos casos de estudio muestran que el enfoque combinado puede alcanzar mejores desempeños en términos de convergencia y calidad de las políticas obtenidas.***

## Introducción

**El aprendizaje por refuerzo ha demostrado ser una herramienta poderosa para resolver problemas de toma de decisiones secuenciales en entornos inciertos. Sin embargo, en escenarios competitivos donde intervienen múltiples agentes, las dinámicas se vuelven más complejas, especialmente cuando se consideran juegos estocásticos. Esta tesis se centra en el estudio de estos entornos, proponiendo un enfoque basado en la integración de Q-learning con un método de muestreo inteligente (Smart Sampling), con el fin de explorar políticas robustas frente a comportamientos adversarios.**

**En las siguientes secciones se desarrollan los fundamentos teóricos necesarios, la motivación del enfoque, su implementación y análisis experimental.**

## Procesos de decisión de Markov (MDP)

Los procesos de decisión de Markov (MDP, por sus siglas en inglés) constituyen la base formal para el aprendizaje por refuerzo. Un MDP se define como una cuádrupla (S, A, P, R), donde S es el conjunto de estados, A el conjunto de acciones, P la función de transición de probabilidad, y R la función de recompensas. El objetivo de un agente que interactúa con un MDP es encontrar una política que maximice su recompensa esperada acumulada a largo plazo.

En esta sección se presenta la definición formal de MDP, el criterio de optimalidad y las ecuaciones de Bellman, fundamentales para los algoritmos de aprendizaje.

## Q-learning

Q-learning es un algoritmo de aprendizaje por refuerzo off-policy que permite aprender una política óptima sin necesidad de conocer el modelo del entorno. Se basa en la estimación de valores de acción (Q-valores) a partir de la interacción con el entorno, utilizando una regla de actualización recursiva.

Aquí se expone la ecuación principal del algoritmo, su comportamiento bajo distintos esquemas de exploración (como ε-greedy), y se discute su convergencia y limitaciones, especialmente en entornos con múltiples agentes o dinámicas complejas.

## Smart Sampling

Smart Sampling es una estrategia orientada a mejorar la eficiencia del aprendizaje en contextos donde el espacio de acciones o transiciones es muy grande. En lugar de muestrear uniformemente las acciones o sucesores, el algoritmo se concentra en aquellas regiones del espacio que son más informativas o relevantes para el aprendizaje.

En esta sección se describe la lógica detrás de Smart Sampling, su implementación básica, y cómo se puede adaptar para integrarse con Q-learning. También se presentan intuiciones sobre por qué esta técnica puede acelerar la convergencia.

## Juegos estocásticos de dos jugadores + interpretación de un juego (parser)

Los juegos estocásticos generalizan los MDPs para el caso de múltiples agentes, permitiendo modelar interacciones estratégicas entre oponentes. En particular, se estudian juegos de suma cero entre dos jugadores, donde las decisiones de ambos influyen en las transiciones y recompensas.

Esta sección introduce el marco formal de los juegos estocásticos y describe el parser desarrollado para interpretar representaciones textuales o estructuradas de estos juegos. Se incluye el formato de entrada, cómo se traduce a estructuras internas y su rol en los experimentos posteriores.

## Unión de los dos algoritmos (código: q_ss, ss_ss)

Aquí se detallan las implementaciones experimentales que combinan Q-learning con Smart Sampling. Se presentan dos variantes principales:

q_ss: Q-learning con muestreo inteligente aplicado en el paso de selección de acciones.

ss_ss: Smart Sampling aplicado tanto a las decisiones como al modelado de las estrategias oponentes.

Se analiza cómo se integran ambos algoritmos, las decisiones de diseño tomadas en el código, y se muestran fragmentos representativos de implementación.

## Casos de estudio + Resultados
Para evaluar el rendimiento de las variantes propuestas, se diseñaron y ejecutaron distintos escenarios de juego, incluyendo entornos simples (como laberintos o tableros) y situaciones más estratégicas.

Se presentan los resultados en términos de:

Velocidad de convergencia.

Estabilidad de las políticas aprendidas.

Comparación contra versiones estándar de Q-learning.

Visualizaciones de evolución de Q-valores y recompensas.

## Conclusión

No tengo ni puta idea de como interpretar mis resultados

## Referencias

- Un canal en indio
- ChatGPT
- Me lo invente

