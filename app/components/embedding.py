from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import EMBEDDING_MODEL_NAME

logger = get_logger(__name__)

@lru_cache(maxsize=1)
def get_embedding_model():
  try:
    logger.info("Loading embedding model")
    model_name = EMBEDDING_MODEL_NAME
    embedding_model = HuggingFaceEmbeddings(
      model_name=model_name,
      encode_kwargs={"normalize_embeddings": True}
    )
    logger.info(f"Embedding model {model_name} loaded successfully")
    return embedding_model
  except Exception as e:
    error_message = CustomException(message=f"Error loading embedding model: {str(e)}")
    logger.error(f"Error loading embedding model: {str(e)}")
    raise error_message from e