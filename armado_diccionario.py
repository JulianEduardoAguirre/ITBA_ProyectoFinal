import json
import datetime
        

def crear_diccionario_desde_json(datos):
    '''
    Genera un diccionario en Python con el formato de datos de la API.
    Claves: 
        Ticker:         Almacena el nombre del ticker
        Resultados:     Lista de diccionarios con los datos financieros de la empresa.

    Retorna el diccionario.
    '''
    
    #datos = json.load(datos_json)

    if datos["count"] < 1:
        print("Archivo sin registros.")
        return None
    else:
        #print("Registros encontrados {}".format(datos["count"]))
        nuevos_datos = {
                "ticker": datos["ticker"]
        }
        
        resultados = []

        for elemento in datos["results"]:
            un_diccionario = {
                "fecha": str(datetime.datetime.fromtimestamp(elemento["t"]/1000))[:10],
                "o": elemento["o"],
                "c": elemento["c"],
                "h": elemento["h"],
                "l": elemento["l"]
            }
            resultados.append(un_diccionario)

        nuevos_datos["resultados"] = resultados
        return nuevos_datos


def datos_para_dataframe(datos_ddbb):
    '''
    Convierte los datos obtenidos desde la base de datos 
    en un diccionario de listas.
    '''
    fecha = []
    open = []
    close = []
    high = []
    low = []

    for elemento in datos_ddbb:
        fecha.append(elemento[0])
        open.append(elemento[1])
        close.append(elemento[2])
        high.append(elemento[3])
        low.append(elemento[4])

    diccionario_datos = {
        "fecha": fecha,
        "open": open,
        "close": close,
        "high": high,
        "low": low
    }
    
    return diccionario_datos


#Para pruebas locales
def extraer_datos_archivo(nombre_archivo):
    '''
    Función para leer un archivo JSON
    Retorna datos.
    '''
    
    try:
        archivo = open(nombre_archivo)
        datos = json.load(archivo)
        archivo.close
        return datos
    except:
        print("Error al abrir el archivo.")