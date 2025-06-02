import random

def gerar_objeto_decorativo():
    """
    Gera um objeto com posição e velocidade aleatória.
    Utilizado para criar um elemento decorativo que se move no fundo.
    """
    return {
        "x": random.randint(0, 1000),
        "y": random.randint(0, 700),
        "vx": random.uniform(-1, 1),
        "vy": random.uniform(-1, 1)
    }
