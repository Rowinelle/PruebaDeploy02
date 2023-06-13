import pandas as pd
import numpy as np
import unicodedata
from datetime import datetime
from fastapi import FastAPI
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI()

fecha = pd.read_csv('datasets/peliculas_por_estreno.csv', parse_dates = ['release_date'])
popularidad = pd.read_csv('datasets/peliculas_por_popularidad.csv')
votos = pd.read_csv('datasets/peliculas_por_votos.csv')
actores = pd.read_csv('datasets/peliculas_por_actor.csv')
directores = pd.read_csv('datasets/peliculas_por_director.csv', parse_dates=['release_date'])

#dtypes = {'popularity' : object, 'overview' : object}
#data = pd.read_csv('dsets/FINALdata_movies_modif.csv', parse_dates = ['release_date'], dtype = dtypes)


#normalizo dias y meses
def trad_fechas(dato):
    diames_norm = unicodedata.normalize('NFD', dato)
    diames_norm = diames_norm.encode('ascii', 'ignore').decode('utf-8')
    diames_norm = diames_norm.lower()

    mapping = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miercoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sabado': 'Saturday',
        'domingo': 'Sunday',
        'enero': 'January',
        'febrero': 'February',
        'marzo': 'March',
        'abril': 'April',
        'mayo': 'May',
        'junio': 'June',
        'julio': 'July',
        'agosto': 'August',
        'septiembre': 'September',
        'octubre': 'October',
        'noviembre': 'November',
        'diciembre': 'December',
    }
    return mapping.get(diames_norm, diames_norm)


#desarrollo de las funciones
@app.get('/')
def nombre():
    return {'comienzo':'Bienvenida'}


@app.get("/peliculas_mes/{mes}")
def cantidad_filmaciones_mes(mes:str):
    mes_num = datetime.strptime(trad_fechas(mes), "%B").month
    pel_mes = fecha[fecha['release_date'].dt.month == mes_num]
    cantidad = len(pel_mes)
    return ('{} películas fueron estrenadas en el mes de {}'.format(cantidad, mes))


@app.get("/peliculas_dia/{dia}")
def cantidad_filmaciones_dia(dia:str):
    dia_tr = trad_fechas(dia)
    pel_dia = fecha[fecha['release_date'].dt.strftime('%A') == dia_tr] 
    cantidaddia = len(pel_dia)
    return ('{} películas fueron estrenadas en los días {}'.format(cantidaddia, dia))


@app.get("/puntuacion_pelicula/{pelicula}")
def score_titulo(pelicula: str):
    filtro = popularidad['title'] == pelicula
    score = popularidad.loc[filtro, 'popularity'].values[0] if filtro.any() else None
    año = popularidad.loc[filtro, 'release_year'].values[0] if filtro.any() else None
    return ('La película {} fue estrenada en el año {} con un score de {}'.format(pelicula, año, round(score, 2)))


@app.get("/votos_pelicula/{pelicula}")
def votos_titulo(pelicula: str):
    filtro = (votos['title'] == pelicula) 
    df_filtrado = votos.loc[filtro].sort_values('vote_count', ascending=False)
    vote_count = df_filtrado.iloc[0]['vote_count']
    if vote_count < 2000:
        return 'La película {} no cuenta con puntajes suficientes.'.format(pelicula)
    total_votos = df_filtrado.iloc[0]['vote_count']
    promedio = df_filtrado.iloc[0]['vote_average']
    año = df_filtrado.iloc[0]['release_year']
    return ('La película {} fue estrenada en el año {}. La misma cuenta con un total de {} valoraciones, con un promedio de {}'.format(pelicula, año, total_votos, promedio))



@app.get("/actor/{actor}")
def get_actor(actor: str):
    cantidad = actores['cast'].apply(lambda x: actor in x).sum()
    retorno = actores.loc[actores['cast'].apply(lambda x: actor in x), 'return'].sum()
    promedio = actores.loc[actores['cast'].apply(lambda x: actor in x), 'return'].mean()
    return ('El actor {} ha participado de {} de filmaciones, el mismo ha conseguido un retorno de {}, con un promedio de {} por filmación'. format(actor, cantidad, round(retorno,2), round(promedio,2)))


@app.get("/director/{nombre_director}")
def get_director(nombre_director: str):
    df_filtrado = directores[directores['crew'].apply(lambda x: nombre_director in x)][['title', 'release_date', 'release_year','return', 'budget', 'revenue']]
    peliculas = df_filtrado['title']
    df_filtrado['budget'] = df_filtrado['budget'].apply(lambda x: str(x))
    año = df_filtrado['release_year'].apply(lambda x: str(x))
    retorno_pelicula = df_filtrado['return']
    budget_pelicula = df_filtrado['budget']
    revenue_pelicula = df_filtrado['revenue']
    retorno = df_filtrado['return'].sum()
    return {'director': nombre_director, 'retorno total': retorno, 'peliculas': peliculas, 'año': año, 'budget': budget_pelicula, 'retorno': retorno_pelicula, 'revenue': revenue_pelicula}
