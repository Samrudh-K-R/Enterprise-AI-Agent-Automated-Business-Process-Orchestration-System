"""
Command Line Interface for Enterprise Agent.
"""

import argparse
import sys
import json
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.agents.enterprise_agent import EnterpriseAgent

def main():
    parser = argparse.ArgumentParser(description="Enterprise Agent CLI")
    parser.add_argument("task", nargs="?", help="Task description to execute")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--config", "-c", help="Path to configuration file", default="config/settings.yaml")
    
    args = parser.parse_args()
    
    try:
        agent = EnterpriseAgent(config_path=args.config)
        
        if args.interactive:
            print(f"Enterprise Agent v{agent.version} - Interactive Mode")
            print("Type 'exit' or 'quit' to stop.")
            print("-" * 40)
            
            while True:
                try:
                    user_input = input("\nTask > ")
                    if user_input.lower() in ('exit', 'quit'):
                        break
                    
                    if not user_input.strip():
                        continue
                        
                    result = agent.execute_task(user_input)
                    print(json.dumps(result, indent=2))
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    
        elif args.task:
            result = agent.execute_task(args.task)
            print(json.dumps(result, indent=2))
            
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Fatal Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
