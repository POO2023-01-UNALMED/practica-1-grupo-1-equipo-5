package uiMain;

// Ana Guarín
// Isabela Hernandez
// Cristian Menaa
// Julián Álvarez

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

import baseDatos.Deserializador;
import gestorAplicacion.confirmacion.Datos;
import baseDatos.Serializador;
import gestorAplicacion.confirmacion.Listador;
import gestorAplicacion.confirmacion.Verificacion;
import gestorAplicacion.interfaz.Abonable;
import gestorAplicacion.interfaz.Ahorro;
import gestorAplicacion.interfaz.Categoria;
import gestorAplicacion.interfaz.Cuenta;
import gestorAplicacion.interfaz.Estadistica;
import gestorAplicacion.interfaz.Garantia;
import gestorAplicacion.interfaz.Ingreso;
import gestorAplicacion.interfaz.Meta;
import gestorAplicacion.interfaz.Prestamo;
import gestorAplicacion.interfaz.Transaccion;
import gestorAplicacion.interfaz.Usuario;


import static gestorAplicacion.confirmacion.Listador.*;
import static gestorAplicacion.confirmacion.Verificacion.*;

import java.io.IOException;

public class Main {
    Usuario usuario;

    static Usuario login() {
        Deserializador.deserializar();
        try {
            return Datos.getUsuarios().get(0);

        } catch (Exception e) {
            return null;
        }
    }

    public static void main(String[] args) throws IOException {
        Usuario usuario = login();
        if (usuario == null) {
            usuario = new Usuario(1, "Julian", "default@correo.com");
            Datos.nuevoUsuario(usuario);
        }

        int option;

        do {
            System.out.println("..... FINANZAS PERSONALES .....");
            System.out.println("..... USUARIO: " + usuario.getNombre() + " .....");
            System.out.println("¿Que operación desea realizar?");
            System.out.println("1. Ver Estadisticas de la cuenta");
            System.out.println("2. Ingresar dinero a su cuenta");
            System.out.println("3. Mover dinero en su cuenta");
            System.out.println("4. Sacar dinero de su cuenta");
            System.out.println("5. Agregar Ahorro a su cuenta");
            System.out.println("6. Agregar Meta a su cuenta");
            System.out.println("7. Modificar Ahorro/Bolsillo/Meta");
            System.out.println("8. Solicitar Prestamo");
            System.out.println("9. Abonar a un préstamo o Meta");
            System.out.println("10. Terminar ");
            System.out.println("");
            option = validarEntradaInt(10, true, 0, false);

            switch (option) {
                case 1 -> saldosDisponibles(usuario);
                case 2 -> ingresaDinero(usuario);
                case 3 -> moverDineroInterno(usuario);
                case 4 -> SacarDinero(usuario);
                case 5 -> agregarAhorro(usuario);
                case 6 -> agregarMeta(usuario);
                case 7 -> opcionModificar(usuario);
                case 8 -> solicitarPrestamo(usuario);
                case 9 -> abonarPrestamoOMeta(usuario);
                case 10 -> {
                    Serializador.serializar();
                    System.exit(0);
                }
                default -> System.out.println("OPCIÓN EN DESARROLLO");
            }
        } while (option != 12);
        System.exit(0);
    }

    //OPCIÓN1
    //Menú de cuentas disponibles y sus respectivos saldos del usuario seleccionado en el login()
    static void saldosDisponibles(Usuario usuario) {
        int option;
        System.out.println("");
        System.out.println("¿Que cuentas desea visualizar?");
        System.out.println("1. Bolsillos");
        System.out.println("2. Ahorros");
        System.out.println("3. Metas");
        System.out.println("4. Prestamos");
        System.out.println("5. Dinero total");
        System.out.println("6. Volver al inicio");
        System.out.println("");
        option = validarEntradaInt(6, true, 0, false);

        switch (option) {
            case 1 -> listarBolsillos(usuario);
            case 2 -> Listador.listarAhorros(usuario);
            case 3 -> Listador.listarMetas(usuario);
            case 4 -> Listador.listarPrestamos(usuario);
            case 5 -> {
                double dineroTot = usuario.getDineroCuenta();
                System.out.println("");
                System.out.println("");
                System.out.println("Dinero total: ");
                System.out.println(dineroTot);

                System.out.println("");
                System.out.println("");
            }
        }
    }

