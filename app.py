import streamlit as st #digunakan untuk membangun antarmuka web
import pandas as pd #untuk memproses data (baca, filter, data csv)

st.set_page_config(page_title="Filter Label Sentimen", layout="wide") #mengatur judul halaman dan atata letak menjadi wide
st.title("Aplikasi Filter Label Sentimen") #menampilkan judul utama

# ───────────────────────────────
# 1) Baca dataset langsung dari file lokal
# ───────────────────────────────
csv_path = "sentiment_data.csv"  # pastikan file ada di direktori yang sama

try:
    df = pd.read_csv(csv_path) #membaca file csv
except Exception as e:
    st.error(f"Gagal membaca file CSV: {e}") #pesan error jika data csv tidak ditemukan
    st.stop()

# ───────────────────────────────
# 2) Validasi kolom
# ───────────────────────────────
if not {"label", "english_tweet"}.issubset(df.columns): #Mengecek apakah file CSV memiliki dua kolom penting
    st.error("Dataset harus memiliki kolom 'label' dan 'english_tweet'.")
    st.stop()

# Salin kolom yang diperlukan
df = df[["label", "english_tweet"]].copy()

# Normalisasi label ke huruf kecil
df["label_lower"] = df["label"].str.lower()

# ───────────────────────────────
# 3) Dropdown pilihan label
# ───────────────────────────────
options = ["positif", "netral", "negatif"]
selected = st.selectbox("Pilih label:", options)

# Filter
filtered = df[df["label_lower"] == selected]

# ───────────────────────────────
# 4) Tampilkan hasil
# ───────────────────────────────
st.markdown(f"### Jumlah data label **{selected}**: {len(filtered)}") #Menampilkan jumlah baris yang sesuai dengan label yang dipilih pada filter
st.dataframe(filtered[["label", "english_tweet"]].reset_index(drop=True)) #menampilkan data hasil filter dalam bentuk tabel interaktif

# Unduh hasil
csv_bytes = filtered[["label", "english_tweet"]].to_csv(index=False).encode("utf-8")
st.download_button( #membuat tombol download dengan nama file berdasarkan label
    "💾 Unduh hasil (CSV)",
    data=csv_bytes,
    file_name=f"label_{selected}.csv",
    mime="text/csv"
)
