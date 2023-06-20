import pickle
import pathlib
import os

class Deserializador:
    def __init__(self):
        self._usuario = None

    def deserializar(self):
        path = os.path.join(pathlib.Path(__file__).parent.parent.parent.parent.absolute(),'practica-2-grupo-1-equipo-5-INTERNO\\baseDatos\\temp\\usuario.pkl')
        picklefile = open(path, "rb")
        usuario = pickle.load(picklefile)
        picklefile.close()
        self._usuario = usuario

    def getArgs(self):
        return self._usuario