    //OPCIÓN2
    //Menú de selección a que cuenta va a realizar el ingreso de dinero y se llama a elección BancoMonto() donde se va a realizar el ingreso
    static void ingresaDinero(Usuario usuario) {
        int option, opc;
        System.out.println("");
        System.out.println("¿Para donde va su dinero?");
        System.out.println("1. Bolsillos");
        System.out.println("2. Ahorros");
        System.out.println("3. Volver al inicio");
        System.out.println("");
        option = validarEntradaInt(3, true, 1, true);
        boolean bool;
        switch (option) {
            case 1 -> {
                List<Categoria> list = new ArrayList<>();
                System.out.println("");
                System.out.println("Bolsillo: ");
                bool = listarBolsillos(usuario);

                for (Categoria bolsillos : Categoria.values()) {
                    list.add(bolsillos);
                }

                if (bool) {
                    opc = validarEntradaInt(8, true, 1, true) - 1;
                    Categoria bolsillo = list.get(opc);

                    double cantidad;
                    System.out.println("");
                    System.out.println("Digite la cantidad que desea ingresar en (utilice ',' para el símbolo decimal) (Cantidad maxima 10000000): ");
                    cantidad = Verificacion.validarEntradaDouble(10000000, true, 0, false);
                    new Ingreso((int) cantidad, LocalDate.now(), bolsillo);
                    System.out.println("");
                    System.out.println("Su nuevo saldo es de " + String.format("%.2f", (double) bolsillo.getSaldo()));
                    System.out.println("");
                    System.out.println("");

                }
            }
            case 2 -> {
                List<Cuenta> list = new ArrayList<>();
                System.out.println("");
                System.out.println("Ahorros: ");
                bool = Listador.listarAhorros(usuario);
                list.addAll(usuario.getAhorros());

                if (bool) {
                    opc = validarEntradaInt(list.size(), true, 1, true) - 1;
                    Cuenta cuenta = list.get(opc);

                    double cantidad;
                    System.out.println("");
                    System.out.println("Digite la cantidad que desea ingresar en (utilice ',' para el símbolo decimal) (Cantidad maxima 10000000): ");
                    cantidad = Verificacion.validarEntradaDouble(10000000, true, 0, false);
                    Ingreso ingreso = new Ingreso(cantidad, LocalDate.now(), cuenta);
                    usuario.nuevoIngreso(ingreso);
                    System.out.println("");
                    System.out.println("Su nuevo saldo es de " + String.format("%.2f", cuenta.getSaldo()));
                    System.out.println("");

                }
            }
        }
    }


