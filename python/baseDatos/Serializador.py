import pickle
import pathlib
import os

class Serializador:
    def __init__(self, usuario):
        self._usuario = usuario

    def serializar(self):
        path = os.path.join(pathlib.Path(__file__).parent.parent.parent.parent.absolute(),'practica-2-grupo-1-equipo-5-INTERNO\\baseDatos\\temp\\usuario.pkl')
        picklefile = open(path, "wb")
        pickle.dump(self._usuario, picklefile)
        picklefile.close()
