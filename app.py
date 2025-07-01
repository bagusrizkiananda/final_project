import streamlit as st
import pandas as pd

st.set_page_config(page_title="Filter Label Sentimen", layout="wide")
st.title("Aplikasi Filter Label Sentimen")

# ───────────────────────────────
# 1) Unggah dataset
# ───────────────────────────────
uploaded = st.file_uploader(
    "Upload file CSV (WAJIB memiliki kolom 'label' dan 'english_tweet')",
    type=["csv"]
)

if uploaded is None:
    st.info("⬆️ Silakan upload CSV untuk mulai.")
    st.stop()

# ───────────────────────────────
# 2) Baca & validasi
# ───────────────────────────────
try:
    df = pd.read_csv(uploaded)
except Exception as e:
    st.error(f"Gagal membaca CSV: {e}")
    st.stop()

if not {"label", "english_tweet"}.issubset(df.columns):
    st.error("Dataset harus memiliki kolom 'label' dan 'english_tweet'.")
    st.stop()

# Buat salinan hanya kolom yang diperlukan
df = df[["label", "english_tweet"]].copy()

# Pastikan huruf kecil untuk pencocokan label
df["label_lower"] = df["label"].str.lower()

# ───────────────────────────────
# 3) Dropdown label
# ───────────────────────────────
options = ["positif", "netral", "negatif"]
selected = st.selectbox("Pilih label:", options)

# Filter berdasarkan label
filtered = df[df["label_lower"] == selected]

# ───────────────────────────────
# 4) Tampilkan hasil
# ───────────────────────────────
st.markdown(f"### Jumlah data label **{selected}**: {len(filtered)}")

# Tampilkan kolom label & english_tweet
st.dataframe(filtered[["label", "english_tweet"]].reset_index(drop=True))

# Unduh hasil
csv_bytes = filtered[["label", "english_tweet"]].to_csv(index=False).encode("utf-8")
st.download_button(
    "💾 Unduh hasil (CSV)",
    data=csv_bytes,
    file_name=f"label_{selected}.csv",
    mime="text/csv"
)
