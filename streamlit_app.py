import streamlit as st
import yaml
import os
# from agent import run_orchestration # Import your agent logic here

# --- Page Config ---
st.set_page_config(layout="wide", page_title="Multi-Agent Orchestrator")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stTextArea textarea { font-family: 'Courier New', Courier, monospace; background-color: #1e1e1e; color: #d4d4d4; }
    .success-box { background-color: #1e1e1e; padding: 20px; border-radius: 10px; color: #00ff00; border: 1px solid #00ff00; font-family: 'Courier New', monospace; }
    .stButton>button { border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Multi-Agent Orchestration Dashboard")

# --- Side-by-Side Layout ---
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.header("📝 Configuration Editor")
    
    # Default YAML template for Agent Orchestration
    default_yaml = """agents:
  - id: researcher
    role: Research Assistant
    goal: Find key insights about the given topic
  - id: writer
    role: Content Writer
    goal: Create a concise summary based on research

workflow:
  type: sequential
  steps:
    - agent: researcher
    - agent: writer

task: "Explain the benefits of Model Context Protocol (MCP) in AI." """
    
    yaml_input = st.text_area("Edit YAML Logic:", value=default_yaml, height=450)

    if st.button("🚀 Run Orchestration", use_container_width=True):
        if not yaml_input:
            st.error("Please provide YAML configuration first.")
        else:
            with st.spinner("Agents are collaborating via MCP..."):
                try:
                    # 1. Parse the YAML configuration
                    config = yaml.safe_load(yaml_input)
                    
                    # 2. TRIGGER YOUR AGENT LOGIC HERE
                    # In your real setup, you'll call: 
                    # result = run_orchestration(config)
                    
                    # Mocking a response for the UI demonstration
                    mock_response = "Agents have successfully processed the task using MCP. " \
                                    "The researcher identified connectivity benefits, and the writer " \
                                    "summarized them into this response."
                    
                    st.session_state.result = mock_response
                    st.toast("Orchestration Complete!", icon="✅")
                    
                except Exception as e:
                    st.error(f"Orchestration Error: {e}")

with col2:
    st.header("📊 Evaluation Panel")
    
    if "result" in st.session_state:
        st.subheader("Final Agent Output")
        st.markdown(f"""
            <div class="success-box">
                {st.session_state.result}
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.write("**Orchestration Metrics:**")
        st.json({
            "Status": "Success",
            "Agents_Active": 2,
            "MCP_Connection": "Active",
            "Mode": "Sequential"
        })
    else:
        st.info("The agents' output and MCP evaluation data will appear here.")