import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import unicodedata
import copy
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Dashboard Sales Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.cache_data.clear()

# ==========================
# PETA
# ==========================
def normalize(name: str) -> str:
    name = str(name).strip().lower()
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    name = name.replace('.', '')
    name = name.replace('-', ' ')
    name = " ".join(name.split())
    return name.strip()

ALIAS = {
    'dki jakarta': 'dki jakarta',
    'yogyakarta': 'yogyakarta',
    'kepulauan bangka belitung': 'bangka belitung',
    'bangka belitung': 'bangka belitung',
    'kepulauan riau': 'kepulauan riau',
    'banten': 'probanten',
    'di yogyakarta': 'daerah istimewa yogyakarta',
}

def alias_key(name: str) -> str:
    n = normalize(name)
    return ALIAS.get(n, n)

@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province-simple.json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    geojson_data = resp.json()
    
    for feature in geojson_data['features']:
        nama_asli_geojson = feature['properties']['Propinsi']
        feature['properties']['match_key'] = alias_key(nama_asli_geojson)
        
    return geojson_data

indo_geojson = load_geojson()

# ==========================
# CSS
# ==========================
st.markdown("""
<style>

/* SEMBUNYIKAN TOOLBAR BAWAAN STREAMLIT, TAPI JANGAN HILANGKAN TOMBOL SIDEBAR */
/* ================= HILANGKAN GAP STREAMLIT ================= */

html,
body,
.stApp{
    margin:0 !important;
    padding:0 !important;
}

/* Header bawaan Streamlit */
header[data-testid="stHeader"]{
    display:none !important;
    height:0 !important;
    min-height:0 !important;
    max-height:0 !important;
    padding:0 !important;
    margin:0 !important;
}

/* Toolbar bawaan Streamlit */
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu,
footer{
    display:none !important;
    visibility:hidden !important;
    height:0 !important;
    min-height:0 !important;
    max-height:0 !important;
    padding:0 !important;
    margin:0 !important;
}

/* Container utama */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
section.main{
    padding-top:0 !important;
    margin-top:0 !important;
}

/* Block container */
.block-container{
    padding-top:0 !important;
    padding-bottom:0 !important;
    padding-left:0 !important;
    padding-right:1rem !important;
    margin-top:0 !important;
    max-width:100% !important;
}

/* Hilangkan jarak pada horizontal block pertama */
div[data-testid="stHorizontalBlock"]{
    margin-top:0 !important;
    padding-top:0 !important;
}

div[data-testid="stVerticalBlock"]{
    margin-top:0 !important;
    padding-top:0 !important;
}

/* BACKGROUND */
.stApp{
    background:#EAF5FF;
}

section.main{
    padding-top:0 !important;
}

/* ================= CARD ================= */

.st-key-summary_card,
.st-key-trend_card,
.st-key-top_card,
.st-key-row2_left_card,
.st-key-row2_middle_card,
.st-key-row2_right_card{
    height:210px !important;
    min-height:210px !important;
    max-height:210px !important;
    box-sizing:border-box !important;
            
    background:white;
    border-radius:12px;
    padding:8px 14px;
    box-shadow:0 3px 10px rgba(0,0,0,.08);
    overflow:visible;
}

/* ---------- ROW 1 ---------- */

/* Summary */
.st-key-summary_card{
    overflow:hidden !important;
}

/* Trend */
.st-key-trend_card{
}

/* ---------- ROW 2 ---------- */

/* Province (tall, kiri) */
.st-key-row2_left_card{
    padding:8px 18px 16px 18px !important;
    overflow:hidden !important;
}

/* Top Product (bawah kiri) */
.st-key-top_card{
    overflow:hidden;
}

/* Category (kanan atas) */
.st-key-row2_middle_card{
}

/* Return (kanan bawah) */
.st-key-row2_right_card{
}

/* ================= HEADINGS ================= */

.st-key-summary_card h3,
.st-key-trend_card h3,
.st-key-top_card h3,
.st-key-row2_left_card h3,
.st-key-row2_middle_card h3,
.st-key-row2_right_card h3{
    font-size:15px;
    margin:0 0 6px 0;
}

[data-testid="stMetricValue"]{
    font-size:20px !important;
}

[data-testid="stMetricLabel"]{
    font-size:12px !important;
}

/* ================= TEXT ================= */

.st-key-summary_card *,
.st-key-trend_card *,
.st-key-top_card *,
.st-key-row2_left_card *,
.st-key-row2_middle_card *,
.st-key-row2_right_card *{

    color:black !important;
}

[data-testid="stMetricLabel"]{
    color:#555 !important;
}

[data-testid="stMetricValue"]{
    color:#111 !important;
}

/* ================= SALES SUMMARY BOXES ================= */

.summary-grid{
    display:flex !important;
    gap:12px !important;
    margin-top:10px !important;
    margin-bottom:0 !important;
    height:160px !important;
    align-items:stretch !important;
}

.summary-box{
    flex:1 !important;
    background:#1B2559 !important;
    border-radius:14px !important;
    padding:14px 14px !important;
    display:flex !important;
    flex-direction:column !important;
    align-items:flex-start !important;
    justify-content:center !important;
    height:160px !important;
    width:auto !important;
    box-sizing:border-box !important;
}

.summary-icon{
    width:27px;
    height:27px;
    border-radius:50%;
    background:#eaf5ff;
    color:#FFFFFF !important;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:15px;
    margin-bottom:10px;
}

.summary-value{
    font-size:20px;
    font-weight:700;
    color:white !important;
    line-height:1.1;
}

.summary-label{
    font-size:12.5px;
    color:#64748B !important;
    margin-top:2px;
}
            
/* ================= CUSTOM LEFT NAVBAR ================= */

/* Panel utama navbar kiri */
.st-key-left_navbar{
    background:#1B2559;
    border-radius:0;
    padding:24px 14px 16px 14px;
    box-shadow:none;

    position:fixed;
    top:0;
    left:0;
    bottom:0;

    width:calc(20vw - 28px);
    height:100dvh;
    min-height:100dvh;

    border:none;
    margin:0;
    box-sizing:border-box;
    z-index:999;

    overflow-y:auto;
    overflow-x:hidden;
}
            
/* Kolom kiri jangan punya padding/margin tambahan */
div[data-testid="column"]:has(.st-key-left_navbar){
    padding:0 !important;
    margin:0 !important;
}

/* Isi navbar memenuhi tinggi */
.st-key-left_navbar > div{
    height:100%;
}
            
/* Semua teks di dalam navbar */
.st-key-left_navbar *{
    color:#0F172A !important;
}

/* Header brand navbar */
.navbar-brand{
    display:flex;
    align-items:center;
    gap:10px;
    padding:10px 8px 16px 8px;
    margin-bottom:14px;
    border-bottom:1px solid rgba(255, 255, 255, 0.30);
}

/* Ikon dashboard */
.navbar-logo{
    width:38px;
    height:38px;
    border-radius:11px;
    background:#DCEAFB;
    color:#FFFFFF !important;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:18px;
    flex-shrink:0;
}

/* Judul Sales Report */
.navbar-title{
    font-size:16px;
    font-weight:800;
    line-height:1.15;
    color:#FFFFFF !important;
}

/* Subtitle Dashboard */
.navbar-subtitle{
    font-size:12px;
    font-weight:500;
    color:#64748B !important;
    margin-top:4px;
}

/* Label FILTER TAHUN */
.navbar-section{
    font-size:11px;
    font-weight:800;
    letter-spacing:.08em;
    color:#8A94B4 !important;
    text-transform:uppercase;

    margin:0 !important;
    padding-left:0 !important;
}
            
/* ================= FILTER BUTTONS NAVBAR ================= */

.st-key-filter_buttons{
    margin-top:0 !important;
    padding-top:0 !important;
}

/* Wrapper utama isi filter */
.st-key-filter_buttons > div{
    display:flex !important;
    flex-direction:column !important;
    gap:10px !important;
}

/* Hilangkan margin bawaan Streamlit di setiap button */
.st-key-filter_buttons [data-testid="element-container"]{
    margin:0 !important;
    padding:0 !important;
    height:auto !important;
    min-height:0 !important;
}

/* Wrapper button */
.st-key-filter_buttons div[data-testid="stButton"]{
    width:100% !important;
    margin:0 !important;
    padding:0 !important;
}

/* Button tahun */
.st-key-filter_buttons div[data-testid="stButton"] > button{
    width:100% !important;
    min-width:100% !important;

    height:52px !important;
    min-height:52px !important;

    border-radius:14px !important;
    padding:0 16px !important;
    margin:0 !important;

    display:flex !important;
    align-items:center !important;
    justify-content:center !important;

    font-size:14px !important;
    font-weight:800 !important;

    border:1px solid transparent !important;
    box-shadow:none !important;
}

/* Teks di dalam button */
.st-key-filter_buttons div[data-testid="stButton"] > button p{
    margin:0 !important;
    padding:0 !important;
    white-space:nowrap !important;
    font-size:14px !important;
    font-weight:800 !important;
}

/* Button tahun */
.st-key-left_navbar div[data-testid="stButton"] > button{
    width:100% !important;
    min-width:100% !important;
    height:54px !important;
    border-radius:14px !important;

    display:flex !important;
    align-items:center !important;
    justify-content:center !important;

    padding:0 16px !important;
    font-size:14px !important;
    font-weight:800 !important;

    border:1px solid transparent !important;
    box-shadow:none !important;
}

/* Teks di dalam button */
.st-key-left_navbar div[data-testid="stButton"] > button p{
    margin:0 !important;
    padding:0 !important;
    white-space:nowrap !important;
    font-size:14px !important;
    font-weight:700 !important;
}

/* Button tidak aktif */
.st-key-filter_buttons div[data-testid="stButton"] > button[kind="secondary"]{
    background:transparent !important;
    color:#FFFFFF !important;
}

/* Teks button tidak aktif */
.st-key-filter_buttons div[data-testid="stButton"] > button[kind="secondary"] p{
    color:#FFFFFF !important;
}

/* Hover button tidak aktif */
.st-key-filter_buttons div[data-testid="stButton"] > button[kind="secondary"]:hover{
    background:#C7DBF4 !important;
    border:1px solid #B4CDEC !important;
    color:#1B2559 !important;
}

.st-key-filter_buttons div[data-testid="stButton"] > button[kind="secondary"]:hover p{
    color:#1B2559 !important;
}

/* Button aktif */
.st-key-filter_buttons div[data-testid="stButton"] > button[kind="primary"]{
    background:#DCEAFB !important;
    color:#1B2559 !important;
    border:1px solid #DCEAFB !important;
    box-shadow:none !important;
}

.st-key-filter_buttons div[data-testid="stButton"] > button[kind="primary"] p{
    color:#000000 !important;
}

/* Footer kecil navbar */
.navbar-footer{
    position:absolute;
    left:12px;
    right:12px;
    bottom:14px;
    padding:10px;
    border-radius:12px;
    background:rgba(255,255,255,.55);
    border:1px solid rgba(255,255,255,.65);
    font-size:11.5px;
    color:#475569 !important;
    line-height:1.35;
}
            
/* ================= POSISI FILTER BUTTONS ================= */

.st-key-filter_buttons{
    position:absolute !important;
    top:135px !important;
    left:0 !important;
    right:0 !important;

    margin:0 !important;
    padding:0 18px 0 18px !important;
    box-sizing:border-box !important;
}

/* Isi container tombol */
.st-key-filter_buttons > div{
    display:flex !important;
    flex-direction:column !important;
    gap:10px !important;

    margin:0 !important;
    padding:0 !important;
}

/* Hilangkan jarak bawaan Streamlit */
.st-key-filter_buttons [data-testid="element-container"]{
    margin:0 !important;
    padding:0 !important;
    height:auto !important;
    min-height:0 !important;
}

/* Wrapper button */
.st-key-filter_buttons div[data-testid="stButton"]{
    width:100% !important;
    margin:0 !important;
    padding:0 !important;
}

/* Button tahun */
.st-key-filter_buttons div[data-testid="stButton"] > button{
    width:100% !important;
    min-width:100% !important;

    height:52px !important;
    min-height:52px !important;

    border-radius:14px !important;
    padding:0 16px !important;
    margin:0 !important;

    display:flex !important;
    align-items:center !important;
    justify-content:center !important;

    font-size:14px !important;
    font-weight:800 !important;

    border:1px solid transparent !important;
    box-shadow:none !important;
}

/* Teks button */
.st-key-filter_buttons div[data-testid="stButton"] > button p{
    margin:0 !important;
    padding:0 !important;
    white-space:nowrap !important;
    font-size:14px !important;
    font-weight:800 !important;
}

/* ================= MAP FULLSCREEN BUTTON ================= */

/* Wrapper tombol fullscreen */
.st-key-map_fullscreen_btn{
    display:flex !important;
    justify-content:flex-end !important;
    align-items:flex-start !important;
    margin:0 !important;
    padding:0 !important;
}

/* Hilangkan jarak bawaan Streamlit */
.st-key-map_fullscreen_btn [data-testid="element-container"]{
    margin:0 !important;
    padding:0 !important;
}

/* Tombol fullscreen */
.st-key-map_fullscreen_btn button{
    width:32px !important;
    height:32px !important;
    min-width:32px !important;
    min-height:32px !important;

    padding:0 !important;
    margin:0 !important;

    border-radius:8px !important;
    background:#DCEAFB !important;
    border:1px solid #C7DBF4 !important;

    color:#1B2559 !important;
    font-size:14px !important;
    font-weight:800 !important;

    display:flex !important;
    align-items:center !important;
    justify-content:center !important;

    box-shadow:none !important;
    line-height:1 !important;
}

/* Hover */
.st-key-map_fullscreen_btn button:hover{
    background:#C7DBF4 !important;
    border:1px solid #AFCDF2 !important;
    color:#1B2559 !important;
}

/* Teks/icon di dalam tombol */
.st-key-map_fullscreen_btn button p{
    margin:0 !important;
    padding:0 !important;
    color:#1B2559 !important;
    font-size:14px !important;
    line-height:1 !important;
}

.st-key-map_fullscreen_btn{
    margin-top:5px !important;
}   


</style>
""", unsafe_allow_html=True)

