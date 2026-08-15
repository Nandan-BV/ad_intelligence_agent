import streamlit as st
from PIL import Image
from modules.analyzer import analyze_ad_creative
from modules.reporter import generate_pdf_report
import pandas as pd

st.set_page_config(page_title="Ad Intelligence & Profit Suite", layout="wide")

st.title("🚀 Competitive Ad Intelligence & Profit Scaling Suite")
st.markdown("Reverse-engineer competitor creative hooks, discover audience blind spots, and generate profit-maximizing counter-strategies instantly using local AI.")

with st.sidebar:
    st.header("Control Panel")
    uploaded_file = st.file_uploader("Upload Competitor Ad Creative", type=["jpg", "jpeg", "png"])
    run_analysis = st.button("🚀 Run Deep Forensic Audit", type="primary")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Target Creative")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("Intelligence Output")
        if run_analysis:
            with st.spinner("Running deep multi-modal analysis via local AI model..."):
                result = analyze_ad_creative(image)
                st.session_state['analysis_result'] = result
                
        if 'analysis_result' in st.session_state:
            res = st.session_state['analysis_result']
            
            if "error" in res and res["hook_type"] == "Connection Error":
                st.error(f"Connection Error: {res['error']}. Make sure Ollama is running (`ollama serve`).")
            else:
                st.metric(label="Estimated Effectiveness Score", value=f"{res.get('estimated_effectiveness_score', 0)} / 10")
                
                st.markdown(f"### 🪝 Hook Type: `{res.get('hook_type', 'N/A')}`")
                st.info(f"**Core Summary:** {res.get('core_hook_summary', 'N/A')}")
                
                st.markdown("#### 🎯 Value Proposition & Audience")
                st.write(f"* **Value Prop:** {res.get('value_proposition', 'N/A')}")
                st.write(f"* **Target Persona:** {res.get('target_audience_persona', 'N/A')}")
                
                st.markdown("#### ⚠️ Competitor Vulnerability")
                st.warning(res.get('competitor_weakness', 'N/A'))
                
                st.markdown("#### 🔥 Winning Counter-Strategy Hook")
                st.success(res.get('counter_strategy_hook', 'N/A'))
                
                st.markdown("#### 💰 Profit Optimization Tip")
                st.write(res.get('profit_optimization_tip', 'N/A'))
                
                # PDF Download Integration
                if st.button("📥 Generate Client Executive PDF Report"):
                    pdf_file = generate_pdf_report(res)
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="Download PDF Playbook",
                            data=f,
                            file_name="Competitor_Profit_Playbook.pdf",
                            mime="application/pdf"
                        )
else:
    st.info("👈 Upload a competitor advertisement image in the sidebar to begin your intelligence audit.")
