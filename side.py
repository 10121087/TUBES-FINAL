import folium
import pandas as pd
import streamlit as st
import streamlit.components.v1 as com
from streamlit_folium import folium_static
import json
import plotly.express as px

# Background


def Judul():
    st.markdown(
        """
        <style>
            div[data-testid="column"]:nth-of-type(1)
            {
            } 

            div[data-testid="column"]:nth-of-type(2)
            {
                text-align: center;
            } 

        </style>
        """, unsafe_allow_html=True
    )
    header_left, header_mid, header_right = st.columns([1, 2, 1])
    with header_mid:
        st.title("Hotel Di Provinsi Jawa Barat")
        st.caption(
            "Data di scrapping dari website Tiket.com")
    st.markdown('---')

# Read Data


# Memasukan Style


def style():
    st.markdown("""
    <style>
    .css-k1ih3n {
    width: 100%;
    padding: 6rem 7rem 9rem;
    min-width: auto;
    max-width: initial;
    margin-top: -80px;
    }
    .css-82vsbp {
    width: 372px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 1rem;
    margin-top: -80px;
    }
    .css-6wvkk3 {
    padding-left: 0px;
    padding-right: 0px;
    margin-top: -80px;
    }

   

    [data-testid="stAppViewContainer"]{
    background-image: url("https://cdn.discordapp.com/attachments/1038017092806512712/1070778864890028112/white_wallpaper_5_4k_hd_white-1920x1080.jpg");
    background-size: 115%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    }

    [data-testid="stHeader"] {
    background: rgba(0,0,0,0);
    }

    [data-testid="stToolbar"] {
    right: 2rem;
    }

  
    """, unsafe_allow_html=True)

# Memformat Float Menjadi Format Rupiah


def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3:
        return 'IDR ' + y
    else:
        p = y[-3:]
        q = y[:-3]
        return formatrupiah(q) + '.' + p

# Manampilkan Rating Bintang


def bintangrating(rating):
    if 0 <= rating <= 0.5:
        bintang = 'rating-static rating-5'
    elif 0.5 < rating <= 1:
        bintang = 'rating-static rating-10'
    elif 1 < rating <= 1.5:
        bintang = 'rating-static rating-15'
    elif 1.5 < rating <= 2:
        bintang = 'rating-static rating-20'
    elif 2 < rating <= 2.5:
        bintang = 'rating-static rating-25'
    elif 2.5 < rating <= 3:
        bintang = 'rating-static rating-30'
    elif 3 < rating <= 3.5:
        bintang = 'rating-static rating-35'
    elif 3.5 < rating <= 4:
        bintang = 'rating-static rating-40'
    elif 4 < rating <= 4.5:
        bintang = 'rating-static rating-45'
    elif 4.5 < rating <= 5:
        bintang = 'rating-static rating-50'
    return bintang

# Membuat Informasi Untuk PopUp di Folium


def popup_html(df, row):
    i = row
    nama = df['nama'].iloc[i]
    url = df['url'].iloc[i]
    gambar = df['gambar'].iloc[i]
    lokasi = df['location'].iloc[i] + "," + df['city'].iloc[i]
    harga = df['price'].iloc[i]
    rating = df['rating'].iloc[i]
    gpsloc = df['gmap'].iloc[i]
    desk = df['deskripsi'].iloc[i]

    left_col_color = "#3e95b5"
    right_col_color = "#f2f9ff"

    html = """
    <!DOCTYPE html>
    <html>

    <style>
    .rating-static {
    width: 60px;
    height: 16px;
    display: block;
    background: url('http://www.itsalif.info/blogfiles/rating/star-rating.png') 0 0 no-repeat;}
    .rating-50 { background-position: 0 0; }
    .rating-40 { background-position: -12px 0; }
    .rating-30 { background-position: -24px 0; }
    .rating-20 { background-position: -36px 0; }
    .rating-10 { background-position: -48px 0; }
    .rating-0 { background-position: -60px 0; }

    .rating-5  { background-position: -48px -16px; }
    .rating-15 { background-position: -36px -16px; }
    .rating-25 { background-position: -24px -16px; }
    .rating-35 { background-position: -12px -16px; }
    .rating-45 { background-position: 0 -16px; }
    </style>

    <center><img src=\"""" + gambar + """\" alt="logo" width=100 height=100 ></center>

    <center><h2 style="margin-bottom:5"; width="200px">{}</h2>""".format(nama) + """</center>

    <center><a href=\"""" + url + """\"target="_blank">Go to the Hotel's Website</a></center>

    <center><h6>{}""".format(formatrupiah(harga)) + """</h6></center>

    <center> <table style="height: 126px; width: 305px;">
    <tbody>
    <tr>
    <center>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;"><center>alamat </span></td>
    <td style="width: 205px;background-color: """ + right_col_color + """;"><center>""" + lokasi + """</td>
    </center>
    </tr>

    <tr>
    <center>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;"><center> Rating </span></td>
    <td style="width: 205px;background-color: """ + right_col_color + """;"><center><span class="{}">""".format(bintangrating(rating)) + """</span>{}</td>""".format(rating) + """
    </center>
    </tr>

    <tr>
    <center>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;"><center>Lokasi </span></td>
    <td style="width: 205px;background-color: """ + right_col_color + """;"><a href=\"""" + gpsloc + """\" target="_blank"><center>Link Location</a></td>
    </center>
    </tr>

    </tbody>
    </table></center>

    </html>
    """
    return html

