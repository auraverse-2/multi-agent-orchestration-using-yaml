import streamlit as st
from yaml_parser import safe_load 
from workflow_executor import run_workflow
import traceback
from dotenv import load_dotenv


load_dotenv()


def render_app():
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
        
        # --- 1. FILE UPLOADER COMPONENT ---
        uploaded_file = st.file_uploader("Upload an Agent Config (.yaml)", type=["yaml", "yml"])

        # Default YAML template
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
        
        # Logic to handle uploaded file content
        if uploaded_file is not None:
            try:
                # Read the file and update the session state
                file_content = uploaded_file.getvalue().decode("utf-8")
                st.session_state.yaml_input = file_content
            except Exception as e:
                st.error(f"Error reading file: {e}")
        
        # Initialize editor content if it doesn't exist
        if "yaml_input" not in st.session_state:
            st.session_state.yaml_input = default_yaml

        # 2. THE EDITOR (Binds to session state)
        yaml_input = st.text_area("Edit YAML Logic:", value=st.session_state.yaml_input, height=400)

        if st.button("🚀 Run Orchestration", use_container_width=True):
            if not yaml_input:
                st.error("Please provide YAML configuration first.")
            else:
                # --- 3. CALL THE VALIDATOR ---
                validation_result = safe_load(yaml_input)

                if not validation_result["valid"]:
                    st.error("❌ YAML Validation Failed")
                    for err in validation_result["errors"]:
                        st.markdown(f"**[{err['type']}]** {err['message']}")
                else:
                    st.session_state.normalized_input = validation_result["normalized_input"]
                    
                    if validation_result.get("warnings"):
                        for warn in validation_result["warnings"]:
                            st.warning(f"⚠️ **{warn['type']}:** {warn['message']}")

                    with st.spinner("Executing workflow..."):
                        try:
                            # Simulated Agent Logic
                            run_workflow(validation_result["normalized_input"])
                            mock_response = "Agents successfully processed the task using the validated configuration. " \
                                            "The researcher identified connectivity benefits, and the writer " \
                                            "summarized them into this response."
                            
                            st.session_state.result = mock_response
                            st.toast("Orchestration Complete!", icon="✅")
                        except Exception as e:
                            traceback.print_exc()
                            st.error(f"Orchestration Error: {e}")

    with col2:
        st.header("📊 Evaluation Panel")
        
        if "result" in st.session_state:
            # 1. View Normalized Config
            with st.expander("🔍 View Normalized Configuration", expanded=False):
                st.json(st.session_state.normalized_input)

            st.divider()

            # 2. View Agent Output
            st.subheader("Final Agent Output")
            st.markdown(f'<div class="success-box">{st.session_state.result}</div>', unsafe_allow_html=True)
            
            st.divider()
            st.write("**Orchestration Metrics:**")
            st.json({
                "Status": "Success",
                "Agents_Active": len(st.session_state.normalized_input["agents"]),
                "Validation": "Passed",
                "MCP_Connection": "Active"
            })
        else:
            st.info("The agents' output and MCP evaluation data will appear here.")


if __name__ == '__main__':
    render_app()
