name = "basic"
init_vars = ["t=0", "s=0", "r=0"]

alphas = [0.05, 0.1, 0.15, 0.2, 0.25]  # Tasa de aprendizaje
final_alphas_porc = [0.5, 0.1, 0.05, 0.01]
gammas = [0.7, 0.8, 0.9, 0.95]  # Factor de descuento
epsilons = [0.4, 0.5, 0.7, 0.9]  # Probabilidad de exploración inicial
epsilon_decays = [0.0001, 0.0005, 0.001]  # Tasa de decrecimiento de epsilon

smart_sampling_ns = [2**8, 2**9, 2**10, 2**12]
q_learning_episodes = [100, 500, 1000, 5000, 10**4]

trans_str = """
--

--Victoria/Derrota
qf: r=1 -> 1
qf: r=2 -> -1

--Jugador 1
--t=0

t=0 -> 0.3: r=2 | 0.7: t=1;s=0 !!!alpha
t=0 -> 0.5: r=2 | 0.5: t=1;s=1 !!!beta

--Jugador 2
--t=1

t=1 ^ s=0 -> 0.2: r=2 | 0.8: r=1 !!!alpha
t=1 ^ s=0 -> 0.5: r=2 | 0.5: r=1 !!!beta

t=1 ^ s=1 -> 0.7: r=2 | 0.3: r=1 !!!alpha
t=1 ^ s=1 -> 0.2: r=2 | 0.8: r=1 !!!beta

"""