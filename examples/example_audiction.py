init_vars = ["t=0", "ronda=0", "x=0", "y=0", "x_coins=10", "y_coins=10", "x_pays=0", "y_pays=0"]
trans_str = """
--Juego de subasta de monedas
--Cada jugador tiene 10 monedas
--Cada ronda se subastan puntos a ciegas (20% vale un punto, 20% vale 2 puntos, ..., 20% vale 5 puntos)
--Cada jugador decide cuánto paga por la ronda y el que pagó más se lleva los puntos
--Gana el jugador con más puntos al final de 5 rondas

--Victoria/Derrota
qf: ronda=5 ^ x>y -> 1
qf: ronda=5 ^ y>x -> -1
qf: ronda=5 ^ x=y -> 0

--Jugador x
--t=0
t=0 ^ x_coins=10 ^ y_pays=0|...|9 -> 1:x_pays=10,t=1 !paga_10
t=0 ^ x_coins=9|10 ^ y_pays=0|...|8 -> 1:x_pays=9,t=1 !paga_9
t=0 ^ x_coins=8|...|10 ^ y_pays=0|...|7 -> 1:x_pays=8,t=1 !paga_8
t=0 ^ x_coins=7|...|10 ^ y_pays=0|...|6 -> 1:x_pays=7,t=1 !paga_7
t=0 ^ x_coins=6|...|10 ^ y_pays=0|...|5 -> 1:x_pays=6,t=1 !paga_6
t=0 ^ x_coins=5|...|10 ^ y_pays=0|...|4 -> 1:x_pays=5,t=1 !paga_5
t=0 ^ x_coins=4|...|10 ^ y_pays=0|...|3 -> 1:x_pays=4,t=1 !paga_4
t=0 ^ x_coins=3|...|10 ^ y_pays=0|...|2 -> 1:x_pays=3,t=1 !paga_3
t=0 ^ x_coins=2|...|10 ^ y_pays=0|...|1 -> 1:x_pays=2,t=1 !paga_2
t=0 ^ x_coins=1|...|10 ^ y_pays=0 -> 1:x_pays=1,t=1 !paga_1

t=0 ^ x_coins=0|...|10 ^ y_pays=0 -> 1:t=1 !no_oferta

--No ofertar pero el otro jugador sí, así que el otro jugador paga y gana puntos, se reinicia las ofertas y siguiente ronda

t=0 ^ x_coins=0|...|10 ^ y_pays=1|...|10 -> 0.2:y_coins=y_coins-y_pays,ronda=ronda+1,y=y+1,y_pays=0,x_pays=0 0.2:y_coins=y_coins-y_pays,ronda=ronda+1,y=y+2,y_pays=0,x_pays=0 0.2:y_coins=y_coins-y_pays,ronda=ronda+1,y=y+3,y_pays=0,x_pays=0 0.2:y_coins=y_coins-y_pays,ronda=ronda+1,y=y+4,y_pays=0,x_pays=0 0.2:y_coins=y_coins-y_pays,ronda=ronda+1,y=y+5,y_pays=0,x_pays=0 !no_oferta

--Jugador y
--t=1
t=1 ^ y_coins=10 ^ x_pays=0|...|9 -> 1:y_pays=10,t=0 !paga_10
t=1 ^ y_coins=9|10 ^ x_pays=0|...|8 -> 1:y_pays=9,t=0 !paga_9
t=1 ^ y_coins=8|...|10 ^ x_pays=0|...|7 -> 1:y_pays=8,t=0 !paga_8
t=1 ^ y_coins=7|...|10 ^ x_pays=0|...|6 -> 1:y_pays=7,t=0 !paga_7
t=1 ^ y_coins=6|...|10 ^ x_pays=0|...|5 -> 1:y_pays=6,t=0 !paga_6
t=1 ^ y_coins=5|...|10 ^ x_pays=0|...|4 -> 1:y_pays=5,t=0 !paga_5
t=1 ^ y_coins=4|...|10 ^ x_pays=0|...|3 -> 1:y_pays=4,t=0 !paga_4
t=1 ^ y_coins=3|...|10 ^ x_pays=0|...|2 -> 1:y_pays=3,t=0 !paga_3
t=1 ^ y_coins=2|...|10 ^ x_pays=0|...|1 -> 1:y_pays=2,t=0 !paga_2
t=1 ^ y_coins=1|...|10 ^ x_pays=0 -> 1:y_pays=1,t=0 !paga_1

--Ningún jugador ofertó, siguiente ronda
t=1 ^ y_coins=0|...|10 ^ x_pays=0 -> 1:t=0,ronda=ronda+1 !no_oferta

--No ofertar pero el otro jugador sí, así que el otro jugador paga y gana puntos, se reinicia las ofertas y siguiente ronda

t=1 ^ y_coins=0|...|10 ^ x_pays=1|...|10 -> 0.2:x_coins=x_coins-x_pays,ronda=ronda+1,x=x+1,x_pays=0,y_pays=0,t=0 0.2:x_coins=x_coins-x_pays,ronda=ronda+1,x=x+2,x_pays=0,y_pays=0,t=0 0.2:x_coins=x_coins-x_pays,ronda=ronda+1,x=x+3,x_pays=0,y_pays=0,t=0 0.2:x_coins=x_coins-x_pays,ronda=ronda+1,x=x+4,x_pays=0,y_pays=0,t=0 0.2:x_coins=x_coins-x_pays,ronda=ronda+1,x=x+5,x_pays=0,y_pays=0,t=0 !no_oferta
"""



