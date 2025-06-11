name = "basic_loop"
init_vars = ["t=0", "s=0", "r=0"]

repeticiones = 25
alphas = [0.5]  # Tasa de aprendizaje
gammas = [1]  # Factor de descuento
epsilons = [0.9]  # Probabilidad de exploración inicial

smart_sampling_ns = [2**10]
q_learning_episodes = [2046]

trans_str = """
--Victoria/Derrota
qf: r=1 -> 1
qf: r=2 -> -1

--Jugador 1
--t=0

t=0 -> 0.3: r=2 | 0.7: t=1;s=0 !!!alpha
t=0 -> 0.3: r=1 | 0.3: t=1;s=1 | 0.4: t=0 !!!beta

--Jugador 2
--t=1

t=1 ^ s=0 -> 0.2: r=2 | 0.8: r=1 !!!alpha
t=1 ^ s=0 -> 0.5: r=2 | 0.5: r=1 !!!beta

t=1 ^ s=1 -> 0.25: r=2 | 0.75: r=1 !!!alpha
t=1 ^ s=1 -> 0.2: r=2 | 0.8: t=0 !!!beta

"""