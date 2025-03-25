import streamlit as st
import pandas as pd
import requests
from data import mfd_2025

# --- Configuration ---
st.set_page_config(page_title="SDGs Desa", page_icon=":earth_americas:", layout="wide")

energi = {
    "d1_1":	"Listrik PLN",
    "d1_2":	"Listrik Non PLN",
    "d1_3":	"Lampu minyak/lilin",
    "d1_4":	"Sumber Penerangan Lainnya",
    "d1_5":	"",
    "d2_1":	"LPG/biogas",
    "d2_2":	"Minyak tanah/batu bara",
    "d2_3":	"Kayu Bakar",
    "d3_1":	"Kayu Bakar - Pembelian",
    "d3_2":	"Kayu Bakar - Diambil dari hutan",
    "d3_3":	"Kayu Bakar - Diambil dari luar hutan"
}

# --- Streamlit App ---
with st.container(border=True):
    with st.container(border=True):
        st.title(":blue[Data Energi Keluarga]")
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
                api_url = f"https://sid.kemendesa.go.id/profile/data_analisis_sdgs?location_code=&village_id={desaterpilih}&on=tcre"

                response = requests.get(api_url)
                data = response.json()

                # --- Data Processing ---
                df = pd.DataFrame([data['data']])

                # --- Gabungkan Data (Jika Data Tersedia) ---
                if df is not None and not df.empty:
                    # 1. Transpose df dan reset index
                    df_transposed = df.T.reset_index()
                    df_transposed.columns = ['index', 'Jumlah KK']  # Rename columns

                    # 2. Buat DataFrame dari dictionary energi
                    df_energi = pd.DataFrame.from_dict(energi, orient='index', columns=['Sumber Energi'])
                    df_energi.index.name = 'index' #Memberi nama index

                    # 3. Gabungkan kedua DataFrame
                    df_gabung = pd.merge(df_energi, df_transposed, left_index=True, right_on='index', how='inner')
                    df_gabung = df_gabung.set_index('index') #Set index
                    
                    with st.container(border=True):
                        st.subheader(f"Jumlah Kepala Keluarga berdasarkan Sumber Energi di ")
                        st.subheader(f":orange[DESA {infodesa['nmdesa'].iloc[0]}], :green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
                        st.dataframe(df_gabung) # Tampilkan DataFrame yang digabungkan

                else:
                    st.warning("Tidak tersedia.")