import streamlit as st
import pandas as pd
import requests
from data import mfd_2025

# --- Configuration ---
st.set_page_config(page_title="SDGs Desa", page_icon=":earth_americas:", layout="wide")

aktivitas = {
    "d1_1":	"Bersekolah",
    "d1_2":	"Ibu Rumah Tangga",
    "d1_3":	"Tidak Bekerja",
    "d1_4":	"Sedang Mencari Pekerjaan",
    "d1_5":	"Bekerja",
    "d2_1":	"Petani Pemilik Lahan",
    "d2_2":	"Petani Penyewa",
    "d2_3":	"Buruh Tani",
    "d2_4":	"Nelayan Pemilik Kapal / Perahu",
    "d2_5":	"Nelayan Penyewa Kapal / Perahu",
    "d2_6":	"Buruh Nelayan",
    "d2_7":	"Guru",
    "d2_8":	"Guru Agama",
    "d2_9":	"Pedagang",
    "d2_10":	"Pengolahan / Industri",
    "d2_11":	"PNS",
    "d2_12":	"TNI",
    "d2_13":	"Perangkat Desa",
    "d2_14":	"Pegawai Kantor Desa",
    "d2_15":	"TKI",
    "d3_1":	"Peserta Jaminan Sosial Pemerintah",
    "d3_2":	"Peserta Jaminan Sosial Swasta"
}

# --- Streamlit App ---
with st.container(border=True):
    with st.container(border=True):
        st.title(":blue[Data Aktivitas Penduduk]")
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
                api_url = f"https://sid.kemendesa.go.id/profile/data_analisis_sdgs?location_code=&village_id={desaterpilih}&on=tveg"

                response = requests.get(api_url)
                data = response.json()

                # --- Data Processing ---
                df = pd.DataFrame([data['data']])

                # --- Gabungkan Data (Jika Data Tersedia) ---
                if df is not None and not df.empty:
                    # 1. Transpose df dan reset index
                    df_transposed = df.T.reset_index()
                    df_transposed.columns = ['index', 'Jumlah Penduduk']  # Rename columns

                    # 2. Buat DataFrame dari dictionary aktivitas
                    df_aktivitas = pd.DataFrame.from_dict(aktivitas, orient='index', columns=['Aktivitas'])
                    df_aktivitas.index.name = 'index' #Memberi nama index

                    # 3. Gabungkan kedua DataFrame
                    df_gabung = pd.merge(df_aktivitas, df_transposed, left_index=True, right_on='index', how='inner')
                    df_gabung = df_gabung.set_index('index') #Set index
                    
                    with st.container(border=True):
                        st.subheader(f"Jumlah Penduduk berdasarkan aktivitas ekonomi di ")
                        st.subheader(f":orange[DESA {infodesa['nmdesa'].iloc[0]}], :green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
                        st.dataframe(df_gabung) # Tampilkan DataFrame yang digabungkan

                else:
                    st.warning("Tidak tersedia.")