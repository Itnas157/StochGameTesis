init_vars = ["t=0", "ac=0", "coins=5", "x=0", "y=0"]
trans_str = """
--Victoria
x=10|...|19 -> 1:_R_=2 !guardar
x=10|...|19 -> 1:_R_=2 !jugar
y=10|...|19 -> 1:_R_=1 !guardar
y=10|...|19 -> 1:_R_=1 !jugar

t=0 ^ ac=15 -> 1:_R_=2 !guardar
t=0 ^ ac=15 -> 1:_R_=2 !jugar
t=1 ^ ac=15 -> 1:_R_=1 !guardar
t=1 ^ ac=15 -> 1:_R_=1 !jugar

--Jugador x
--Caso tengo 5 monedas
t=0 ^ coins=5 ^ x=0|...|9 ^ ac=0|5|10 -> 1:x=x+ac,ac=0,t=1 !guardar
t=0 ^ coins=5 ^ x=0|...|9 ^ ac=0|5|10 -> 0.03125:ac=ac+5 0.15625:coins=1 0.3125:coins=2 0.3125:coins=3 0.15625:coins=4 0.03125:ac=0,t=1 !jugar

--Caso tengo 4 monedas
t=0 ^ coins=4 ^ x=0|...|9 ^ ac=0|5|10 -> 1:x=x+1+ac,coins=5,ac=0,t=1 !guardar
t=0 ^ coins=4 ^ x=0|...|9 ^ ac=0|5|10 -> 0.0625:coins=5,ac=ac+5 0.25:coins=1 0.375:coins=2 0.25:coins=3 0.0625:coins=5,ac=0,t=1 !jugar

--Caso tengo 3 monedas
t=0 ^ coins=3 ^ x=0|...|9 ^ ac=0|5|10 -> 1:x=x+2+ac,coins=5,ac=0,t=1 !guardar
t=0 ^ coins=3 ^ x=0|...|9 ^ ac=0|5|10 -> 0.125:coins=5,ac=ac+5 0.375:coins=1 0.375:coins=2 0.125:coins=5,ac=0,t=1 !jugar

--Caso tengo 2 monedas
t=0 ^ coins=2 ^ x=0|...|9 ^ ac=0|5|10 -> 1:x=x+3+ac,coins=5,ac=0,t=1 !guardar
t=0 ^ coins=2 ^ x=0|...|9 ^ ac=0|5|10 -> 0.25:coins=5,ac=ac+5 0.5:coins=1 0.25:coins=5,ac=0,t=1 !jugar

--Caso tengo una moneda
t=0 ^ coins=1 ^ x=0|...|9 ^ ac=0|5|10 -> 1:x=x+4+ac,coins=5,ac=0,t=1 !guardar
t=0 ^ coins=1 ^ x=0|...|9 ^ ac=0|5|10 -> 0.5:coins=5,ac=ac+5 0.5:coins=5,ac=0,t=1 !jugar

--Jugador y
--Caso tengo 5 monedas
t=1 ^ coins=5 ^ y=0|...|9 ^ ac=0|5|10 -> 1:y=y+ac,ac=0,t=0 !guardar
t=1 ^ coins=5 ^ y=0|...|9 ^ ac=0|5|10 -> 0.03125:ac=ac+5 0.15625:coins=1 0.3125:coins=2 0.3125:coins=3 0.15625:coins=4 0.03125:ac=0,t=0 !jugar

--Caso tengo 4 monedas
t=1 ^ coins=4 ^ y=0|...|9 ^ ac=0|5|10 -> 1:y=y+1+ac,coins=5,ac=0,t=0 !guardar
t=1 ^ coins=4 ^ y=0|...|9 ^ ac=0|5|10 -> 0.0625:coins=5,ac=ac+5 0.25:coins=1 0.375:coins=2 0.25:coins=3 0.0625:coins=5,ac=0,t=0 !jugar

--Caso tengo 3 monedas
t=1 ^ coins=3 ^ y=0|...|9 ^ ac=0|5|10 -> 1:y=y+2+ac,coins=5,ac=0,t=0 !guardar
t=1 ^ coins=3 ^ y=0|...|9 ^ ac=0|5|10 -> 0.125:coins=5,ac=ac+5 0.375:coins=1 0.375:coins=2 0.125:coins=5,ac=0,t=0 !jugar

--Caso tengo 2 monedas
t=1 ^ coins=2 ^ y=0|...|9 ^ ac=0|5|10 -> 1:y=y+3+ac,coins=5,ac=0,t=0 !guardar
t=1 ^ coins=2 ^ y=0|...|9 ^ ac=0|5|10 -> 0.25:coins=5,ac=ac+5 0.5:coins=1 0.25:coins=5,ac=0,t=0 !jugar

--Caso tengo una moneda
t=1 ^ coins=1 ^ y=0|...|9 ^ ac=0|5|10 -> 1:y=y+4+ac,coins=5,ac=0,t=0 !guardar
t=1 ^ coins=1 ^ y=0|...|9 ^ ac=0|5|10 -> 0.5:coins=5,ac=ac+5 0.5:coins=5,ac=0,t=0 !jugar
"""