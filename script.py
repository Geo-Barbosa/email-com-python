from datetime import date
from zipfile import ZipFile, ZIP_DEFLATED
import os
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviar_email(email_cont, ano_mes, cnpj, perfil):
    ano = ano_mes[:4]
    mes = ano_mes[4:]
    cnpj_formatado = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
    subject = f"Arquivos Fiscais | Mês {mes} de {ano} | CNPJ: {cnpj_formatado} | Caixa {perfil}"
    body = (f"Olá, prezados!\n"
            f"Segue em anexo os arquivos fiscais do mês {mes} de {ano} da empresa de CNPJ {cnpj_formatado} do Caixa {perfil}\n"
            f"Este é um email de envio automático, por favor, não responda!\n"
            f"Qualquer dúvida, por favor entre em contato no número (11) 5032-1007 (De segunda à sexta, 9h às 18h)\n"
            f"Atenciosamente\n") # O corpo do Email vai aqui
    sender_email = "naoresponda@ggautomacao.com.br" # O email fonte vai aqui
    receiver_email = email_cont # Para quem o email será encaminhado
    password = "ggpaco@123" # Senha do email fonte

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = f"{ano_mes} - Caixa {perfil}.zip"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def remove_pula_linha(var):
    for y in var:
        var = var.rstrip('\n')
    return var


def anoMes():
    ano = date.today().year
    mes = date.today().month
    if mes == 1:
        ano = ano - 1
        mes = 12
    elif mes < 10:
        mes = f'0{mes-1}'
    else:
        mes = mes - 1
    return f'{ano}{mes}'


def compactar(diretorio, ano_mes, perfil):
            arquivos = os.listdir(diretorio)
            arquivozip = ZipFile(f'{ano_mes} - Caixa {perfil}.zip', 'w', compression=ZIP_DEFLATED)
            for nome in arquivos:
                arquivozip.write(f'{diretorio}/{nome}', nome)
            arquivozip.close()


def excluir_pasta(ano_mes, perfil):
    os.remove(f'{ano_mes} - Caixa {perfil}.zip')
    return True


def excluir_passado(ano_mes):
    ano = int(ano_mes[:4])
    mes = int(ano_mes[4:])
    if mes == 1:
        ano = ano - 1
        mes = 12
    elif mes == 10:
        mes = '09'
    else:
        mes = mes - 1
    if os.path.exists(f'C:/Pacnet/pdv/{ano}{mes}.pac'):
        os.remove(f'C:/Pacnet/pdv/{ano}{mes}.pac')


file = open('config.ini', 'r')
x = file.readline(5)
cnpj = file.readline()
cnpj = remove_pula_linha(cnpj)
x = file.readline(19)
emailCont = file.readline()
emailCont = remove_pula_linha(emailCont)
x = file.readline(7)
perfil = file.readline()
file.close()
anoMes = anoMes()
if os.path.exists(f'C:/Pacnet/pdv/{anoMes}.pac'):
    pass
else:
    diretorio = f'C:/Pacnet/pdv/Vendas/{cnpj}/{anoMes}'
    compactar(diretorio, anoMes, perfil)
    enviar_email(emailCont, anoMes, cnpj, perfil)
    controle = excluir_pasta(anoMes, perfil)
    if controle:
        arquivo = ZipFile(f'C:/Pacnet/pdv/{anoMes}.pac', 'w')
        arquivo.close()
    else:
        pass
excluir_passado(anoMes)
