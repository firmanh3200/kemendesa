import streamlit as st
import pandas as pd
import requests
from data import mfd_2025

# --- Configuration ---
st.set_page_config(page_title="SDGs Desa", page_icon=":earth_americas:", layout="wide")

faskes = {
    "d1": "RUMAH SAKIT",
    "d2": "RUMAH SAKIT BERSALIN",
    "d3": "PUSKESMAS DENGAN RAWAT INAP",
    "d4": "PUSKESMAS TANPA RAWAT INAP",
    "d5": "PUSKESMAS PEMBANTU",
    "d6": "POLIKLINIK / BALAI PENGOBATAN",
    "d7": "TEMPAT PRAKTIK DOKTER",
    "d8": "RUMAH BERSALIN",
    "d9": "TEMPAT PRAKTIK BIDAN",
    "d10": "POSKESDES",
    "d11": "POLINDES",
    "d12": "APOTIK",
    "d13": "TOKO KHUSUS OBAT / JAMU",
    "d14": "POSYANDU",
    "d15": "POSBINDU",
    "d16": "TEMPAT PRAKTIK DUKUN BAYI / BERSALIN / PRARAJI"
}

# --- Streamlit App ---
with st.container(border=True):
    with st.container(border=True):
        st.title(":blue[Data Kesehatan Desa]")
        st.caption('Sumber: https://sid.kemendesa.go.id/profile')
        kol1, kol2, kol3 = st.columns(3)
        with kol1:
            kabkot = mfd_2025['idkab'].unique().tolist()
            kabterpilih1 = st.selectbox("Filter IDKAB", kabkot, key='kabkot1')
        with kol2:
            kec = mfd_2025[mfd_2025['idkab'] == kabterpilih1]['idkec'].unique().tolist()
            kecterpilih1 = st.selectbox("Filter IDKEC", kec, key='kec1')
        with kol3:
            desa = mfd_2025[mfd_2025['idkec'] == kecterpilih1]['iddesa'].unique().tolist()
            desaterpilih = st.selectbox("Filter IDDESA", desa, key='desa1')

        # --- API Configuration (Keep this configurable) ---
        if kol1 and kol2 and kol3:
            from data import mfd_2025_cantik
            # Filter the infodesa DataFrame correctly
            infodesa = mfd_2025_cantik[mfd_2025_cantik['iddesa'] == desaterpilih]

            # Check if infodesa is empty
            if infodesa.empty:
                st.warning("Data desa tidak ditemukan.  Periksa kembali IDDESA.")
            else:
                api_url = f"https://sid.kemendesa.go.id/profile/data_analisis_sdgs?location_code=&village_id={desaterpilih}&on=tvpov"

                response = requests.get(api_url)
                data = response.json()

                # --- Data Processing ---
                df = pd.DataFrame([data['data']])

                # --- Gabungkan Data (Jika Data Tersedia) ---
                if df is not None and not df.empty:
                    # 1. Transpose df dan reset index
                    df_transposed = df.T.reset_index()
                    df_transposed.columns = ['index', 'Jumlah']  # Rename columns

                    # 2. Buat DataFrame dari dictionary faskes
                    df_faskes = pd.DataFrame.from_dict(faskes, orient='index', columns=['Fasilitas Kesehatan'])
                    df_faskes.index.name = 'index' #Memberi nama index

                    # 3. Gabungkan kedua DataFrame
                    df_gabung = pd.merge(df_faskes, df_transposed, left_index=True, right_on='index', how='inner')
                    df_gabung = df_gabung.set_index('index') #Set index
                    
                    with st.container(border=True):
                        st.subheader(f"Jumlah Kunjungan ke Fasilitas Kesehatan (Kali) di ")
                        st.subheader(f":orange[DESA {infodesa['nmdesa'].iloc[0]}], :green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
                        st.dataframe(df_gabung) # Tampilkan DataFrame yang digabungkan

                else:
                    st.warning("Tidak tersedia.")
penyakit = {
    "d1_1":	"MUNTABER/DIARE",
    "d2_1":	"DEMAM BERDARAH",
    "d3_1":	"CAMPAK",
    "d4_1":	"MALARIA",
    "d5_1":	"FLU BURUNG / SARS",
    "d6_1":	"COVID-19",
    "d7_1":	"HEPATITIS B",
    "d8_1":	"HEPATITIS E",
    "d9_1":	"DIFTERI",
    "d10_1":	"CHIKUNGUNYA",
    "d11_1":	"LEPTOSPIROSIS",
    "d12_1":	"KOLERA",
    "d14_1":	"JANTUNG",
    "d15_1":	"TBC PARU - PARU",
    "d16_1":	"KANKER",
    "d17_1":	"DIABETES / KENCING MANIS / GULA",
    "d18_1":	"LUMPUH",
    "d19_1":	"LAINNYA"
}                    
with st.expander('Jenis Penyakit'):
    url1 = f"https://sid.kemendesa.go.id/profile/data_analisis_sdgs?location_code=&village_id={desaterpilih}&on=tdav"

    response1 = requests.get(url1)
    data1 = response1.json()

    # --- Data Processing ---
    df1 = pd.DataFrame([data1['data']])

    # --- Gabungkan Data (Jika Data Tersedia) ---
    if df1 is not None and not df.empty:
        # 1. Transpose df dan reset index
        df_transposed = df1.T.reset_index()
        df_transposed.columns = ['index', 'Jumlah Penderita']  # Rename columns

        # 2. Buat DataFrame dari dictionary faskes
        df_penyakit = pd.DataFrame.from_dict(penyakit, orient='index', columns=['Jenis Penyakit'])
        df_penyakit.index.name = 'index' #Memberi nama index

        # 3. Gabungkan kedua DataFrame
        df_gabung = pd.merge(df_penyakit, df_transposed, left_index=True, right_on='index', how='inner')
        df_gabung = df_gabung.set_index('index') #Set index
        
        with st.container(border=True):
            st.subheader(f"Jumlah Penderita (Orang) berdasarkan Jenis Penyakit di ")
            st.subheader(f":orange[DESA {infodesa['nmdesa'].iloc[0]}], :green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
            st.dataframe(df_gabung) # Tampilkan DataFrame yang digabungkan

    else:
        st.warning("Tidak tersedia.")
        
air = {
    "d1_1":	"MCK Sendiri",
    "d1_2":	"MCK Berkelompok",
    "d1_3":	"MCK Umum",
    "d2_1":	"Air Mandi - Ledeng/perpipaan berbayar/air isi ulang/kemasan",
    "d2_2":	"Air Mandi - Perpipaan",
    "d2_3":	"Air Mandi - Mata air/sumur",
    "d2_4":	"Air Mandi - Sungai, danau, embung",
    "d2_5":	"Air Mandi - Tadah air hujan",
    "d3_1":	"Air Minum - Ledeng/perpipaan berbayar/air isi ulang/kemasan",
    "d3_2":	"Air Minum - Mata air/sumur",
    "d3_3":	"Air Minum - Sungai, danau, embung",
    "d3_4":	"Air Minum - Tadah air hujan",
    "d3_5":	"Air Minum - Lainnya",
    "d4_1":	"Jamban Sendiri",
    "d4_2":	"Jamban Berkelompok",
    "d4_3":	"Jamban Umum"
}

with st.expander('Sanitasi'):
    url2 = f"https://sid.kemendesa.go.id/profile/data_analisis_sdgs?location_code=&village_id={desaterpilih}&on=tcws"

    response2 = requests.get(url2)
    data2 = response2.json()

    # --- Data Processing ---
    df2 = pd.DataFrame([data2['data']])

    # --- Gabungkan Data (Jika Data Tersedia) ---
    if df2 is not None and not df2.empty:
        # 1. Transpose df dan reset index
        df_transposed = df2.T.reset_index()
        df_transposed.columns = ['index', 'Jumlah KK']  # Rename columns

        # 2. Buat DataFrame dari dictionary faskes
        df_air = pd.DataFrame.from_dict(air, orient='index', columns=['Fasilitas'])
        df_air.index.name = 'index' #Memberi nama index

        # 3. Gabungkan kedua DataFrame
        df_gabung = pd.merge(df_air, df_transposed, left_index=True, right_on='index', how='inner')
        df_gabung = df_gabung.set_index('index') #Set index
        
        with st.container(border=True):
            st.subheader(f"Jumlah Kepala Keluarga berdasarkan Fasilitas Sanitasi di ")
            st.subheader(f":orange[DESA {infodesa['nmdesa'].iloc[0]}], :green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
            st.dataframe(df_gabung) # Tampilkan DataFrame yang digabungkan

    else:
        st.warning("Tidak tersedia.")    