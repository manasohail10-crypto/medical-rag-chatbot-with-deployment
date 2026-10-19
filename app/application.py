import os
from functools import lru_cache
from flask import Flask,render_template,request,session,redirect,url_for
from flask_session import Session
from dotenv import load_dotenv
from app.components.retriever import create_qa_chain
from app.common.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

MAX_PROMPT_LENGTH = 2000

app = Flask(__name__)

secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY is missing. Add it to your .env file.")
app.secret_key = secret_key

# Keep chat history on the server, because a normal Flask cookie session is limited to about 4 KB
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(os.getcwd() , "flask_session")
app.config["SESSION_PERMANENT"] = False
Session(app)


@lru_cache(maxsize=1)
def get_qa_chain():
    # Built once and reused, so the FAISS index is not loaded again for every question
    return create_qa_chain()


@app.route("/" , methods=["GET","POST"])
def index():
    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        user_input = (request.form.get("prompt") or "").strip()

        if not user_input:
            return redirect(url_for("index"))

        if len(user_input) > MAX_PROMPT_LENGTH:
            session["error"] = f"Your question is too long. Please keep it under {MAX_PROMPT_LENGTH} characters."
            return redirect(url_for("index"))

        messages = session["messages"]
        messages.append({"role" : "user" , "content" : user_input})
        session["messages"] = messages

        try:
            response = get_qa_chain().invoke({"query" : user_input})
            result = response.get("result" , "No response")

            messages.append({"role" : "assistant" , "content" : result})
            session["messages"] = messages

        except Exception:
            logger.exception("Error while answering the question")
            session["error"] = "Sorry, something went wrong while answering. Please try again."

        return redirect(url_for("index"))

    error = session.pop("error" , None)
    return render_template("index.html" , messages=session.get("messages" , []) , error=error)


@app.route("/clear")
def clear():
    session.pop("messages" , None)
    session.pop("error" , None)
    return redirect(url_for("index"))


if __name__=="__main__":
    app.run(host="0.0.0.0" , port=5000 , debug=False , use_reloader=False)