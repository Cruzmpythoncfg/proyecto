import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Proyecto Python CFG",
    page_icon="🏗",
    layout="wide",
    initial_sidebar_state="expanded",
    )

def load_data():
    # Carga de los Archivos
    gdf = gpd.read_file('Estados_Venezuela.shp')
    cdf = pd.read_excel('casos.xlsx', usecols= ['Caso', 'Creado en', 'Transmisor/Nombre', 'Estatus', 'Transmisor/Provincia/Nombre provincia', 'Categoría/Nombre de categoría', 'Mensaje/Contenido']) #
    pdf = pd.read_excel('proyectos.xlsx')

    # Limpieza de los archivos
    cdf = cdf.rename(columns={'Transmisor/Provincia/Nombre provincia':'ESTADO'})
    pdf = pdf.rename(columns={'Organización/Provincia/Nombre provincia':'ESTADO'})

    # Union de los archivos
    mdf = gdf.merge(cdf, on='ESTADO')
    mdf = mdf.sort_values(by='Caso')
    mdf = mdf.reset_index(drop=True)
    return gdf, cdf, pdf, mdf

gdf, cdf, pdf, mdf = load_data()


def main():
    titulo, cerrar = st.columns([0.8, 0.2])
    with titulo:
        st.title("Sistema de Consulta de Organizaciones")
        st.markdown(
            """
            #### Elaborado por: Cruz David Mata
            *Oficina de Atención Ciudadana*\n
            *Fondo de Compensación Interterritorial*\n
            *Consejo Federal de Gobierno*
            """
        )
    with cerrar:
        st.image("logo.svg", width=250)
 
    st.write("# Bienvenido al sistema")
    Inicio, organizaciones, analisis = st.tabs(["Inicio", "Consulta de Organización", "Analisis Exploratorio"])
    with Inicio:
        general()
    with organizaciones:
        consulta()
    with analisis: 
        detallado()

@st.cache_data
def general():
    mapa, datos = st.columns([0.7, 0.3])
    with mapa:
        st.title('Mapa de Venezuela')
        fig, ax = plt.subplots()
        gdf.plot(column='ESTADO', ax=ax, figsize=(10, 10), cmap='Dark2', legend=False) 
        st.pyplot(fig)
    with datos:
        st.title('Casos por estado')
        st.write(mdf['ESTADO'].value_counts())
        
def detallado():
    casos, proyectos = st.columns(2)
    with casos:
        st.title('Casos Recibidos')
        casos = cdf['Caso'].value_counts()
        c_describe, c_dtypes = st.columns([0.4, 0.6])
        with c_describe:
            st.write("describe()")
            st.write(casos.describe())
        st.write(cdf.info())
        with c_dtypes:
            st.write("dtypes()")
            st.write(cdf.dtypes)
        st.write(cdf.head(8))
    with proyectos:
        st.title('Proyectos Registrados')
        p_describe, p_dtypes = st.columns([0.4, 0.6])
        with p_describe:
            st.write("describe()")
            st.write(pdf.describe())
        st.write(pdf.info())
        with p_dtypes:
            st.write("dtypes()")
            st.write(pdf.dtypes)
        st.write(pdf.head())


def consulta():
    cod, info = st.columns([0.3, 0.7])
    with cod:
        codigo = st.text_input("# Codigo de organización")
    with info:
        if codigo != "":
            pdf_process = pdf.loc[(pdf["Organización/Código"]==codigo), ]
            st.title("Información de la Organización")
            try:
                st.write(f"Nombre de la Organización: {pdf.loc[pdf['Organización/Código'] == codigo]['Organización/Nombre'].values[0]}")
                st.write(f"Código de la Organización: {pdf.loc[pdf['Organización/Código'] == codigo]['Organización/Código'].values[0]}")
                st.write(f"Estado de Ubicación: {pdf.loc[pdf['Organización/Código'] == codigo]['ESTADO'].values[0]}")
                st.write(f"Parroquia de Ubicación: {pdf.loc[pdf['Organización/Código'] == codigo]['Organización/Parroquia/Parroquia'].values[0]}")
            except IndexError:
                st.write("No se encontró la Organización") 

    try:
        obpp = pdf.loc[pdf['Organización/Código'] == codigo]['Organización/Nombre'].values[0]
    except IndexError:
        obpp = "No se encontró la Organización"
    cdf_process = cdf.loc[(cdf["Transmisor/Nombre"]==obpp), ]
    if obpp != "No se encontró la Organización":
        st.title('Proyectos Registrados por la Organización')
        st.write(pdf_process)
        st.title('Casos enviados por la Organización')
        st.write(cdf_process)



if __name__ == "__main__":
    main()
