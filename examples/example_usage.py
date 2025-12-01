"""
Example usage of the Enterprise Agent.

This script demonstrates how to initialize and use the Enterprise Agent
for various business process automation tasks.
"""

import sys
import os
from pathlib import Path

# Add the project root to sys.path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.agents.enterprise_agent import EnterpriseAgent
from src.workflows.workflow_engine import WorkflowEngine, Workflow


def example_basic_usage():
    """Example: Basic agent usage."""
    print("=" * 50)
    print("Example 1: Basic Agent Usage")
    print("=" * 50)
    
    # Initialize agent with configuration
    agent = EnterpriseAgent(config_path="config/settings.yaml")
    
    # Execute a simple task
    result = agent.execute_task(
        task_description="Process customer order",
        context={"order_id": "12345", "customer_id": "67890"}
    )
    
    print(f"Task Result: {result}")
    print()


def example_workflow_execution():
    """Example: Workflow execution."""
    print("=" * 50)
    print("Example 2: Workflow Execution")
    print("=" * 50)
    
    # Create workflow engine
    engine = WorkflowEngine()
    
    # Define a simple workflow
    workflow = Workflow(
        name="order_processing",
        description="Process customer order workflow"
    )
    
    # Add tasks to workflow
    def validate_order(context):
        print("  - Validating order...")
        return {"valid": True}
    
    def process_payment(context):
        print("  - Processing payment...")
        return {"payment_id": "pay_123"}
    
    def fulfill_order(context):
        print("  - Fulfilling order...")
        return {"shipped": True}
    
    workflow.add_task("validate", validate_order, dependencies=[])
    workflow.add_task("payment", process_payment, dependencies=["validate"])
    workflow.add_task("fulfill", fulfill_order, dependencies=["payment"])
    
    # Register and execute workflow
    engine.register_workflow(workflow)
    results = engine.execute_workflow("order_processing")
    
    print(f"Workflow Results: {results}")
    print()


def example_agent_capabilities():
    """Example: Check agent capabilities."""
    print("=" * 50)
    print("Example 3: Agent Capabilities")
    print("=" * 50)
    
    agent = EnterpriseAgent(config_path="config/settings.yaml")
    
    capabilities = agent.get_capabilities()
    status = agent.get_status()
    
    print(f"Agent: {status['name']}")
    print(f"Version: {status['version']}")
    print(f"Capabilities: {', '.join(capabilities)}")
    print()


if __name__ == "__main__":
    print("\nEnterprise Agent - Example Usage\n")
    
    try:
        example_basic_usage()
        example_workflow_execution()
        example_agent_capabilities()
        
        print("=" * 50)
        print("All examples completed successfully!")
        print("=" * 50)
    
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()

