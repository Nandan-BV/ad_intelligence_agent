import streamlit as st
from PIL import Image
from modules.analyzer import analyze_ad_creative
from modules.reporter import generate_pdf_report
from modules.agents import run_multi_agent_audit

st.set_page_config(page_title="Ad Intelligence & Profit Suite", layout="wide")

st.title("🚀 Competitive Ad Intelligence & Profit Scaling Suite")
st.markdown("Reverse-engineer competitor creative hooks, discover audience blind spots, and generate profit-maximizing counter-strategies instantly using local AI agents.")

with st.sidebar:
    st.header("Control Panel")
    uploaded_file = st.file_uploader("Upload Competitor Ad Creative", type=["jpg", "jpeg", "png"])
    run_analysis = st.button("🚀 Run Multi-Agent Forensic Audit", type="primary")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 1.3])
    
    with col1:
        st.subheader("Target Creative")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("Autonomous Multi-Agent Intelligence Output")
        if run_analysis:
            with st.spinner("Step 1/2: Extracting visual ad features via LLaVA..."):
                base_result = analyze_ad_creative(image)
                st.session_state['base_result'] = base_result
                
            with st.spinner("Step 2/2: CrewAI Agents (Auditor, Copywriter, CMO) collaborating on strategy..."):
                summary_string = (
                    f"Hook Type: {base_result.get('hook_type')}. "
                    f"Summary: {base_result.get('core_hook_summary')}. "
                    f"Value Prop: {base_result.get('value_proposition')}."
                )
                agent_output = run_multi_agent_audit(summary_string)
                st.session_state['agent_output'] = agent_output
                
        if 'base_result' in st.session_state:
            res = st.session_state['base_result']
            st.metric(label="Estimated Effectiveness Score", value=f"{res.get('estimated_effectiveness_score', 0)} / 10")
            st.markdown(f"**Quick Hook Classification:** `{res.get('hook_type', 'N/A')}`")
            
        if 'agent_output' in st.session_state:
            st.markdown("---")
            st.markdown("### 🧠 Collaborative Growth & Strategy Playbook")
            st.markdown(st.session_state['agent_output'])
            
            # PDF Download Integration
            if st.button("📥 Generate Client Executive PDF Report"):
                pdf_file = generate_pdf_report(st.session_state['base_result'])
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="Download PDF Playbook",
                        data=f,
                        file_name="Competitor_Profit_Playbook.pdf",
                        mime="application/pdf"
                    )
else:
    st.info("👈 Upload a competitor advertisement image in the sidebar to run your autonomous multi-agent audit.")
