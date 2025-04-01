name = "race"
init_vars = ["t=0", "x=0", "y=0"]

repeticiones = 25
alphas = [0.1]  # Tasa de aprendizaje
final_alphas_porc = [0.1]
gammas = [0.9]  # Factor de descuento
epsilons = [0.9]  # Probabilidad de exploración inicial
epsilon_decays = [0.001]  # Tasa de decrecimiento de epsilon

smart_sampling_ns = [2**10]
q_learning_episodes = [2500]

trans_str = """
--Juego de carrera entre dos jugadores
--El primero en llegar a la posición 10 gana
--Cada jugador tiene tres opciones:
--1. 100% de probabilidad de avanzar 1 posición
--2. 50% de probabilidad de avanzar 2 posiciones y 50% de quedarse quieto
--3. 50% de probabilidad de avanzar 3 posiciones y 50% de retroceder 1 posición

--Victoria/Derrota
qf: x=10 -> 1
qf: y=10 -> -1

--Jugador x
--t=0

t=0 ^ x=0|...|9 -> 1: x=x+1;t=1 !!!mov_seguro
t=0 ^ x=0|...|9 -> 0.5: x=min(x+2, 10);t=1 | 0.5: x=x;t=1 !!!mov_2
t=0 ^ x=0|...|9 -> 0.5: x=min(x+3, 10);t=1 | 0.5: x=max(x-1,0);t=1 !!!mov_3

--Jugador y
--t=1

t=1 ^ y=0|...|9 -> 1: y=y+1;t=0 !!!mov_seguro
t=1 ^ y=0|...|9 -> 0.5: y=min(y+2, 10);t=0 | 0.5: y=y;t=0 !!!mov_2
t=1 ^ y=0|...|9 -> 0.5: y=min(y+3, 10);t=0 | 0.5: y=max(y - 1, 0);t=0 !!!mov_3
"""