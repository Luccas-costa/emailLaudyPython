from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException
from fastapi.responses import JSONResponse
from email.message import EmailMessage
import smtplib
import os

app = FastAPI(title="Email API LaudyCardio")

# ===== CONFIGURAÇÕES =====
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

API_KEY = os.getenv("API_KEY")


@app.get("/")
def home():
    return {"status": "API funcionando!"}


from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException
from fastapi.responses import JSONResponse
from email.message import EmailMessage
import smtplib
import mimetypes

@app.post("/enviar-email")
async def enviar_email(
    email: str = Form(...),
    assunto: str = Form(...),
    mensagem: str = Form(...),
    arquivo: UploadFile = File(...),
    x_api_key: str = Header(None)
):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")

    try:

        conteudo = await arquivo.read()

        msg = EmailMessage()

        msg["Subject"] = assunto
        msg["From"] = SMTP_USER
        msg["To"] = email

        msg.set_content(mensagem)

        tipo, _ = mimetypes.guess_type(arquivo.filename)

        if tipo:
            maintype, subtype = tipo.split("/")
        else:
            maintype = "application"
            subtype = "octet-stream"

        msg.add_attachment(
            conteudo,
            maintype=maintype,
            subtype=subtype,
            filename=arquivo.filename
        )

        smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)
        smtp.quit()

        return {
            "sucesso": True
        }

    except Exception as ex:

        return JSONResponse(
            status_code=500,
            content={
                "sucesso": False,
                "erro": str(ex)
            }
        )