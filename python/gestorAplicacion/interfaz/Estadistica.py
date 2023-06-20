from enum import Enum


class Garantia(Enum):
    Vivienda = 1
    Lote = 2
    Carro = 3
    Moto = 4


class Estadistica:
    @staticmethod
    def calcular_posible_cantidad_prestamo(usuario, ingresos, edad, hijos, opc_garantia):
        if not usuario.getAhorros():
            return Estadistica.promediar_variables_del_usuario(ingresos, 0, edad, hijos, opc_garantia)
        else:
            promedio_ahorros = Estadistica.calcular_promedio_ahorros(usuario)
            return Estadistica.promediar_variables_del_usuario(ingresos, promedio_ahorros, edad, hijos, opc_garantia)

    @staticmethod
    def calcular_promedio_ahorros(usuario):
        total_ahorros = sum(ahorro.getSaldo() for ahorro in usuario.getAhorros())
        cantidad_ahorros = len(usuario.getAhorros())

        promedio_ahorros = total_ahorros / cantidad_ahorros

        return promedio_ahorros

    @staticmethod
    def promediar_variables_del_usuario(ingresos, promedio_ahorros, edad, hijos, opc_garantia):
        multiplicador_cantidad_a_prestar = 3
        posible_prestamo = 7 * (ingresos * 0.3)

        ingreso_de_8_meses = ingresos * 8
        if promedio_ahorros > ingreso_de_8_meses:
            multiplicador_cantidad_a_prestar += 4
        elif promedio_ahorros > ingreso_de_8_meses / 2:
            multiplicador_cantidad_a_prestar += 3
        elif promedio_ahorros > ingreso_de_8_meses / 2:
            multiplicador_cantidad_a_prestar += 2
        if edad > 72 or edad < 16:
            multiplicador_cantidad_a_prestar -= 3
        if hijos > 0:
            multiplicador_cantidad_a_prestar -= 2
        if opc_garantia > 0:
            garantia = Garantia(opc_garantia)
            if garantia == Garantia.Vivienda:
                multiplicador_cantidad_a_prestar += 7
            elif garantia == Garantia.Lote:
                multiplicador_cantidad_a_prestar += 5
            elif garantia == Garantia.Carro:
                multiplicador_cantidad_a_prestar += 3
            elif garantia == Garantia.Moto:
                multiplicador_cantidad_a_prestar += 1

        posible_prestamo = (posible_prestamo + promedio_ahorros) * multiplicador_cantidad_a_prestar

        return posible_prestamo
