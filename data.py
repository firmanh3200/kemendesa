import pandas as pd

def kamus():
    mfd = pd.read_csv('data/mfd2023.csv', sep=',', 
                            dtype={'idkab':'str', 'idkec':'str', 'iddesa':'str'}, encoding='utf-8')
    
    mendagri = pd.read_csv('data/kdkec.csv', sep=',', 
                            dtype={'idkab':'str', 'idkec':'str', 'kodedapodik':'str'}, encoding='utf-8')
    
    mfd32 = pd.read_csv('data/mfd_23_1_32.csv', 
                            dtype={'kdkab':'str', 'kdkec':'str', 'kddesa':'str', 'iddesa':'str'}, encoding='utf-8')
    mfd32['idkec'] = mfd32['iddesa'].str[:7]
    
    # Filter mfd berdasarkan idkec yang ada di mendagri
    mfd_2025 = mfd[mfd['idkec'].isin(mendagri['idkec'])]
    mfd32_2025 = mfd32[mfd32['idkec'].isin(mendagri['idkec'])]
    
    mfd_2025_a = pd.merge(mfd_2025, mfd32_2025[['iddesa', 'stat_pem', 'nmdesa', 'nmkec', 'nmkab', 'latitude', 'longitude']], on='iddesa', how='left')
    mfd_2025_cantik = pd.merge(mfd_2025_a, mendagri, on='idkec', how='left')
    
    return mfd_2025, mfd_2025_cantik
mfd_2025, mfd_2025_cantik = kamus()

