import inspect
import logging
import json
from typing import Callable, Dict, List, Optional, get_type_hints
import os

import fitz  # PyMuPDF
from semantic_kernel.functions import kernel_function
from models.messages_kernel import AgentType


class ContentTools:
    """Define Content Processing functions (tools) for document extraction and processing"""

    agent_name = AgentType.CONTENT_PROCESSING.value

    @staticmethod
    @kernel_function(
        description="Extract text content from a PDF document."
    )
    async def extract_text_from_pdf(file_path: str) -> str:
        """
        Extract all text content from a PDF document.
        
        Args:
            file_path: The path to the PDF file to extract text from
            
        Returns:
            The extracted text content from all pages
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return f"Error: File not found at {file_path}"
            
            # Open the PDF document
            doc = fitz.open(file_path)
            text = ""
            
            # Extract text from each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += page.get_text()
            
            doc.close()
            return text
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {str(e)}")
            return f"Error extracting text from PDF: {str(e)}"

    @staticmethod
    @kernel_function(
        description="Parse a document into logical sections based on headings and structure."
    )
    async def parse_sections(text: str, min_section_length: int = 100) -> str:
        """
        Parse a document text into logical sections based on headings and structure.
        
        Args:
            text: The document text to parse
            min_section_length: Minimum character length for a section to be considered valid
            
        Returns:
            JSON string containing the identified sections with titles and content
        """
        try:
            # Split text by lines
            lines = text.split('\n')
            sections = []
            current_section = {"title": "Introduction", "content": ""}
            
            # Simple heuristic to identify headings and section breaks
            for line in lines:
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Potential heading detection (simplified heuristic)
                is_heading = (
                    (len(line) < 100 and line.isupper()) or  # ALL CAPS lines
                    (len(line) < 80 and line.endswith(':')) or  # Lines ending with colon
                    any(line.startswith(prefix) for prefix in ["#", "Chapter", "Section"]) or  # Markdown or explicit headings
                    (len(line) < 60 and not line.endswith('.') and not line.endswith(','))  # Short lines not ending with punctuation
                )
                
                if is_heading:
                    # Save previous section if it has enough content
                    if len(current_section["content"]) >= min_section_length:
                        sections.append(current_section)
                    
                    # Start new section
                    current_section = {"title": line, "content": ""}
                else:
                    # Add line to current section
                    current_section["content"] += line + "\n"
            
            # Add the last section if it has content
            if len(current_section["content"]) >= min_section_length:
                sections.append(current_section)
            
            return json.dumps(sections, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error parsing sections: {str(e)}")
            return f"Error parsing sections: {str(e)}"

    @staticmethod
    @kernel_function(
        description="Summarize text content to a specified length."
    )
    async def summarize_text(text: str, max_length: int = 1000) -> str:
        """
        Summarize text content to a specified maximum length.
        Note: This is a placeholder. In a real implementation, this would use an LLM to create the summary.
        
        Args:
            text: The text to summarize
            max_length: Maximum length for the summary in characters
            
        Returns:
            Summarized text
        """
        # This is a placeholder - in a real implementation, you would call an LLM here
        # In this solution, we're using Azure OpenAI, so other agents would handle the summarization
        if len(text) <= max_length:
            return text
        
        return f"This is a placeholder for text summarization. In a real implementation, " \
               f"this would call the Azure OpenAI service to summarize the input text " \
               f"which is {len(text)} characters long to a maximum of {max_length} characters."
               
    @staticmethod
    @kernel_function(
        description="Connect to SharePoint and retrieve documents from a specified library"
    )
    async def get_documents_from_sharepoint(
        site_url: str, 
        library_name: str, 
        username: str = None, 
        password: str = None
    ) -> str:
        """
        Connect to SharePoint and retrieve documents from a specified document library.
        Note: This is a placeholder. In a real implementation, this would use Microsoft Graph API.
        
        Args:
            site_url: The SharePoint site URL
            library_name: The document library name
            username: Optional username for authentication
            password: Optional password for authentication
            
        Returns:
            JSON string containing the list of documents found
        """
        # This is a placeholder - in a real implementation, you would use Microsoft Graph API
        example_docs = [
            {"name": "Product_Specifications.pdf", "size": "1.2 MB", "modified": "2025-07-30"},
            {"name": "Technical_Manual.docx", "size": "3.5 MB", "modified": "2025-08-01"},
            {"name": "Project_Plan.xlsx", "size": "0.8 MB", "modified": "2025-08-02"}
        ]
        
        return json.dumps({
            "site": site_url,
            "library": library_name,
            "documents": example_docs
        }, ensure_ascii=False)
        
    @staticmethod
    @kernel_function(
        description="Extract tables from a PDF document as structured data"
    )
    async def extract_tables_from_pdf(file_path: str) -> str:
        """
        Extract tables from a PDF document and convert them to structured data.
        Note: This is a placeholder. In a real implementation, this would use a PDF table extraction library.
        
        Args:
            file_path: The path to the PDF file
            
        Returns:
            JSON string containing the extracted tables
        """
        # This is a placeholder - in a real implementation, you would use a library like tabula-py
        example_table = [
            ["ID", "Name", "Department", "Role"],
            ["1", "John Smith", "Engineering", "Senior Developer"],
            ["2", "Jane Doe", "Marketing", "Director"],
            ["3", "Robert Johnson", "Finance", "Analyst"]
        ]
        
        return json.dumps({
            "file": file_path,
            "tables": [
                {
                    "page": 1,
                    "data": example_table
                }
            ]
        }, ensure_ascii=False)

    @classmethod
    def get_all_kernel_functions(cls) -> Dict[str, Callable]:
        """
        Returns a dictionary of all methods in this class that have the @kernel_function annotation.
        
        Returns:
            Dict[str, Callable]: Dictionary with function names as keys and function objects as values
        """
        kernel_functions = {}

        # Get all class methods
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            # Skip this method itself and any private/special methods
            if name.startswith("_") or name == "get_all_kernel_functions":
                continue

            # Check if the method has the kernel_function annotation
            if hasattr(method, "__kernel_function__") or "kernel_function" in str(
                getattr(method, "__annotations__", {})
            ):
                kernel_functions[name] = method

        return kernel_functions

    @classmethod
    def generate_tools_json_doc(cls) -> str:
        """
        Generate a JSON document containing information about all methods in the class.

        Returns:
            str: JSON string containing the methods' information
        """
        tools_list = []

        # Get all methods from the class that have the kernel_function annotation
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            # Skip this method itself and any private methods
            if name.startswith("_") or name == "generate_tools_json_doc":
                continue

            # Check if the method has the kernel_function annotation
            if hasattr(method, "__kernel_function__"):
                # Get method description from docstring or kernel_function description
                description = ""
                if hasattr(method, "__doc__") and method.__doc__:
                    description = method.__doc__.strip()

                # Get kernel_function description if available
                if hasattr(method, "__kernel_function__") and getattr(
                    method.__kernel_function__, "description", None
                ):
                    description = method.__kernel_function__.description

                # Get argument information by introspection
                sig = inspect.signature(method)
                args_dict = {}

                # Get type hints if available
                type_hints = get_type_hints(method)

                # Process parameters
                for param_name, param in sig.parameters.items():
                    # Skip first parameter 'cls' for class methods (though we're using staticmethod now)
                    if param_name in ["cls", "self"]:
                        continue

                    # Get parameter type
                    param_type = "string"  # Default type
                    if param_name in type_hints:
                        type_obj = type_hints[param_name]
                        # Convert type to string representation
                        if hasattr(type_obj, "__name__"):
                            param_type = type_obj.__name__.lower()
                        else:
                            # Handle complex types like List, Dict, etc.
                            param_type = str(type_obj).lower()
                            if "int" in param_type:
                                param_type = "int"
                            elif "float" in param_type:
                                param_type = "float"
                            elif "bool" in param_type:
                                param_type = "boolean"
                            else:
                                param_type = "string"

                    # Create parameter description
                    args_dict[param_name] = {
                        "description": param_name,
                        "title": param_name.replace("_", " ").title(),
                        "type": param_type,
                    }

                # Add the tool information to the list
                tool_entry = {
                    "agent": cls.agent_name,
                    "function": name,
                    "description": description,
                    "arguments": json.dumps(args_dict).replace('"', "'"),
                }

                tools_list.append(tool_entry)

        # Return the JSON string representation
        return json.dumps(tools_list, ensure_ascii=False, indent=2)
