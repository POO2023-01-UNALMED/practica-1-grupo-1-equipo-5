# Ana Guarín
# Isabela Hernandez
# Julián Álvarez
class Cuenta:

    def __init__(self, usuario, nombre):
        self._usuario = usuario
        self._saldo = 0
        self._nombre = nombre

    def getNombre(self):
        return self._nombre

    def setNombre(self, nombre):
        self._nombre = nombre

    def getUsuario(self):
        return self._usuario

    def setUsuario(self, usuario):
        self._usuario = usuario

    def depositar(self, cantidad):
        self._saldo = self._saldo + cantidad

    def retirar(self, cantidad):
        if cantidad<=self._saldo:
            self._saldo = self._saldo - cantidad
            return True
        else:
            return False

    def getSaldo(self):
        return self._saldo

    def setSaldo(self, saldo):
        self._saldo = saldo
