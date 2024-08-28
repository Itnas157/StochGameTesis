# Definimos todos los estados
States = ["Init", "T", "F", "TT", "TF", "FT", "FF"]

# Definimos todas las decisiones
Labels = ["heads", "tails"]

# Repartimos los estados en una funcion que toma un estado y devuelve a quien le pertenece
Partitions = [
    ["Init"],
    ["T", "F"]
]

# Al llegar a un final, decidimos cuanto vale
Weights = [
   ("TF", 1),
   ("TT", 0.5),
   ("FF", 0.5),
   ("FT", 0)
]

# Definimos las transiciones
Transitions = [
   ("Init", "heads", 0.5, "T"),
   ("Init", "heads", 0.5, "F"),
   ("Init", "tails", 0.5, "T"),
   ("Init", "tails", 0.5, "F"),
   ("T", "heads", 0.5, "TT"),
   ("T", "heads", 0.5, "TF"),
   ("T", "tails", 0.5, "TT"),
   ("T", "tails", 0.5, "TF"),
   ("F", "heads", 0.5, "FT"),
   ("F", "heads", 0.5, "FF"),
   ("F", "tails", 0.5, "FT"),
   ("F", "tails", 0.5, "FF")
]