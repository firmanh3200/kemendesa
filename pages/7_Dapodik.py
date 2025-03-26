import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
#import html5lib
import lxml

st.set_page_config(layout='wide')

# Ambil tanggal hari ini
tanggal_hari_ini = datetime.now().strftime("%d-%m-%Y")

with st.container(border=True):
    with st.container(border=True):
        st.header("Direktori Pendidikan - Dapodik")
        st.warning(f"Sumber: referensi.data.kemdikbud.go.id, Kondisi: {tanggal_hari_ini}")

kodapodik = pd.read_csv('data/kodedapodik.csv', dtype={'namakab':'str', 'namakec':'str','idkec':'str'}, sep=';', encoding='utf-8')

pilihankab = kodapodik['namakab'].unique()
with st.container(border=True):
    kol1, kol2 = st.columns(2)
    with kol1:
        kabterpilih = st.selectbox('Pilih Kabupaten/Kota', pilihankab)
    with kol2:
        pilihankec = kodapodik[kodapodik['namakab'] == kabterpilih]['namakec'].unique()
        kecterpilih = st.selectbox('Pilih Kecamatan', pilihankec)
    
if kabterpilih and kecterpilih:
    st.subheader(f'Fasilitas Pendidikan di Kecamatan {kecterpilih}, {kabterpilih}')
    
    idkec = kodapodik[(kodapodik['namakab'] == kabterpilih) & (kodapodik['namakec'] == kecterpilih)]['idkec'].iloc[0]    
    with st.expander("PAUD"):
        
        # Ambil data dari URL
        url1 = f"https://referensi.data.kemdikbud.go.id/pendidikan/paud/{idkec}/3"
        response1 = requests.get(url1)
        soup1 = BeautifulSoup(response1.content, 'html.parser')

        # Temukan tabel dalam HTML
        table1 = soup1.find('table')
        df1 = pd.read_html(str(table1))[0]
        df1['NPSN'] = df1['NPSN'].astype(str)
        
        st.dataframe(df1, use_container_width=True, hide_index=True)
        
    with st.expander("Pendidikan Dasar"):
        # Ambil data dari URL
        url2 = f"https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/{idkec}/3"
        response2 = requests.get(url2)
        soup2 = BeautifulSoup(response2.content, 'html.parser')

        # Temukan tabel dalam HTML
        table2 = soup2.find('table')
        df2 = pd.read_html(str(table2))[0]
        df2['NPSN'] = df2['NPSN'].astype(str)
        
        st.dataframe(df2, use_container_width=True, hide_index=True)
        
    with st.expander("Pendidikan Menengah"):
        # Ambil data dari URL
        url3 = f"https://referensi.data.kemdikbud.go.id/pendidikan/dikmen/{idkec}/3"
        response3 = requests.get(url3)
        soup3 = BeautifulSoup(response3.content, 'html.parser')

        # Temukan tabel dalam HTML
        table3 = soup3.find('table')
        df3 = pd.read_html(str(table3))[0]
        df3['NPSN'] = df3['NPSN'].astype(str)
        
        st.dataframe(df3, use_container_width=True, hide_index=True)
    
    with st.expander("Pendidikan Masyarakat"):
        # Ambil data dari URL
        url4 = f"https://referensi.data.kemdikbud.go.id/pendidikan/dikmas/{idkec}/3"
        response4 = requests.get(url4)
        soup4 = BeautifulSoup(response4.content, 'html.parser')

        # Temukan tabel dalam HTML
        table4 = soup4.find('table')
        df4 = pd.read_html(str(table4))[0]
        
        st.dataframe(df4, use_container_width=True, hide_index=True)
        
    with st.expander("Yayasan Pendidikan"):
        # Ambil data dari URL
        url5 = f"https://referensi.data.kemdikbud.go.id/pendidikan/yayasan/{idkec}/3"
        response5 = requests.get(url5)
        soup5 = BeautifulSoup(response5.content, 'html.parser')

        # Temukan tabel dalam HTML
        table5 = soup5.find('table')
        df5 = pd.read_html(str(table5))[0]
        
        st.dataframe(df5, use_container_width=True, hide_index=True)
        
    with st.expander("Cagar Budaya"):
        # Ambil data dari URL
        url6 = f"https://referensi.data.kemdikbud.go.id/kebudayaan/cagarbudaya/{idkec}/3"
        response6 = requests.get(url6)
        soup6 = BeautifulSoup(response6.content, 'html.parser')

        # Temukan tabel dalam HTML
        table6 = soup6.find('table')
        df6 = pd.read_html(str(table6))[0]
        
        st.dataframe(df6, use_container_width=True, hide_index=True)
            
    with st.expander("Pendidikan Tinggi"):
        # Ambil data dari URL
        url7 = f"https://referensi.data.kemdikbud.go.id/pendidikan/dikti/{idkec}/3"
        response7 = requests.get(url7)
        soup7 = BeautifulSoup(response7.content, 'html.parser')   #  or 'lxml'
        
        table7 = soup7.find('table')
        df7 = pd.read_html(str(table7))[0]
        st.dataframe(df7, use_container_width=True, hide_index=True)
        
