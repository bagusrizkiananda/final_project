import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
DATA_PATH = Path(__file__).parent / "sentiment_data.csv"  # default dataset

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data(csv_path: Path) -> pd.DataFrame:
    """Load and standardise the sentiment dataset.

    The function automatically detects the comment and label columns, so the
    CSV can use different header names (e.g. `komentar`, `full_text`, etc.)
    without needing code changes.
    """
    if not csv_path.exists():
        st.error(f"Dataset not found at {csv_path.relative_to(Path(__file__).parent)}")
        st.stop()

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.lower()  # case‑insensitive matching

    # Detect the comment column
    comment_candidates = [
        "komentar", "comment", "full_text", "text", "english_tweet",
    ]
    comment_col = next((c for c in comment_candidates if c in df.columns), None)

    # Detect the sentiment/label column
    label_candidates = [
        "sentimen", "sentiment", "label", "labels",
    ]
    label_col = next((c for c in label_candidates if c in df.columns), None)

    if comment_col is None or label_col is None:
        st.error(
            "CSV must contain a column for comments and a column for sentiment/label.\n"
            "Example column names: komentar, full_text (for comments) and sentimen, label (for sentiment)."
        )
        st.stop()

    # Keep only the two relevant columns and rename for consistency
    df = df[[comment_col, label_col]].rename(columns={comment_col: "comment", label_col: "sentiment"})
    return df

# -----------------------------------------------------------------------------
# Streamlit frontend
# -----------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(
        page_title="Sentiment Comment Filter",
        page_icon="🗂️",
        layout="wide",
    )

    st.title("🗂️ Sentiment Comment Filter")
    st.write(
        """
        Load a CSV file containing comments and their sentiment labels, then filter
        and download the comments by sentiment category. If you don't upload your
        own CSV, the built‑in **sentiment_data.csv** will be used.
        """
    )

    # Optional CSV upload overrides default dataset
    uploaded_file = st.file_uploader("Upload a CSV (optional)", type=["csv"])
    if uploaded_file is not None:
        data_source = uploaded_file
    else:
        data_source = DATA_PATH

    df = load_data(data_source)  # type: ignore[arg-type]

    # Sidebar controls ---------------------------------------------------------
    st.sidebar.header("Filter options")
    available_sentiments = sorted(df["sentiment"].dropna().unique())
    selected_sentiments = st.sidebar.multiselect(
        "Select sentiment(s)", options=available_sentiments, default=available_sentiments
    )

    # Apply filter -------------------------------------------------------------
    filtered_df = df[df["sentiment"].isin(selected_sentiments)]

    # Main panel ---------------------------------------------------------------
    st.subheader("Filtered results")
    st.write(f"Showing **{len(filtered_df):,}** comments out of **{len(df):,}**")
    st.dataframe(filtered_df, use_container_width=True)

    # Download button ----------------------------------------------------------
    csv_bytes = filtered_df.to_csv(index=False).encode("utf‑8")
    st.download_button(
        label="📥 Download filtered CSV",
        data=csv_bytes,
        file_name="filtered_comments.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