# Menampilkan Folium


def Tampil(df, pilih):
    with open("Jabar_By_Kab.geojson") as response:
        grid = json.load(response)

        lat = df.latitude.mean()
        lon = df.longitude.mean()
        peta = folium.Map(location=[lon, lat], zoom_start=9,
                          control_scale=True)

    if pilih == "all":
        df1 = df
    if pilih == "city":
        df1 = pd.DataFrame(df.groupby(["city"]).mean()).reset_index()
        folium.GeoJson(
            grid,
            style_function=lambda feature: {
                "fillColor": "#ffff00",
                "color": "black",
                "weight": 1,
                "dashArray": "1, 1",
            },).add_to(peta)
    for i, location_info in df1.iterrows():
        if pilih == "all":
            html = popup_html(df, i)

        if pilih == "city":
            html = popup_html_kota(df, i)
        color = 'red'
        popup = folium.Popup(folium.Html(html, script=True), max_width=500)
        folium.Marker([location_info["longitude"], location_info["latitude"]],
                      popup=popup, tooltip=location_info["city"], icon=folium.Icon(color=color, icon='hotel',
                                                                                   prefix='fa', prefer_canvas=True)).add_to(peta)

    # peta.save("index.html")

    # return st_folium(peta, width=1450, height=600, key='foliumMap1')
    return folium_static(peta, width=1300, height=720,)

# Membuat Informasi Untuk PopUp di Folium


def popup_html_kota(df, row):
    i = row
    jumlah = pd.DataFrame(df.groupby(["city"]).count()).reset_index()
    jumlah = jumlah.iloc[i, 1]
    Data_Jabar = df.groupby(["city"]).mean().reset_index()
    nama = Data_Jabar['city'].iloc[i]
    gambar = Gambar(nama)
    harga = Data_Jabar['price'].iloc[i]
    rating = Data_Jabar['rating'].iloc[i]

    left_col_color = "#3e95b5"
    right_col_color = "#f2f9ff"
    html = ("""
    <!DOCTYPE html>
    <html>

    <style>
    .rating-static {
    width: 60px;
    height: 16px;
    display: block;
    background: url('http://www.itsalif.info/blogfiles/rating/star-rating.png') 0 0 no-repeat;}
    .rating-50 { background-position: 0 0; }
    .rating-40 { background-position: -12px 0; }
    .rating-30 { background-position: -24px 0; }
    .rating-20 { background-position: -36px 0; }
    .rating-10 { background-position: -48px 0; }
    .rating-0 { background-position: -60px 0; }

    .rating-5  { background-position: -48px -16px; }
    .rating-15 { background-position: -36px -16px; }
    .rating-25 { background-position: -24px -16px; }
    .rating-35 { background-position: -12px -16px; }
    .rating-45 { background-position: 0 -16px; }
    </style>

    <center><img src='""" + gambar + """' alt="logo" width=100 height=100 ></center>
    <center><h2 style="margin-bottom:5"; width="200px">{}""".format(nama) + """</h2></center>

    <center><h4>{}""".format(formatrupiah(int(harga))) + """</h4></center>
    <table>
    <tbody>
    <tr>
        <td style="background-color: #3e95b5;"><span style="color: #ffffff;"><center>Rating</center></span></td>
    </tr>
    <tr>
        <td style="width: 205px;background-color: """ + right_col_color + """;"><center><span class="{}">""".format(bintangrating(float("%.2f" % rating))) + """</span>{}</td>""".format("%.2f" % rating) + """
    </tr>
    <tr>
        <td style="background-color: #3e95b5;"><span style="color: #ffffff;"><center>Jumlah</center></span></td>
    </tr>
    <tr>
        <td style="width: 100px height=205px";background-color: """ + right_col_color + """;"><center>{}</center></td>""".format(jumlah) + """
    </tr>
    </tbody>
    </table>
"""
            )
    return html

