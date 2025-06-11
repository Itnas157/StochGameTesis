name = "race"
init_vars = ["t=0", "x=0", "y=0"]

repeticiones = 25
alphas = [0.5]  # Tasa de aprendizaje
gammas = [1]  # Factor de descuento
epsilons = [0.9]  # Probabilidad de exploración inicial

smart_sampling_ns = [2**10]
q_learning_episodes = [2046]

trans_str = """
--Victoria/Derrota
qf: x=10 -> 1
qf: y=10 -> -1

--Jugador x
--t=0

t=0 ^ x=0|...|9 -> 1: x=x+1;t=1 !!!mov_seguro
t=0 ^ x=0|...|9 -> 0.5: x=min(x+2, 10);t=1 | 0.5: x=x;t=1 !!!mov_2
t=0 ^ x=0|...|9 -> 0.4: x=min(x+3, 10);t=1 | 0.6: x=max(x-1,0);t=1 !!!mov_3

--Jugador y
--t=1

t=1 ^ y=0|...|9 -> 1: y=y+1;t=0 !!!mov_seguro
t=1 ^ y=0|...|9 -> 0.5: y=min(y+2, 10);t=0 | 0.5: y=y;t=0 !!!mov_2
t=1 ^ y=0|...|9 -> 0.4: y=min(y+3, 10);t=0 | 0.6: y=max(y - 1, 0);t=0 !!!mov_3
"""