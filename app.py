import streamlit as st
import pandas as pd

st.set_page_config(page_title="Filter Sentimen Berdasar Label", layout="wide")
st.title("Aplikasi Filter Komentar - Berdasarkan Label")

# ─────────────────────────────────────────────
# 1. Unggah atau baca dataset
# ─────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload file CSV (harus memiliki kolom 'komentar' & 'label')",
    type=["csv"]
)

if uploaded_file is None:
    st.info("⬆️ Silakan upload file CSV Anda untuk mulai.")
    st.stop()

# ─────────────────────────────────────────────
# 2. Muat dan validasi data
# ─────────────────────────────────────────────
try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Gagal membaca CSV: {e}")
    st.stop()

missing_cols = [c for c in ["komentar", "label"] if c not in df.columns]
if missing_cols:
    st.error(f"Dataset tidak memiliki kolom: {', '.join(missing_cols)}")
    st.stop()

# ─────────────────────────────────────────────
# 3. Pilihan label & filter
# ─────────────────────────────────────────────
label_options = sorted(df["label"].unique(), key=str)  # urut alfabet
selected_label = st.selectbox("Pilih label", options=label_options)

filtered_df = df[df["label"].str.lower() == selected_label.lower()]

# ─────────────────────────────────────────────
# 4. Tampilkan hasil
# ─────────────────────────────────────────────
st.markdown(f"### Hasil untuk label **{selected_label}**")
st.write(f"Jumlah komentar: **{len(filtered_df)}**")

st.dataframe(filtered_df.reset_index(drop=True))

# (Opsional) Unduh hasil
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="💾 Unduh hasil sebagai CSV",
    data=csv,
    file_name=f"komentar_{selected_label}.csv",
    mime="text/csv",
)