# Mengamnil Gambar Kota dan Kabupaten


def Gambar(nama):
    if nama == "Bandung":
        imgs = "https://1.bp.blogspot.com/-DvA9sqLXktY/YDYycmGHqvI/AAAAAAAABkE/007xqDiYu0I4NijKrXhNiNlJxmpSgCg_ACLcBGAsYHQ/s821/logo%2Bkota%2Bbandung.png"
    elif nama == "Banjar":
        imgs = "https://1.bp.blogspot.com/-G-_2UG04h7M/YDY0Ct3ezgI/AAAAAAAABkQ/N__u89Dxta8dTrL427SXsRcuUm_LfEtmgCPcBGAYYCw/s821/logo%2Bkota%2Bbanjar.png"
    elif nama == "Bekasi":
        imgs = "https://1.bp.blogspot.com/-FKwGyoUYKgg/YFby9Q3WgyI/AAAAAAAACD0/RG3MEWXxeGs8Zd_aEkF2npDNCDzINr1gACNcBGAsYHQ/s2048/Kota%2BBekasi.png"
    elif nama == "Bogor":
        imgs = "https://1.bp.blogspot.com/-La5QRUyE3wg/YDY01bUqyRI/AAAAAAAABkU/KvH8tvrLWak7AXKFVQRm_SbG3b4Br6dhQCLcBGAsYHQ/s1600/logo%2Bkota%2Bbogor.png"
    elif nama == "Ciamis":
        imgs = "https://1.bp.blogspot.com/-6V62GJyifGc/YDYXMT42rRI/AAAAAAAABh8/7sl3CPRaK1U1JVRhm_Vrwqgek-GPoLgcACLcBGAsYHQ/s599/logo%2Bkabupaten%2Bciamis.png"
    elif nama == "Cianjur":
        imgs = "https://1.bp.blogspot.com/-AvdnQAZ4bAE/YDYXk7FrfEI/AAAAAAAABiE/ojgdDH3Ns2IJ7uDXPWPgawKNyHrthDCqwCLcBGAsYHQ/s560/logo%2Bkabupaten%2Bcianjur.png"
    elif nama == "Cikarang":
        imgs = "https://1.bp.blogspot.com/-kCol9gsswgQ/YDYUNdE4c8I/AAAAAAAABhs/4xKQuFS8B38bN7wtCk6X7VyynZcnbCpKQCLcBGAsYHQ/s1100/logo%2Bkabupaten%2Bbekasi.png"
    elif nama == "Cimahi":
        imgs = "https://1.bp.blogspot.com/-1-ussgHn0N8/YDY2EvpkA0I/AAAAAAAABkc/ubpICLt6BBMOJJhLfvmAaDGnqZp6vpq7QCLcBGAsYHQ/s400/logo%2Bkota%2Bcimahi.png"
    elif nama == "Cirebon":
        imgs = "https://1.bp.blogspot.com/-Qh4ev9Qkus4/YDY3H1nWzGI/AAAAAAAABkk/RmrEy0s7oxIx3PQ2Gml7KD7hsNZu-pvDACLcBGAsYHQ/s1024/logo%2Bkota%2Bcirebon.png"
    elif nama == "Depok":
        imgs = "https://1.bp.blogspot.com/-t3q-ACnU1vE/YDY3z4-RmHI/AAAAAAAABks/0AHEb0QYq9YMGhDfaZH9quIXOX1Ia1QmwCLcBGAsYHQ/s599/logo%2Bkota%2Bdepok.png"
    elif nama == "Garut":
        imgs = "https://1.bp.blogspot.com/-b9Z5k58y-YQ/YDYX5sU4L0I/AAAAAAAABiQ/37ZpXgxCxbsf-HdaE2QihYJBnbY23jWoACLcBGAsYHQ/s599/logo%2Bkabupaten%2Bgarut.png"
    elif nama == "Indramayu":
        imgs = "https://1.bp.blogspot.com/-kqseC7E0S-Y/YDYaRPiA6AI/AAAAAAAABic/qy-XqPjSrt0z_DCeQpTcmrn_kIsoLiWoQCLcBGAsYHQ/s1100/logo%2Bkabupaten%2Bindramayu.png"
    elif nama == "Karawang":
        imgs = "https://1.bp.blogspot.com/-E2BeyDNWSyw/YDYa4B5MkLI/AAAAAAAABik/1Wu1Roee9gw8kNvlukSKzhRh01weYrv-wCLcBGAsYHQ/s600/logo%2Bkabupaten%2Bkarawang.png"
    elif nama == "Kuningan":
        imgs = "https://1.bp.blogspot.com/-1Heb42-uDJ8/YDYbo1XCyVI/AAAAAAAABis/i-yfWlQmiBIVRTsvIXYJHeRwfmYZ9xgDACLcBGAsYHQ/s1100/logo%2Bkabupaten%2Bkuningan.png"
    elif nama == "Majalengka":
        imgs = "https://1.bp.blogspot.com/-Xc_mKzUsQrM/YDYcro-6SpI/AAAAAAAABi0/SRCPmf-Jih0N1XcDLnMIAIGEsToe1QuZACLcBGAsYHQ/s599/logo%2Bkabupaten%2Bmajalengka.png"
    elif nama == "Pangandaran":
        imgs = "https://1.bp.blogspot.com/--ezmDr3hbQk/YDYgTgxZqhI/AAAAAAAABjU/IQpWZvwfCtArlQUErXAMexpGoRtD4QdKwCLcBGAsYHQ/s1100/logo%2Bkabupaten%2Bpangandaran.png"
    elif nama == "Purwakarta":
        imgs = "https://1.bp.blogspot.com/-CCkoOZzS6Ao/YDYgZVgTqaI/AAAAAAAABjY/8sOWxRbbf7k9FjC6OYmi-43b7MSB2PhTgCLcBGAsYHQ/s1024/logo%2Bkabupaten%2Bpurwakarta.png"
    elif nama == "Subang":
        imgs = "https://1.bp.blogspot.com/-enp28V1Y4IY/YDYgrfv5ocI/AAAAAAAABjk/jkA-EAb5BeEFzQ-iE2igEoZ6jfPXHLpkgCLcBGAsYHQ/s1100/logo%2Bkabupaten%2Bsubang.png"
    elif nama == "Sukabumi":
        imgs = "https://1.bp.blogspot.com/-hUF0x5PZrek/YDY4AZPlAbI/AAAAAAAABkw/HvzJB2Pe83QHFzdPhJF0jXk9qHbCG-HVgCLcBGAsYHQ/s677/logo%2Bkota%2Bsukabumi.png"
    elif nama == "Sumedang":
        imgs = "https://1.bp.blogspot.com/-ryeXd-MZy3o/YDYhDc2wDVI/AAAAAAAABjw/p2CaFPnfhPYYo_BoS0eT6cCSqpTqdTRCQCLcBGAsYHQ/s599/logo%2Bkabupaten%2Bsumedang.png"
    elif nama == "Tasikmalaya":
        imgs = "https://1.bp.blogspot.com/-LIXRBpJw4kM/YDY4J-MoDqI/AAAAAAAABk0/bMobhQxrWW47b1wTJTx6Vg2GcuPHdFnewCLcBGAsYHQ/s1200/logo%2Bkota%2Btasikmalaya.png"
    return imgs

