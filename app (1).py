st.markdown("### 🧭 Chọn phòng nghiên cứu")

col1, col2 = st.columns(2)

with col1:
    st.info(
        "🚗 **TRANG 1 — Ô TÔ 3D**\n\n"
        "Khung gầm, thân vỏ, bánh xe, phanh, hệ thống treo, "
        "hệ thống lái, nội thất và các hệ thống phụ trợ."
    )

    st.page_link(
        "pages/01_oto_3d.py",
        label="Mở trang Ô tô 3D",
        icon="🚗"
    )

with col2:
    st.success(
        "⚙️ **TRANG 2 — ĐỘNG CƠ & HỘP SỐ**\n\n"
        "Động cơ I4, hộp số 6 cấp, bánh răng, trục, "
        "đồng tốc, số lùi và đường truyền mô-men."
    )

    st.page_link(
        "pages/02_dong_co_hop_so.py",
        label="Mở trang Động cơ & Hộp số",
        icon="⚙️"
    )
