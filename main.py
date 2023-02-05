import streamlit as st
import pandas as pd
import time
import hydralit_components as hc
from streamlit_option_menu import option_menu
from PIL import Image
from side import about, info1, info2, info3, info4, style, footer, detail1


# KONFIGURASI PAGE #HARUS DI AWAL
# 4.0 Changes
im = Image.open("py.png")
st.set_page_config(page_title=' Kelompok PyTorch',
                   page_icon=im,
                   layout='wide',
                   initial_sidebar_state="collapsed"
                   )


# ADD DATA FRAME
@st.cache
def ambil_data():
    df = pd.read_excel(
        io='hotel_jawabarat_tiket_fix.xlsx',
        engine='openpyxl',
    )
    return df
df = ambil_data()

# Tambahan Latar dan Style CSS
style()

# Memanggil Streamlit SideBar
with st.sidebar:
    # Memanggil Streamlit option Menu
    selected = option_menu("Pytorch", ["Dashboard", "Detail Hotel",  "About"], menu_icon="cast",
                           icons=['house', 'search', "person"], default_index=0, orientation="vertical",
                           )

# Streamlit Option Menu Dashboard
if selected == "Dashboard":
    # Memanggil Hydralit loader
    with hc.HyLoader('Memuat Data', hc.Loaders.pacman, height=200):
        time.sleep(2)
        # Memanggil Info1 (Tampilan Info Jumlah dan Rata-Rata Rating dan Harga Hotel di Jawa Barat)
        info1(df)
        # Memanggil Info2 (Tampilan Barchar dan LineChar Info Hotel Di Kota dan Kabupaten di Jawa Barat)
        info2(df)
        # Memanggil Info3 (Tampilan PieChar Info Hotel Di Kota dan Kabupaten di Jawa Barat)
        info3(df)
        # Memanggil Info4 (Tampilan Streamlit Folium yang menampilkan Titik Rata-Rata Dari Hotel Disetiap Kotanya dengan Popup data Di Markernya)
        info4(df)

# Streamlit Option Menu Detail Hotel
if selected == "Detail Hotel":
    # Memanggil Hydralit loader
    with hc.HyLoader('Memuat Data', hc.Loaders.standard_loaders, height=200):
        time.sleep(2)
    # Memanggil Side Bar
    detail1(df)

if selected == "About":
    # Memanggil Hydralit loader
    with hc.HyLoader('Memuat Data', hc.Loaders.pacman, height=150):
        time.sleep(1)
    # Memanggil About
    about()

# Memanggil Footer
footer()
