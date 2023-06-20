class Transaccion:

    def __init__(self, monto, fechaCreacion):
        self._monto = monto
        self._fechaCreacion = fechaCreacion

    def getMonto(self):
        return self._monto

    def setMonto(self, monto):
        self._monto = monto

    def getFechaCreacion(self):
        return self._fechaCreacion

    def setFechaCreacion(self, fechaCreacion):
        self._fechaCreacion = fechaCreacion
