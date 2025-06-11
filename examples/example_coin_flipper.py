name = "coin_flipper"
init_vars = ["t=0", "j1=0", "j2=0", "caras=0", "coins=4"]

repeticiones = 25
alphas = [0.5]  # Tasa de aprendizaje
gammas = [1]  # Factor de descuento
epsilons = [0.9]  # Probabilidad de exploración inicial

smart_sampling_ns = [2**10]
q_learning_episodes = [2046]

trans_str = """
--Victoria/Derrota
qf: j1=15 -> 1
qf: j2=15 -> -1

--Jugador 1
--t=0

t=0 ^ j1=0|...|14 ^ coins=0|...|4 ^ caras=1|...|15 -> 1: j1=min(j1+caras, 15);t=1;caras=0;coins=4 !!!guardar
t=0 ^ j1=0|...|14 ^ coins=1 ^ caras=0|...|15 -> 0.5: caras=min(caras+1, 15);coins=4 | 0.5: caras=0;coins=4;t=1 !!!tirar
t=0 ^ j1=0|...|14 ^ coins=2 ^ caras=0|...|15 -> 0.25: caras=min(caras+2, 15);coins=4 | 0.5: caras=min(caras+1, 15);coins=1 | 0.25: caras=0;coins=4;t=1 !!!tirar
t=0 ^ j1=0|...|14 ^ coins=3 ^ caras=0|...|15 -> 0.125: caras=min(caras+3, 15);coins=4 | 0.375: caras=min(caras+2, 15);coins=1 | 0.375: caras=min(caras+1, 15);coins=2 | 0.125: caras=0;coins=4;t=1 !!!tirar
t=0 ^ j1=0|...|14 ^ coins=4 ^ caras=0|...|15 -> 0.0625: caras=min(caras+4, 15);coins=4 | 0.25: caras=min(caras+3, 15);coins=1 | 0.375: caras=min(caras+2, 15);coins=2 | 0.25: caras=min(caras+1, 15);coins=3 | 0.0625: caras=0;coins=4;t=1 !!!tirar

--Jugador 2
--t=1

t=1 ^ j2=0|...|14 ^ coins=0|...|4 ^ caras=1|...|15 -> 1: j2=min(j2+caras, 15);t=0;caras=0;coins=4 !!!guardar
t=1 ^ j2=0|...|14 ^ coins=1 ^ caras=0|...|15 -> 0.5: caras=min(caras+1, 15);coins=4 | 0.5: caras=0;coins=4;t=0 !!!tirar
t=1 ^ j2=0|...|14 ^ coins=2 ^ caras=0|...|15 -> 0.25: caras=min(caras+2, 15);coins=4 | 0.5: caras=min(caras+1, 15);coins=1 | 0.25: caras=0;coins=4;t=0 !!!tirar
t=1 ^ j2=0|...|14 ^ coins=3 ^ caras=0|...|15 -> 0.125: caras=min(caras+3, 15);coins=4 | 0.375: caras=min(caras+2, 15);coins=1 | 0.375: caras=min(caras+1, 15);coins=2 | 0.125: caras=0;coins=4;t=0 !!!tirar
t=1 ^ j2=0|...|14 ^ coins=4 ^ caras=0|...|15 -> 0.0625: caras=min(caras+4, 15);coins=4 | 0.25: caras=min(caras+3, 15);coins=1 | 0.375: caras=min(caras+2, 15);coins=2 | 0.25: caras=min(caras+1, 15);coins=3 | 0.0625: caras=0;coins=4;t=0 !!!tirar

"""