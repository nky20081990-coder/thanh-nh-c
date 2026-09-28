import streamlit as pd
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Viện Học Thanh Nhạc Trực Tuyến - Tiến sĩ Thanh Nhạc",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Giao diện Tiêu đề chính
st.title("🎵 Viện Học Thanh Nhạc Trực Tuyến")
st.markdown("""
*Chào mừng các em đến với không gian học nhạc lý và luyện thanh tương tác. 
Hệ thống này được thiết kế theo tiêu chuẩn sư phạm âm nhạc chính quy, giúp các em vững nhạc lý, chuẩn cao độ và mở rộng tầm giọng tại nhà.*
""")

# Thanh bên (Sidebar) - Thông tin Giảng viên & Hướng dẫn cơ bản
with st.sidebar:
    st.header("👨‍🏫 Góc Tiến Sĩ Thanh Nhạc")
    st.info("""
    **Lời khuyên luyện tập:**
    1. Luôn giữ thẳng lưng khi ngồi hoặc đứng hát.
    2. Lấy hơi bằng bụng (cơ hoành), không nhấc vai.
    3. Mở vòm họng như khi đang ngáp ngủ để âm thanh vang và sáng hơn.
    """)
    
    st.subheader("📋 Các bước học tập")
    st.markdown("""
    - **Bước 1:** Học vị trí và cách mở khẩu hình 7 nốt cơ bản ở tab **1. Phím Đàn & Phát Âm**.
    - **Bước 2:** Nhận diện các ký hiệu âm nhạc cốt lõi ở tab **2. Ký Tự Nhạc Lý**.
    - **Bước 3:** Bật máy luyện thanh để tập mở giọng hàng ngày ở tab **3. Máy Luyện Thanh**.
    """)

# Tạo các Tab chức năng chính trên giao diện
tab1, tab2, tab3 = st.tabs(["🎹 1. Phím Đàn & Phát Âm", "🎼 2. Ký Tự Nhạc Lý", "🎤 3. Máy Luyện Thanh"])

# --- TAB 1: PHÍM ĐÀN VÀ PHÁT ÂM (Web Audio API tích hợp) ---
with tab1:
    st.header("Phím Đàn Tương Tác & Hướng Dẫn Khẩu Hình")
    st.caption("Nhấp vào từng phím đàn để nghe cao độ chuẩn và xem hướng dẫn mở khẩu hình từ Tiến sĩ.")
    
    # Nhúng HTML/JS chứa Audio Engine để phát âm thanh ngay lập tức không qua server
    piano_html = """
    <style>
        .piano-container { display: flex; justify-content: center; background: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .piano-key { width: 60px; height: 200px; background: white; border: 1px solid #ccc; border-radius: 0 0 5px 5px; cursor: pointer; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 15px; font-weight: bold; font-family: sans-serif; transition: background 0.1s; user-select: none; }
        .piano-key:active { background: #e0e0e0; }
        .info-card { background: #f0f2f6; border-left: 5px solid #ff4b4b; padding: 15px; border-radius: 5px; margin-top: 15px; font-family: sans-serif; min-height: 80px; }
    </style>

    <div class="piano-container">
        <div class="piano-key" onclick="playNote(261.63, 'Đô (Do)', 'Mở hàm theo chiều dọc, thả lỏng đầu lưỡi chạm vào răng hàm dưới. Âm thanh dày dặn.')">C4 (Đô)</div>
        <div class="piano-key" onclick="playNote(293.66, 'Rê (Re)', 'Khẩu hình hơi dẹt nhẹ so với Đô, đưa âm thanh ra phía trước răng cửa.')">D4 (Rê)</div>
        <div class="piano-key" onclick="playNote(329.63, 'Mi (Mi)', 'Khóe môi cười nhẹ, nâng cơ má (mask) để âm thanh bay, sáng và không bị sập tiếng.')">E4 (Mi)</div>
        <div class="piano-key" onclick="playNote(349.23, 'Fa (Fa)', 'Mở dọc hàm như nốt Đô nhưng đẩy hơi chủ động hơn để giữ vị trí âm thanh cao.')">F4 (Fa)</div>
        <div class="piano-key" onclick="playNote(392.00, 'Sol (Sol)', 'Vòm họng trong mở rộng tối đa (như ngáp), tạo khoảng vang lớn ở phía sau.')">G4 (Sol)</div>
        <div class="piano-key" onclick="playNote(440.00, 'La (La)', 'Thả lỏng toàn bộ cơ hàm, lưỡi nằm phẳng, phát âm tự nhiên và vang dội.')">A4 (La)</div>
        <div class="piano-key" onclick="playNote(493.88, 'Si (Si)', 'Vị trí âm thanh rất cao sát hốc mũi, chuẩn bị chuyển giao sang quãng cao (Head voice).')">B4 (Si)</div>
    </div>

    <div id="instruction-box" class="info-card">
        <strong>💡 Hướng dẫn từ Tiến sĩ:</strong> Chọn một nốt nhạc ở trên để nghe âm thanh và xem kỹ thuật hát!
    </div>

    <script>
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playNote(frequency, noteName, guide) {
            // Khởi tạo sóng âm phát tiếng piano mượt
            const osc = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(frequency, audioCtx.currentTime);
            
            // Tạo hiệu ứng âm thanh nhỏ dần (Fade out)
            gainNode.gain.setValueAtTime(0.5, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.2);
            
            osc.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            osc.start();
            osc.stop(audioCtx.currentTime + 1.2);
            
            // Cập nhật chỉ dẫn khẩu hình lên màn hình
            document.getElementById('instruction-box').innerHTML = `<strong>✨ Nốt ${noteName}:</strong> ${guide}`;
        }
    </script>
    """
    st.components.v1.html(piano_html, height=360)

