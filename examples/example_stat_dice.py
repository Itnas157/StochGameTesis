init_vars = ["t=0", "x=0", "y=0", "ac=0"]
trans_str = """
--Juego de lanzar un dado hasta llegar a 20
--Cada jugador tiene dos opciones:
--Guardar lo acumulado o lanzar de nuevo
--Si el jugador lanza de nuevo, el dado se suma al acumulado
--Si sale un 6, el acumulado se pierde y el turno pasa al otro jugador
--Sólo se acumula hasta 20

--Victoria/Derrota
qf: x=20 -> 1
qf: y=20 -> -1

--Jugador x
--t=0

t=0 ^ x=0|...|19 ^ ac=0|...|20 -> 1:x=x+ac'min'20,t=1 !guardar
t=0 ^ x=0|...|19 ^ ac=0|...|20 -> 0.166666:ac=ac+1 or 0.166666:ac=ac+2 or 0.166666:ac=ac+3 or 0.166666:ac=ac+4 or 0.166666:ac=ac+5 or 0.16667:ac=0,t=1 !lanzar

--Jugador y
--t=1

t=1 ^ y=0|...|19 ^ ac=0|...|20 -> 1:y=y+ac'min'20,t=0 !guardar
t=1 ^ y=0|...|19 ^ ac=0|...|20 -> 0.166666:ac=ac+1 0.166666:ac=ac+2 0.166666:ac=ac+3 0.166666:ac=ac+4 0.166666:ac=ac+5 0.16667:ac=0,t=0 !lanzar
"""