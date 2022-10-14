#FUNCIONES PARA REALIZAR LOS PEDIDOS A LA API
import requests as rs


def validar_ticker(ticker, api_key):
    '''
    Consulta a la API si existe un ticker de nombre ingresado por el usuario.
    Retorna True en caso que exista el ticker en la API
    '''
    if ticker != "":

        url_ticker = f"https://api.polygon.io/v3/reference/tickers?ticker={ticker}&type=CS&market=stocks&active=true&sort=ticker&order=asc&limit=10&apiKey={api_key}"
        resultado = rs.get(url_ticker).json()

        if resultado.get('count', -1) != -1:
            print("Ticker correcto\n")
            return True
        else:
            print("Ticker inexistente o mal escrito\n")
            return False
    else:
        print("Debe ingresar un ticker\n")
        return False


def API_solicitar_datos_ticker(ticker, fecha_inicio, fecha_cierre, api_key):
    '''
    Realiza el pedido de datos a la API
    Recibe por parametros: nombre del ticker, fechas (inicio y cierre) junto a la API_key.
    Retorna los datos del ticker

    {
    "ticker": "AAPL",
    "queryCount": 28,
    "resultsCount": 28,
    "adjusted": true,
    "results": [
                    {
                        "v": 77287356.0,
                        "vw": 146.991,
                        "o": 145.935,
                        "c": 146.8,
                        "h": 148.195,
                        "l": 145.81,
                        "t": 1626926400000,
                        "n": 480209
                    },
                    {
                        "v": Volumen de transacciones
                        "vw": Volumen de transacciones (pesado)
                        "o": Precio de apertura
                        "c": Precio de cierre
                        "h": Precio máximo en el período
                        "l": Precio mínimo en el período
                        "t": Unix Msec timestamp
                        "n": Número de transacciones en el período
                    }
                ]
        }
    '''
    #Datos para el armado del request
    limit = "500"                   #5000 - 50000
    multiplicador = "1"             #Multiplica la escala de tiempo
    escala_de_tiempo = "day"        #segundo-hora-dia-semana-mes-semestre-año
    orden = "asc"

    api_url_barras = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplicador}/{escala_de_tiempo}/{fecha_inicio}/{fecha_cierre}?adjusted=true&sort={orden}&limit={limit}&apiKey={api_key}"

    resultado = rs.get(api_url_barras).json()


    if resultado.get('count', -1) != -1:
        print("Consulta exitosa\n")
        print(f"Resultados encontrados: {resultado['count']}\n")
        return resultado
    else:
        print("No se encontraron registros\n")
        return None


def prueba_api_key(api_key):
    url = f"https://api.polygon.io/v3/reference/tickers?ticker=AAPL&type=CS&market=stocks&active=true&sort=ticker&order=asc&limit=10&apiKey={api_key}"

    valor = rs.get(url).json()
    if valor.get("error", '-1') == "Unknown API Key":
        print("\nAPI_KEY Incorrecta")
        print("Debe dirigirse a 'https://polygon.io/stocks' para generar una nueva.\n")
        #Es importante crear una cuenta en 'https://polygon.io/' y dirigirse a
        # 'https://polygon.io/dashboard/api-keys' para generar una nueva API_KEY 
        return False
    else:
        print("\nAPI_KEY correcta")
        return True
