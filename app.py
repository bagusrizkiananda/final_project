import streamlit as st
import pandas as pd

st.set_page_config(page_title="Filter Label Sentimen", layout="wide")   # tata letak lebar
st.title("Aplikasi Filter Label Sentimen")

# ───────────────────────────────
# 1) Unggah dataset
# ───────────────────────────────
uploaded = st.file_uploader(
    "Upload file CSV (WAJIB memiliki kolom 'label')",
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

if "label" not in df.columns:
    st.error("Dataset tidak memiliki kolom 'label'.")
    st.stop()

# Hanya kolom label yang dipakai
df = df[["label"]].copy()

# Pastikan huruf kecil untuk pencocokan
df["label_lower"] = df["label"].str.lower()

# ───────────────────────────────
# 3) Dropdown label
# ───────────────────────────────
options = ["positif", "netral", "negatif"]          # label baku
selected = st.selectbox("Pilih label:", options)

# Filter
filtered = df[df["label_lower"] == selected]

# ───────────────────────────────
# 4) Tampilkan hasil
# ───────────────────────────────
st.markdown(f"### Jumlah data label **{selected}**: {len(filtered)}")

# Opsional: tampilkan tabel label saja
st.dataframe(filtered[["label"]].reset_index(drop=True))

# Opsional: unduh hasil
csv_bytes = filtered[["label"]].to_csv(index=False).encode("utf-8")
st.download_button(
    "💾 Unduh hasil (CSV)",
    data=csv_bytes,
    file_name=f"label_{selected}.csv",
    mime="text/csv"
)

ubah agar menampilkan header english_tweet