# ==========================
# DATA
#===========================

df_raw = pd.read_csv("Data/data_penjualan_clean.csv")

# Ubah order_date menjadi datetime
df_raw['order_date'] = pd.to_datetime(df_raw['order_date'])

# Hitung revenue
df_raw['revenue'] = df_raw['final_price'] * df_raw['quantity']

# Ambil tahun dari order_date
df_raw['year'] = df_raw['order_date'].dt.year


# ==========================
# CUSTOM LEFT NAVBAR
# ==========================

nav_col, main_col = st.columns([0.20, 0.80], gap="small")

with nav_col:
    with st.container(key="left_navbar"):

        st.markdown(
            """
            <div class="navbar-brand">
                <div class="navbar-logo">📊</div>
                <div>
                    <div class="navbar-title">Sales Report</div>
                    <div class="navbar-subtitle">Dashboard</div>
                </div>
            </div>

            <div class="navbar-section">Filter Tahun</div>
            """,
            unsafe_allow_html=True
        )

        if "selected_year" not in st.session_state:
            st.session_state.selected_year = "Semua Tahun"

        menu_tahun = ["Semua Tahun", "2023", "2022", "2021"]

        with st.container(key="filter_buttons"):
            for tahun in menu_tahun:
                button_type = "primary" if st.session_state.selected_year == tahun else "secondary"

                if st.button(
                    tahun,
                    key=f"nav_{tahun}",
                    use_container_width=True,
                    type=button_type
                ):
                    st.session_state.selected_year = tahun
                    st.rerun()

        selected_year = st.session_state.selected_year


