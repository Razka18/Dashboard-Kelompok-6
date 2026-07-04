import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Dashboard Sales Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# GLOBAL STYLE (card look, background, spacing)
# =========================================================
st.markdown(
    """
    <style>
        .stApp {
            background-color: #dbe7f2;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1300px;
        }
        .dash-title {
            font-size: 28px;
            font-weight: 700;
            color: #14213d;
            margin-bottom: 1.2rem;
        }
        .card {
            background-color: #ffffff;
            border-radius: 18px;
            padding: 1.2rem 1.4rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            height: 100%;
            margin-bottom: 1.2rem;
        }
        .card-title {
            font-size: 14px;
            font-weight: 700;
            color: #14213d;
            margin-bottom: 0.8rem;
        }
        .metric-box {
            background-color: #eef2f7;
            border-radius: 14px;
            padding: 0.8rem;
            text-align: left;
        }
        .metric-icon {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background-color: #14213d;
            display: inline-block;
            margin-bottom: 0.4rem;
        }
        .metric-value {
            font-size: 18px;
            font-weight: 700;
            color: #14213d;
        }
        .metric-label {
            font-size: 11px;
            color: #6b7280;
        }
        .placeholder-box {
            background-color: #f4f6f9;
            border: 1px dashed #c3cbd6;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #9aa4b2;
            font-size: 13px;
        }
        .list-row {
            display: flex;
            justify-content: space-between;
            padding: 0.4rem 0;
            border-bottom: 1px solid #f0f2f5;
            font-size: 12px;
            color: #14213d;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# TITLE
# =========================================================
st.markdown('<div class="dash-title">Dashboard Sales Report</div>', unsafe_allow_html=True)

# =========================================================
# ROW 1 — Sales Summary | Tren Penjualan
# =========================================================
row1_col1, row1_col2 = st.columns([1, 1.3])

with row1_col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Sales Summary</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    metric_labels = ["Total Revenue", "Total Order", "Average Rating", "Return Rate"]
    for col, label in zip([m1, m2, m3, m4], metric_labels):
        with col:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-icon"></div>
                    <div class="metric-value">--</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Tren Penjualan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="placeholder-box" style="height:170px;">[ line chart placeholder ]</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ROW 2 — Revenue per Product Category | Payment Method Distribution
# =========================================================
row2_col1, row2_col2 = st.columns([1, 1.3])

with row2_col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Revenue per Product Category</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="placeholder-box" style="height:180px;">[ bar chart placeholder ]</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Payment Method Distribution</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="placeholder-box" style="height:180px;">[ bar chart placeholder ]</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ROW 3 — Revenue per Province/City (map) | Return Analysis + Top 10 list
# =========================================================
row3_col1, row3_col2 = st.columns([1, 1.3])

with row3_col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Revenue per Province atau City</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="placeholder-box" style="height:340px;">[ map placeholder ]</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with row3_col2:
    # Return Analysis card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Return Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="placeholder-box" style="height:140px;">[ bar chart placeholder ]</div>',
        unsafe_allow_html=True,
    )
    legend1, legend2 = st.columns(2)
    with legend1:
        st.markdown(
            '<div style="font-size:11px; color:#6b7280;">Reality Sales<br>'
            '<span style="color:#2ec4b6; font-weight:700;">--</span></div>',
            unsafe_allow_html=True,
        )
    with legend2:
        st.markdown(
            '<div style="font-size:11px; color:#6b7280;">Target Sales<br>'
            '<span style="color:#f4a261; font-weight:700;">--</span></div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Top 10 Product Subcategory card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Top 10 Product Subcategory</div>', unsafe_allow_html=True)

    header_l, header_m, header_r = st.columns([1, 3, 1])
    with header_l:
        st.markdown('<span style="font-size:11px; color:#9aa4b2;">#</span>', unsafe_allow_html=True)
    with header_m:
        st.markdown('<span style="font-size:11px; color:#9aa4b2;">Nama</span>', unsafe_allow_html=True)
    with header_r:
        st.markdown('<span style="font-size:11px; color:#9aa4b2;">Sales</span>', unsafe_allow_html=True)

    for i in range(1, 5):
        st.markdown(
            f"""
            <div class="list-row">
                <span>{i:02d}</span>
                <span style="flex:1; margin-left:12px;">Product name --</span>
                <span>--%</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)