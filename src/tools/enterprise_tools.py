"""
Enterprise tools for agent operations - API clients, database queries, file processing, etc.
"""

import requests
from typing import Dict, Any, Optional, List
from pathlib import Path
from loguru import logger


class APIClient:
    """Tool for making API calls to enterprise systems."""
    
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        retry_attempts: int = 3,
        headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts
            headers: Default headers for requests
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.headers = headers or {}
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(self.retry_attempts):
            try:
                response = requests.get(
                    url,
                    params=params,
                    headers=self.headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == self.retry_attempts - 1:
                    logger.error(f"API GET request failed after {self.retry_attempts} attempts: {e}")
                    raise
                logger.warning(f"API GET request attempt {attempt + 1} failed, retrying...")
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(self.retry_attempts):
            try:
                response = requests.post(
                    url,
                    data=data,
                    json=json,
                    headers=self.headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == self.retry_attempts - 1:
                    logger.error(f"API POST request failed after {self.retry_attempts} attempts: {e}")
                    raise
                logger.warning(f"API POST request attempt {attempt + 1} failed, retrying...")


class DatabaseQuery:
    """Tool for executing database queries."""
    
    def __init__(self, connection_string: str):
        """
        Initialize database query tool.
        
        Args:
            connection_string: Database connection string
        """
        self.connection_string = connection_string
        logger.info("Database query tool initialized")
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Execute a database query.
        
        Args:
            query: SQL query string
            params: Query parameters
        
        Returns:
            Query results as list of dictionaries
        """
        # Placeholder implementation
        # In production, this would use SQLAlchemy or similar ORM
        logger.info(f"Executing database query: {query[:50]}...")
        return []


class FileProcessor:
    """Tool for processing files."""
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize file processor.
        
        Args:
            base_path: Base path for file operations
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        logger.info(f"File processor initialized with base path: {self.base_path}")
    
    def read_file(self, file_path: str) -> str:
        """
        Read file content.
        
        Args:
            file_path: Path to file (relative to base_path)
        
        Returns:
            File content as string
        """
        full_path = self.base_path / file_path
        logger.info(f"Reading file: {full_path}")
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {full_path}")
        
        return full_path.read_text(encoding='utf-8')
    
    def write_file(self, file_path: str, content: str) -> None:
        """
        Write content to file.
        
        Args:
            file_path: Path to file (relative to base_path)
            content: Content to write
        """
        full_path = self.base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Writing file: {full_path}")
        full_path.write_text(content, encoding='utf-8')

    def list_files(self, directory: str = ".", pattern: str = "*") -> List[str]:
        """
        List files in a directory.
        
        Args:
            directory: Directory to list (relative to base_path)
            pattern: Glob pattern to filter files
            
        Returns:
            List of file paths
        """
        dir_path = self.base_path / directory
        if not dir_path.exists():
             raise FileNotFoundError(f"Directory not found: {dir_path}")
             
        return [str(p.relative_to(self.base_path)) for p in dir_path.glob(pattern) if p.is_file()]