# --- TAB 2: KÝ TỰ NHẠC LÝ ---
with tab2:
    st.header("Thư Viện Kí Tự Bản Nhạc")
    st.write("Hiểu rõ các biểu tượng này là chìa khóa để em tự đọc bất kỳ bản nhạc nào.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎼 Ký hiệu nền tảng")
        symbols = {
            "🎼 Khóa Sol (Treble Clef)": "Nằm ở đầu khuôn nhạc, xác định vị trí nốt Sol ở dòng kẻ thứ 2. Thường dùng cho các giọng ca cao và trung (Soprano, Mezzo, Tenor).",
            "𝄢 Khóa Fa (Bass Clef)": "Xác định nốt Fa ở dòng kẻ thứ 4. Thường dành cho các giọng ca trầm (Baritone, Bass) hoặc tay trái đàn Piano.",
            "𝄴 Số chỉ nhịp (Time Signature)": "Ví dụ 4/4, 3/4. Số trên chỉ số phách trong một ô nhịp, số dưới chỉ độ dài của mỗi phách.",
            "♯ Dấu Thăng (Sharp)": "Đặt trước nốt nhạc, có nhiệm vụ tăng cao độ của nốt đó lên nửa cung (1/2 tone).",
            "♭ Dấu Giáng (Flat)": "Đặt trước nốt nhạc, có nhiệm vụ hạ thấp cao độ của nốt đó xuống nửa cung (1/2 tone)."
        }
        for title, desc in symbols.items():
            with st.expander(title):
                st.write(desc)

    with col2:
        st.subheader("⏱️ Độ dài hình nốt & Nhịp phách")
        notes = {
            "𝄫 Nốt Tròn (Whole Note)": "Độ dài tương đương **4 phách**. Đây là bài tập tuyệt vời nhất để em rèn luyện làn hơi dài và đều đặn.",
            "𝄬 Nốt Trắng (Half Note)": "Độ dài tương đương **2 phách**. Ngân dài vừa phải, giữ vững vị trí âm thanh không để bị tuột.",
            "𝄭 Nốt Đen (Quarter Note)": "Độ dài tương đương **1 phách**. Nền tảng của nhịp điệu hành khúc và nhịp đập cơ bản.",
            "𝄮 Nốt Móc Đơn (Eighth Note)": "Độ dài tương đương **1/2 phách**. Đòi hỏi cơ hàm bập nhả linh hoạt và linh hoạt.",
            "𝄽 Dấu Lặng Đen (Quarter Rest)": "Nghỉ hoàn toàn trong **1 phách**. Tận dụng khoảng lặng này để thả lỏng cơ bụng và lấy hơi nhanh (catch breath)."
        }
        for title, desc in notes.items():
            with st.expander(title):
                st.write(desc)

