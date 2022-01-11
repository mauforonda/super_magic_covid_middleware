#!/usr/bin/env python3

import pandas as pd

# Funciones

def parse_simple(url, tipo):
    
    df = pd.read_csv(url).rename(columns={'Unnamed: 0': ''}).tail(90)
    df['tipo'] = tipo
    return df[columnas]

def cobertura(hospitalizacion, tipo):
    
    dep_map = {
        'beni': 'Beni',
        'chuquisaca': 'Chuquisaca',
        'cochabamba': 'Cochabamba',
        'la paz': 'La Paz',
        'oruro': 'Oruro',
        'pando': 'Pando',
        'potosi': 'Potosí',
        'santa cruz': 'Santa Cruz',
        'tarija': 'Tarija'
    }
    
    datos = {}
    for dep in hospitalizacion.columns.get_level_values(0).unique():
        datos[dep] = (hospitalizacion[dep]['hospitalizados'][tipo] / hospitalizacion[dep]['camas_habilitadas'][tipo])
    datos = pd.concat(datos, axis=1).tail(90) * 100
    datos.columns = [dep_map[c] for c in datos.columns]
    datos = datos[departamentos]
    datos['tipo'] = tipo
    datos = datos.reset_index().rename(columns={'index': ''})
    return datos

# Variables

urls = dict(
    casos = 'https://github.com/mauforonda/covid19-bolivia-udape/raw/master/confirmados_diarios.csv',
    decesos = 'https://github.com/mauforonda/covid19-bolivia-udape/raw/master/decesos_diarios.csv',
    positividad = 'https://github.com/dquintani/covid/raw/main/positividad_diaria_ajuste.csv',
    pruebas = 'https://github.com/dquintani/covid/raw/main/pruebas_diarias.csv',
    hospitalizacion = 'https://github.com/pr0nstar/covid19-data/raw/master/processed/bolivia/hospitalizations.csv'
)

departamentos = ['Chuquisaca', 'La Paz', 'Cochabamba', 'Oruro', 'Potosí', 'Tarija','Santa Cruz', 'Beni', 'Pando']
columnas = [''] + departamentos + ['tipo']

# Datos

casos = parse_simple(urls['casos'], 'casos')
decesos = parse_simple(urls['decesos'], 'decesos')

positividad = parse_simple(urls['positividad'], 'positividad')
positividad[departamentos] = positividad[departamentos] * 100

pruebas = parse_simple(urls['pruebas'], 'pruebas')
pruebas[departamentos] = pruebas[departamentos].astype(int)

hospitalizacion = pd.read_csv(urls['hospitalizacion'], header=[0,1,2], index_col=[0], skiprows=[3])

internacion = uti = cobertura(hospitalizacion, 'internacion')
uci = cobertura(hospitalizacion, 'uci')
uti = cobertura(hospitalizacion, 'uti')

master = pd.concat([
    casos,
    decesos,
    positividad,
    pruebas,
    internacion,
    uci,
    uti
])

# Archivo

master.to_csv('docs/master.csv', index=False, float_format="%.2f")
