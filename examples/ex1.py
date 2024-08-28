# Definimos todos los estados
States = ["Init", "H", "T", "HH", "HT", "TH", "TT"]

# Definimos todas las decisiones
Labels = ["h", "t"]

# Repartimos los estados en una funcion que toma un estado y devuelve a quien le pertenece
Partitions = [
    ["Init"],
    ["H", "T"]
]

# Al llegar a un final, decidimos cuanto vale
Weights = [
   ("HH", 1),
   ("HT", 0.5),
   ("TH", 0.5),
   ("TT", 0)
]

Transitions = [
   ("Init", "h", 0.5, "H"),
   ("Init", "h", 0.5, "T"),
   ("Init", "t", 0.5, "H"),
   ("Init", "t", 0.5, "T"),
   ("H", "h", 0.5, "HH"),
   ("H", "h", 0.5, "HT"),
   ("H", "t", 0.5, "HT"),
   ("H", "t", 0.5, "HH"),
   ("T", "h", 0.5, "TH"),
   ("T", "h", 0.5, "TT"),
   ("T", "t", 0.5, "TT"),
   ("T", "t", 0.5, "TH")
]