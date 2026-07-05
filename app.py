import streamlit as st
import pandas as pd
import plotly.express as px
import time
from gemini_core import get_sentiment


st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🎯",
    layout="wide"
)

with st.sidebar:
    st.title("🎯 Sentiment Analyzer")
    st.markdown("Analyze customer reviews using Google Gemini AI.")
    st.divider()
    st.markdown("**How to use:**")
    st.markdown("1. **Single Review** — paste text and click Analyze")
    st.markdown("2. **Bulk CSV** — upload a CSV with a `review` column")
    st.divider()

def render_charts(results_df):
    st.subheader("📊 Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        sentiment_counts = results_df["sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]

        color_map = {
            "Positive": "#2ecc71",
            "Negative": "#e74c3c",
            "Neutral":  "#95a5a6",
            "Mixed":    "#f39c12"
        }

        fig1 = px.bar(
            sentiment_counts,
            x="Sentiment",
            y="Count",
            color="Sentiment",
            color_discrete_map=color_map,
            title="Sentiment Distribution",
            text="Count"
        )
        fig1.update_traces(textposition="outside")
        fig1.update_layout(showlegend=False, yaxis_title="Number of Reviews")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        confidence_numeric = (
            results_df["confidence"]
            .str.replace("%", "", regex=False)
            .astype(float) / 100
        )

        fig2 = px.histogram(
            x=confidence_numeric,
            nbins=10,
            title="Confidence Score Distribution",
            labels={"x": "Confidence Score"},
            color_discrete_sequence=["#3498db"]
        )
        fig2.update_layout(yaxis_title="Number of Reviews", bargap=0.1)
        st.plotly_chart(fig2, use_container_width=True)

    all_themes = (
        results_df["themes"]
        .dropna()
        .str.split(", ")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
        .reset_index()
    )
    all_themes.columns = ["Theme", "Count"]

    if not all_themes.empty:
        fig3 = px.bar(
            all_themes,
            x="Count",
            y="Theme",
            orientation="h",
            title="Top 10 Themes Across All Reviews",
            text="Count",
            color_discrete_sequence=["#9b59b6"]
        )
        fig3.update_traces(textposition="outside")
        fig3.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No themes found to display.")


st.header("Customer Review Analyzer")

tab1, tab2 = st.tabs(["Single Review", "Bulk CSV Upload"])


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


with tab2:
    st.markdown("Upload a CSV file with a `review` column to analyze all reviews at once.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if "review" not in df.columns:
            st.error(f"CSV must have a column named `review`. Found columns: {list(df.columns)}")
        else:
            st.success(f"Loaded {len(df)} reviews. Ready to analyze.")
            st.dataframe(df.head(3), use_container_width=True)

            analyze_all_btn = st.button("Analyze All Reviews", type="primary")

            if analyze_all_btn:
                results = []
                progress_bar = st.progress(0, text="Starting analysis...")

                for i, row in enumerate(df["review"]):
                    progress = (i + 1) / len(df)
                    progress_bar.progress(progress, text=f"Analyzing review {i + 1} of {len(df)}...")

                    result = get_sentiment(str(row))

                    results.append({
                        "review": row,
                        "sentiment": result["sentiment"],
                        "confidence": f"{result['confidence']:.0%}",
                        "themes": ", ".join(result["themes"]),
                        "summary": result["summary"]
                    })

                    time.sleep(10)

                progress_bar.empty()
                st.success("Analysis complete!")

                results_df = pd.DataFrame(results)

                st.subheader("📋 Results Table")
                st.dataframe(results_df, use_container_width=True)

                csv_output = results_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download Results as CSV",
                    data=csv_output,
                    file_name="sentiment_results.csv",
                    mime="text/csv"
                )

                st.divider()
                render_charts(results_df)