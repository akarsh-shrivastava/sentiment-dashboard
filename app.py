import streamlit as st
from gemini_core import get_sentiment

st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="🎯",
    layout="centered"
)

with st.sidebar:
    st.title("🎯 Sentiment Analyzer")
    st.markdown("Analyze customer reviews using Google Gemini AI.")
    st.divider()
    st.markdown("**How to use:**")
    st.markdown("1. Paste a customer review in the text box")
    st.markdown("2. Click **Analyze Sentiment**")
    st.markdown("3. View results below")
    st.divider()



st.header("Customer Review Analyzer")
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
        with st.spinner("Analyzing..."):
            result = get_sentiment(review_input)

        # Color mapping for sentiment
        sentiment_color = {
            "Positive": "green",
            "Negative": "red",
            "Neutral": "gray",
            "Mixed": "orange"
        }
        color = sentiment_color.get(result["sentiment"], "gray")

        # Top-level summary card
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Sentiment", value=result["sentiment"])
        with col2:
            st.metric(label="Confidence", value=f"{result['confidence']:.0%}")

        st.markdown(f"**Summary:** {result['summary']}")
        st.divider()

        # Expandable sections
        with st.expander("🏷️ Themes", expanded=True):
            if result["themes"]:
                # Display themes as pills/badges using columns
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