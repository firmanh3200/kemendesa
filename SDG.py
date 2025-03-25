import streamlit as st
import pandas as pd
import requests  
from data import mfd_2025


# --- Configuration ---
st.set_page_config(page_title="SDGs Desa", page_icon=":earth_americas:", layout="wide")

# --- Functions ---

def fetch_data(api_url):
    """Fetches data from the API and returns it as a JSON object.
       Handles potential errors gracefully."""
    try:
        response = requests.get(api_url)  
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from API: {e}") 
        return None
    except ValueError as e:
        st.error(f"Error parsing JSON: {e}") 
        return None


def process_data(data):
    """Processes the fetched data into a pandas DataFrame.
       Handles missing or invalid data gracefully."""
    if data is None or not data.get('data'): 
        st.warning("No data available or data format is incorrect.")
        return None

    sdgs_data = data['data']
    try:
        df = pd.DataFrame(sdgs_data)
        
        if not all(col in df.columns for col in ['goals', 'title', 'score']):
            st.warning("Missing required columns ('goals', 'title', 'score') in the data.")
            return None

        df = df[['goals', 'title', 'score']] 
        return df
    except (KeyError, TypeError) as e:
        st.error(f"Error processing data: {e}. Check the data structure.") 
        return None

# --- Streamlit App ---
with st.container(border=True):
    with st.container(border=True):
        st.title(":blue[Data SDGs Desa]")
        st.caption('Sumber: https://sid.kemendesa.go.id/sdgs')
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

        # --- API Configuration ---
        if kol1 and kol2 and kol3:
            from data import mfd_2025_cantik
            
            infodesa = mfd_2025_cantik[mfd_2025_cantik['iddesa'] == desaterpilih]

            
            if infodesa.empty:
                st.warning("Data desa tidak ditemukan.  Periksa kembali IDDESA.")
            else:
                api_url = f"https://sid.kemendesa.go.id/sdgs/searching/score-sdgs?location_code=&village_id={desaterpilih}"

                #api_url = f"https://sid.kemendesa.go.id/sdgs/searching/score-sdgs?location_code=&province_id=32&city_id={kabterpilih1}&district_id={kecterpilih1}&village_id={desaterpilih}"

                # --- Data Fetching ---
                data = fetch_data(api_url)

                # --- Data Processing ---
                df = process_data(data)

                # --- Display DataTable (if data is available) ---
                if df is not None and not df.empty:
                    with st.container(border=True):
                        st.subheader(f":orange[INDIKATOR SDG's DESA {infodesa['nmdesa'].iloc[0]}]")
                        st.subheader(f":green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
                        st.dataframe(df, hide_index=True)  # Display DataFrame with Streamlit's table
                else:
                    st.warning("Tidak tersedia.")
                    
with st.expander('Bantuan Sosial'):
    komponen_bansos = {
        "d1": "Penerima BLT Dana Desa Desa",
        "d2": "Penerima Program Keluarga Harapan",
        "d3": "Penerima Bantuan Sosial Tunai",
        "d4": "Penerima Bantuan Presiden / Banpres",
        "d5": "Penerima Bantuan UMKM",
        "d6": "Penerima Bantuan Untuk Pekerja",
        "d7": "Penerima Bantuan Pendidikan Anak",
        "d8": "Penerima Bantuan Lainnya",
        "d9_1": "Lantai Marmer/Granit",
        "d9_2": "Lantai Keramik",
        "d9_3": "Lantai Parket/vinil/permadani",
        "d9_4": "Lantai Ubin/tegel/teraso",
        "d9_5": "Lantai Kayu/papan kualitas tinggi",
        "d9_6": "Lantai Semen/bata merah",
        "d9_7": "Lantai Bambu",
        "d9_8": "Lantai Kayu/papan kualitas rendah",
        "d10_1": "Dinding Semen/beton/kayu berkualitas tinggi",
        "d10_2": "Dinding Kayu berkualitas rendah/bambu",
        "d10_3": "",  
        "d11_1": "Jendela berfungsi",
        "d11_2": "Jendela tidak berfungsi",
        "d11_3": "Tidak ada jendela",
        "d12_1": "Atap Genteng",
        "d12_2": "Atap Kayu Jerami"
    }
    url1 = f"https://sid.kemendesa.go.id/profile/data_analisis_sdgs?location_code=&village_id={desaterpilih}&on=tnp"
    
    response1 = requests.get(url1)
    data1 = response1.json()
    df1 = pd.DataFrame([data1['data']])
    df2 = df1.T
    
    st.subheader('Data Bantuan Sosial dan Informasi Perumahan (KK)')
    kol1, kol2 = st.columns(2)
    with kol1:
        st.dataframe(komponen_bansos)
    with kol2:
        st.dataframe(df2, hide_index=False)

