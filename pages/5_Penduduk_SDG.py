import streamlit as st
import pandas as pd
import requests
import json
from data import mfd_2025

# --- Configuration ---
st.set_page_config(page_title="Penduduk Kemendesa", page_icon=":busts_in_silhouette:", layout="wide")

# --- Functions ---

def fetch_data(api_url):
    """Fetches population data from the API and returns it as a JSON object."""
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from API: {e}")
        return None
    except json.JSONDecodeError as e:  # Handle JSON decoding errors
        st.error(f"Error parsing JSON response: {e}")
        return None


def process_age_data(data):
    """Processes age group data into a DataFrame with the desired format."""
    if not data:
        return None

    age_groups = {}
    for key, value in data.items():
        if key.startswith(('l_', 'p_')):
            prefix, age_range = key.split('_', 1) # Split on the first underscore
            age_groups.setdefault(age_range, {}).update({prefix: value})

    # Create a list of dictionaries for the DataFrame
    age_data = []
    for age_range, counts in age_groups.items():
        age_data.append({
            "Kelompok Umur": age_range.replace("_", " - "), # Replace underscores in age range
            "Laki-laki": counts.get("l", 0), # Get "l" value, default to 0 if missing
            "Perempuan": counts.get("p", 0)  # Get "p" value, default to 0 if missing
        })

    df_age = pd.DataFrame(age_data)
    # Reorder the columns
    df_age = df_age[["Kelompok Umur", "Laki-laki", "Perempuan"]]
    return df_age

def process_other_data(data):
    """Processes other data into a DataFrame."""
    if not data:
        return None

    #  Create a list of dictionaries for the DataFrame
    other_data = []
    for key, value in data.items():
        if not key.startswith(('l_', 'p_')): # Exclude age-related keys
            other_data.append({
                "Keterangan": key.replace("_", " ").title(),  # Format the key
                "Nilai": value
            })

    df_other = pd.DataFrame(other_data)
    return df_other

def display_metrics(data):
    """Displays key population metrics and other data."""
    if not data:
        st.warning("No data to display.")
        return

    st.subheader(f":orange[DESA {infodesa['nmdesa'].iloc[0]}]")
    st.subheader(f":green[KECAMATAN {infodesa['nmkec'].iloc[0]}, {infodesa['nmkab'].iloc[0]}]")
    
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            if 'total_data' in data:
                col1.metric("Jumlah Penduduk", data['total_data'])
        with col2:
            if 'gender_men' in data and 'gender_women' in data:
                col2.metric("Laki-laki", data['gender_men'])
                #col2.metric("Perempuan", data['gender_women'])
        with col3:
            if 'kawin' in data and 'belum_kawin' in data:
                col3.metric("Perempuan", data['gender_women'])
                #col3.metric("Belum Kawin", data['belum_kawin'])

    kol1, kol2 = st.columns(2)
    with kol1:
        with st.container(border=True):
            st.subheader("Distribusi Kelompok Umur")
                                
            df_age = process_age_data(data)
            if df_age is not None and not df_age.empty:
                st.dataframe(df_age, hide_index = True)
            else:
                st.warning("Data tidak tersedia")

    with kol2:
        with st.container(border=True):
            st.subheader("Data Lainnya")
            df_other = process_other_data(data)
            if df_other is not None and not df_other.empty:
                st.dataframe(df_other, hide_index = True)
            else:
                st.warning("Data tidak tersedia")


# --- Streamlit App ---
st.title("Data Penduduk")
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

# --- API Configuration (Keep this configurable) ---
if kol1 and kol2 and kol3:
    from data import mfd_2025_cantik
    # Filter the infodesa DataFrame correctly
    infodesa = mfd_2025_cantik[mfd_2025_cantik['iddesa'] == desaterpilih]

    # Check if infodesa is empty
    if infodesa.empty:
        st.warning("Data desa tidak ditemukan.  Periksa kembali IDDESA.")
    else:
        api_url = f"https://sid.kemendesa.go.id/population-statistic/data?location_code=&village_id={desaterpilih}&on=population"

# --- Data Fetching ---
data = fetch_data(api_url)

# --- Data Display ---
display_metrics(data)