# Simple web app to generate and send contract via email
import os
from flask import Flask, render_template, request
from flask import Flask, render_template_string, request
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


app = Flask(__name__)

FORM_HTML = """
<!doctype html>
<title>Gerar Contrato</title>
<h1>Preencha os dados do contrato</h1>
<form method=post>
  <label>Nome completo:<input type=text name=Comprador required></label><br>
  <label>CPF:<input type=text name=CPF required></label><br>
  <label>RG:<input type=text name=RG required></label><br>
  <label>Órgão emissor:<input type=text name=Emissor required></label><br>
  <label>Estado civil:<input type=text name=EstadoCivil required></label><br>
  <label>Profissão:<input type=text name=Profissao required></label><br>
  <label>Endereço:<input type=text name=Endereco required></label><br>
  <label>Número:<input type=text name=Numero required></label><br>
  <label>Complemento:<input type=text name=Complemento></label><br>
  <label>Bairro:<input type=text name=Bairro required></label><br>
  <label>Cidade:<input type=text name=Cidade required></label><br>
  <label>CEP:<input type=text name=CEP required></label><br>
  <label>Quadra:<input type=text name=Quadra required></label><br>
  <label>Lote:<input type=text name=Lote required></label><br>
  <label>Testemunha 1:<input type=text name=Testemunha required></label><br>
  <label>CPF Testemunha 1:<input type=text name=CPFTest required></label><br>
  <label>Testemunha 2:<input type=text name=Testemunha2 required></label><br>
  <label>CPF Testemunha 2:<input type=text name=CPFTest2 required></label><br>
  <input type=submit value=Gerar>
</form>
{% if status %}<p>{{status}}</p>{% endif %}
"""

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'Contrato Vitorino.docx')
RECIPIENT = os.environ.get('DEFAULT_RECIPIENT', 'rba1807@gmail.com')

@app.route('/', methods=['GET', 'POST'])
def index():
    status = ''
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
        except Exception as e:
            status = f'Falha ao enviar: {e}'
    return render_template("form.html", status=status)
    return render_template_string(FORM_HTML, status=status)

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
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
