import pandas as pd
import matplotlib.pyplot as plt

def generar_dataframe(datos_df):
    '''
    Genera un dataframe con los datos del diccionario obtenido con la función
    '''
    mi_dataframe = pd.DataFrame({'open': datos_df["open"],
                       'close': datos_df["close"],
                       'high': datos_df["high"],
                       'low': datos_df["low"]},
                       index = datos_df["fecha"])
    
    return mi_dataframe


def graficar_candlesticks(ticker, datos_dataframe):
    '''
    Realiza el gráfico de velas japonesas con los datos recibidos.
    '''

    #Crear figura
    plt.figure()

    #Parámetros
    width = .4
    width2 = .05
    col1 = "green"
    col2 = "red"

    for i, dia in enumerate(datos_dataframe.index):

        if (datos_dataframe.close[i] >= datos_dataframe.open[i]):
            col = col1
        else:
            col = col2

        plt.bar(datos_dataframe.index[i], datos_dataframe.close[i] - datos_dataframe.open[i] , width, bottom = datos_dataframe.open[i] ,color = col)
        plt.bar(datos_dataframe.index[i], datos_dataframe.high[i] - datos_dataframe.close[i] , width2, bottom = datos_dataframe.close[i], color = col)
        plt.bar(datos_dataframe.index[i], datos_dataframe.low[i] - datos_dataframe.open[i], width2, bottom = datos_dataframe.open[i], color = col)

    plt.title(ticker)
    plt.xticks(rotation=45, ha='right')
    plt.show()
