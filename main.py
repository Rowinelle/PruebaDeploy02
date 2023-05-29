import pandas as pd
import unicodedata
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()


dtypes = {'popularity' : object, 'overview' : object}


data = pd.read_csv(r'C:\Users\romin\Documents\PROGRAMACION\CIENCIA DE DATOS\HENRY\LABS\PI MLops\repo\dsets\FINALdata_movies_modif.csv', parse_dates = ['release_date'], dtype = dtypes)


def trad_fechas(dato):
    diames_norm = unicodedata.normalize('NFD', dato)
    diames_norm = diames_norm.encode('ascii', 'ignore').decode('utf-8')
    diames_norm = diames_norm.lower()
    if diames_norm == 'lunes':
        return 'Monday'
    elif diames_norm == 'martes':
        return 'Tuesday'
    elif diames_norm == 'miercoles':
        return 'Wednesday'
    elif diames_norm == 'jueves':
        return 'Thursday'
    elif diames_norm == 'viernes':
        return 'Friday'
    elif diames_norm == 'sabado':
        return 'Saturday'
    elif diames_norm == 'domingo':
        return 'Sunday'
    elif diames_norm == 'enero':
        return 'January'
    elif diames_norm == 'febrero':
        return 'February'
    elif diames_norm == 'marzo':
        return 'March'
    elif diames_norm == 'abril':
        return 'April'
    elif diames_norm == 'mayo':
        return 'May'
    elif diames_norm == 'junio':
        return 'June'
    elif diames_norm == 'julio':
        return 'July'
    elif diames_norm == 'agosto':
        return 'August'
    elif diames_norm == 'septiembre':
        return 'September'
    elif diames_norm == 'octubre':
        return 'October'
    elif diames_norm == 'noviembre':
        return 'November'
    elif diames_norm == 'diciembre':
        return 'December'
    



@app.get('/')
def nombre():
    return {'mascota':'Danita'}



@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes:str):
    mes_num = datetime.strptime(trad_fechas(mes), "%B").month
    pelxmes = data[data['release_date'].dt.month == mes_num]
    cantidadmes = len(pelxmes)
    return {'mes' : mes, 'cantidad': cantidadmes}