# Filter data berdasarkan pilihan navbar
if selected_year == "Semua Tahun":
    df = df_raw.copy()
else:
    df = df_raw[df_raw['year'] == int(selected_year)].copy()


# Jika data kosong
if df.empty:
    st.warning(f"Tidak ada data untuk pilihan: {selected_year}")
    st.stop()


# Group per bulan berdasarkan data yang sudah difilter
monthly_sales = (
    df.groupby(df['order_date'].dt.to_period('M'))
      .agg(
          revenue=("revenue", "sum"),
          total_orders=("order_id", "nunique")
      )
      .reset_index()
)

def format_rupiah(value):
    if value >= 1_000_000_000:
        return f"Rp {value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"Rp {value/1_000_000:.2f}M"
    else:
        return f"Rp {value:,.0f}"
    

monthly_sales["order_date"] = monthly_sales["order_date"].astype(str)
monthly_sales["revenue_label"] = monthly_sales["revenue"].apply(format_rupiah)

df['match_key'] = df['customer_province'].apply(alias_key)

revenue_provinsi = (
    df.groupby(['customer_province', 'match_key'])
      .agg(
          revenue=("revenue", "sum"),
          total_orders=("order_id", "nunique")
      )
      .reset_index()
)

revenue_provinsi['Total Revenue'] = revenue_provinsi['revenue'].apply(format_rupiah)


