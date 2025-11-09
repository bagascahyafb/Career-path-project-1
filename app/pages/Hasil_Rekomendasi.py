import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import time

# --- FUNGSI CACHE (TIDAK BERUBAH) ---
@st.cache_resource
def load_data_and_models():
    """Memuat semua data dan model yang dibutuhkan."""
    try:
        user_profile_df = pd.read_csv('dataset/processed_user_profiles.csv')
        user_skill_matrix = pd.read_csv('dataset/processed_user_skills.csv')
        skill_category_df = pd.read_csv('dataset/skill_categories.csv')
        global_skill_similarity_df = joblib.load('models/collaborative_skill_similarity.joblib')
        
        return user_profile_df, user_skill_matrix, skill_category_df, global_skill_similarity_df
    except FileNotFoundError:
        return None, None, None, None

# --- FUNGSI REKOMENDASI HELPER (TIDAK BERUBAH) ---
def collaborative_recommender(known_skills, skill_similarity_df, top_n_skills=10):
    all_recommendations = pd.Series(dtype=float)
    for skill in known_skills:
        if skill in skill_similarity_df.columns:
            recommendations = skill_similarity_df[skill].sort_values(ascending=False)
            all_recommendations = pd.concat([all_recommendations, recommendations])
    
    if all_recommendations.empty:
        return pd.Series(dtype=float)
        
    final_recommendations = all_recommendations.groupby(all_recommendations.index).sum()
    final_recommendations = final_recommendations.drop(known_skills, errors='ignore')
    return final_recommendations.sort_values(ascending=False).head(top_n_skills)

# --- FUNGSI OTAK KCR-LITE (REVISI BESAR) ---
def get_recommendations(
    selected_job, 
    selected_exp, 
    selected_skills,
    global_profile_df,
    global_skill_matrix,
    global_skill_sim_df,
    skill_category_df,
    min_squad_size=20
):
    
    # --- Langkah 1: Pre-Filtering berdasarkan Konteks ---
    squad_profiles = global_profile_df[
        (global_profile_df['job_title'] == selected_job) &
        (global_profile_df['years_experience'] == selected_exp)
    ]
    squad_user_ids = squad_profiles['user_id'].tolist()
    
    status_message = ""
    use_fallback_model = False # Flag untuk menentukan model
    
    # --- Langkah 2: Cek Ukuran "Squad" ---
    if len(squad_user_ids) < min_squad_size:
        use_fallback_model = True
        status_message = (
            f"Konteks Anda (Jabatan: '{selected_job}', Pengalaman: '{selected_exp}') terlalu spesifik. "
            f"Hanya ditemukan {len(squad_user_ids)} profesional yang cocok. "
            "Menggunakan model global untuk rekomendasi."
        )
    else:
        status_message = (
            f"Rekomendasi ini dibuat khusus untuk Anda, berdasarkan analisis "
            f"terhadap **{len(squad_user_ids)} profesional** lain yang memiliki "
            f"jabatan dan pengalaman yang sama dengan Anda."
        )

    # --- Langkah 3: Tentukan Logika (Cold-Start atau Collaborative) ---
    
    if not selected_skills:
        # --- LOGIKA A: COLD-START "STARTER PACK" ---
        # Pengguna tidak punya skill, jadi kita rekomendasikan skill paling populer dalam konteks mereka.
        status_message += "\n\nAnda belum memilih skill, jadi berikut adalah **'Starter Pack'** paling populer untuk jalur karir ini."
        
        if use_fallback_model:
            # Ambil popularitas dari SEMUA pengguna
            squad_skill_matrix = global_skill_matrix
        else:
            # Ambil popularitas HANYA dari "squad" kontekstual
            squad_skill_matrix = global_skill_matrix[global_skill_matrix['user_id'].isin(squad_user_ids)]
        
        # Hitung popularitas
        skill_popularity = squad_skill_matrix.drop(columns=['user_id']).sum().sort_values(ascending=False)
        recommendations = skill_popularity.head(10)
        
    else:
        # --- LOGIKA B: COLLABORATIVE FILTERING (Seperti sebelumnya) ---
        # Pengguna punya skill, kita cari kemiripannya.
        
        if use_fallback_model:
            final_sim_df = global_skill_sim_df
        else:
            # Buat "Otak" Baru On-the-Fly
            contextual_skill_matrix = global_skill_matrix[global_skill_matrix['user_id'].isin(squad_user_ids)]
            skills_only_matrix = contextual_skill_matrix.drop(columns=['user_id'])
            skill_user_matrix = skills_only_matrix.T
            contextual_sim_matrix = cosine_similarity(skill_user_matrix)
            final_sim_df = pd.DataFrame(
                contextual_sim_matrix,
                index=skills_only_matrix.columns,
                columns=skills_only_matrix.columns
            )
            
        recommendations = collaborative_recommender(
            known_skills=selected_skills,
            skill_similarity_df=final_sim_df
        )

    # --- Langkah 4: Format Output ---
    if not recommendations.empty:
        recs_df = recommendations.reset_index()
        # Jika 'recommendations' adalah series popularitas, kolomnya 'index' dan 0 (count)
        # Jika 'recommendations' adalah series skor, kolomnya 'index' dan 0 (score)
        recs_df.columns = ['Skill', 'Skor Rekomendasi/Popularitas']
        recs_df = pd.merge(recs_df, skill_category_df, on='Skill', how='left')
        final_recs_df = recs_df[['Skill', 'Kategori', 'Skor Rekomendasi/Popularitas']]
    else:
        final_recs_df = pd.DataFrame(columns=['Skill', 'Kategori', 'Skor Rekomendasi/Popularitas'])
        
    return final_recs_df, status_message

