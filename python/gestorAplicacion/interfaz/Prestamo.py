import datetime
import math

class Prestamo:
    tasa = 0.18

    def __init__(self, usuario, montoPrestado, periodos, referencia, garantia=None):
        self.montoPrestado = montoPrestado
        self.totalPagado = 0
        self.fechaFinal = datetime.date.today() + datetime.timedelta(months=periodos)
        self.fechaInicio = datetime.date.today()
        self.garantia = garantia

    @staticmethod
    def calcularCuotas(posibleCantidadPrestamo, ingresoMensual, gastoVivienda):
        infoCuotas = [0, 0]
        cantidadQuePodraPagar = ingresoMensual * 0.3

        if gastoVivienda >= ingresoMensual:
            return infoCuotas

        porcentajeGastoVivienda = gastoVivienda / ingresoMensual
        if porcentajeGastoVivienda > 0.7:
            return infoCuotas

        if porcentajeGastoVivienda > 0.5:
            cantidadQuePodraPagar = ingresoMensual * 0.1
            infoCuotas[0] = Prestamo.calcularPeriodos(cantidadQuePodraPagar, posibleCantidadPrestamo)
            infoCuotas[1] = cantidadQuePodraPagar
            return infoCuotas

        infoCuotas[0] = Prestamo.calcularPeriodos(cantidadQuePodraPagar, posibleCantidadPrestamo)
        infoCuotas[1] = cantidadQuePodraPagar
        return infoCuotas

    @staticmethod
    def calcularPeriodos(cantidadQuePodraPagar, posibleCantidadPrestamo):
        periodos = math.log(abs(1 - ((Prestamo.tasa * posibleCantidadPrestamo) / cantidadQuePodraPagar))) / math.log(abs(1 + Prestamo.tasa))
        return round(periodos)

    def getTasa(self):
        return Prestamo.tasa

    def getFechaInicio(self):
        return self.fechaInicio

    def getFechaFinal(self):
        return self.fechaFinal

    def getGarantia(self):
        return self.garantia

    def setGarantia(self, garantia):
        self.garantia = garantia

    def getMontoPrestado(self):
        return self.montoPrestado

    def setMontoPrestado(self, montoPrestado):
        self.montoPrestado = montoPrestado

    def getTotalPagado(self):
        return self.totalPagado

    def abonar(self, monto, origen):
        if origen.retirar(monto):
            self.totalPagado += monto
            if self.totalPagado >= self.getMontoPrestado():
                self.pagado = True
                print("Felicidades pagaste tu prestamo")
                return True
        print("No puedes abonar, saldo insuficiente")
        return None

    def abonar(self, monto, origen):
        arreglo = [0]
        if not self.pagado:
            if origen.getSaldo() >= monto:
                origen.setSaldo(origen.getSaldo() - monto)
                self.totalPagado += monto
                if self.totalPagado >= self.getMontoPrestado():
                    self.pagado = True
                arreglo[0] = monto
                return arreglo
            else:
                return None
        return None

    def terminar(self, cuenta):
        return None

    def terminar(self, categoria):
        return None

    def isPagado(self):
        return self.pagado

    def setPagado(self, pagado):
        self.pagado = pagado
