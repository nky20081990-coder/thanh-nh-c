
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from common import box,cylinder,gear,shaft,setup_fig

st.set_page_config(page_title="Động cơ & Hộp số",page_icon="⚙️",layout="wide")

st.markdown("""
<style>
.stApp{background:radial-gradient(circle at 50% 5%,#14263c 0%,#07101b 52%,#040a12 100%);color:#eaf3ff}
.block-container{padding-top:1rem}
[data-testid="stMetric"]{background:#0b1726;border:1px solid #20344c;border-radius:10px}
div[data-testid="stExpander"]{background:#0b1726;border:1px solid #20344c;border-radius:10px}
</style>
""", unsafe_allow_html=True)

st.title("⚙️ ĐỘNG CƠ & HỘP SỐ — PHÂN RÃ CHUYÊN SÂU")
st.caption("Mô phỏng học thuật cụm động lực. Hộp số được dựng theo nguyên lý hộp số sàn nhiều cấp.")

tab1,tab2=st.tabs(["🔥 Động cơ I4","⚙️ Hộp số"])

with tab1:
    explode=st.slider("Mức phân rã động cơ",0.0,1.0,.25,.02,key="engine_ex")
    fig=go.Figure()
    parts=[
        ("Nắp máy", [0,0,.9],[1.25,1.0,.18],"#8c3434"),
        ("Thân máy", [0,0,.35],[1.15,1.05,.75],"#b83a3a"),
        ("Cácte dầu", [0,-.05,-.12],[1.15,1.1,.20],"#5d6670"),
        ("Cổ hút", [0,.72,.68],[.55,.55,.25],"#607d8b"),
        ("Cổ xả",[0,-.72,.60],[.62,.45,.25],"#9b6a3b"),
    ]
    for name,c,s,col in parts:
        pos=np.array(c)+np.array([0,0,explode*.65])
        fig.add_trace(box(pos,s,col,name))
    # 4 cylinders
    for x in [-.36,-.12,.12,.36]:
        pos=np.array([x,0,.82])+np.array([0,0,explode*.8])
        fig.add_trace(cylinder(pos,.095,.52,"#c6ccd1","Xi lanh","Z"))
    fig.add_trace(shaft([[-.5,-.0,.18],[.5,0,.18]],"#c2c7cd","Trục khuỷu",8))
    setup_fig(fig,[-1.8,1.8],[-1.7,1.7],[-1.4,2.4],height=620)
    st.plotly_chart(fig,use_container_width=True,config={"displaylogo":False,"scrollZoom":True})
    a,b,c,d=st.columns(4)
    a.metric("Kiểu","I4")
    b.metric("Dung tích minh họa","2.0 L")
    c.metric("Xi lanh","4")
    d.metric("Hệ thống","ICE")
    st.info("Đây là mô hình hình học minh họa nguyên lý, không đại diện kích thước của một động cơ thương mại cụ thể.")

