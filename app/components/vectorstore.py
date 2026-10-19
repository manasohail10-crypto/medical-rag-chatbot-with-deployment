import os
import time
from langchain_community.vectorstores import FAISS
from app.components.embedding import get_embedding_model
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import DB_FAISS_PATH

logger = get_logger(__name__)

BATCH_SIZE = 32

def load_vector_store():
  try:
    embedding_model = get_embedding_model()
    logger.info(f"Loading vectorstore from {DB_FAISS_PATH}")
    if os.path.exists(os.path.join(DB_FAISS_PATH, "index.faiss")):
      logger.info("Loading existing vector store")
      return FAISS.load_local(DB_FAISS_PATH,embedding_model,allow_dangerous_deserialization=True)
    else:
      logger.error("No VectorStore Found")
      raise CustomException(message="No VectorStore Found")
  except CustomException:
    raise
  except Exception as e:
    error_message = CustomException(message=f"Error loading vectorstore: {str(e)}")
    logger.error(f"Error loading vectorstore: {str(e)}")
    raise error_message from e


def create_vectorstore(documents):
  try:
    if not documents:
      logger.error("No documents provided")
      raise CustomException(message="No documents provided")
    total = len(documents)
    logger.info(f"Creating vectorstore from {total} chunks")
    embedding_model = get_embedding_model()
    db = None
    start = time.time()
    for i in range(0, total, BATCH_SIZE):
      batch = documents[i:i + BATCH_SIZE]
      if db is None:
        db = FAISS.from_documents(documents=batch,embedding=embedding_model)
      else:
        db.add_documents(batch)
      done = min(i + BATCH_SIZE, total)
      elapsed = time.time() - start
      minutes_left = (elapsed / done) * (total - done) / 60
      logger.info(f"Embedded {done}/{total} chunks | {elapsed / 60:.1f} min used | about {minutes_left:.1f} min left")
    db.save_local(DB_FAISS_PATH)
    logger.info(f"Vectorstore created and saved to {DB_FAISS_PATH}")
    return db
  except CustomException:
    raise
  except Exception as e:
    error_message = CustomException(message=f"Error creating vectorstore: {str(e)}")
    logger.error(f"Error creating vectorstore: {str(e)}")
    raise error_message from e