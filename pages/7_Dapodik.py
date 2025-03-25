import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Ambil tanggal hari ini
tanggal_hari_ini = datetime.now().strftime("%d-%m-%Y")

st.header("Direktori Pendidikan - Dapodik")
st.warning(f"Sumber: referensi.data.kemdikbud.go.id, Kondisi: {tanggal_hari_ini}")

with st.expander("PAUD"):
    # Ambil data dari URL
    url = f"https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/020000/1/all/all/all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Temukan tabel dalam HTML
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
with st.expander("Pendidikan Dasar"):
    # Ambil data dari URL
    url = f"https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/020000/1/all/all/all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Temukan tabel dalam HTML
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
with st.expander("Pendidikan Menengah"):
    # Ambil data dari URL
    url = f"https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/020000/1/all/all/all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Temukan tabel dalam HTML
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
with st.expander("Pendidikan Tinggi"):
    # Ambil data dari URL
    url = f"https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/020000/1/all/all/all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Temukan tabel dalam HTML
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
with st.expander("Pendidikan Masyarakat"):
    # Ambil data dari URL
    url = f"https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/020000/1/all/all/all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Temukan tabel dalam HTML
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
with st.expander("Yayasan Pendidikan"):
    # Ambil data dari URL
    url = f"https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/020000/1/all/all/all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Temukan tabel dalam HTML
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
with st.expander("Cagar Budaya"):
    # Ambil data dari URL
    url = f"https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/020000/1/all/all/all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Temukan tabel dalam HTML
    table = soup.find('table')
    df = pd.read_html(str(table))[0]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
