import streamlit as st
import pandas as pd

st.set_page_config(page_title="Filter Label Sentimen", layout="wide")
st.title("Aplikasi Filter Label Sentimen")

# ─────────────────────────────────────
# 1) Pilih sumber data CSV
# ─────────────────────────────────────
csv_options = {
    "Sentiment Original": "sentiment_data.csv",
    "Naive Bayes Classification": "naive_bayes_classified_data.csv"
}

selected_file_label = st.selectbox("Pilih sumber data CSV:", list(csv_options.keys()))
csv_path = csv_options[selected_file_label]

# ─────────────────────────────────────
# 2) Baca dan validasi data
# ─────────────────────────────────────
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    st.error(f"Gagal membaca file '{csv_path}': {e}")
    st.stop()

if not {"label", "english_tweet"}.issubset(df.columns):
    st.error(f"File '{csv_path}' harus memiliki kolom 'label' dan 'english_tweet'.")
    st.stop()

# Hanya ambil kolom yang dibutuhkan
df = df[["label", "english_tweet"]].copy()
df["label_lower"] = df["label"].str.lower()

# ─────────────────────────────────────
# 3) Pilih label dan filter
# ─────────────────────────────────────
options = ["positif", "netral", "negatif"]
selected_label = st.selectbox("Pilih label:", options)

filtered = df[df["label_lower"] == selected_label]

# ─────────────────────────────────────
# 4) Tampilkan dan unduh hasil
# ─────────────────────────────────────
st.markdown(f"### Jumlah data label **{selected_label}**: {len(filtered)}")
st.dataframe(filtered[["label", "english_tweet"]].reset_index(drop=True))

csv_bytes = filtered[["label", "english_tweet"]].to_csv(index=False).encode("utf-8")
st.download_button(
    "💾 Unduh hasil (CSV)",
    data=csv_bytes,
    file_name=f"{selected_file_label.lower().replace(' ', '_')}_{selected_label}.csv",
    mime="text/csv"
)
