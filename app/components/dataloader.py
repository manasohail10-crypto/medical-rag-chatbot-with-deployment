from app.components.pdf_loader import load_pdf_file,create_text_chunk
from app.components.vectorstore import create_vectorstore
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def process_and_store_Pdf():
  try:
    logger.info("Starting PDF processing")
    documents = load_pdf_file()
    logger.info("PDF files loaded successfully")
    chunks = create_text_chunk(documents)
    logger.info("Text chunks created")
    db = create_vectorstore(chunks)
    logger.info("VectorStore Created Successfully")
    return db
  except CustomException:
    raise
  except Exception as e:
    logger.error(f"Error in processing and storing PDF: {str(e)}")
    raise CustomException(message=f"Error in processing and storing PDF: {str(e)}") from e

if __name__ == "__main__":
  process_and_store_Pdf()