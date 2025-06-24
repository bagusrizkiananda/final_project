import streamlit as st
import pandas as pd
import pickle
from pathlib import Path
from typing import Union

# -----------------------------------------------------------------------------
# Configuration (edit these filenames to match what you push to GitHub)
# -----------------------------------------------------------------------------
DATA_PATH = Path(__file__).parent / "sentiment_data.csv"  # fallback CSV
MODEL_PATH = Path(__file__).parent / "sentiment_model.pkl"  # fallback model

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data(source: Union[Path, str]) -> pd.DataFrame:
    """Load a CSV containing a text column to classify."""
    df = pd.read_csv(source)
    df.columns = df.columns.str.lower()

    # Attempt to auto-detect the text column
    text_candidates = [
        "komentar", "comment", "text", "full_text", "tweet", "review"
    ]
    text_col = next((c for c in text_candidates if c in df.columns), None)

    if text_col is None:
        st.error(
            "CSV must contain a column with the comments/reviews to classify.\n"
            "Example column names: komentar, comment, full_text, text."
        )
        st.stop()

    return df.rename(columns={text_col: "comment"})


@st.cache_resource(show_spinner=False)
def load_model(model_source: Union[Path, str]):
    """Load a pickled scikit‑learn sentiment classifier (Pipeline)."""
    return pickle.load(open(model_source, "rb"))


# -----------------------------------------------------------------------------
# Streamlit app
# -----------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="ML Sentiment Classifier", page_icon="🤖", layout="wide")
    st.title("🤖 Machine‑Learning Sentiment Classifier")

    st.markdown(
        """
        **Upload** a CSV of comments *or* test a single sentence below.
        By default, the app uses **sentiment_data.csv** and **sentiment_model.pkl** bundled in the repository.
        """
    )

    # Sidebar – upload model ---------------------------------------------------
    st.sidebar.header("Model")
    uploaded_model = st.sidebar.file_uploader("Upload a .pkl model (optional)", type=["pkl"])
    if uploaded_model is not None:
        model_src = uploaded_model
    else:
        model_src = MODEL_PATH

    try:
        model = load_model(model_src)  # type: ignore[arg-type]
    except Exception as e:
        st.sidebar.error(f"Failed to load model: {e}")
        st.stop()

    # Model info
    st.sidebar.success("Model loaded successfully ✅")

    # Single comment prediction ----------------------------------------------
    st.subheader("🔍 Quick Test")
    user_text = st.text_input("Enter a sentence to classify", "I love this product!")
    if user_text:
        pred = model.predict([user_text])[0]
        st.write(f"**Predicted sentiment:** {pred}")
        st.divider()

    # Batch prediction on CSV --------------------------------------------------
    st.subheader("📄 Batch Classification")
    uploaded_csv = st.file_uploader("Upload CSV of comments (optional)", type=["csv"])

    if uploaded_csv is not None:
        data_src = uploaded_csv
    else:
        data_src = DATA_PATH

    df = load_data(data_src)  # type: ignore[arg-type]

    # Predict
    with st.spinner("Classifying comments..."):
        df["sentiment"] = model.predict(df["comment"].astype(str))

    # Filter controls
    st.sidebar.header("Filter results")
    available_sentiments = sorted(df["sentiment"].unique())
    selected = st.sidebar.multiselect("Select sentiment(s)", available_sentiments, default=available_sentiments)
    filtered_df = df[df["sentiment"].isin(selected)]

    # Display
    st.write(f"Showing **{len(filtered_df):,}** of **{len(df):,}** classified comments.")
    st.dataframe(filtered_df, use_container_width=True)

    # Download predictions
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download predictions as CSV",
        data=csv_bytes,
        file_name="predicted_comments.csv",
        mime="text/csv",
    )

    # Summary counts
    st.subheader("📊 Sentiment Distribution")
    counts = df["sentiment"].value_counts().reset_index()
    counts.columns = ["Sentiment", "Count"]
    st.bar_chart(counts.set_index("Sentiment"))


if __name__ == "__main__":
    main()
