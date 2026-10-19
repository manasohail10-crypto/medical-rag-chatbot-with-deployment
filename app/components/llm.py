from langchain_groq import ChatGroq
from app.config.config import GROQ_API_KEY,LLM_MODEL_NAME
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_llm(model_name=LLM_MODEL_NAME):
  try:
    if not GROQ_API_KEY:
      logger.error("GROQ_API_KEY is missing")
      raise CustomException(message="GROQ_API_KEY is missing")
    logger.info(f"Loading LLM {model_name}")
    llm = ChatGroq(
      model=model_name,
      temperature=0.3,
      max_tokens=512
    )
    logger.info("LLM loaded successfully")
    return llm
  except CustomException:
    raise
  except Exception as e:
    logger.error(f"Error in loading LLM: {str(e)}")
    raise CustomException(message=f"Error in loading LLM: {str(e)}") from e