# --- TAMPILAN HALAMAN HASIL (REVISI) ---
st.set_page_config(page_title="Hasil Rekomendasi", layout="wide")
st.title("📄 Hasil Rekomendasi Anda (Context-Aware)")
st.write("Di halaman ini, Anda akan melihat rekomendasi skill yang dipersonalisasi berdasarkan profil yang telah Anda isi sebelumnya.")

if 'form_submitted' in st.session_state and st.session_state['form_submitted']:
    
    g_profile_df, g_skill_matrix, g_skill_cat_df, g_skill_sim_df = load_data_and_models()
    
    if g_profile_df is not None:
        selected_job = st.session_state['user_input_job']
        selected_exp = st.session_state['user_input_exp']
        selected_skills = st.session_state['user_input_skills']

        with st.spinner('Menganalisis konteks Anda dan membuat rekomendasi...'):
            start_time = time.time()
            recommendations_df, status_msg = get_recommendations(
                selected_job, selected_exp, selected_skills,
                g_profile_df, g_skill_matrix, g_skill_sim_df, g_skill_cat_df
            )
            end_time = time.time()

        st.success(f"Selesai dalam {end_time - start_time:.2f} detik.")
        st.info(status_msg) # Tampilkan pesan status (sekarang bisa ada info 'Starter Pack')
        
        st.subheader("Profil Anda (Input)")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Konteks Jabatan", selected_job)
        with col2:
            st.metric("Konteks Pengalaman", selected_exp)
        
        st.write("**Skill Dikuasai:**")
        st.info(", ".join(selected_skills) if selected_skills else "Belum ada skill yang dipilih (Mode 'Starter Pack').")

        st.markdown("---")
        
        # Ganti judul berdasarkan logika cold-start
        if not selected_skills:
            st.subheader("🚀 'Starter Pack' Populer Untuk Anda Pelajari")
        else:
            st.subheader("🔥 Top 10 Rekomendasi Untuk Anda Pelajari")
        
        if not recommendations_df.empty:
            st.dataframe(recommendations_df, use_container_width=True)
        else:
            # Pesan ini sekarang seharusnya SANGAT jarang muncul
            st.warning("Tidak ada rekomendasi yang bisa diberikan untuk konteks ini.")
            
    else:
        st.error("Model tidak berhasil dimuat, aplikasi tidak bisa berjalan.")
else:
    st.warning("⬅️ Silakan isi dan simpan profil Anda di halaman **'Formulir Input'** terlebih dahulu.")
    st.page_link("Formulir_Input.py", label="Kembali ke Formulir", icon="🏠")

