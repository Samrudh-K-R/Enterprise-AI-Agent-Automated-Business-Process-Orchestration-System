import streamlit as st
import sys
import os
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).parent))

from src.agents.enterprise_agent import EnterpriseAgent
from src.workflows.workflow_engine import WorkflowEngine, Workflow, TaskStatus

# Page config
st.set_page_config(
    page_title="Enterprise AI Agent",
    page_icon="🤖",
    layout="wide"
)

# Initialize Agent and Workflow Engine
@st.cache_resource
def get_agent_and_engine():
    agent = EnterpriseAgent()
    engine = WorkflowEngine()
    
    # Register example workflow
    workflow = Workflow("order_processing", "Process customer orders")
    
    def validate_order(context):
        return {"valid": True}
        
    def process_payment(context):
        return {"payment_id": "pay_123"}
        
    def fulfill_order(context):
        return {"shipped": True}
        
    workflow.add_task("validate", validate_order)
    workflow.add_task("payment", process_payment, dependencies=["validate"])
    workflow.add_task("fulfill", fulfill_order, dependencies=["payment"])
    
    engine.register_workflow(workflow)
    
    return agent, engine

agent, engine = get_agent_and_engine()

# Sidebar
st.sidebar.title("Enterprise AI Agent")
mode = st.sidebar.radio("Select Mode", ["Single Task", "Workflow"])

if mode == "Single Task":
    st.title("🤖 Single Task Execution")
    st.markdown("Execute individual tasks using the Enterprise Agent.")
    
    task_desc = st.text_area("Task Description", "Process customer order #12345")
    
    if st.button("Execute Task"):
        with st.spinner("Executing task..."):
            result = agent.execute_task(task_desc)
            
        if result["status"] == "success":
            st.success("Task Completed Successfully!")
            st.json(result)
        else:
            st.error(f"Task Failed: {result.get('error')}")
            st.json(result)

elif mode == "Workflow":
    st.title("⚙️ Workflow Orchestration")
    st.markdown("Execute complex multi-step business workflows.")
    
    workflow_name = st.selectbox("Select Workflow", list(engine.workflows.keys()))
    
    if st.button("Run Workflow"):
        st.write("### Execution Log")
        
        with st.spinner(f"Running workflow: {workflow_name}..."):
            try:
                results = engine.execute_workflow(workflow_name)
                
                # Display results in a nice format
                st.success("Workflow Completed!")
                
                for task_name, task_result in results.items():
                    status = task_result["status"]
                    icon = "✅" if status == "completed" else "❌"
                    
                    with st.expander(f"{icon} Task: {task_name} ({status})"):
                        st.json(task_result)
                        
            except Exception as e:
                st.error(f"Workflow failed: {str(e)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.info(f"Agent Version: {agent.version}")
