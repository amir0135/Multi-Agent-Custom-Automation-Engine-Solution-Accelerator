"""Advanced test script for the ContentProcessingAgent focusing on PDF functionality"""

import asyncio
import os
import sys
import tempfile
import io

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # src/backend
sys.path.insert(0, parent_dir)

# Create a simple mock for AgentType since we don't need the actual enum for testing
class MockAgentType:
    class CONTENT_PROCESSING:
        value = "Content_Processing_Agent"

# Monkey patch the import in content_tools
sys.modules['models.messages_kernel'] = type('MockModule', (), {'AgentType': MockAgentType})

# Now import our content tools
from kernel_tools.content_tools import ContentTools

# Override agent_name in ContentTools for testing
ContentTools.agent_name = MockAgentType.CONTENT_PROCESSING

# Check if PyMuPDF is installed
try:
    import fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("PyMuPDF not installed. PDF tests will be skipped.")

async def create_test_pdf():
    """Create a simple PDF for testing"""
    if not PYMUPDF_AVAILABLE:
        return None
        
    pdf_path = os.path.join(tempfile.gettempdir(), "test_document.pdf")
    
    # Create a new PDF
    doc = fitz.open()
    page = doc.new_page()
    
    # Add a title
    page.insert_text((50, 50), "Test Document", fontsize=16)
    
    # Add some content
    page.insert_text((50, 100), "Section 1: Introduction", fontsize=14)
    page.insert_text((50, 130), "This is a test document created for testing the ContentTools.", fontsize=12)
    
    page.insert_text((50, 180), "Section 2: Main Content", fontsize=14)
    page.insert_text((50, 210), "This section contains the main content of the document.", fontsize=12)
    page.insert_text((50, 240), "It demonstrates the text extraction capabilities.", fontsize=12)
    
    page.insert_text((50, 290), "Section 3: Conclusion", fontsize=14)
    page.insert_text((50, 320), "This is the conclusion of the test document.", fontsize=12)
    
    # Save the PDF
    doc.save(pdf_path)
    doc.close()
    
    return pdf_path

async def test_pdf_extraction():
    """Test the PDF extraction functionality"""
    if not PYMUPDF_AVAILABLE:
        print("Skipping PDF extraction test as PyMuPDF is not available")
        return
        
    print("\nTesting PDF extraction...")
    
    # Create a test PDF
    pdf_path = await create_test_pdf()
    if not pdf_path:
        print("Could not create test PDF")
        return
        
    try:
        # Test extracting text from PDF
        extracted_text = await ContentTools.extract_text_from_pdf(pdf_path)
        print(f"Extracted text from PDF:\n{extracted_text}")
        
        # Test tables extraction (placeholder function)
        tables_json = await ContentTools.extract_tables_from_pdf(pdf_path)
        print(f"\nExtracted tables from PDF:\n{tables_json}")
        
        # Test parsing sections from extracted text
        sections_json = await ContentTools.parse_sections(extracted_text)
        print(f"\nParsed sections from PDF text:\n{sections_json}")
        
        print("\nPDF tests completed successfully!")
    finally:
        # Clean up
        if pdf_path and os.path.exists(pdf_path):
            os.unlink(pdf_path)

async def main():
    """Main test function"""
    print("Testing ContentTools advanced features...")
    
    # Run the PDF extraction test
    await test_pdf_extraction()

if __name__ == "__main__":
    asyncio.run(main())