geojson_keys = {
    feature['properties']['match_key']
    for feature in indo_geojson['features']
}

dataset_keys = set(revenue_provinsi['match_key'])

unmatched_province = sorted(dataset_keys - geojson_keys)

if unmatched_province:
    st.warning(f"Provinsi belum cocok dengan GeoJSON: {unmatched_province}")



# ==========================
# SALES SUMMARY
# ==========================

# Revenue
total_revenue = (df['final_price'] * df['quantity']).sum()


# Total Order
total_orders = df['order_id'].nunique()

# Return Rate
return_rate = (df['is_returned'].sum() / total_orders) * 100 if total_orders > 0 else 0

# Rating Rata-rata
avg_rating = df['rating'].mean()

# ==========================
# RETURN ANALYSIS
# ==========================

return_df = (
    df[df["is_returned"] == True]
    .groupby("return_reason")
    .size()
    .reset_index(name="total_return")
    .sort_values("total_return", ascending=True)
)

# ==========================
# REVENUE PER PRODUCT CATEGORY
# ==========================

revenue_category = (
    df.groupby("product_category")["revenue"]
    .sum()
    .reset_index()
    .sort_values("revenue", ascending=True)
)
revenue_category['revenue_label'] = revenue_category['revenue'].apply(format_rupiah)