# Menampilakan Sidebar


def sidebar(df):
    # BAGIAN SIDEBAR
    pilihan = df
    with st.sidebar:
        with st.expander('Filter disini'):
            carikota = df['city'].unique()

            kota = st.multiselect(
                label='Pilih Kota:',
                options=carikota
            )

            carilokasi = df.query(
                'city == @kota'
            ).reset_index(drop=True)

            lokasi = st.multiselect(
                'Pilih Kecamatan:',
                options=carilokasi['location'].unique()
            )

            carihotel = carilokasi.query(
                'location == @lokasi'
            ).reset_index(drop=True)

            # st.dataframe(df_kotket)
            hotel = st.multiselect(
                'Nama Hotel:',
                options=carihotel['nama'].unique()
            )

            df_hotel = carihotel.query(
                'nama == @hotel').reset_index(drop=True)

            if len(kota) > 0 and len(lokasi) > 0 and len(hotel) > 0:
                pilihan = df_hotel
                tipe = "hotel"
            elif len(kota) > 0 and len(lokasi) > 0:
                pilihan = carihotel
                tipe = "kecamatan"
            elif len(kota) > 0:
                pilihan = carilokasi
                tipe = "kota"
            elif len(kota) == 0:
                pilihan = df
                tipe = "provinsi"
    return pilihan, tipe