    //Opcion3
    static void moverDineroInterno(Usuario usuario) {
        int option;
        System.out.println("");
        System.out.println("¿Para donde va su dinero?");
        System.out.println("1. Bolsillos");
        System.out.println("2. Ahorros");
        System.out.println("3. Volver al inicio");
        System.out.println("");
        option = validarEntradaInt(3, true, 1, true);
        boolean bool = false;
        switch (option) {
            case 1 -> {
                Categoria destino;
                Object origen;
                List<Categoria> list = new ArrayList<>();
                System.out.println("");
                System.out.println("Bolsillos: ");
                bool = listarBolsillos(usuario);

                for (Categoria bolsillos : Categoria.values()) {
                    list.add(bolsillos);
                }

                if (bool) {
                    int opc = validarEntradaInt(8, true, 1, true) - 1;
                    destino = list.get(opc);
                    origen = seleccionarCuentaDeOrigen(usuario, destino);

                    if (origen instanceof Cuenta) {
                        Cuenta origen2 = (Cuenta) origen;
                        if (origen != null && origen2.getSaldo() > 0) {
                            System.out.println("");
                            System.out.println("Ingrese la cantidad a transferir (entre 0 y " + String.format("%.2f", origen2.getSaldo()) + ")");
                            double monto = Verificacion.validarEntradaDouble(origen2.getSaldo(), true, 0, false);

                            boolean retirado = origen2.retirar(monto);

                            if (!retirado) {
                                System.out.println("");
                                System.out.println("");
                                System.err.println("No fue posible retirar");
                                System.out.println("");
                                System.out.println("");
                                return;
                            }
                            destino.setSaldo(destino.getSaldo() + monto);
                            System.out.println("");
                            System.out.println("Nuevo saldo de la cuenta de origen de: " + String.format("%.2f", origen2.getSaldo()));
                            System.out.println("Nuevo saldo de la cuenta de destino de: " + String.format("%.2f", destino.getSaldo()));
                            System.out.println("");
                        } else {
                            System.out.println("");
                            System.out.println("");
                            System.out.println("La cuenta no existe o no contiene dinero");
                            System.out.println("");
                        }

                    }

                    if (origen instanceof Categoria) {
                        Categoria origen2 = (Categoria) origen;
                        if (origen != null && origen2.getSaldo() > 0) {
                            System.out.println("");
                            System.out.println("Ingrese la cantidad a transferir (entre 0 y " + String.format("%.2f", origen2.getSaldo()) + ")");
                            double monto = Verificacion.validarEntradaDouble(origen2.getSaldo(), true, 0, false);

                            boolean retirado = true;
                            if (monto > origen2.getSaldo()) {
                                retirado = false;
                            }

                            if (!retirado) {
                                System.out.println("");
                                System.out.println("");
                                System.err.println("No fue posible retirar");
                                System.out.println("");
                                System.out.println("");
                                return;
                            }
                            origen2.setSaldo(origen2.getSaldo() - monto);
                            destino.setSaldo(destino.getSaldo() + monto);
                            System.out.println("");
                            System.out.println("Nuevo saldo de la cuenta de origen de: " + String.format("%.2f", origen2.getSaldo()));
                            System.out.println("Nuevo saldo de la cuenta de destino de: " + String.format("%.2f", destino.getSaldo()));
                            System.out.println("");
                        } else {
                            System.out.println("");
                            System.out.println("");
                            System.out.println("La cuenta no existe o no contiene dinero");
                            System.out.println("");
                        }

                    }
                }
            }

            case 2 -> {
                Cuenta destino;
                Object origen;
                List<Cuenta> list = new ArrayList<>();
                System.out.println("");
                System.out.println("Ahorros: ");
                bool = Listador.listarAhorros(usuario);
                list.addAll(usuario.getAhorros());

                if (bool) {
                    int opc = validarEntradaInt(list.size(), true, 1, true) - 1;
                    destino = list.get(opc);
                    origen = seleccionarCuentaDeOrigen(usuario, destino);

                    if (origen instanceof Cuenta) {
                        Cuenta origen2 = (Cuenta) origen;
                        if (origen != null && origen2.getSaldo() > 0) {
                            System.out.println("");
                            System.out.println("Ingrese la cantidad a transferir (entre 0 y " + String.format("%.2f", origen2.getSaldo()) + ")");
                            double monto = Verificacion.validarEntradaDouble(origen2.getSaldo(), true, 0, false);

                            boolean retirado = origen2.retirar(monto);

                            if (!retirado) {
                                System.out.println("");
                                System.out.println("");
                                System.err.println("No fue posible retirar");
                                return;
                            }
                            destino.depositar(monto);
                            System.out.println("");
                            System.out.println("Nuevo saldo de la cuenta de origen de: " + String.format("%.2f", origen2.getSaldo()));
                            System.out.println("Nuevo saldo de la cuenta de destino de: " + String.format("%.2f", destino.getSaldo()));
                            System.out.println("");
                        } else {
                            System.out.println("");
                            System.out.println("");
                            System.out.println("La cuenta no existe o no contiene dinero");
                            System.out.println("");
                        }

                    }

                    if (origen instanceof Categoria) {
                        Categoria origen2 = (Categoria) origen;
                        if (origen != null && origen2.getSaldo() > 0) {
                            System.out.println("");
                            System.out.println("Ingrese la cantidad a transferir (entre 0 y " + String.format("%.2f", origen2.getSaldo()) + ")");
                            double monto = Verificacion.validarEntradaDouble(origen2.getSaldo(), true, 0, false);

                            boolean retirado = true;
                            if (monto > origen2.getSaldo()) {
                                retirado = false;
                            }

                            if (!retirado) {
                                System.out.println("");
                                System.out.println("");
                                System.err.println("No fue posible retirar");
                                return;
                            }
                            origen2.setSaldo(origen2.getSaldo() - monto);
                            destino.depositar(monto);
                            System.out.println("");
                            System.out.println("Nuevo saldo de la cuenta de origen de: " + String.format("%.2f", origen2.getSaldo()));
                            System.out.println("Nuevo saldo de la cuenta de destino de: " + String.format("%.2f", destino.getSaldo()));
                            System.out.println("");
                        } else {
                            System.out.println("");
                            System.out.println("");
                            System.out.println("La cuenta no existe o no contiene dinero");
                        }

                    }

                }
            }
        }
    }

