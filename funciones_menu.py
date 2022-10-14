#ARMADO DE LA FUNCIÓN PRINCIPAL DEL PROYECTO
import graficacion as gf
import db_tickers as db
import conexion_api as ca
import para_fechas as pf
import armado_diccionario as ad 

def ingreso_ticker(api_key):
    existe_ticker = False
    while not existe_ticker:

        ticker = input("Ingrese ticker a pedir:\n")
        existe_ticker = ca.validar_ticker(ticker, api_key)
    return ticker


def agregar_deshabilitado(palabra):
    """Agrega la palabra deshabilitado adelante de una palabra
    """

    return "(deshabilitado) " + palabra


def ingreso_fechas():
    fechas_correctas = False
    while not fechas_correctas:
        fecha_inicio = False
        fecha_fin = False
        while fecha_inicio == False:
            fecha_1 = input("Ingrese fecha de inicio (YYYY-MM-DD):\n")
            fecha_inicio = pf.ingresar_fecha(fecha_1)

        while fecha_fin == False:
            fecha_2 = input("Ingrese fecha de fin (YYYY-MM-DD):\n")
            fecha_fin = pf.ingresar_fecha(fecha_2)

        fechas_correctas = pf.comparar_fechas(fecha_1, fecha_2)
        if not fechas_correctas:
            print("Fecha de fin no puede ser anterior a fecha de inicio\nIngrese nuevamente las fechas:\n ")
    return fecha_1, fecha_2


def menu_principal():

    #Crear base de datos
    con, cur = db.conexion_db()
    
    #Crear tablas
    db.crear_tablas(con, cur)

    #API_KEY
    #Es importante crear una cuenta en 'https://polygon.io/' y dirigirse a
    # 'https://polygon.io/dashboard/api-keys' para generar una nueva API_KEY 
    key_correcta = False


    opcion = ""
    mult = 5
    guiones = "-" * mult
    print(guiones + " Trabajo Final ITBA " + guiones)

    while opcion != "x":
        print("\n\t\tMENÚ PRINCIPAL\n")
        
        #GENERAR AQUÍ LAS OPCIONES CON STRIKE
        opcion_a = "Actualización de datos"
        opcion_b = "Visualización de datos"
        if key_correcta:
            menu = f"\nIngrese una opción.\n\na) {opcion_a}\nb) {opcion_b}\nc) Ingresar clave (API_KEY)\nx) Finalizar\n\n"          
        else:
            menu = f"\nIngrese una opción.\n\na) {agregar_deshabilitado(opcion_a)}\nb) {agregar_deshabilitado(opcion_b)}\nc) Ingresar clave (API_KEY)\nx) Finalizar\n\n"
        
        opcion = input(menu).lower()

        if opcion not in ["a", "b", "c", "x"]:
            print("\Opción incorrecta.\nIntente nuevamente.\n\n")
        else:
            if opcion == "a":
                if key_correcta:
                    print("---- ACTUALIZACIÓN DE DATOS ----\n")

                    #Ingreso y validación del ticker ingresado por el usuario. Consulta a la API si existe un ticker con ese nombre
                    ticker = ingreso_ticker(api_key)

                    #Ingreso y validación de las fechas ingresadas por el usuario
                    fecha_1, fecha_2 = ingreso_fechas()

                    print("\nPidiendo datos...")
                    datos_api = ca.API_solicitar_datos_ticker(ticker, fecha_1, fecha_2, api_key)        #Diccionario

                    if datos_api:
                        datos_api_dicc = ad.crear_diccionario_desde_json(datos_api)
                        db.insertar_datos(datos_api_dicc, cur, con)
                        print("Datos guardados correctamente\n")
                else:
                    print("\nPrimero debe ingresar una API_KEY válida.")

            elif opcion == "b":
                if key_correcta:
                    print("---- VISUALIZACIÓN DE DATOS ----\n\n")
                    opcion_v = ""
                    while opcion_v != "x":
                        opcion_v = input("Ingrese una opción\n\na) Resumen\nb) Gráfico de ticker\nx) Salir\n\n")
                        if opcion_v == "a":                                     #Resumen
                            print("\nPresentando resumen\n")
                            db.informacion_ticker(cur)                          #Muestra un resumen de todos los tickers almacenados en la BBDD

                        elif opcion_v == "b":                                   #Gráfico de velas japonesas

                            ticker = input("Ingrese el ticker a graficar: ")
                            fecha_a, fecha_b = ingreso_fechas()

                            datos = db.consultar_datos(ticker, fecha_a, fecha_b, cur)

                            if datos:
                                datos_para_df = ad.datos_para_dataframe(datos)
                                datos_df =  gf.generar_dataframe(datos_para_df)
                                print("\nPreparando gráfico\n")
                                print("Recuerde cerrar la figura para continuar...\n")
                                gf.graficar_candlesticks(ticker, datos_df)                            
                            else:
                                print("\nNo se hallaron registros en la base de datos.")
                                print(f"\n\tTicker: '{ticker}'\n\tDesde {fecha_a} hasta {fecha_b}\n")
                else:
                    print("\nPrimero debe ingresar una API_KEY correcta")

            elif opcion == "c":
                key_correcta = False
                #Es importante crear una cuenta en 'https://polygon.io/' y dirigirse a
                # 'https://polygon.io/dashboard/api-keys' para generar una nueva API_KEY 

                api_key = input("Ingrese su nueva clave (API_KEY): \n")
                key_correcta = ca.prueba_api_key(api_key)
            else:
                print("Fin del programa.\n")

#No usada
def tachar_palabras(palabra):
    """Toma una palabra y genera la misma con el efecto de tachado.
    No se muestra correctamente en algunos entornos, por lo que omite su uso.
    """
    palabra_tachada = ''
    for c in palabra:
        palabra_tachada = '\u0336' + palabra_tachada + c + '\u0336'
    return palabra_tachada