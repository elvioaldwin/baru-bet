import streamlit as st
import datetime
import pandas as pd
import emoji

# Mengatur tema
st.set_page_config(layout="wide", page_title="Kalkulator BMI Canggih", page_icon=":scales:")

# Ini adalah rumus perhitungan BMI
def calculate_bmi(weight, height):
    bmi = weight / ((height / 100) ** 2)
    return bmi

# Fungsi ini menerima nilai BMI dan mengembalikan rekomendasi 
# kesehatan berdasarkan kategori BMI.
def interpret_bmi(bmi):
    if bmi < 18.5:
        return ("Underweight🥩🍴", 
                "Ayo, tingkatkan asupan makananmu dengan pilihan yang lebih banyak dan bernutrisi! Jadikan setiap suapan sebagai langkah cerdas menuju kesehatan yang lebih baik. Selalu ada ruang untuk lebih banyak kebaikan di piringmu!",
                "#3498db",
                [("Yoga", "Memperbaiki postur dan meningkatkan massa otot tanpa beban berlebih"),
                 ("Berenang", "Melatih semua grup otot tanpa risiko cedera"),
                 ("Berjalan cepat", "Meningkatkan kekuatan otot dengan risiko rendah")],
                "Setiap langkah kecil adalah kemajuan. Anda lebih kuat dari yang Anda pikir!")
    elif 18.5 <= bmi < 25:
        return ("Normal👌😉", 
                "Mari kita terus jaga semangat! Pertahankan pola makan sehat dan rutin berolahraga sebagai investasi terbaik untuk kesehatan jangka panjangmu. Ayo buat setiap hari sebagai langkah positif menuju versi terbaik dirimu!.",
                "#2ecc71",
                [("Berlari", "Membakar kalori dan meningkatkan kesehatan kardiovaskular"),
                 ("Berenang", "Cardio yang efektif dan rendah risiko"),
                 ("Latihan beban", "Membangun massa otot dan memperkuat tulang")],
                "Tetaplah konsisten dan nikmati prosesnya; Anda sedang melakukan hal-hal luar biasa untuk tubuh Anda!")
    elif 25 <= bmi < 30:
        return ("Overweight🏃‍♂️🏊‍♂️", 
                "Ayo, mulai kurangi asupan kalori dan tingkatkan aktivitas fisikmu! Setiap langkah kecil yang kamu ambil membawa dampak besar bagi kesehatan dan kesejahteraanmu. Bersama, kita bisa menjalani hidup yang lebih sehat dan penuh energi!",
                "#f39c12",
                [("Berjalan kaki cepat", "Cardio ringan untuk memulai dan membakar kalori"),
                 ("Berenang", "Mengurangi beban sendi saat berolahraga"),
                 ("Aerobik air", "Menyenangkan dan efektif untuk menurunkan berat badan")],
                "Setiap langkah adalah langkah ke arah yang benar. Terus bergerak maju!")
    else:
        return ("Obese🏋️‍♂️🍴", 
                "Mulai Hari Ini - Ingat, perjalanan seribu mil dimulai dengan satu langkah. Tak peduli seberapa kecil, langkah pertama Anda menuju kesehatan yang lebih baik adalah yang paling penting!",
                "#e74c3c",
                [("Berjalan kaki", "Mulai dengan sesuatu yang mudah dan bertahap"),
                 ("Latihan kekuatan", "Membantu membakar kalori bahkan saat istirahat"),
                 ("Streching", "Latihan interval intensitas rendah untuk memulai tanpa risiko tinggi")],
                "Setiap hari membawa peluang baru untuk menjadi lebih baik. Jangan menyerah!")

# Menampilkan informasi terkait BMI dengan detail olahraga
def display_bmi_info(bmi):
    category, advice, color, exercises, motivation = interpret_bmi(bmi)
    st.success(f'BMI Anda adalah {bmi:.2f}.')
    st.metric(label="Kategori", value=category, delta_color="off", help=advice)
    st.caption(advice)
    st.markdown("**Saran Olahraga:**")
    for exercise, benefit in exercises:
        with st.expander(f"{exercise}"):
            st.markdown(f"**Manfaat:** {benefit}")
    st.markdown("**Motivasi:**")
    st.markdown(motivation)

# Menambahkan fitur pengingat asupan air
def display_water_intake_reminder():
    st.sidebar.subheader("💧 Pengingat Asupan Air")
    if 'daily_water_target' not in st.session_state:
        st.session_state['daily_water_target'] = 2000  # nilai default 2000 ml per hari

    daily_target = st.sidebar.number_input("Target asupan air harian (ml):", min_value=1000, max_value=5000, value=st.session_state['daily_water_target'])
    st.session_state['daily_water_target'] = daily_target

    if st.sidebar.button("Atur Pengingat Minum"):
        st.sidebar.success(f"Pengingat untuk minum air telah diatur. Target Anda adalah {daily_target} ml per hari.")

    # Menampilkan log asupan air
    if 'water_log' not in st.session_state:
        st.session_state['water_log'] = []

    water_intake = st.sidebar.number_input("Tambahkan asupan air (ml):", min_value=100, max_value=1000, step=100)
    if st.sidebar.button("Tambahkan Asupan"):
        st.session_state['water_log'].append(water_intake)
        st.sidebar.success(f"Anda telah menambahkan {water_intake} ml air.")

    if st.session_state['water_log']:
        total_intake = sum(st.session_state['water_log'])
        st.sidebar.write(f"Total asupan air hari ini: {total_intake} ml")
        if total_intake >= daily_target:
            st.sidebar.success("Selamat! Anda telah mencapai target asupan air hari ini.")
        else:
            st.sidebar.warning(f"Anda masih perlu {daily_target - total_intake} ml lagi untuk mencapai target.")

