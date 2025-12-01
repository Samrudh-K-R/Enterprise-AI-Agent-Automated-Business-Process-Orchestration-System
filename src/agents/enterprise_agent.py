"""
Enterprise Agent - Main agent implementation for business process automation.
"""

import yaml
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from loguru import logger


class EnterpriseAgent:
    """
    Enterprise-grade AI agent for automating business processes,
    handling workflows, and integrating with enterprise systems.
    """
    
    def __init__(
        self,
        config_path: Optional[str] = None,
        config_dict: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the Enterprise Agent.
        
        Args:
            config_path: Path to YAML configuration file
            config_dict: Configuration dictionary (alternative to config_path)
        """
        self.config = self._load_config(config_path, config_dict)
        self._setup_logging()
        self.logger = logger
        
        self.name = self.config.get("agent", {}).get("name", "Enterprise Agent")
        self.version = self.config.get("agent", {}).get("version", "1.0.0")
        
        logger.info(f"Initialized {self.name} v{self.version}")
    
    def _load_config(
        self,
        config_path: Optional[str],
        config_dict: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Load configuration from file or dictionary."""
        if config_dict:
            return config_dict
        
        if config_path:
            config_file = Path(config_path)
            if config_file.exists():
                with open(config_file, 'r') as f:
                    return yaml.safe_load(f)
            else:
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        # Return default configuration
        return {
            "agent": {
                "name": "Enterprise Agent",
                "version": "1.0.0"
            }
        }
    
    def _setup_logging(self):
        """Configure logging based on agent settings."""
        log_config = self.config.get("logging", {})
        
        if log_config.get("file_path"):
            log_file = Path(log_config["file_path"])
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            logger.add(
                log_file,
                rotation=log_config.get("max_file_size", "10MB"),
                retention=log_config.get("backup_count", 5),
                level=log_config.get("log_level", "INFO"),
                format=log_config.get("format", "{time} - {name} - {level} - {message}")
            )
    
    def execute_task(
        self,
        task_description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a task using the enterprise agent.
        
        Args:
            task_description: Description of the task to execute
            context: Optional context dictionary with additional information
        
        Returns:
            Dictionary with task execution results
        """
        logger.info(f"Executing task: {task_description}")
        
        try:
            # Task execution logic
            result = self._process_task(task_description, context or {})
            
            logger.info("Task completed successfully")
            return {
                "status": "success",
                "result": result,
                "timestamp": datetime.now().isoformat(),
                "agent": self.name
            }
        
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "agent": self.name
            }
    
    def _process_task(
        self,
        task_description: str,
        context: Dict[str, Any]
    ) -> Any:
        """
        Process the actual task (to be implemented based on specific use case).
        
        Args:
            task_description: Task description
            context: Context dictionary
        
        Returns:
            Task result
        """
        # Basic implementation of task processing
        task_lower = task_description.lower()
        
        if "echo" in task_lower:
            return {"action": "echo", "output": task_description.replace("echo", "").strip()}
        
        elif "reverse" in task_lower:
             text_to_reverse = task_description.replace("reverse", "").strip()
             return {"action": "reverse", "output": text_to_reverse[::-1]}
             
        elif "calculate" in task_lower:
            try:
                # WARNING: eval is dangerous in production, using for simple demo only
                # In a real enterprise agent, use a safe math parser
                expression = task_description.replace("calculate", "").strip()
                # Simple safety check - only allow digits and basic math operators
                if not all(c.isdigit() or c.isspace() or c in "+-*/()." for c in expression):
                     raise ValueError("Unsafe characters in expression")
                return {"action": "calculate", "expression": expression, "result": eval(expression)}
            except Exception as e:
                return {"action": "calculate", "error": str(e)}
        
        else:
            # Use LLM for general tasks
            try:
                from src.tools.llm_client import LLMClient
                llm = LLMClient() # Fixed: removed config_dict argument
                response = llm.query(task_description)
                return {
                    "action": "llm_query",
                    "output": response,
                    "model": llm.model,
                    "mode": "mock" if llm.use_mock else "real"
                }
            except Exception as e:
                logger.error(f"LLM processing failed: {e}")
                return {
                    "task": task_description,
                    "context": context,
                    "processed": False,
                    "error": str(e)
                }
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities."""
        return self.config.get("agent", {}).get("capabilities", [])
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "name": self.name,
            "version": self.version,
            "status": "active",
            "capabilities": self.get_capabilities(),
            "timestamp": datetime.now().isoformat()
        }