# Menampilakn detail Hotel


def html_hotel(df, row):
    i = row
    nama = df['nama'].iloc[i]
    url = df['url'].iloc[i]
    gambar = df['gambar'].iloc[i]
    lokasi = df['location'].iloc[i] + "," + df['city'].iloc[i]
    harga = df['price'].iloc[i]
    rating = df['rating'].iloc[i]
    gpsloc = df['gmap'].iloc[i]
    desk = df['deskripsi'].iloc[i]

    html = """
        <!doctype html>
        <html lang="en">

        <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
                integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
                integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
                crossorigin="anonymous"></script>
        </head>
        <style>
        .card {
        background-color: rgb(241 241 241 / 41%);}

        .rating-static {
        width: 60px;
        height: 16px;
        display: block;
        background: url('http://www.itsalif.info/blogfiles/rating/star-rating.png') 0 0 no-repeat;}
        .rating-50 { background-position: 0 0; }
        .rating-40 { background-position: -12px 0; }
        .rating-30 { background-position: -24px 0; }
        .rating-20 { background-position: -36px 0; }
        .rating-10 { background-position: -48px 0; }
        .rating-0 { background-position: -60px 0; }

        .rating-5  { background-position: -48px -16px; }
        .rating-15 { background-position: -36px -16px; }
        .rating-25 { background-position: -24px -16px; }
        .rating-35 { background-position: -12px -16px; }
        .rating-45 { background-position: 0 -16px; }
        </style>
        <body style="background-color: transparent;">
        <div data-bs-theme="dark" class="container-sm  border-0">
            <div class="card text-start border-0">
                <center>
                <div class="card mb-3 border-0" style="max-width: 540px;">
                    <center>
                    <img class="card-img-top border border-dark rounded" src=\"""" + gambar + """\" alt="Title" width=300px height=300px>
                    </center>
                </div>
                </center>
                <div class="card-body  border-0">
                    <h4 class="card-title"><a href=\"""" + url + """\"target="_blank">"""+nama+"""</a></h4>
                    <h4 class="card-title">   {}""".format(formatrupiah(harga)) + """</h4>
                    <p class="card-text">""" + lokasi + """</p>
                    <p class="card-text"><a href=\"""" + gpsloc + """\"target="_blank">GPS LOCATION</a></p>
                    <p class="card-text">{}""".format(rating) + """<span class="{}">""".format(bintangrating(rating)) + """ </span></p>
                    <p class="card-text">""" + desk + """</p>
                    
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

# Menampilkan Detail Hotel yang di Tampilkan


def detail1(df):
    detail, tipe = sidebar(df)
    st.markdown("""
            <center><h1>Detail Posisi Hotel Jawa Barat</h1></center>
            <center><h4>Sesuai koordinat Hotel</h4></center>
            """, unsafe_allow_html=True)
    # 4.0Changes
    col1, col2, col3 = st.columns((1, 10, 1), gap='large')
    with col2:
        Tampil(detail, "all")
    detailpref(detail, tipe)
# Menampilkan Info di Hotel Jawa Barat


def info1(df):
    with st.container():
        totalrpall = int(df['price'].mean())
        totalhotel = int(df['nama'].count())
        totalrating = float(df['rating'].mean())
        rupiah = formatrupiah(totalrpall)
        rating = "%.2f" % totalrating

        Judul()
        show1, show2, show3, show4 = st.columns((4, 4, 4, 2), gap='large')
        with show1:
            st.image(
                'https://cdn.discordapp.com/attachments/934418750646677554/1070359489716424755/rupiah1.png', use_column_width='Auto')
            st.metric(label='Rata Rata Harga', value=(rupiah))
        with show2:
            st.image(
                'https://cdn.discordapp.com/attachments/934418750646677554/1070359490064560208/hotel.png')
            st.metric(label='Total Hotel', value=(totalhotel))
        with show3:
            st.image(
                'https://cdn.discordapp.com/attachments/934418750646677554/1070359489280213012/rating.png')
            st.metric(label='Rata-Rata Rating', value=(rating))
        with show4:
            st.image(
                'https://cdn.discordapp.com/attachments/934418750646677554/1070730246044782602/love.png')
            st.metric(label='Impression', value='Good')


# Menampilkan Barchart dan Linechart


def info2(df):
    with st.container():
        bar = df.groupby(['city']).mean().reset_index()
        bar2 = df.groupby(['city']).count().reset_index()
        Q1, Q2, Q3 = st.columns(3)
        with Q1:
            columns1 = bar[['city', 'price']]
            fig = px.bar(columns1,
                         x='city',
                         y='price',
                         labels={"price": "Harga", "city": "Kota"},
                         title='<b>Harga Rata-Rata Hotel per Kota/Kab</b>')
            fig.update_xaxes(rangeslider_visible=True)
            fig.update_layout(xaxis_range=['Bandung', 'Cirebon'],
                              title={'x': 0.5},
                              plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)",
                              xaxis=(dict(showgrid=False)),
                              yaxis=(dict(showgrid=False)),)
            st.plotly_chart(fig, use_container_width=True)

        with Q2:

            columns2 = bar2[['city', 'location']]
            fig = px.line(columns2,
                          x='city',
                          y='location',
                          markers=True,
                          labels={"location": "Total Hotel", "city": "Kota"},
                          title='<b>Total Hotel per Kota/Kab</b>')
            fig.update_xaxes(rangeslider_visible=True)
            fig.update_layout(xaxis_range=['Bandung', 'Cirebon'],
                              plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)",
                              xaxis=(dict(showgrid=False)),
                              yaxis=(dict(showgrid=False)),)
            st.plotly_chart(fig, use_container_width=True)

        with Q3:
            bar3 = bar.astype({'rating': float})
            columns3 = bar3[['city', 'rating']]
            fig = px.bar(columns3,
                         x='city',
                         y='rating',
                         labels={"rating": "Rating rata-rata", "city": "Kota"},
                         title='<b>Rating Rata-Rata Hotel per Kota/Kab</b>')
            fig.update_layout(title={'x': 0.5},
                              plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)",
                              xaxis=(dict(showgrid=False)),
                              yaxis=(dict(showgrid=False)))
            st.plotly_chart(fig, use_container_width=True)
    st.markdown('---')

# Menampilkan Piechart


def info3(df):
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            pai = df.groupby(['city']).count().reset_index()
            columns2 = pai[['city', 'location']]

            fig = px.pie(columns2, values='location', names='city',
                         labels={"location": "Total Ulasan", "city": "Kota"},
                         title='Total Ulasan Hotel di Jawa Barat')
            fig.update_traces(textposition='inside',
                              hoverinfo='label+percent', textinfo='percent', textfont_size=18)
            fig.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)'
            })
            st.plotly_chart(fig)

        with col2:
            # 4.0 changes
            html2 = """
                <!doctype html>
                <html lang="en">
                <style>
                .row-wrap {
                    text-align: center;
                    float: center;
                    margin: 0 10px;
                }

                .row-middle {
                    font-family: calibri;
                    font-size: 120px;
                }

                .row-bottom {
                    font-family: calibri;
                }
                </style>
                <body>
                        <center>
                        <h1 style="font-family:calibri">JUMLAH HOTEL TERBANYAK ADA DI BANDUNG DENGAN TOTAL</h1>
                        <div class="row-wrap">
                            <div class="row-middle">849</div>
                                <div class="row-bottom">Hotel</div>
                        </div>
                        </center>
                </body>
                </html>"""
            com.html(html2, width=600, height=500)

    with st.container():
        lom1, lom2 = st.columns((2, 2), gap='large')

        with lom2:
            dfpie = df
            carikotapie = dfpie['city'].unique()
            kotapie = st.selectbox(
                label='Pilih Kota:',
                options=carikotapie
            )
            carilokasipie = df.query(
                'city == @kotapie'
            ).reset_index(drop=True)
            removed = str(kotapie).replace("[", "")
            removed = removed.replace("]", "")
            removed = removed.replace("'", "")
            tittle = "Jumlah Hotel dengan ulasan tertentu di " + removed
            pai = carilokasipie.groupby(
                ["impression"]).count().reset_index()
            fig = px.pie(pai, values='city', names='impression',
                         labels={"impression": "Ulasan",
                                 "city": "Jumlah Kota"},
                         title=tittle)
            fig.update_layout({
                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                'paper_bgcolor': 'rgba(0, 0, 0, 0)'
            })
            st.plotly_chart(fig)

            with lom1:
                jumlah_hotel = carilokasipie.count().reset_index()
                htmlpie = """
                    <!doctype html>
                    <html lang="en">
                    <style>
                    .row-middle {
                    font-family: calibri;
                    font-size: 80px;
                    }
                    </style>
                    <body>
                            <center><h1 style="font-family:calibri">DISINI ANDA DAPAT MEMILIH UNTUK MENAMPILKAN PERSENTASE IMPRESSION HOTEL DI KOTA YANG ADA DI JAWA BARAT</h1>
                            <p style="font-family:calibri">Silahkan memilih untuk menampilkan ulasan hotel di kota/kab """+removed+"""</p>
                            <h1 class="row-middle">"""+str(jumlah_hotel.iloc[0, 1])+"""</h1><h3 style="font-family:calibri">Hotel Yang Di Ulas </h3>
                    </body>
                    </html>"""
                com.html(htmlpie, width=800, height=500)
# Menampilkan Folium Kota di Jawa Barat


def info4(df):
    with st.container():
        st.markdown("""
        <center><h1>Peta Data Hotel Jawa Barat</h1><h5>Berdasarkan Kabupaten dan Kota</h5></center>
        """, unsafe_allow_html=True)
        kolom1, kolom2, kolom3 = st.columns((1, 12, 1))
        with kolom2:
            Tampil(df, "city")

# Menampilkan Folium Detail Posisi Hotel


def detailpref(detail, tipe):
    jumlah = len(detail)
    if tipe == "hotel":
        for i in range(0, jumlah):
            def conten(df, i):
                com.html(html_hotel(df, i), width=1700, height=1000)
                return conten
            conten(detail, i)

# Menampilkan About


def about():
    # 4.0 changes
    html = """
