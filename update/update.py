#!/usr/bin/env python3

import pandas as pd

# Funciones

def parse_simple(url, tipo):
    
    df = pd.read_csv(url).rename(columns={'Unnamed: 0': ''}).tail(90)
    df['tipo'] = tipo
    if 'Potosi' in df.columns:
        df = df.rename(columns={'Potosi': 'Potosí'})
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

def aplicacion(vacunas, tipo):
    
    dep_map = {
        'La Paz': 'La Paz',
        'Cochabamba': 'Cochabamba',
        'Santa Cruz': 'Santa Cruz',
        'Oruro': 'Oruro',
        'Potosi': 'Potosí',
        'Tarija': 'Tarija',
        'Chuquisaca': 'Chuquisaca',
        'Beni': 'Beni',
        'Pando': 'Pando'
    }
    
    datos = {}
    for dep in vacunas.columns.get_level_values(0).unique():
        datos[dep] = vacunas[dep][tipo]
    datos = pd.concat(datos, axis=1).tail(91)
    datos.columns = [dep_map[c] for c in datos.columns]
    datos = datos[departamentos].dropna().diff().dropna().astype(int)
    datos['tipo'] = tipo.lower()
    datos = datos.reset_index().rename(columns={'index': ''})
    return datos

# Variables

urls = dict(
    casos = 'https://github.com/sociedatos/covid19-bo-casos_por_departamento/raw/master/confirmados_diarios.csv',
    decesos = 'https://github.com/sociedatos/covid19-bo-casos_por_departamento/raw/master/decesos_diarios.csv',
    positividad = 'https://github.com/sociedatos/covid19-bo-pruebas_por_departamento/raw/master/positividad.csv',
    pruebas = 'https://github.com/sociedatos/covid19-bo-pruebas_por_departamento/raw/master/pruebas.csv',
    hospitalizacion = 'https://github.com/sociedatos/bo-hospitalizados_por_departamento/raw/master/hospitalizados_por_departamento.csv',
    vacunas = 'https://github.com/sociedatos/covid19-bo-vacunas_por_departamento/raw/master/vaccinations.csv'
)

departamentos = ['Chuquisaca', 'La Paz', 'Cochabamba', 'Oruro', 'Potosí', 'Tarija','Santa Cruz', 'Beni', 'Pando']
columnas = [''] + departamentos + ['tipo']

# Datos

casos = parse_simple(urls['casos'], 'casos')
decesos = parse_simple(urls['decesos'], 'decesos')

positividad = parse_simple(urls['positividad'], 'positividad')
positividad[departamentos] = positividad[departamentos] * 100

pruebas = parse_simple(urls['pruebas'], 'pruebas')
pruebas[departamentos] = pruebas[departamentos]

hospitalizacion = pd.read_csv(urls['hospitalizacion'], header=[0,1,2], index_col=[0], skiprows=[3])

internacion = uti = cobertura(hospitalizacion, 'internacion')
uci = cobertura(hospitalizacion, 'uci')
uti = cobertura(hospitalizacion, 'uti')

vacunas = pd.read_csv(urls['vacunas'], header=[0,1], parse_dates=[0], index_col=[0])

primera = aplicacion(vacunas, 'Primera')
segunda = aplicacion(vacunas, 'Segunda')
tercera = aplicacion(vacunas, 'Tercera')
unica = aplicacion(vacunas, 'Unica')

master = pd.concat([
    casos,
    decesos,
    positividad,
    pruebas,
    internacion,
    uci,
    uti,
    primera,
    segunda,
    tercera,
    unica
])
master[''] = pd.to_datetime(master[''])
master = master.dropna()

# Archivo

master.to_csv('docs/master.csv', index=False, float_format="%.2f")
