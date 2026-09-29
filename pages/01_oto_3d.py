
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from common import box, cylinder, setup_fig

st.set_page_config(page_title="Ô tô 3D", page_icon="🚗", layout="wide")

st.markdown("""
<style>
.stApp{background:radial-gradient(circle at 50% 5%,#14263c 0%,#07101b 52%,#040a12 100%);color:#eaf3ff}
.block-container{padding-top:1rem}
[data-testid="stMetric"]{background:#0b1726;border:1px solid #20344c;border-radius:10px}
div[data-testid="stExpander"]{background:#0b1726;border:1px solid #20344c;border-radius:10px}
</style>
""", unsafe_allow_html=True)

st.title("🚗 Ô TÔ 3D — PHÂN RÃ KỸ THUẬT")
st.caption("Trang riêng cho cấu tạo tổng thể của ô tô. Xoay, zoom và phân rã mô hình.")

parts=[
("Khung gầm","box",[0,0,.12],[1.7,4.1,.25],"#59636f"),
("Động cơ","box",[0,1.35,.72],[.95,1.15,.72],"#c62828"),
("Hộp số","box",[0,.25,.50],[.82,.95,.48],"#2869b8"),
("Két nước","box",[0,2.0,.65],[1.18,.12,.58],"#4f9ac0"),
("Ắc quy","box",[-.55,.85,.42],[.42,.55,.34],"#262b32"),
("Nội thất","box",[0,-.25,.78],[1.35,1.75,.72],"#252b33"),
("Mui xe","box",[0,1.48,1.16],[1.55,1.05,.10],"#bfc7d0"),
("Mái xe","box",[0,-.25,1.45],[1.52,1.75,.10],"#aeb7c1"),
("Cản trước","box",[0,2.35,.55],[1.78,.20,.42],"#aab3bd"),
("Cản sau","box",[0,-2.38,.55],[1.78,.20,.42],"#aab3bd"),
("Giảm xóc trước trái","cyl",[-.86,1.42,0],.09,.55,"#2e8b57"),
("Giảm xóc trước phải","cyl",[.86,1.42,0],.09,.55,"#2e8b57"),
("Giảm xóc sau trái","cyl",[-.86,-1.42,0],.09,.55,"#2e8b57"),
("Giảm xóc sau phải","cyl",[.86,-1.42,0],.09,.55,"#2e8b57"),
]

explode=st.sidebar.slider("Mức độ phân rã",0.0,1.0,.35,.02)
show=st.sidebar.checkbox("Hiện lưới",True)

fig=go.Figure()
dirs={
"Khung gầm":np.array([0,0,0]),"Động cơ":np.array([0,1.0,.5]),
"Hộp số":np.array([0,1.2,.3]),"Két nước":np.array([0,1.8,.5]),
"Ắc quy":np.array([-1,0,.6]),"Nội thất":np.array([0,0,1.0]),
"Mui xe":np.array([0,1.0,1.3]),"Mái xe":np.array([0,0,1.8]),
"Cản trước":np.array([0,2,.3]),"Cản sau":np.array([0,-2,.3])
}
for p in parts:
    name,kind,center,*rest=p
    if kind=="box":
        size,color=rest
        pos=np.array(center)+dirs.get(name,np.array([1 if "trái" in name else -1,0,-.5]))*explode
        fig.add_trace(box(pos,size,color,name))
    else:
        radius,height,color=rest
        side=-1 if "trái" in name else 1
        pos=np.array(center)+np.array([side*.7,0,-.55])*explode
        fig.add_trace(cylinder(pos,radius,height,color,name,"Z"))

# wheels
for x in [-.95,.95]:
    for y in [1.42,-1.42]:
        pos=np.array([x,y,-.18])+np.array([1.2*np.sign(x),0,-.6])*explode
        fig.add_trace(cylinder(pos,.38,.22,"#15191e","Bánh xe","X"))

fig.add_trace(go.Scatter3d(x=[-.95,.95],y=[1.42,1.42],z=[-.18,-.18],mode="lines",line=dict(color="#77818c",width=5)))
fig.add_trace(go.Scatter3d(x=[-.95,.95],y=[-1.42,-1.42],z=[-.18,-.18],mode="lines",line=dict(color="#77818c",width=5)))

setup_fig(fig,[-4,4],[-5,5],[-2.5,4],height=720)
fig.update_layout(scene=dict(
    xaxis=dict(title="X",range=[-4,4],showgrid=show),
    yaxis=dict(title="Y",range=[-5,5],showgrid=show),
    zaxis=dict(title="Z",range=[-2.5,4],showgrid=show),
    aspectmode="manual",aspectratio=dict(x=1,y=1.25,z=.78),
    camera=dict(eye=dict(x=1.65,y=1.8,z=1.2))
))
st.plotly_chart(fig,use_container_width=True,config={"displaylogo":False,"scrollZoom":True})

m=st.columns(5)
for col,val,label in zip(m,["32","1,45 t","4,80 m","1,85 m","1,45 m"],["Bộ phận","Khối lượng","Dài","Rộng","Cao"]):
    col.metric(label,val)

st.markdown("### 🔩 Các hệ thống chính")
for title,desc in [
("Khung gầm","Kết cấu chịu lực và nền tảng liên kết các hệ thống."),
("Động lực","Động cơ, hộp số, truyền động và hệ thống làm mát."),
("Treo & phanh","Kiểm soát dao động, bám đường và giảm tốc."),
("Thân vỏ","Các panel bảo vệ cabin và tạo hình khí động học."),
("Điện & điều khiển","Ắc quy, đèn, cảm biến và cơ cấu lái."),
]:
    with st.expander(title):
        st.write(desc)

st.page_link("app.py",label="← Trang chính",icon="🏠")
st.page_link("pages/02_dongcohopso.py",label="→ Sang Động cơ & Hộp số",icon="⚙️")