with tab2:
    st.markdown("### ⚙️ Hộp số sàn 6 cấp — mô hình phân rã")
    col1,col2=st.columns([1,3])
    with col1:
        ex=st.slider("Mức phân rã hộp số",0.0,1.0,.45,.02)
        gear_mode=st.radio("Hiển thị",["Toàn bộ","Chỉ bánh răng","Chỉ trục & đồng tốc"])
        selected=st.selectbox("Chọn cụm",[
            "Vỏ hộp số","Trục sơ cấp","Trục trung gian","Trục thứ cấp",
            "Bánh răng 1","Bánh răng 2","Bánh răng 3","Bánh răng 4",
            "Bánh răng 5","Bánh răng 6","Bánh răng số lùi",
            "Bộ đồng tốc 1-2","Bộ đồng tốc 3-4","Bộ đồng tốc 5-6","Vi sai"
        ])
    with col2:
        fig=go.Figure()

        # housing halves
        if gear_mode=="Toàn bộ":
            fig.add_trace(box([0,0,0],[2.0,3.3,1.35],"#53606d","Vỏ hộp số",.32))

        # three parallel shafts
        shafts=[
            ("Trục sơ cấp",[-.65,0,.10],"#d0d6dc"),
            ("Trục trung gian",[0,0,-.25],"#aab3bc"),
            ("Trục thứ cấp",[.65,0,.10],"#d0d6dc")
        ]
        if gear_mode in ["Toàn bộ","Chỉ trục & đồng tốc"]:
            for name,c,col in shafts:
                pos=np.array(c)+np.array([0,0,ex*.65])
                fig.add_trace(cylinder(pos,.09,2.9,col,name,"Y"))

        # gears: paired gears along Y
        gear_specs=[
            ("Bánh răng 1",-.95,.38,.24),
            ("Bánh răng 2",-.58,.34,.21),
            ("Bánh răng 3",-.20,.30,.19),
            ("Bánh răng 4",.18,.28,.18),
            ("Bánh răng 5",.56,.25,.16),
            ("Bánh răng 6",.94,.23,.15),
            ("Bánh răng số lùi",1.28,.20,.13),
        ]
        for name,y,r1,r2 in gear_specs:
            # fixed gear on intermediate shaft
            if gear_mode in ["Toàn bộ","Chỉ bánh răng"]:
                p=np.array([0,y,-.25])+np.array([0,0,ex*.65])
                fig.add_trace(gear(p,r1,r1*.70,.22,"#2f75b5",name+" — trục trung gian",teeth=max(10,int(r1*34))))
                # mating gear on secondary
                p2=np.array([.65,y,.10])+np.array([0,0,ex*.65])
                fig.add_trace(gear(p2,r2,r2*.68,.18,"#b67b2d",name+" — trục thứ cấp",teeth=max(10,int(r2*38))))

        # synchronizers
        syncs=[
            ("Bộ đồng tốc 1-2",-.76),
            ("Bộ đồng tốc 3-4",.0),
            ("Bộ đồng tốc 5-6",.76)
        ]
        if gear_mode in ["Toàn bộ","Chỉ trục & đồng tốc"]:
            for name,y in syncs:
                p=np.array([.65,y,.10])+np.array([0,0,ex*.65])
                fig.add_trace(cylinder(p,.16,.18,"#d6a72c",name,"Y"))

        # selector/forks
        if gear_mode=="Toàn bộ":
            fig.add_trace(shaft([[.65,-.9,.42],[.65,.9,.42]],"#6fb1e8","Thanh chọn số",5))

        setup_fig(fig,[-1.8,1.8],[-1.9,1.9],[-1.5,1.8],height=680)
        st.plotly_chart(fig,use_container_width=True,config={"displaylogo":False,"scrollZoom":True})

    st.markdown("### 📚 Từ điển cấu tạo hộp số")
    descriptions={
        "Vỏ hộp số":"Bao kín và định vị các trục, ổ bi, bánh răng; đồng thời chứa dầu bôi trơn.",
        "Trục sơ cấp":"Nhận mô-men từ ly hợp và đưa công suất vào hộp số.",
        "Trục trung gian":"Mang các bánh răng chủ động và truyền công suất giữa các cấp.",
        "Trục thứ cấp":"Nhận mô-men sau khi chọn tỷ số truyền và truyền tới hệ thống truyền lực.",
        "Bộ đồng tốc 1-2":"Đồng bộ tốc độ giữa bánh răng và trục trước khi khóa cấp số.",
        "Bộ đồng tốc 3-4":"Đảm nhiệm quá trình đồng tốc và khóa số 3 hoặc 4.",
        "Bộ đồng tốc 5-6":"Đảm nhiệm quá trình đồng tốc và khóa số 5 hoặc 6.",
        "Vi sai":"Cho phép hai bánh chủ động quay với tốc độ khác nhau khi xe vào cua.",
    }
    if selected in descriptions:
        st.info(descriptions[selected])
    else:
        st.info("Bánh răng được mô phỏng theo kích thước tương đối để minh họa nguyên lý tỷ số truyền.")

    x,y,z,w=st.columns(4)
    x.metric("Cấp số tiến","6")
    y.metric("Số lùi","1")
    z.metric("Trục chính","3")
    w.metric("Đồng tốc","3 cụm")

st.markdown("---")
st.page_link("app.py",label="← Trang chính",icon="🏠")
st.page_link("pages/01_Ô_tô_3D.py",label="← Ô tô 3D",icon="🚗")
