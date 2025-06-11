name = "dice"
init_vars = ["t=0", "j1=0", "j2=0", "ac=0"]

repeticiones = 25
alphas = [0.5]  # Tasa de aprendizaje
gammas = [1]  # Factor de descuento
epsilons = [0.9]  # Probabilidad de exploración inicial

smart_sampling_ns = [2**11]
q_learning_episodes = [2046]

trans_str = """
--Juego de lanzar un dado hasta llegar a 50
--Cada jugador tiene dos opciones:
--Guardar lo acumulado o lanzar de nuevo
--Si el jugador lanza de nuevo, el dado se suma al acumulado
--Si sale un 6, el acumulado se pierde y el turno pasa al otro jugador
--Sólo se acumula hasta 20

--Victoria/Derrota
qf: j1=50 -> 1
qf: j2=50 -> -1

--Jugador 1
--t=0

t=0 ^ j1=0|...|49 ^ ac=0|...|50 -> 1: j1=min(j1+ac, 50);t=1 !!!guardar
t=0 ^ j1=0|...|19 ^ ac=0|...|50 -> 0.166666: ac=min(ac+1, 50) | 0.166666: ac=min(ac+2, 50) | 0.166666: ac=min(ac+3, 50) | 0.166666: ac=min(ac+4, 50) | 0.166666: ac=min(ac+5, 50) | 0.16667: ac=0;t=1 !!!lanzar

--Jugador y
--t=1

t=1 ^ j2=0|...|49 ^ ac=0|...|50 -> 1: j2=min(j2+ac, 50);t=0 !!!guardar
t=1 ^ j2=0|...|19 ^ ac=0|...|50 -> 0.166666: ac=min(ac+1, 50) | 0.166666: ac=min(ac+2, 50) | 0.166666: ac=min(ac+3, 50) | 0.166666: ac=min(ac+4, 50) | 0.166666: ac=min(ac+5, 50) | 0.16667: ac=0;t=0 !!!lanzar
"""