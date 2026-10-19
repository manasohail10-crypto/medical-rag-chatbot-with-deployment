from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from app.components.llm import load_llm
from app.components.vectorstore import load_vector_store
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE = """
Answer the question strictly based on the context provided.
If the answer is not in the context, say "I don't know based on the provided documents."
Context: {context}
Question: {question}
Answer: 
"""

def set_custom_prompt():
  try:
    prompt_template = PromptTemplate(
      template=CUSTOM_PROMPT_TEMPLATE,
      input_variables=["context", "question"]
    )
    return prompt_template
  except Exception as e:
    logger.error(f"Error setting custom prompt: {e}")
    raise CustomException(message=f"Error setting custom prompt: {str(e)}") from e

def create_qa_chain():
  try:
    logger.info("Loading a VectorStore for the Context")
    db = load_vector_store()
    if db is None:
      logger.error("VectorStore is not available")
      raise CustomException(message="VectorStore is not available")
    llm = load_llm()
    if llm is None:
      logger.error("LLM is not available")
      raise CustomException(message="LLM is not available")
    logger.info("Creating a Retriever from the VectorStore")
    qa_chain = RetrievalQA.from_chain_type(
      llm=llm,
      chain_type="stuff",
      retriever=db.as_retriever(
        search_kwargs={
          "k": 2
        }
      ),
      return_source_documents=True,
      chain_type_kwargs={"prompt": set_custom_prompt()}
    )
    logger.info("QA chain created successfully")
    return qa_chain
  except CustomException as e:
    logger.error(f"Error creating QA chain: {e}")
    raise
  except Exception as e:
    logger.error(f"Unexpected error creating QA chain: {e}")
    raise CustomException(message=f"Unexpected error creating QA chain: {str(e)}") from e