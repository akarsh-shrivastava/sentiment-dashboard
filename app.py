import streamlit as st
import pandas as pd
import time
from gemini_core import get_sentiment

# --- Page config (must be first) ---
st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🎯",
    layout="centered"
)

# --- Sidebar ---
with st.sidebar:
    st.title("🎯 Sentiment Analyzer")
    st.markdown("Analyze customer reviews using Google Gemini AI.")
    st.divider()
    st.markdown("**How to use:**")
    st.markdown("1. **Single Review** — paste text and click Analyze")
    st.markdown("2. **Bulk CSV** — upload a CSV with a `review` column")
    st.divider()
    st.caption("Built with Streamlit + Google Gemini Flash")

# --- Main area ---
st.header("Customer Review Analyzer")

tab1, tab2 = st.tabs(["Single Review", "Bulk CSV Upload"])

# ── TAB 1: Single Review (same as Day 3) ──────────────────────────────────────
with tab1:
    st.markdown("Paste a single customer review below to analyze its sentiment and extract key themes.")

    review_input = st.text_area(
        label="Customer Review",
        placeholder="e.g. The product arrived late but the quality was excellent...",
        height=150
    )

    analyze_btn = st.button("Analyze Sentiment", type="primary")

    if analyze_btn:
        if not review_input.strip():
            st.warning("Please enter a review before analyzing.")
        else:
            with st.spinner("Analyzing with Gemini..."):
                result = get_sentiment(review_input)

            sentiment_color = {
                "Positive": "green",
                "Negative": "red",
                "Neutral": "gray",
                "Mixed": "orange"
            }

            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Sentiment", value=result["sentiment"])
            with col2:
                st.metric(label="Confidence", value=f"{result['confidence']:.0%}")

            st.markdown(f"**Summary:** {result['summary']}")
            st.divider()

            with st.expander("🏷️ Themes", expanded=True):
                if result["themes"]:
                    cols = st.columns(len(result["themes"]))
                    for i, theme in enumerate(result["themes"]):
                        cols[i].markdown(f"`{theme}`")
                else:
                    st.write("No themes identified.")

            with st.expander("✅ Positive Aspects", expanded=True):
                if result["positive_aspects"]:
                    for item in result["positive_aspects"]:
                        st.markdown(f"- {item}")
                else:
                    st.write("None mentioned.")

            with st.expander("❌ Negative Aspects", expanded=True):
                if result["negative_aspects"]:
                    for item in result["negative_aspects"]:
                        st.markdown(f"- {item}")
                else:
                    st.write("None mentioned.")

# ── TAB 2: Bulk CSV Upload ─────────────────────────────────────────────────────
with tab2:
    st.markdown("Upload a CSV file with a `review` column to analyze all reviews at once.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Check the column exists
        if "review" not in df.columns:
            st.error(f"CSV must have a column named `review`. Found columns: {list(df.columns)}")
        else:
            st.success(f"Loaded {len(df)} reviews. Ready to analyze.")
            st.dataframe(df.head(3), use_container_width=True)  # preview first 3 rows

            analyze_all_btn = st.button("Analyze All Reviews", type="primary")

            if analyze_all_btn:
                results = []
                progress_bar = st.progress(0, text="Starting analysis...")

                for i, row in enumerate(df["review"]):
                    # Update progress bar
                    progress = (i + 1) / len(df)
                    progress_bar.progress(progress, text=f"Analyzing review {i + 1} of {len(df)}...")

                    # Call Gemini
                    result = get_sentiment(str(row))

                    # Flatten the result for the table
                    results.append({
                        "review": row,
                        "sentiment": result["sentiment"],
                        "confidence": f"{result['confidence']:.0%}",
                        "themes": ", ".join(result["themes"]),
                        "summary": result["summary"]
                    })

                    # Small delay to avoid hitting Gemini rate limits
                    time.sleep(10)

                progress_bar.empty()  # remove progress bar when done
                st.success("Analysis complete!")

                # Build results dataframe
                results_df = pd.DataFrame(results)
                st.dataframe(results_df, use_container_width=True)

                # Download button
                csv_output = results_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download Results as CSV",
                    data=csv_output,
                    file_name="sentiment_results.csv",
                    mime="text/csv"
                )