    static Object seleccionarCuentaDeOrigen(Usuario usuario, Object destino) {
        boolean repet = false;
        do {
            int option, opc;
            Object origen;
            repet = false;
            System.out.println("¿De donde sale su dinero?");
            System.out.println("1. Bolsillos");
            System.out.println("2. Ahorros");
            System.out.println("3. Volver al inicio");
            System.out.println("");
            option = validarEntradaInt(3, true, 1, true);
            boolean bool = false;

            switch (option) {
                case 1 -> {
                    List<Categoria> list = new ArrayList<>();
                    System.out.println("");
                    System.out.println("Bolsillos: ");
                    bool = listarBolsillos(usuario);

                    for (Categoria bolsillos : Categoria.values()) {
                        list.add(bolsillos);
                    }

                    if (bool) {
                        opc = validarEntradaInt(8, true, 1, true) - 1;
                        origen = list.get(opc);
                        if (origen == destino) {
                            System.out.println("");
                            System.out.println("NO PUEDES ENVIAR EL DINERO AL MISMO LUGAR");
                            repet = true;
                        } else {
                            return origen;
                        }
                    }


                }
                case 2 -> {
                    List<Cuenta> list = new ArrayList<>();
                    System.out.println("");
                    System.out.println("Ahorros: ");
                    bool = Listador.listarAhorros(usuario);
                    list.addAll(usuario.getAhorros());

                    if (bool) {
                        opc = validarEntradaInt(list.size(), true, 1, true) - 1;
                        origen = list.get(opc);
                        if (origen == destino) {
                            System.out.println("");
                            System.out.println("NO PUEDES ENVIAR EL DINERO AL MISMO LUGAR");
                            System.out.println("");
                            repet = true;
                        } else {
                            return origen;
                        }
                    }
                }
            }

        } while (repet);
        return null;
    }

    //OPCION 4
    private static void SacarDinero(Usuario usuario) {
        int option;
        Cuenta destino = null;
        System.out.println("");
        System.out.println("¿Desea hacer?");
        System.out.println("1. Retiro");
        System.out.println("2. Volver al menu");
        System.out.println("");
        option = Verificacion.validarEntradaInt(3, true, 1, true);
        switch (option) {
            case 2:
                return;
        }
        Object origen = seleccionarCuentaDeOrigen(usuario, destino);

        if (origen instanceof Categoria) {
            boolean retirado = true;
            Categoria origen2 = (Categoria) origen;
            if (origen != null && origen2.getSaldo() > 0) {
                System.out.println("");
                System.out.println("Ingrese la cantidad a retirar (entre 0 y " + String.format("%.2f", origen2.getSaldo()) + ")");
                double monto = Verificacion.validarEntradaDouble(origen2.getSaldo(), true, 0, false);
                if (monto > origen2.getSaldo()) {
                    retirado = false;
                }
                if (retirado) {
                    origen2.setSaldo(origen2.getSaldo() - monto);
                    System.out.println("");
                    System.out.println("Retiro Exitoso");
                    System.out.println("Nuevo saldo en " + origen2.name() + " es: " + String.format("%.2f", origen2.getSaldo()));
                    System.out.println("");
                } else {
                    System.out.println("");
                    System.out.println("");
                    System.out.println("Retiro Fallido");
                    System.out.println("");
                }

            } else {
                System.out.println("");
                System.out.println("");
                System.out.println("La cuenta no existe o no contiene dinero");
                System.out.println("");
            }
        }
        if (origen instanceof Cuenta) {
            Cuenta origen2 = (Cuenta) origen;
            boolean retirado = true;
            if (origen != null && origen2.getSaldo() > 0) {
                System.out.println("");
                System.out.println("Ingrese la cantidad a transferir (entre 0 y " + String.format("%.2f", origen2.getSaldo()) + ")");
                double monto = Verificacion.validarEntradaDouble(origen2.getSaldo(), true, 0, false);
                retirado = origen2.retirar(monto);
                if (retirado) {
                    System.out.println("");
                    System.out.println("Retiro Exitoso");
                    System.out.println("Nuevo saldo en " + origen2.getNombre() + " es: " + String.format("%.2f", origen2.getSaldo()));
                    System.out.println("");
                } else {
                    System.out.println("");
                    System.out.println("");
                    System.out.println("Retiro Fallido");
                    System.out.println("");
                }
            } else {
                System.out.println("");
                System.out.println("");
                System.out.println("La cuenta no existe o no contiene dinero");
                System.out.println("");
            }
        }
    }