# ==========================
# TOP 10 SUBPRODUCT
# ==========================

top_product = (
    df.groupby("product_subcategory")
      .agg(
          sales=("order_id", "nunique")
      )
      .reset_index()
      .sort_values("sales", ascending=False)
      .head(10)
)

# ==========================
# CHART
# ==========================

def lighten_color(hex_color, amount):
    """
    amount:
    0   = warna asli
    1   = putih
    0.5 = 50% lebih terang
    """
    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)

    return f"#{r:02x}{g:02x}{b:02x}"


def generate_base_gradient(n, base_color="#1B2559"):
    if n <= 1:
        return [base_color]

    # Karena revenue_category kamu ascending,
    # data paling besar biasanya tampil di paling atas.
    # Maka warna dibuat: bawah terang -> atas gelap.
    light_amounts = [
        0.72 - (i * (0.72 / (n - 1)))
        for i in range(n)
    ]

    return [
        lighten_color(base_color, amount)
        for amount in light_amounts
    ]

def hex_to_rgba(hex_color, alpha=1):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def render_top10_subcategory_table(data):
    base_color = "#1B2559"

    if data.empty:
        return """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            html, body {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                font-family: Arial, sans-serif;
                background: transparent;
                overflow: hidden;
            }

            .top10-empty {
                color: #64748B;
                font-size: 12px;
                padding: 8px 0;
            }
        </style>
        </head>

        <body>
            <div class="top10-empty">No data available</div>
        </body>
        </html>
        """

    df_top = data.copy().reset_index(drop=True)
    df_top["rank"] = df_top.index + 1

    rows_html = ""

    for _, row in df_top.iterrows():
        rows_html += f"""
        <div class="top10-row">
            <div class="top10-rank">{int(row['rank'])}</div>

            <div class="top10-name">
                {row['product_subcategory']}
            </div>

            <div class="top10-sales">
                <span class="top10-sales-badge">{int(row['sales']):,}</span>
            </div>
        </div>
        """

    table_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            font-family: Arial, sans-serif;
            background: transparent;
            overflow: hidden;
        }}

        .top10-table {{
            width: 100%;
            height: 100%;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            background: transparent;
        }}

        .top10-header,
        .top10-row {{
            display: grid;
            grid-template-columns: 45px minmax(120px, 1fr) 90px;
            align-items: center;
            column-gap: 10px;
        }}

        .top10-header {{
            color: #8A94B4;
            font-size: 11px;
            font-weight: 700;
            padding: 0 2px 7px 2px;
            border-bottom: 1px solid #E9EEF7;
            flex-shrink: 0;
        }}

        .top10-body {{
            flex: 1;
            min-height: 0;
            overflow-y: auto;
            overflow-x: hidden;
            padding-right: 4px;
        }}

        .top10-body::-webkit-scrollbar {{
            width: 5px;
        }}

        .top10-body::-webkit-scrollbar-track {{
            background: #EEF2F8;
            border-radius: 999px;
        }}

        .top10-body::-webkit-scrollbar-thumb {{
            background: {base_color};
            border-radius: 999px;
        }}

        .top10-row {{
            padding: 9px 2px;
            border-bottom: 1px solid #EEF2F8;
        }}

        .top10-row:last-child {{
            border-bottom: none;
        }}

        .top10-rank {{
            color: {base_color};
            font-size: 12px;
            font-weight: 700;
           
        }}

        .top10-name {{
            color: {base_color};
            font-size: 12px;
            font-weight: 700;
            line-height: 1.25;
            word-break: break-word;
        }}

        .top10-sales {{
            text-align: right;
        }}

        .top10-sales-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 54px;
            height: 24px;
            padding: 0 9px;
            border-radius: 10px;
            border: 1.3px solid rgba(27, 37, 89, 0.55);
            color: {base_color};
            background: #FFFFFF;
            font-size: 12px;
            font-weight: 800;
            box-sizing: border-box;
        }}
    </style>
    </head>

    <body>
        <div class="top10-table">
            <div class="top10-header">
                <div>No</div>
                <div>Name</div>
                <div style="text-align:right;">Total Sales</div>
            </div>

            <div class="top10-body">
                {rows_html}
            </div>
        </div>
    </body>
    </html>
    """

    return table_html

category_colors = generate_base_gradient(
    len(revenue_category),
    base_color="#1B2559"
)

return_colors = generate_base_gradient(
    len(return_df),
    base_color="#1B2559"
)



# Line chart
fig = px.line(
    monthly_sales,
    x='order_date',
    y='revenue',
    markers=True,
    custom_data=[
        "revenue_label",
        "total_orders"
    ]
)

fig.update_traces(
    line=dict(
        color="#1B2559",
        width=3
    ),
    marker=dict(
        color="#1B2559",
        size=7
    ),
    hovertemplate=
    "<b>%{x}</b><br>" +
    "Revenue: %{customdata[0]}<br>" +
    "Total Order: %{customdata[1]:,}" +
    "<extra></extra>"
    
)

fig.update_layout(
    height=160,
    margin=dict(l=10, r=10, t=30, b=10),

    paper_bgcolor="white",
    plot_bgcolor="white",

    font=dict(color="black"),

    hoverlabel=dict(
        bgcolor="#EAF5FF",
        font_size=12,
        font_color="black"
    ),

    xaxis_title=None,
    yaxis_title=None,
    dragmode=False,

    xaxis=dict(
        showgrid=False,
        tickfont=dict(color="black"),
        fixedrange=True
    ),

    yaxis=dict(
        showgrid=True,
        gridcolor="#E5E7EB",
        tickfont=dict(color="black"),
        fixedrange=True
    )
)

fig_return = px.bar(
    return_df,
    x="total_return",
    y="return_reason",
    orientation="h",
    text="total_return",
    custom_data=[
        "return_reason",
        "total_return"
    ]
)

fig_return.update_traces(
    marker=dict(
        color=return_colors,
        line=dict(
            color="white",
            width=1
        )
    ),
    textposition="inside",
    insidetextanchor="end",
    textfont=dict(color="white", size=12),
    hovertemplate=
    "<b>Return Reason: %{customdata[0]}</b><br>" +
    "Total Return: %{customdata[1]:,}" +
    "<extra></extra>"
)

fig_return.update_layout(

    height=160,

    paper_bgcolor="white",
    plot_bgcolor="white",

    margin=dict(l=10, r=10, t=10, b=10),

    xaxis_title=None,
    yaxis_title=None,
    dragmode=False,

    font=dict(color="black"),

    hoverlabel=dict(
        bgcolor="#EAF5FF",
        font_size=12,
        font_color="black"
    ),

    xaxis=dict(
        showgrid=True,
        gridcolor="#E5E7EB",
        tickfont=dict(color="black"),
        fixedrange=True
    ),

    yaxis=dict(
        showgrid=False,
        tickfont=dict(color="black"),
        fixedrange=True
    )
)

fig_category = px.bar(
    revenue_category,
    x="revenue",
    y="product_category",
    orientation="h",
    text="revenue_label",
    custom_data=[
        "product_category",
        "revenue_label"
    ]
)

fig_category.update_traces(
    marker=dict(
        color=category_colors,
        line=dict(
            color="white",
            width=1
        )
    ),
    textposition="inside",
    insidetextanchor="end",
    textfont=dict(color="white", size=12),
    hovertemplate=
    "<b>Category: %{customdata[0]}</b><br>" +
    "Revenue: %{customdata[1]}" +
    "<extra></extra>"
)

fig_category.update_layout(
    height=160,

    paper_bgcolor="white",
    plot_bgcolor="white",

    margin=dict(l=10, r=10, t=10, b=10),

    xaxis_title=None,
    yaxis_title=None,\
    dragmode=False,

    font=dict(color="black"),

    showlegend=False,
    coloraxis_showscale=False,

    hoverlabel=dict(
        bgcolor="#EAF5FF",
        font_size=12,
        font_color="black"
    ),

    xaxis=dict(
        showgrid=True,
        gridcolor="#E5E7EB",
        tickfont=dict(color="black"),
        fixedrange=True
    ),

    yaxis=dict(
        showgrid=False,
        tickfont=dict(color="black"),
        fixedrange=True
    )
)

blue_scale = [
    [0.0, "#DCEAFB"],
    [0.25, "#AFCDF2"],
    [0.50, "#5B9BD5"],
    [0.75, "#2563EB"],
    [1.0, "#1B2559"]
]

fig_map = px.choropleth_mapbox(
    revenue_provinsi,
    geojson=indo_geojson,
    locations='match_key',
    featureidkey='properties.match_key',
    color='revenue',
    color_continuous_scale=blue_scale,
    mapbox_style="carto-positron",
    zoom=4.0,
    center={"lat": -6.2, "lon": 110.5},
    opacity=0.9,
    custom_data=[
        "customer_province",
        "Total Revenue",
        "total_orders"
    ]
)

fig_map.update_traces(
    hovertemplate=
    "<b>%{customdata[0]}</b><br>" +
    "Revenue: %{customdata[1]}<br>" +
    "Total Order: %{customdata[2]:,}" +
    "<extra></extra>"
)

fig_map.update_layout(
    height=140,
    margin={"r":0, "t":0, "l":0, "b":0},
    paper_bgcolor="white",
    plot_bgcolor="white",
    coloraxis_showscale=False,
    dragmode=False,
    hoverlabel=dict(
        bgcolor="#EAF5FF",
        font_size=12,
        font_color="black"
    )
)

fig_map_fullscreen = copy.deepcopy(fig_map)

fig_map_fullscreen.update_layout(
    height=650,
    margin={"r":0, "t":0, "l":0, "b":0},
    paper_bgcolor="white",
    plot_bgcolor="white",
    coloraxis_showscale=False,
    dragmode="pan"
)

@st.dialog("Revenue per Province", width="large")
def show_map_fullscreen():
    st.plotly_chart(
        fig_map_fullscreen,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "scrollZoom": True,
            "displaylogo": False
        }
    )

    
# =====================================
# DASHBOARD
# =====================================
with main_col:
    # =====================================
    # ROW 1: Summary | Trend
    # =====================================

    row1_left, row1_right = st.columns([1.28, 1], gap="small")

    with row1_left:

        # ---------- Sales Summary ----------
        with st.container(key="summary_card"):

            st.markdown("### Sales Summary")

            st.markdown(f"""
            <div class="summary-grid">
                <div class="summary-box">
                    <div class="summary-icon">📊</div>
                    <div class="summary-value">{format_rupiah(total_revenue)}</div>
                    <div class="summary-label">Total Revenue</div>
                </div>
                <div class="summary-box">
                    <div class="summary-icon">📄</div>
                    <div class="summary-value">{total_orders:,}</div>
                    <div class="summary-label">Total Order</div>
                </div>
                <div class="summary-box">
                    <div class="summary-icon">⭐</div>
                    <div class="summary-value">{avg_rating:.2f}</div>
                    <div class="summary-label">Average Rating</div>
                </div>
                <div class="summary-box">
                    <div class="summary-icon">📦</div>
                    <div class="summary-value">{return_rate:.2f}%</div>
                    <div class="summary-label">Return Rate</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with row1_right:

        # ---------- Trend ----------
        with st.container(key="trend_card"):

            st.markdown("### Tren Penjualan")

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

    st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)

    # =====================================
    # ROW 2: (Province + Top Product) | (Category + Return)
    # =====================================

    row2_left, row2_right = st.columns([1.20, 1.60], gap="small")

    with row2_left:

        # ---------- Revenue Province ----------
        with st.container(key="row2_left_card"):

            map_title_col, map_btn_col = st.columns([0.94, 0.06])

            with map_title_col:
                st.markdown("### Revenue per Province")

            with map_btn_col:
                if st.button("⛶", key="map_fullscreen_btn", help="Fullscreen Mode"):
                    show_map_fullscreen()

            st.plotly_chart(
                fig_map,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "scrollZoom": True
                }
            )

        st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)

        # ---------- Top Product ----------
        with st.container(key="top_card"):

            st.markdown("### Top 10 Product Subcategory")

            components.html(
                render_top10_subcategory_table(top_product),
                height=160,
                scrolling=False
            )
    with row2_right:

        # ---------- Revenue Category ----------
        with st.container(key="row2_middle_card"):

            st.markdown("### Revenue per Category")

            st.plotly_chart(
                fig_category,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)

        # ---------- Return ----------
        with st.container(key="row2_right_card"):

            st.markdown("### Return Analysis")

            st.plotly_chart(
                fig_return,
                use_container_width=True,
                config={"displayModeBar": False}
            )