<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
        crossorigin="anonymous"></script>
</head>
<style>
    .card {
    background-color: #9999992b;
    backdrop-filter: blur(14px);
    border: 0px solid rgb(0 0 0 / 0%);
    box-shadow: 0 15px 25px rgba(129, 124, 124, 0.9);
    }
</style>
<body style="background-color: transparent;">
    <div class="container-fluid">
        <center>
            <p class="fs-1 fw-bold">PyTorch</p>
        </center>
        <hr>
    </div>
    <div class="container">
        <div class="row">
            <div class="col">
                <div class="container">
                    <div class="card mb-3" style="max-width: 540px;">
                        <div class="row g-0">
                            <div class="col-md-5">
                            <img src='https://cdn.discordapp.com/attachments/934418750646677554/1070340230839803994/abdul.jpg' class="img rounded-start" alt="Card title" style="max-height:170px">
                            </div>
                            <div class="col-md-7">
                                <div class="card-body">
                                    <h5 class="card-title">MUHAMMAD ABDUL ROHMAN SIDIK</h5>
                                    <p class="card-title">10121122</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col">
                <div class="container">
                    <div class="card mb-3" style="max-width: 540px;">
                        <div class="row g-0">
                            <div class="col-md-5">
                                <img src='https://cdn.discordapp.com/attachments/1043917615233519619/1071531819977158796/image.png' class="img rounded-start" alt="Card title" style="max-height:170px">
                            </div>
                            <div class="col-md-7">
                                <div class="card-body">
                                    <h5 class="card-title">A. MUH. ARYA TENRI AJENG</h5>
                                    <p class="card-title">10121087</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col">
                <div class="container">
                    <div class="card mb-3" style="max-width: 540px;">
                        <div class="row g-0">
                            <div class="col-md-5">
                                <img src="https://cdn.discordapp.com/attachments/934418750646677554/1070340788715790406/adib.jpeg" class="img rounded-start" alt="Card title" style="max-height:170px">
                            </div>
                            <div class="col-md-7">
                                <div class="card-body">
                                    <h5 class="card-title">ADIB JAHFAL AL ASYARY</h5>
                                    <p class="card-title">1012108</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="row">
            <div class="col">
                <div class="container">
                    <div class="card mb-3" style="max-width: 540px;">
                        <div class="row g-0">
                            <div class="col-md-5">
                                <img src="https://cdn.discordapp.com/attachments/934418750646677554/1070340788946473030/rozaan.jpg" class="img rounded-start" alt="Card title" style="max-height:170px">
                            </div>
                            <div class="col-md-7">
                                <div class="card-body">
                                    <h5 class="card-title">MUHAMMAD ROZAAN ALDRIANTAMA</h5>
                                    <p class="card-title">10121111</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col">
            </div>
            <div class="col">
                <div class="container">
                    <div class="card mb-3" style="max-width: 540px;">
                        <div class="row g-0">
                            <div class="col-md-5">
                                <img src="https://cdn.discordapp.com/attachments/934418750646677554/1070667904242155570/img.jpg" class="img rounded-start" alt="Card title" style="max-height:170px">
                            </div>
                            <div class="col-md-7">
                                <div class="card-body">
                                    <h5 class="card-title">MUCHAMMAD DAFFA ABDULLOH</h5>
                                    <p class="card-title">10121120</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="container-fluid">
        <div class="card text-start">
            <h1 class="card-title">Deskripsi</h1>
            <div class="card-body">
                <h4 class="card-title">Latar Belakang</h4>
                <p class="card-text">Penginapan atau Hotel biasanya sangat di butuhkan oleh orang - orang, baik
                    wisatawan atau pekerja yang sedang berdinas di luar kota. Oleh karena itu kami memilih topik ini agar
                    kedepannya aplikasi yang kami buat dapat digunakan atau dijadikan referensi oleh orang - orang agar
                    mempermudah mereka dalam mencari penginapan atau hotel khususnya di Jawa Barat</p>
            </div>
            <div class="card-body">
                <h4 class="card-title">Tujuan</h4>
                <p class="card-text">Tujuan dari dibuatnya aplikasi ini adalah untuk memudahkan para wisatawan yang
                    ingin mencari hotel di Jawa Barat dengan melihat perbandingan harga maupun rating di setiap kotanya
                    bahkan bisa dibandingkan antar hotelnya, selain itu pengguna bisa melihat secara langsung letak
                    hotel yang mereka cari dan membandingkannya langsung didalam map yang sudah di sajikan</p>
            </div>
            <div class="card-body">
                <h4 class="card-title">Pengambilan Data</h4>
                <p class="card-text">Data yang tersaji dalam aplikasi ini di ambil dari website Tiket.com dengan
                    menggunakan metode html parsing dengan menggunakan tools python BeautifulSoup. Pengambilan data
                    diambil dengan cara memparsing data website perpage mengambil data penting dan mengambil data url
                    subpage hotel kemudian diparsing kembali untuk mengambil data yang di butuhkan</p>
            </div>
        </div>
    </div>


</body>

</html>"""
    return com.html(html, width=1700, height=1000)


# Menampilkan Footer
def footer():
    st.markdown("""
    <footer class="css-164nlkn egzxvld1"><center> by KELOMPOK PyTorch IF-3</center>
    </footer>
    """, unsafe_allow_html=True)
