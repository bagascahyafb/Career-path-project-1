import streamlit as st
import pandas as pd

@st.cache_resource
def load_form_data():
    try:
        user_profile_df = pd.read_csv('dataset/processed_user_profiles.csv')
        user_skill_matrix = pd.read_csv('dataset/processed_user_skills.csv')
        return user_profile_df, user_skill_matrix
    except FileNotFoundError:
        return None, None

user_profile_df, user_skill_matrix = load_form_data()

st.set_page_config(page_title="Formulir Rekomendasi", layout="centered")
st.title("🚀 Career Path Recommender")
st.markdown("#### Selamat datang di aplikasi Career Path Recommender!")
st.write("Aplikasi ini dirancang untuk membantu Anda menemukan jalur karir yang paling sesuai berdasarkan profil profesional dan keahlian teknis Anda pada bidang pengolahan data.")

st.markdown("### Langkah 1: Lengkapi Profil Anda")
st.write("Isi formulir di bawah ini, klik tombol 'Simpan Profil', lalu navigasikan ke halaman 'Hasil Rekomendasi' di sidebar kiri.")

if user_profile_df is None or user_skill_matrix is None:
    st.error("Gagal memuat data. Pastikan notebook Fase 1 sudah dijalankan.")
else:
    job_titles = user_profile_df['job_title'].dropna().unique().tolist()
    experiences = user_profile_df['years_experience'].dropna().unique().tolist()
    all_skills = user_skill_matrix.drop(columns=['user_id']).columns.tolist()

    with st.form(key='profile_form'):
        st.subheader("Profil Profesional")
        selected_job = st.selectbox("Pilih Jabatan Anda Saat Ini:", job_titles)
        selected_exp = st.selectbox("Pilih Pengalaman Pemrograman Anda:", experiences)
        
        st.subheader("Keahlian Teknis")
        selected_skills = st.multiselect("Pilih Skill yang Sudah Anda Kuasai:", all_skills)
        
        submit_button = st.form_submit_button(label='Simpan Profil & Siapkan Rekomendasi')

    if submit_button:
        st.session_state['user_input_job'] = selected_job
        st.session_state['user_input_exp'] = selected_exp
        st.session_state['user_input_skills'] = selected_skills
        st.session_state['form_submitted'] = True
        
        st.success("✅ Profil Anda berhasil disimpan!")
        st.info("Sekarang, silakan klik halaman **'Hasil Rekomendasi'** pada menu di sebelah kiri.")