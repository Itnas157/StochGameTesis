name = "block"
init_vars = ["t=0", "j1=2", "j2=2", "clock=5"]

repeticiones = 25
alphas = [0.5]  # Tasa de aprendizaje
gammas = [1]  # Factor de descuento
epsilons = [0.9]  # Probabilidad de exploración inicial

smart_sampling_ns = [2**10]
q_learning_episodes = [2046]

trans_str = """
--Juego donde hay que bloquear al otro jugador

--Victoria/Derrota
qf: j1=0 ^ j2=0 ^ clock=0 -> 1
qf: j1=1 ^ j2=1 ^ clock=0 -> 1
qf: j1=2 ^ j2=2 ^ clock=0 -> 1
qf: j1=3 ^ j2=3 ^ clock=0 -> 1
qf: j1=4 ^ j2=4 ^ clock=0 -> 1

qf: j1=0 ^ j2=1|...|4 ^ clock=0 -> -1
qf: j1=1 ^ j2=0|2|3|4 ^ clock=0 -> -1
qf: j1=2 ^ j2=0|1|3|4 ^ clock=0 -> -1
qf: j1=3 ^ j2=0|1|2|4 ^ clock=0 -> -1
qf: j1=4 ^ j2=0|...|3 ^ clock=0 -> -1

--Jugador 1
--t=0
t=0 ^ j1=0|...|4 ^ clock=1|...|5 -> 0.8: t=1 | 0.1: j1=max(0,j1-1);t=1 | 0.1: j1=min(4,j1+1);t=1 !!!quieto
t=0 ^ j1=0|...|3 ^ clock=1|...|5 -> 0.5: t=1 | 0.5: j1=j1+1;t=1 !!!derecha
t=0 ^ j1=1|...|4 ^ clock=1|...|5 -> 0.5: t=1 | 0.5: j1=j1-1;t=1 !!!izquierda

--Jugador 2
--t=1
t=1 ^ j2=0|...|4 ^ clock=1|...|5 -> 0.4: t=0;clock=clock-1 | 0.3: j2=max(0,j2-1);t=0;clock=clock-1 | 0.3: j2=min(4,j2+1);t=0;clock=clock-1 !!!quieto
t=1 ^ j2=0|...|3 ^ clock=1|...|5 -> 0.9: t=0;clock=clock-1 | 0.1: j2=j2+1;t=0;clock=clock-1 !!!derecha
t=1 ^ j2=1|...|4 ^ clock=1|...|5 -> 0.9: t=0;clock=clock-1 | 0.1: j2=j2-1;t=0;clock=clock-1 !!!izquierda

"""