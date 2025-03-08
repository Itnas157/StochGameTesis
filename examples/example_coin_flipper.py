name = "coin_flipper"
init_vars = ["t=1", "j1=0", "j2=0", "caras=0", "coins=4"]
trans_str = """
--Juego de tirar monedas, gana el que llegue a 15 caras primero
--Se tiran cuatro monedas:
-- Cuando sale cara en una moneda, se aparta
-- Si sale cruz, se puede volver a tirar
-- Si todas son cruz, se pierde el turno y pasa al siguiente jugador
--Ej:
--Jugador 1 tira y salen 2 caras y 2 cruz; aparta las 2 caras y vuelve a tirar las 2 cruces, le sale una cara y una cruz, guarda las 3 caras y termina su turno.
--El jugador 2 tira y le salen 3 caras y una cruz, decide volver a tirar la cruz y le sale otra vez cruz, pierde su turno.
--Resultado de esa ronda: El jugador 1 va 3 caras mientras que el jugador 2 va 0.

--Victoria/Derrota
qf: j1=15 -> 1
qf: j2=15 -> -1

--Jugador 1
--t=0

t=0 ^ j1=0|...|14 ^ caras=0|...|15 -> 1: j1=min(j1+caras, 15);t=1 !!!guardar
t=0 ^ j1=0|...|14 ^ coins=1 ^ caras=0|...|15 -> 0.5: caras=min(caras+1, 15);coins=4 | 0.5: caras=0;coins=4;t=1 !!!tirar
t=0 ^ j1=0|...|14 ^ coins=2 ^ caras=0|...|15 -> 0.25: caras=min(caras+2, 15);coins=4 | 0.5: caras=min(caras+1, 15);coins=1 | 0.25: caras=0;coins=4;t=1 !!!tirar
t=0 ^ j1=0|...|14 ^ coins=3 ^ caras=0|...|15 -> 0.125: caras=min(caras+3, 15);coins=4 | 0.375: caras=min(caras+2, 15);coins=1 | 0.375: caras=min(caras+1, 15);coins=2 | 0.125: caras=0;coins=4;t=1 !!!tirar
t=0 ^ j1=0|...|14 ^ coins=4 ^ caras=0|...|15 -> 0.0625: caras=min(caras+4, 15);coins=4 | 0.25: caras=min(caras+3, 15);coins=1 | 0.375: caras=min(caras+2, 15);coins=2 | 0.25: caras=min(caras+1, 15);coins=3 | 0.0625: caras=0;coins=4;t=1 !!!tirar

--Jugador 2
--t=1

t=1 ^ j2=0|...|14 ^ caras=0|...|15 -> 1: j2=min(j2+caras, 15);t=0 !!!guardar
t=1 ^ j2=0|...|14 ^ coins=1 ^ caras=0|...|15 -> 0.5: caras=min(caras+1, 15);coins=4 | 0.5: caras=0;coins=4;t=0 !!!tirar
t=1 ^ j2=0|...|14 ^ coins=2 ^ caras=0|...|15 -> 0.25: caras=min(caras+2, 15);coins=4 | 0.5: caras=min(caras+1, 15);coins=1 | 0.25: caras=0;coins=4;t=0 !!!tirar
t=1 ^ j2=0|...|14 ^ coins=3 ^ caras=0|...|15 -> 0.125: caras=min(caras+3, 15);coins=4 | 0.375: caras=min(caras+2, 15);coins=1 | 0.375: caras=min(caras+1, 15);coins=2 | 0.125: caras=0;coins=4;t=0 !!!tirar
t=1 ^ j2=0|...|14 ^ coins=4 ^ caras=0|...|15 -> 0.0625: caras=min(caras+4, 15);coins=4 | 0.25: caras=min(caras+3, 15);coins=1 | 0.375: caras=min(caras+2, 15);coins=2 | 0.25: caras=min(caras+1, 15);coins=3 | 0.0625: caras=0;coins=4;t=0 !!!tirar

"""