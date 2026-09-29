
import streamlit as st

st.set_page_config(page_title="3D Vehicle Engineering Lab", page_icon="🚗", layout="wide")

st.markdown("""
<style>
.stApp{background:radial-gradient(circle at 50% 5%,#14263c 0%,#07101b 52%,#040a12 100%);color:#eaf3ff}
.block-container{padding-top:1rem}
[data-testid="stMetric"]{background:#0b1726;border:1px solid #20344c;border-radius:10px}
div[data-testid="stExpander"]{background:#0b1726;border:1px solid #20344c;border-radius:10px}
.badge{display:inline-block;padding:4px 9px;border-radius:999px;background:#12345a;color:#8fc7ff;font-size:12px}
</style>
""", unsafe_allow_html=True)

st.title("🚗 3D VEHICLE ENGINEERING LAB")
st.caption("Hệ thống mô phỏng cấu tạo ô tô — tách riêng xe tổng thể và cụm động cơ/hộp số.")

c1,c2,c3 = st.columns(3)
c1.metric("Trang mô phỏng","02")
c2.metric("Cụm chuyên sâu","Động cơ + Hộp số")
c3.metric("Công nghệ","Streamlit + Plotly + NumPy")

st.markdown("### 🧭 Chọn phòng nghiên cứu")
a,b = st.columns(2)
with a:
    st.info("🚗 **TRANG 1 — Ô TÔ 3D**\n\nKhung gầm, thân vỏ, bánh xe, phanh, treo, lái, nội thất, hệ thống nhiên liệu và xả.")
    st.pages_link("pages/01_Ô_TÔ_3D.py", label="Mở trang Ô TÔ 3D", icon="🚗")
with b:
    st.success("⚙️ **TRANG 2 — DONG CO & HOP SO**\n\nPhân rã sâu động cơ và hộp số: vỏ hộp số, trục vào, trục trung gian, trục ra, bánh răng và bộ đồng tốc.")
    st.pages_link("pages/02_Động_cơ_Hộp_số.py", label="Mở trang Động cơ & Hộp số", icon="⚙️")

st.markdown("---")
st.markdown("### 🧰 Cấu trúc dự án")
st.code("""Trang chính
├── 🚗 Ô tô 3D
│   ├── Khung gầm / thân vỏ
│   ├── Treo / phanh / lái
│   ├── Bánh xe
│   └── Nội thất
└── ⚙️ Động cơ & Hộp số
    ├── Động cơ I4
    └── Hộp số sàn 6 cấp mô phỏng
        ├── Vỏ hộp số
        ├── Trục sơ cấp
        ├── Trục trung gian
        ├── Trục thứ cấp
        ├── Bánh răng 1–6
        ├── Bánh răng số lùi
        ├── Bộ đồng tốc
        └── Vi sai""")
