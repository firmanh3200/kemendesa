import streamlit as st
import pandas as pd
import requests
from data import mfd_2025

# --- Configuration ---
st.set_page_config(page_title="SDGs Desa", page_icon=":earth_americas:", layout="wide")

fasilitas = {
    "d1_1":	"Rumah - Milik Sendiri",
    "d1_2":	"Rumah - Kontrak/ Sewa",
    "d1_3":	"Rumah - Bebas Sewa",
    "d1_4":	"Rumah - Dipinjami",
    "d1_5":	"Rumah - Dinas",
    "d2_1":	"Lahan - Milik Sendiri",
    "d2_2":	"Lahan - Milik Orang Lain",
    "d2_3":	"Lahan - Tanah Negara",
    "d3_1":	"TPS - Tidak ada",
    "d3_2":	"TPS - Di kebun/ sungai",
    "d3_3":	"TPS - Dibakar",
    "d3_4":	"TPS - Tempat Sampah",
    "d3_5":	"TPS - Tempat Sampah Diangkut Reguler",
    "d4":	"Jumlah Rumah Dibawah Suite/SUTT/SUTTAS",
    "d5":	"Jumlah Rumah Dibantaran Sungai",
    "d6":	"Jumlah Rumah Dirasakan Kumuh",
    "d7":	"Jumlah Rumah Di Gunung/Bukit",
    "d9":	"Transportasi Umum ke Pekerjaan Utama (Orang)",
    "d14":	"Transportasi Umum ke Lahan Pertanian (Orang)",
    "d19":	"Transportasi Umum ke Sekolah (Orang)",
    "d24":	"Transportasi Umum ke Lokasi Berobat (Orang)",
    "d29":	"Transportasi Umum ke Lokasi Beribadah (Orang)",
    "d34":	"Transportasi Umum ke Rekreasi (Orang)"
}

# --- Streamlit App ---
with st.container(border=True):
    with st.container(border=True):
        st.title(":blue[Data Fasilitas Permukiman dan Transportasi]")
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
                api_url = f"https://sid.kemendesa.go.id/profile/data_analisis_sdgs?location_code=&village_id={desaterpilih}&on=tsc"

                response = requests.get(api_url)
                data = response.json()

                # --- Data Processing ---
                df = pd.DataFrame([data['data']])

                # --- Gabungkan Data (Jika Data Tersedia) ---
                if df is not None and not df.empty:
                    # 1. Transpose df dan reset index
                    df_transposed = df.T.reset_index()
                    df_transposed.columns = ['index', 'Jumlah KK']  # Rename columns

                    # 2. Buat DataFrame dari dictionary fasilitas
                    df_fasilitas = pd.DataFrame.from_dict(fasilitas, orient='index', columns=['Sumber fasilitas'])
                    df_fasilitas.index.name = 'index' #Memberi nama index

                    # 3. Gabungkan kedua DataFrame
                    df_gabung = pd.merge(df_fasilitas, df_transposed, left_index=True, right_on='index', how='inner')
                    df_gabung = df_gabung.set_index('index') #Set index
                    
                    with st.container(border=True):
                        st.subheader(f"Jumlah Kepala Keluarga berdasarkan Fasilitas di ")
                        st.subheader(f":orange[DESA {infodesa['nmdesa'].iloc[0]}], :green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
                        st.dataframe(df_gabung, use_container_width=True) # Tampilkan DataFrame yang digabungkan

                else:
                    st.warning("Tidak tersedia.")

buang = {
    "d1_1":	"Tangki / Instalasi pengelolaan limbah",
    "d1_2":	"Sawah / Kolam / Sungai / Drainase / Laut",
    "d1_3":	"Lubang Ditanah"
}                    
with st.expander('Pembuangan Limbah Cair'):
    url1 = f"https://sid.kemendesa.go.id/profile/data_analisis_sdgs?location_code=&village_id={desaterpilih}&on=tcp"

    response1 = requests.get(url1)
    data1 = response1.json()

    # --- Data Processing ---
    df1 = pd.DataFrame([data1['data']])

    # --- Gabungkan Data (Jika Data Tersedia) ---
    if df1 is not None and not df1.empty:
        # 1. Transpose df dan reset index
        df_transposed = df1.T.reset_index()
        df_transposed.columns = ['index', 'Jumlah KK']  # Rename columns

        # 2. Buat DataFrame dari dictionary fasilitas
        df_buang = pd.DataFrame.from_dict(buang, orient='index', columns=['Pembuangan Limbah'])
        df_buang.index.name = 'index' #Memberi nama index

        # 3. Gabungkan kedua DataFrame
        df_gabung = pd.merge(df_buang, df_transposed, left_index=True, right_on='index', how='inner')
        df_gabung = df_gabung.set_index('index') #Set index
        
        with st.container(border=True):
            st.subheader(f"Jumlah Kepala Keluarga berdasarkan Fasilitas di ")
            st.subheader(f":orange[DESA {infodesa['nmdesa'].iloc[0]}], :green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
            st.dataframe(df_gabung, use_container_width=True) # Tampilkan DataFrame yang digabungkan

    else:
        st.warning("Tidak tersedia.")