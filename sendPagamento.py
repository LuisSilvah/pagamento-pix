
import crcmod
import qrcode

def Payload (nome, chavepix, valor, cidade, txtId, fileNameQrcode):
    nome = nome
    chavepix = chavepix
    valor = valor.replace(',', '.')
    cidade = cidade
    txtId = txtId

    nome_tam = len(nome)
    chavepix_tam = len(chavepix)
    valor_tam = len(valor)
    cidade_tam = len(cidade)
    txtId_tam = len(txtId)

    merchantAccount_tam = f'0014BR.GOV.BCB.PIX01{chavepix_tam:02}{chavepix}'
    transactionAmount_tam = f'{valor_tam:02}{float(valor):.2f}'

    addDataField_tam = f'05{txtId_tam:02}{txtId}'

    nome_tam = f'{nome_tam:02}'

    cidade_tam = f'{cidade_tam:02}'

    payloadFormat = '000201'
    merchantAccount = f'26{len(merchantAccount_tam):02}{merchantAccount_tam}'
    merchantCategCode = '52040000'
    transactionCurrency = '5303986'
    transactionAmount = f'54{transactionAmount_tam}'
    countryCode = '5802BR'
    merchantName = f'59{nome_tam:02}{nome}'
    merchantCity = f'60{cidade_tam:02}{cidade}'
    addDataField = f'62{len(addDataField_tam):02}{addDataField_tam}'
    crc16 = '6304'
    
    payload = gerarPayload(payloadFormat, merchantAccount, merchantCategCode, transactionCurrency, transactionAmount, countryCode, merchantName, merchantCity, addDataField, crc16)

    imgQrcode = qrcode.make(payload)
    imgQrcode.save(fileNameQrcode)
    
    return payload
  
def gerarPayload(payloadFormat, merchantAccount, merchantCategCode, transactionCurrency, transactionAmount, countryCode, merchantName, merchantCity, addDataField, crc16):
    payload = f'{payloadFormat}{merchantAccount}{merchantCategCode}{transactionCurrency}{transactionAmount}{countryCode}{merchantName}{merchantCity}{addDataField}{crc16}'

    return gerarCrc16(crc16, payload)
    
def gerarCrc16(crc16Code, payload):
    crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)

    crc16Code = hex(crc16(str(payload).encode('utf-8')))

    crc16Code_formatado = str(crc16Code).replace('0x', '').upper().zfill(4)

    payload_completa = f'{payload}{crc16Code_formatado}'

    # gerarQrCode(payload_completa, diretorioQrCode)
        
    return payload_completa


# Parâmetros necessários
nome = "NOME SOBRENOME"
chavepix = "CHAVE PIX"
valor = '1.00'
cidade = "CIDADE"
txtId = "DESCRIÇÃO"
fileNameQrcode = "teste.png"

# Funcionando para chave pix CPF ou EMAIL

payload = Payload(nome, chavepix, valor, cidade, txtId, fileNameQrcode)

print("chave copia e cola: ", payload)

"""Resultado"""

# 00020126310014BR.GOV.BCB.PIX0109CHAVE PIX52040000530398654041.005802BR5914NOME SOBRENOME6006CIDADE62130509DESCRIÇÃO6304D1C3

"""Observação"""

# QR Code gerado é salvo no diretório de desenvolvimento.