from cx_Freeze import setup, Executable

setup(
    name="FutGol2D",
    version="1.0",
    description="Jogo 2D de futebol feito em Python",
    executables=[Executable("main.py")]
)
