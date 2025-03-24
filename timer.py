import time

def timer(func):
    """Decorador para medir el tiempo de ejecución de una función."""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()  # Inicia el cronómetro
        result = func(*args, **kwargs)  # Ejecuta la función
        end = time.perf_counter()  # Detiene el cronómetro
        print(f"{func.__name__} tardó {end - start:.6f} segundos en ejecutarse")
        return result  # Devuelve el resultado original
    return wrapper