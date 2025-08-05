"""Test script for the ContentProcessingAgent and ContentTools"""

import asyncio
import os
import sys
import tempfile
import json

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # src/backend
sys.path.insert(0, parent_dir)

from kernel_tools.content_tools import ContentTools

# Create a simple mock for AgentType since we don't need the actual enum for testing
class MockAgentType:
    class CONTENT_PROCESSING:
        value = "Content_Processing_Agent"

# Monkey patch the import in content_tools
sys.modules['models.messages_kernel'] = type('MockModule', (), {'AgentType': MockAgentType})

# Override agent_name in ContentTools for testing
ContentTools.agent_name = MockAgentType.CONTENT_PROCESSING

async def test_content_tools():
    """Test the ContentTools class functions"""
    print("Testing ContentTools...")
    
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(suffix='.txt', mode='w', delete=False) as temp_file:
        temp_file.write("This is a test document.\n\n")
        temp_file.write("# Section 1: Introduction\n\n")
        temp_file.write("This is the introduction section with some content.\n\n")
        temp_file.write("# Section 2: Main Content\n\n")
        temp_file.write("This is the main content section with more details.\n\n")
        temp_file.write("# Section 3: Conclusion\n\n")
        temp_file.write("This is the conclusion section that summarizes the document.\n\n")
        temp_path = temp_file.name
    
    try:
        # Test parse_sections function
        print("Testing parse_sections...")
        sections_json = await ContentTools.parse_sections(open(temp_path).read())
        print(f"parse_sections result: {sections_json}")
        
        # Test summarize_text function
        print("\nTesting summarize_text...")
        summary = await ContentTools.summarize_text("This is a long text that needs to be summarized. It contains multiple sentences and should be shortened by the summarization function.")
        print(f"summarize_text result: {summary}")
        
        # Test SharePoint connection placeholder
        print("\nTesting get_documents_from_sharepoint...")
        sharepoint_result = await ContentTools.get_documents_from_sharepoint(
            "https://contoso.sharepoint.com/sites/documents", 
            "Technical Documentation"
        )
        print(f"get_documents_from_sharepoint result: {sharepoint_result}")
        
        print("\nAll tests completed successfully!")
    finally:
        # Clean up
        os.unlink(temp_path)

if __name__ == "__main__":
    asyncio.run(test_content_tools())