# Menampilkan saran diet berdasarkan BMI
def display_diet_suggestions(bmi):
    if bmi < 18.5:
        diet = """
        - Perbanyak konsumsi makanan tinggi kalori dan nutrisi seperti kacang-kacangan, alpukat, dan keju.
        - Tambahkan smoothie atau milkshake yang diperkaya dengan protein.
        - Makan lebih sering dengan porsi yang lebih kecil namun lebih sering.
        """
    elif 18.5 <= bmi < 25:
        diet = """
        - Pertahankan diet seimbang dengan banyak buah, sayuran, protein tanpa lemak, dan biji-bijian utuh.
        - Minum air yang cukup dan batasi konsumsi gula dan makanan olahan.
        - Pertimbangkan untuk mengatur porsi makan dan waktu makan secara teratur.
        """
    elif 25 <= bmi < 30:
        diet = """
        - Kurangi asupan kalori harian dan hindari makanan cepat saji serta makanan tinggi gula.
        - Fokus pada makanan yang mengandung banyak serat seperti sayuran, buah, dan biji-bijian utuh.
        - Pertimbangkan untuk meningkatkan aktivitas fisik secara bertahap.
        """
    else:
        diet = """
        - Fokus pada pengurangan asupan kalori dan konsultasi dengan ahli gizi untuk mendapatkan rencana makan yang sesuai.
        - Batasi konsumsi makanan tinggi lemak dan gula.
        - Tingkatkan konsumsi sayuran, buah, dan protein tanpa lemak.
        """
    st.write("### Saran Diet Berdasarkan BMI Anda:")
    st.write(diet)

# Pelacakan berat badan
def display_weight_tracking():
    st.subheader("Tracking Berat Badan🏋️‍♂️")
    if 'weight_data' not in st.session_state or st.session_state['weight_data'] is None:
        st.session_state['weight_data'] = pd.DataFrame(columns=['Tanggal', 'Berat'])
    
    with st.form("weight_form"):
        date = st.date_input("Tanggal")
        weight = st.number_input("Berat Badan (kg)", min_value=0.1)
        submit_button = st.form_submit_button("Tambah Data")
        if submit_button:
            new_data = pd.DataFrame({'Tanggal': [date], 'Berat': [weight]})
            st.session_state['weight_data'] = pd.concat([st.session_state['weight_data'], new_data], ignore_index=True)
            st.success("Data Berat Badan Ditambahkan")

    if st.session_state['weight_data'].empty:
        st.write("Belum ada data yang ditambahkan.")
    else:
        st.write(st.session_state['weight_data'])

# Fungsi utama
def main():
    st.header('Interactive BMI Calculator👌')
    st.markdown("<hr style='border: 2px solid blue; border-radius: 5px;'/>", unsafe_allow_html=True)
    display_group_members()
    about_app()
    display_bmi_table()
    bmi_calculator_layout()
    external_data_tracking_features()

def display_group_members():
    st.write("## Anggota Kelompok:")
    st.markdown("""
    - **Elvio Aldwin Faqih** (2320521)
    - **Indana Zulfa** (2320531)
    - **Nayla Rahma** (2320540)
    - **Pramesthi Dewi Amelia** (2320543)
    - **Raden Kayla Syawal Sabira** (2320547)
    """, unsafe_allow_html=True)

def about_app():
    st.write("## Tentang Aplikasi Ini")
    st.write("""
    Aplikasi ini dirancang khusus untuk membantu Anda dengan cara yang mudah dan cepat
    dalam menghitung serta memahami nilai BMI (Body Mass Index) Anda. Cukup masukkan berat
    dan tinggi badan Anda, dan biarkan aplikasi ini melakukan sisanya. Aplikasi ini tidak hanya menghitung
    BMI Anda, tetapi juga memberikan penjelasan mendetail tentang kategori kesehatan yang sesuai dengan hasil pengukuran BMI Anda,
    saran olahraga yang cocok dalam bentuk tabel, serta kata-kata motivasi untuk membangun semangat Anda.
    """)

def display_bmi_table():
    # Data untuk tabel BMI
    df = pd.DataFrame({
        "Kategori": ["Underweight", "Normal", "Overweight", "Obese"],
        "Min BMI": [0, 18.5, 25, 30],
        "Max BMI": [18.5, 24.99, 29.99, 60]
    })
    st.write("## Tabel Rentang BMI")
    st.table(df)

def bmi_calculator_layout():
    # Layout dengan kolom
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Kalkulator BMI")
        weight = st.number_input("Berat (kg)", min_value=1.0, format="%.2f")
        height = st.number_input("Tinggi (cm)", min_value=1.0, format="%.2f")
        bmi = 0  # Nilai default untuk BMI
        if st.button('Hitung BMI'):
            bmi = calculate_bmi(weight, height)
            st.write(f"BMI Anda adalah {bmi:.2f}")
            display_bmi_info(bmi)  # Menampilkan informasi BMI termasuk saran diet dan motivasi

    with col2:
        st.subheader("Saran Diet dan Motivasi")
        if bmi > 0:  # Pastikan BMI sudah dihitung sebelum menampilkan saran diet dan motivasi
            display_diet_suggestions(bmi)

def external_data_tracking_features():
    st.markdown("## Data Tracking")
    display_weight_tracking()
    display_water_intake_reminder()

if __name__ == '__main__':
    main()

