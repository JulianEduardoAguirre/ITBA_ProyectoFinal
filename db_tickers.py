#FUNCIONES UTILIZADAS PARA INTERACTUAR CON LA BASE DE DATOS LOCAL
import sqlite3

#genera la conexión y regresa el cursor para comunicarse con la misma
def conexion_db():
    '''
    Crea la base de datos "stocks.db", si no existe.
    Si existe, conecta con la BBDD y retorna el cursor a la base de datos
    '''

    nombre_db = "stocks.db"
    con = sqlite3.connect(nombre_db)
    cur = con.cursor()

    return con, cur

#Crea las tablas usadas en el proyecto
def crear_tablas(conexion, cursor):
    '''
    Crea las tablas:
    - ticker: Almacena los nombres de los tickers.
    - datos:  Almacena los datos financieros y la fecha correspondiente.

    Recibe el cursor a la base de datos.
    '''

    sql_tabla_tickers = '''
                        CREATE TABLE IF NOT EXISTS ticker (
                            id INTEGER PRIMARY KEY UNIQUE,
                            nombre TEXT
                        )
                        '''

    sql_tabla_datos = '''
                        CREATE TABLE IF NOT EXISTS datos (
                            id INTEGER PRIMARY KEY,
                            fecha DATE,
                            open FLOAT,
                            close FLOAT,
                            high FLOAT,
                            low FLOAT,
                            ticker_id INTEGER,
                            FOREIGN KEY (ticker_id) REFERENCES ticker(id)
                        )
                        '''

    cursor.execute(sql_tabla_tickers)
    cursor.execute(sql_tabla_datos)
    conexion.commit()

#Permite consultar a la base de datos si existen registros de un determinado ticker
def ticker_consultar_id(ticker, cursor):
    '''
    Consulta si existe un ticker con el nombre correspondiente.
    Si lo encuentra, regresa su id.
    Si no existe, retorna None
    '''
    sql_consultar_existencia = f'''
                    SELECT id
                    FROM ticker
                    WHERE nombre = '{ticker}'
                    ;
                    '''
    cursor.execute(sql_consultar_existencia)

    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]
    else:
        return None
 
#Consulta si existe una entrada de los datos --> Evito insertar duplicados
def datos_consultar_entrada(id_ticker, fecha, cursor):
    '''Consulta si una entrada ya se encuentra en la tabla para un ticker y una fecha dadas.
    Retorna True o False
    '''
    sql_consultar_entrada = f'''
                    SELECT fecha, ticker_id
                    FROM datos
                    WHERE fecha = '{fecha}' AND ticker_id = '{id_ticker}'
                    ;
                    '''
    
    cursor.execute(sql_consultar_entrada)
    resultado = cursor.fetchone()

    if resultado:
        return True
    else:
        return False

#Inserta un ticker en la DDBB. Regresa el valor del id con el que se inserta
def ticker_insertar(ticker, cursor):
    '''
    Recibe el nombre de un ticker y lo inserta en la DDBB.
    Retorna el id con el que se almacena en la DDBB.
    '''

    sql_insertar_ticker = f"""
                        INSERT INTO ticker (nombre)
                        VALUES ('{ticker}')
                        ;
                        """

    cursor.execute(sql_insertar_ticker)

    id_insertado = ticker_consultar_id(ticker, cursor)
    print("id insertado", id_insertado)
    return id_insertado

#Toma un diccionario con todas las entradas consultadas a la API y las inserta en la DDBB
def insertar_datos(mi_dicc, cursor, conexion):
    '''
    Recibe los datos procesados y el cursor de la conexión a la BBDD.
    Inserta los datos financieros del ticker correspondiente en la tabla "datos".
    '''
    nombre_ticker = mi_dicc["ticker"]
    id_ticker = ticker_consultar_id(nombre_ticker, cursor)

    if id_ticker == None:
        id_ticker = ticker_insertar(nombre_ticker, cursor)
    
    lista_resultados = mi_dicc["resultados"]
    
    for elm in lista_resultados:
        fecha = elm["fecha"]
        open = elm["o"]
        close = elm["c"]
        high = elm["h"]
        low = elm["l"]

        if not datos_consultar_entrada(id_ticker, fecha, cursor):
            sql_insertar_datos = f"""
                            INSERT INTO datos (fecha, open, close, high, low, ticker_id)
                            VALUES ('{fecha}', '{open}', '{close}', '{high}', '{low}', '{id_ticker}')
                            ;
                            """
            cursor.execute(sql_insertar_datos)
    
    conexion.commit()

#Consulta los datos de un ticker en particular, para el periodo especificado
def consultar_datos(nombre_ticker, fecha_inicio, fecha_cierre, cursor):
    '''
    Consulta todos los datos de un ticker, para un periodo de tiempo ingresados por el usuario.
    Retorna un diccionario con los datos en caso que la consulta sea correcta. En caso contrario, retorna None
    '''
    
    id = ticker_consultar_id(nombre_ticker, cursor)
    sql_consultar_entrada = f'''
                SELECT fecha, open, close, high, low
                FROM datos
                WHERE ticker_id = '{id}'
                AND fecha BETWEEN '{fecha_inicio}' AND '{fecha_cierre}'
                ORDER BY fecha
                ;
                '''

    cursor.execute(sql_consultar_entrada)
    datos = cursor.fetchall()

    if datos:
        return datos
    else:
        return None

#Generar el renglón como en el enunciado
def informacion_ticker(cursor):
    '''
    Consulta a la base de datos e imprime los datos disponibles.
        Nombre_de_ticker - Fecha_mínima <-> Fecha_máxima
    '''
    
    buscar_info = '''SELECT ticker.nombre, MIN(datos.fecha) AS minimo, MAX(datos.fecha) AS maximo
               FROM ticker
               INNER JOIN datos
               WHERE ticker.id = datos.ticker_id
               GROUP BY ticker.nombre
               ;
               '''

    cursor.execute(buscar_info)
    datos = cursor.fetchall()

    if datos:
        print("{:<6}      {:<10}     {:<10}".format("Ticker", "Desde", "Hasta"))
        for row in datos:
            info = "{:<6} - {:<10} <-> {:<10}".format(row[0], row[1], row[2])
            print(info)
    else:
        print("Sin registros en la base de datos.")
    
    print()


