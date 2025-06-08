# Gerador de Contratos

Aplicação simples em Flask para gerar contratos a partir de um modelo `.docx` e enviar por e-mail.

## Requisitos

- Python 3.10+
- Pacotes listados em `requirements.txt`

## Configuração

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Copie `.env.example` para `.env` e preencha `EMAIL_USER` e `EMAIL_PASS` com os dados de sua conta de e-mail. Opcionalmente ajuste `DEFAULT_RECIPIENT`, `SMTP_SERVER` e `SMTP_PORT`. O arquivo `.env` é carregado automaticamente pela aplicação.

## Uso

Execute a aplicação com:

```bash
python3 app.py
```

Acesse `http://localhost:5000` em seu navegador, preencha o formulário e envie. O contrato será preenchido com os dados informados e enviado para o e-mail configurado.
Após o envio, uma mensagem indicará se o e-mail foi enviado com sucesso ou se ocorreu algum erro.

O arquivo `Contrato Vitorino.docx` é o modelo utilizado e **não deve ser alterado**.