    //OPCIÓN5
    //Se agrega un colchón al usuario que se seleccionó en el login() con el nombre, la divisa y la fecha de retiro seleccionada por el usuario
    static void agregarAhorro(Usuario usuario) {
        int fecha;
        String nombre;

        System.out.println("");
        System.out.println("Escriba el nombre que desea asignarle al ahorro: ");
        nombre = Verificacion.validarEntradaTexto(true);

        System.out.println("");
        System.out.println("Elija la fecha en que desea liberar el ahorro: ");
        for (int i = 1; i <= 12; i++) {
            System.out.println(i + ". " + LocalDate.now().plusMonths(i));
        }
        System.out.println("");
        fecha = validarEntradaInt(12, true, 1, true);
        Ahorro ahorro = new Ahorro(usuario, nombre, LocalDate.now().plusMonths(fecha));
        usuario.nuevoAhorro(ahorro);

        System.out.println("");
        System.out.println("");
        System.out.println("ahorro " + nombre + " AGREGADO CON EXITO");
        System.out.println("");
        System.out.println("");
    }


    //OPCION 6
    private static void agregarMeta(Usuario usuario) {
        String nombre;
        double objetivo;

        System.out.println("");
        System.out.println("Escriba el nombre que desea asignarle a la meta: ");
        nombre = Verificacion.validarEntradaTexto(true);
        System.out.println("");
        System.out.println("Ingrese el valor objetivo que desea asignarle a la meta (recuerde que no podra sacar el dinero de una meta hasta alcanzar el objetivo): ");
        objetivo = validarEntradaDouble(Double.MAX_VALUE, true, 0, true);
        Meta meta = new Meta(usuario, nombre, LocalDate.now(), objetivo);
        usuario.nuevaMeta(meta);

        System.out.println("");
        System.out.println("");
        System.out.println("Meta Agregada Con Exito");
        System.out.println("");
    }

    //OPCION 7
    //Menú para la eleccion de modificacion, sea bolsillo, colchón o meta, luego se envia la eleccion a la funcion modificar
    static void opcionModificar(Usuario usuario) {
        int opcion, opc;
        System.out.println("");
        System.out.println("¿Que desea modificar?");
        System.out.println("1. Bolsillo");
        System.out.println("2. Ahorro");
        System.out.println("3. Meta");
        System.out.println("4. Volver al inicio");
        System.out.println("");
        opcion = validarEntradaInt(4, true, 1, true);
        boolean bool = false;

        switch (opcion) {
            case 1 -> {
                List<Categoria> list = new ArrayList<>();
                System.out.println("");
                System.out.println("Bolsillos: ");
                bool = Listador.listarBolsillos(usuario);

                for (Categoria bolsillos : Categoria.values()) {
                    list.add(bolsillos);
                }

                if (bool) {
                    opc = validarEntradaInt(list.size(), true, 1, true) - 1;
                    modificar(list.get(opc));
                }
            }
            case 2 -> {
                List<Ahorro> list = new ArrayList<>();
                System.out.println("");
                System.out.println("Ahorros: ");
                bool = Listador.listarAhorros(usuario);
                list.addAll(usuario.getAhorros());

                if (bool) {
                    opc = validarEntradaInt(list.size(), true, 1, true) - 1;
                    modificar(list.get(opc));
                }
            }
            case 3 -> {
                List<Meta> list = new ArrayList<>();
                System.out.println("");
                System.out.println("Metas: ");
                bool = Listador.listarMetas(usuario);
                list.addAll(usuario.getMetas());

                if (bool) {
                    opc = validarEntradaInt(list.size(), true, 1, true) - 1;
                    modificar(usuario, list.get(opc));
                }
            }
        }

    }