# --- TAB 3: MÁY LUYỆN THANH TỰ ĐỘNG ---
with tab3:
    st.header("Máy Phát Chuỗi Âm Luyện Thanh")
    st.write("Hãy chọn nguyên âm và bài tập, máy sẽ đánh tiếng đàn mẫu cho em hát theo.")
    
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        vowel = st.selectbox("👉 Chọn nguyên âm luyện giọng:", ["Ah (Mở vòm họng)", "Mi (Tập trung độ vang má)", "Ma (Thả lỏng hàm dưới)"])
    with col_ctrl2:
        exercise = st.selectbox("👉 Chọn mẫu mẫu luyện thanh:", ["Thang âm 5 nốt (Scale 1-2-3-4-5-4-3-2-1)", "Hợp âm rải (Arpeggio 1-3-5-3-1)"])

    st.markdown("---")
    st.subheader("🎯 Bắt đầu luyện tập")
    st.caption("Nhấp nút bên dưới để nghe chuỗi âm chạy mẫu và hòa giọng cùng đàn.")

    # Mã HTML/JS điều khiển bộ phát chuỗi âm luyện giọng tự động
    vocal_engine_html = f"""
    <style>
        .btn-play {{ background-color: #ff4b4b; color: white; border: none; padding: 12px 30px; font-size: 18px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; transition: 0.2s; }}
        .btn-play:hover {{ background-color: #ff3333; }}
        .display-screen {{ background: #262730; color: #00ffcc; padding: 20px; text-align: center; font-size: 24px; border-radius: 8px; margin-top: 15px; font-family: monospace; border: 2px solid #4f5163; }}
    </style>

    <button class="btn-play" onclick="startVocalExercise()">▶ KÍCH HOẠT CHUỖI LUYỆN THANH</button>
    <div id="vocal-screen" class="display-screen">Sẵn sàng... Nhấn nút để bắt đầu hát mẫu [{vowel.split(' ')[0]}]</div>

    <script>
        const vCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        // Định nghĩa tần số các nốt trong chuỗi Đô trưởng cơ bản
        const frequencies = {{
            'Đô': 261.63, 'Rê': 293.66, 'Mi': 329.63, 'Fa': 349.23, 'Sol': 392.00
        }};

        function playTone(freq, duration, startTime) {{
            const osc = vCtx.createOscillator();
            const gain = vCtx.createGain();
            
            osc.type = 'sine'; // Tiếng sine êm dịu thích hợp làm nền hát theo
            osc.frequency.setValueAtTime(freq, startTime);
            
            gain.gain.setValueAtTime(0.4, startTime);
            gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration - 0.05);
            
            osc.connect(gain);
            gain.connect(vCtx.destination);
            
            osc.start(startTime);
            osc.stop(startTime + duration);
        }}

        function startVocalExercise() {{
            const now = vCtx.currentTime;
            const screen = document.getElementById('vocal-screen');
            let sequence = [];
            
            // Kiểm tra cấu hình bài tập từ Python
            const selectedEx = "{exercise}";
            
            if(selectedEx.includes("5 nốt")) {{
                // Chuỗi nốt chạy lên và chạy xuống: Do-Re-Mi-Fa-Sol-Fa-Mi-Re-Do
                sequence = [
