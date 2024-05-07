import streamlit as st
import datetime
import pandas as pd

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

# Menampilkan informasi terkait BMI
def display_bmi_info(bmi):
    category, advice, color, exercises, motivation = interpret_bmi(bmi)
    st.success(f'BMI Anda adalah {bmi:.2f}.')
    st.metric(label="Kategori", value=category, delta_color="off", help=advice)
    st.caption(advice)
    st.markdown("**Saran Olahraga:**")
    exercise_table = { "Aktivitas": [], "Manfaat": [] }
    for exercise, benefit in exercises:
        exercise_table["Aktivitas"].append(exercise)
        exercise_table["Manfaat"].append(benefit)
    st.table(exercise_table)
    st.markdown("**Motivasi:**")
    st.markdown(motivation)

# Menambahkan fitur pengingat
def display_reminder():
    st.sidebar.subheader("🗓️Pengingat untuk Aktivitas🕛")
    date = st.sidebar.date_input("Pilih tanggal:")
    time = st.sidebar.time_input("Pilih waktu:")
    activity = st.sidebar.text_input("Deskripsi aktivitas:")
    if st.sidebar.button("Set Pengingat"):
        reminder_time = datetime.datetime.combine(date, time)
        st.session_state['reminders'].append((reminder_time, activity))
        st.sidebar.success(f"Pengingat untuk '{activity}' telah diatur pada {reminder_time.strftime('%Y-%m-%d %H:%M')}.")

# Menampilkan saran diet berdasarkan BMI
def display_diet_suggestions(bmi):
    if bmi < 18.5:
        diet = "Perbanyak protein"
    elif 18.5 <= bmi < 25:
        diet = "usahakan diet yang seimbang"
    elif 25 <= bmi < 30:
        diet = "hindari gula berlebihan"
    else:
        diet = "kurangi lemak dan kurangi kalori.atau konsultasi ke nutrionist"
    st.subheader("Saran Diet")
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
    st.write("## Anggota Kelompok:")
    st.markdown("""
    - **Elvio Aldwin Faqih** (2320521)
    - **Indana Zulfa** (2320531)
    - **Nayla Rahma** (2320540)
    - **Pramesthi Dewi Amelia** (2320543)
    - **Raden Kayla Syawal Sabira** (2320547)
    """, unsafe_allow_html=True)
    st.write("## Tentang Aplikasi Ini")
    st.write("""
    Aplikasi ini dirancang khusus untuk membantu Anda dengan cara yang mudah dan cepat
    dalam menghitung serta memahami nilai BMI (Body Mass Index) Anda. Cukup masukkan berat
    dan tinggi badan Anda, dan biarkan aplikasi ini melakukan sisanya. Aplikasi ini tidak hanya menghitung
    BMI Anda, tetapi juga memberikan penjelasan mendetail tentang kategori kesehatan yang sesuai dengan hasil pengukuran BMI Anda,
    saran olahraga yang cocok dalam bentuk tabel, serta kata-kata motivasi untuk membangun semangat Anda.
    """)

    # Tabel BMI
    bmi_categories = {
        "Kategori": ["Underweight", "Normal", "Overweight", "Obese"],
        "BMI Range": ["di bawah 18.5", "antara 18.5 dan 24.99", "antara 25 dan 29.99", "30 atau lebih"]
    }
    st.table(bmi_categories)

    # Input pengguna dan menu pilihan
    with st.sidebar:
        st.session_state['reminders'] = []
        menu_options = ["Beranda", "Kalkulator BMI", "Pengingat Aktivitas", "Tracking Berat Badan"]
        menu_choice = st.selectbox("Menu", menu_options)

    if menu_choice == "Beranda":
        st.write("Selamat datang di Aplikasi Kalkulator BMI!")
    elif menu_choice == "Kalkulator BMI":
        name = st.text_input("Masukkan nama Anda:")
        weight = st.number_input("Masukkan berat Anda (dalam kg):", min_value=1.0, format="%.2f")
        height = st.number_input("Masukkan tinggi Anda (dalam cm):", min_value=1.0, format="%.2f")
        if st.button('Hitung BMI'):
            if weight > 0 and height > 0:
                bmi = calculate_bmi(weight, height)
                display_bmi_info(bmi)
                display_diet_suggestions(bmi)
            else:
                st.error("Mohon masukkan data yang valid!")
    elif menu_choice == "Pengingat Aktivitas":
        display_reminder()
    elif menu_choice == "Tracking Berat Badan":
        display_weight_tracking()

if __name__ == '__main__':
    main()

