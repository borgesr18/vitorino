# Simple web app to generate and send contract via email
import os
from flask import Flask, render_template, request
from docxtpl import DocxTemplate
import smtplib
from email.message import EmailMessage
from io import BytesIO
from pathlib import Path


def load_env() -> None:
    """Load variables from a .env file if it exists."""
    env_path = Path(__file__).with_name('.env')
    if env_path.exists():
        with env_path.open() as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, val = line.split('=', 1)
                os.environ.setdefault(key.strip(), val.strip())


load_env()

app = Flask(__name__)


TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'Contrato Vitorino.docx')
RECIPIENT = os.environ.get('DEFAULT_RECIPIENT', 'rba1807@gmail.com')

@app.route('/', methods=['GET', 'POST'])
def index():
    status = ''
    status_type = ''
    if request.method == 'POST':
        data = {k: request.form.get(k) for k in request.form.keys()}
        try:
            doc = DocxTemplate(TEMPLATE_PATH)
            doc.render({
                'Comprador': data.get('Comprador'),
                'CPF': data.get('CPF'),
                'RG': data.get('RG'),
                'Emissor': data.get('Emissor'),
                'EstadoCivil': data.get('EstadoCivil'),
                'Profissao': data.get('Profissao'),
                'Endereço': data.get('Endereco'),
                'Numero': data.get('Numero'),
                'Complemento': data.get('Complemento'),
                'Bairro': data.get('Bairro'),
                'Cidade': data.get('Cidade'),
                'CEP': data.get('CEP'),
                'Quadra': data.get('Quadra'),
                'Lote': data.get('Lote'),
                'Testemunha': data.get('Testemunha'),
                'CPF Test': data.get('CPFTest'),
                'Testemunha2': data.get('Testemunha2'),
                'CPF Test2': data.get('CPFTest2'),
            })
            buf = BytesIO()
            doc.save(buf)
            buf.seek(0)
            send_email(buf.getvalue(), data.get('Comprador'))
            status = 'Contrato enviado com sucesso.'
            status_type = 'success'
        except Exception as e:
            status = f'Falha ao enviar: {e}'
            status_type = 'error'
    return render_template("form.html", status=status, status_type=status_type)

def send_email(content: bytes, comprador: str):
    user = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']
    msg = EmailMessage()
    msg['Subject'] = 'Contrato Gerado'
    msg['From'] = user
    msg['To'] = RECIPIENT
    msg.set_content(f'Contrato gerado para {comprador}.')
    msg.add_attachment(content, maintype='application', subtype='vnd.openxmlformats-officedocument.wordprocessingml.document', filename='Contrato.docx')
    host = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    port = int(os.environ.get('SMTP_PORT', '465'))
    with smtplib.SMTP_SSL(host, port) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
