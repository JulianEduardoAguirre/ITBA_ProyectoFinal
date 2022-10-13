#FUNCIONES NECESARIAS PARA PROCESAR FECHAS
import datetime

def validar_formato_fecha(fecha):
    '''
    Función para comprobar que se ingresó una cadena con formato correcto aaaa/mm/dd
    Retorna True en caso afirmativo.
    '''

    try:
        anio, mes, dia = fecha.split("-")

        if not (int(dia) in range(1, 100) and int(mes) in range(1, 100) and int(anio) in range(1, 10000)):
            #print("Formato de fecha incorrecto")
            return False
        else:
            return True
    except:
        #print("Formato de fecha incorrecto")
        return False


def validar_fecha(fecha):
    '''
    Función para comprobar que una fecha existe en el calendario.
    Recibe una cadena en formato correcto y devuelve un objeto fecha
    '''
    valido = True
    try:
        anio, mes, dia = fecha.split("-")
        datetime.datetime(int(anio), int(mes), int(dia))
    except ValueError:
        valido = False

    return valido


def convertir_a_datetime(fecha):
    '''
    Función que toma la cadena ingresada por el usuario y la convierte en tipo Datetime.
    Necesaria para la función comparar_fechas().
    Retorna un elemento Datetime
    '''
    anio, mes, dia = fecha.split("-")
    return datetime.datetime(int(anio), int(mes), int(dia))


def comparar_fechas(fecha1, fecha2):
    '''
    Función que compara dos fechas.
    Retorna true si la segunda fecha es mayor o igual que la primera.
    '''
    fecha_1 = convertir_a_datetime(fecha1)
    fecha_2 = convertir_a_datetime(fecha2)

    return fecha_2 >= fecha_1


def ingresar_fecha(fecha):
    '''
    Función para ingresar una fecha por teclado.
    Pide al usuario que ingrese por teclado una fecha en un formato específico.
    Realiza validación de formato y de validez de la fecha ingresada.
    En caso válido, retorna True
    '''

    #fecha = input("Ingrese una fecha (AAAA/MM/DD): ")

    if validar_formato_fecha(fecha):
        if validar_fecha(fecha):
            print("Fecha válida.\n")
            #fecha_return = convertir_a_datetime(fecha)
            #print(fecha_return)
            #return fecha_return
            return True
        else:
            print("La fecha ingresada no es correcta")
            return False
    else:
        print("Formato incorrecto")
        return False




#FUNCIONES NO UTILIZADAS
def datetime_a_string(fecha):
    '''
    Toma un objeto datetime y lo convierte en un string con el formato correcto para consultar a la API
    '''

    return "{0:0>4}-{1:0>2}-{2:0>2}".format((fecha.year), (fecha.month), (fecha.day)) 
