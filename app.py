import streamlit as st
import pandas as pd
from modules.processor import preprocess_image
from modules.analyzer import analyze_ad_creative
from modules.reporter import generate_market_report, summarize_metrics

st.set_page_config(page_title="Competitive Ad Intelligence Agent", layout="wide")

st.title("🕵️‍♂️ Competitive Ad Intelligence & Creative Analyzer")
st.markdown("Upload competitor ad creatives to reverse-engineer their hooks, value propositions, and targeting strategies instantly.")

st.sidebar.header("Configuration")
model_choice = st.sidebar.selectbox("Select VLM Engine", ["llava (Local Ollama)", "gpt-4o-mini (Cloud API)"])
api_endpoint = st.sidebar.text_input("API Endpoint", value="http://localhost:11434/api/generate")

uploaded_files = st.file_uploader("Upload Competitor Ad Creatives", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if 'analyses' not in st.session_state:
        st.session_state.analyses = []

    if st.button("🚀 Run Competitive Analysis Pipeline", type="primary"):
        st.session_state.analyses = []
        progress_bar = st.progress(0)
        for i, file in enumerate(uploaded_files):
            image = preprocess_image(file)
            with st.spinner(f'Analyzing creative {i+1} of {len(uploaded_files)}...'):
                analysis = analyze_ad_creative(image, api_endpoint=api_endpoint)
                analysis['filename'] = file.name
                st.session_state.analyses.append(analysis)
            progress_bar.progress((i + 1) / len(uploaded_files))
        st.success('Analysis complete!')

    if st.session_state.analyses:
        st.markdown('---')
        st.subheader('📊 Market Intelligence Summary')
        df = generate_market_report(st.session_state.analyses)
        metrics = summarize_metrics(df)
        col1, col2, col3 = st.columns(3)
        col1.metric('Total Creatives Analyzed', metrics.get('total_ads_analyzed', 0))
        col2.metric('Avg. Effectiveness Score', f"{metrics.get('average_effectiveness_score', 0)} / 10")
        col3.metric('Primary Hook Strategy', list(metrics.get('dominant_hook_types', {'N/A': 0}).keys())[0])
        st.markdown('### Detailed Creative Breakdown')
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label='📥 Download Intelligence Report (CSV)', data=csv, file_name='competitor_ad_intelligence_report.csv', mime='text/csv')