    //Condicional para ver que opción se va a modificar segun el usuario
    static void modificar(Usuario usuario, Object x) {
        if (x instanceof Categoria then) {
            modificar(then);
        } else if (x instanceof Ahorro then) {
            modificar(then);
        } else if (x instanceof Meta then) {
            modificar(usuario, then);
        }
    }

    //Menú para modificar saldo o presupuesto de un bolsillo
    static void modificar(Categoria bolsillo) {
        int opcion;
        System.out.println("");
        System.out.println("¿Que desea modificar?");
        System.out.println("1. Presupuesto");
        System.out.println("2. Volver al inicio");
        System.out.println("");
        opcion = validarEntradaInt(2, true, 1, true);

        switch (opcion) {
            case 1:
                System.out.println("");
                System.out.println("Nuevo presupuesto:");
                double nuevoPrusupuesto = Verificacion.validarEntradaDouble(Double.MAX_VALUE, true, 0, false);
                bolsillo.setPresupuesto(nuevoPrusupuesto);
                break;
            case 2:
                return;
        }
        System.out.println("");
        System.out.println("");
        System.out.println("MODIFICACION REALIZADA CON EXITO");
        System.out.println("");
    }

    //Menú para modificar nombre o fecha minima de retiro de un ahorro
    static void modificar(Ahorro colchon) {
        int opcion;
        System.out.println("");
        System.out.println("¿Que desea modificar?");
        System.out.println("1. Nombre");
        System.out.println("2. Cambiar fecha");
        System.out.println("3. Volver al inicio");
        System.out.println("");
        opcion = validarEntradaInt(3, true, 1, true);

        switch (opcion) {
            case 1 -> {
                System.out.println("");
                System.out.println("Nuevo nombre:");
                String nombre = Verificacion.validarEntradaTexto(true);
                colchon.setNombre(nombre);
            }
            case 2 -> {
                System.out.println("");
                System.out.println("Que desea modificar?");
                System.out.println("1. Dias");
                System.out.println("2. Meses");
                System.out.println("3. Años");
                System.out.println("4. Volver al inicio");
                System.out.println("");
                opcion = validarEntradaInt(4, true, 1, true);
                int limite = 0;
                int total = 0;
                switch (opcion) {
                    case 1:
                        limite = 31;
                        break;
                    case 2:
                        limite = 12;
                        break;
                    case 3:
                        limite = 10;
                        break;
                    case 4:
                        return;
                }
                System.out.println("");
                System.out.println("Ingrese la cantidad que desa modificar (entre 1 y " + limite + ")");
                total = Verificacion.validarEntradaInt(limite, true, 1, true);

                System.out.println("");
                System.out.println("¿Aumentar o reducir?");
                System.out.println("1. Aumentar");
                System.out.println("2. Reducir");
                System.out.println("3. Volver al inicio");
                System.out.println("");
                int opcion2 = Verificacion.validarEntradaInt(3, true, 1, true);
                if (opcion2 == 3) {
                    return;
                } else if (opcion2 == 2) {
                    switch (opcion) {
                        case 1 -> colchon.setFechaRetiro(colchon.getFechaRetiro().minusDays(total));
                        case 2 -> colchon.setFechaRetiro(colchon.getFechaRetiro().minusMonths(total));
                        case 3 -> colchon.setFechaRetiro(colchon.getFechaRetiro().minusYears(total));
                    }
                } else {
                    switch (opcion) {
                        case 1 -> colchon.setFechaRetiro(colchon.getFechaRetiro().plusDays(total));
                        case 2 -> colchon.setFechaRetiro(colchon.getFechaRetiro().plusMonths(total));
                        case 3 -> colchon.setFechaRetiro(colchon.getFechaRetiro().plusYears(total));
                    }
                }
            }
