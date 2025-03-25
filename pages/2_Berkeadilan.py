import streamlit as st
import pandas as pd
import requests
from data import mfd_2025

# --- Configuration ---
st.set_page_config(page_title="SDGs Desa", page_icon=":earth_americas:", layout="wide")

adil = {
    "d1_1":	"Tunanetra (buta)",
    "d1_2":	"Tunarungu (tuli)",
    "d1_3":	"Tunawicara (bisu)",
    "d1_4":	"Tunarungu - wicara (tuli & bisu)",
    "d1_5":	"Tunadaksa (cacat tubuh)",
    "d1_6":	"Tunagrahita (cacat mental)",
    "d1_7":	"Tunalaras (gangguan mengendalikan emosi dan kontrol sosial)",
    "d1_8":	"Pernah Cacat Kusta",
    "d1_9":	"Cacat Ganda (fisik & mental)",
    "d1_10":	"Dipasung"
}

# --- Streamlit App ---
with st.container(border=True):
    with st.container(border=True):
        st.title(":blue[Data Berkeadilan]")
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
                api_url = f"https://sid.kemendesa.go.id/profile/data_analisis_sdgs?location_code=&village_id={desaterpilih}&on=tvopaj"

                response = requests.get(api_url)
                data = response.json()

                # --- Data Processing ---
                df = pd.DataFrame([data['data']])

                # --- Gabungkan Data (Jika Data Tersedia) ---
                if df is not None and not df.empty:
                    # 1. Transpose df dan reset index
                    df_transposed = df.T.reset_index()
                    df_transposed.columns = ['index', 'Jumlah Penduduk (Orang)']  # Rename columns

                    # 2. Buat DataFrame dari dictionary adil
                    df_adil = pd.DataFrame.from_dict(adil, orient='index', columns=['Keterangan'])
                    df_adil.index.name = 'index' #Memberi nama index

                    # 3. Gabungkan kedua DataFrame
                    df_gabung = pd.merge(df_adil, df_transposed, left_index=True, right_on='index', how='inner')
                    df_gabung = df_gabung.set_index('index') #Set index
                    
                    with st.container(border=True):
                        st.subheader(f"Jumlah Penduduk di ")
                        st.subheader(f":orange[DESA {infodesa['nmdesa'].iloc[0]}], :green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
                        st.dataframe(df_gabung) # Tampilkan DataFrame yang digabungkan

                else:
                    st.warning("Tidak tersedia.")
                    
mitra = {
    "d1":	"Memiliki Nomor HP",
    "d2":	"Memiliki Whatsapp",
    "d3":	"Memiliki Email",
    "d4":	"Memiliki Facebook",
    "d5":	"Memiliki Twitter",
    "d6":	"Memiliki Instagram"
}
with st.expander('Kemitraan Pembangunan Desa'):
    url1 = f"https://sid.kemendesa.go.id/profile/data_analisis_sdgs?location_code=&village_id={desaterpilih}&on=tvdp"

    response1 = requests.get(url1)
    data1 = response1.json()

    # --- Data Processing ---
    df1 = pd.DataFrame([data1['data']])

    # --- Gabungkan Data (Jika Data Tersedia) ---
    if df1 is not None and not df1.empty:
        # 1. Transpose df dan reset index
        df_transposed = df1.T.reset_index()
        df_transposed.columns = ['index', 'Jumlah Penduduk (Orang)']  # Rename columns

        # 2. Buat DataFrame dari dictionary adil
        df_mitra = pd.DataFrame.from_dict(mitra, orient='index', columns=['Keterangan'])
        df_mitra.index.name = 'index' #Memberi nama index

        # 3. Gabungkan kedua DataFrame
        df_gabung = pd.merge(df_mitra, df_transposed, left_index=True, right_on='index', how='inner')
        df_gabung = df_gabung.set_index('index') #Set index
        
        with st.container(border=True):
            st.subheader(f"Jumlah Penduduk di ")
            st.subheader(f":orange[DESA {infodesa['nmdesa'].iloc[0]}], :green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
            st.dataframe(df_gabung) # Tampilkan DataFrame yang digabungkan

    else:
        st.warning("Tidak tersedia.")    