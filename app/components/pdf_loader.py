import os 
from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import DATA_PATH,CHUNK_OVERLAP,CHUNK_SIZE

logger = get_logger(__name__)


def load_pdf_file():
  try:
    if not os.path.exists(DATA_PATH):
      raise CustomException(message="PDF file not found")
    logger.info(f'Loading PDF files {DATA_PATH}')
    loader = DirectoryLoader(DATA_PATH,glob='*.pdf',loader_cls=PyPDFLoader)
    documents = loader.load()
    if not documents:
      logger.warning("No documents found")
    logger.info(f"{len(documents)} PDF files loaded successfully")
    return documents
  except Exception as e:
    error_meesage = CustomException(message=f"Error loading PDF files: {str(e)}")
    logger.error(f"Error loading PDF files: {str(e)}")
    raise error_meesage


def create_text_chunk(documents):
  try:
    if not documents:
      raise CustomException(message="No documents found")
    logger.info(f"Creating text chunks from {len(documents)} documents")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP,separators=["\n\n", "\n", ".", " "])
    chunks = text_splitter.split_documents(documents)
    logger.info(f"{len(chunks)} text chunks created successfully")
    return chunks
  except Exception as e:
    error_meesage = CustomException(message=f"Error creating text chunks: {str(e)}")
    logger.error(f"Error creating text chunks: {str(e)}")
    raise error_meesage


