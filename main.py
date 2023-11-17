from flask import Flask, make_response, send_file
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import urllib.parse

app = Flask(__name__)

@app.route("/pdf/<nome>/<cpf>/<chavepix>/<instituicao>")
def pdf(nome, cpf, chavepix, instituicao):
    # cria uma imagem com os dados passados na URL
    imagem = Image.open('comprovante.jpg')
    draw = ImageDraw.Draw(imagem)
    fonte = ImageFont.truetype('Gill Sans Bold.otf', 40)
    valor = "R$ 977,94"
    dataehora = datetime.now()
    data = dataehora.strftime("%d/%m/%Y")
    horario = dataehora.strftime("%H:%M:%S")
    draw.text((410,530), valor,font=fonte,fill=(3,92,167,255))
    draw.text((1215,530), data,font=fonte,fill=(3,92,167,255))
    fonte = ImageFont.truetype('Gill Sans.otf', 28)
    draw.text((1260,570), horario,font=fonte,fill=(3,92,167,255))
    fonte = ImageFont.truetype('Gill Sans Bold.otf', 30)
    nome_formatado = urllib.parse.unquote_plus(nome)
    draw.text((68,930), nome_formatado,font=fonte,fill=(58,72,88,255))
    fonte = ImageFont.truetype('Gill Sans Bold.otf', 35)
    draw.text((68,1050), formatar_cpf(cpf),font=fonte,fill=(58,72,88,255))
    fonte = ImageFont.truetype('Gill Sans Bold.otf', 30)
    instituicao_formatada = urllib.parse.unquote_plus(instituicao)
    draw.text((66,1180), instituicao_formatada,font=fonte,fill=(58,72,88,255))
    fonte = ImageFont.truetype('Gill Sans Bold.otf', 33)
    draw.text((58,2055), valor.replace("R$",""),font=fonte,fill=(58,72,88,255))
    draw.text((60,2180), dataehora.strftime("%d/%m/%Y - %H:%M:%S"),font=fonte,fill=(58,72,88,255))
    draw.text((64,2540), chavepix,font=fonte,fill=(58,72,88,255))
    # salva a imagem em um arquivo temporário
    imagem.save("temp.pdf", format="PDF")
    # envia o arquivo para o cliente
    return send_file("temp.pdf", mimetype="application/pdf")

def formatar_cpf(cpf):
    # verifica se o cpf é uma string com 11 dígitos
    if isinstance(cpf, str) and len(cpf) == 11 and cpf.isdigit():
        # insere os pontos e o traço nos lugares certos
        cpf_formatado = cpf[:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:]
        # retorna o cpf formatado
        return cpf_formatado
    else:
        # retorna uma mensagem de erro se o cpf for inválido
        return "CPF inválido"

if __name__ == "__main__":
    app.run(debug=True)