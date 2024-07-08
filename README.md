# Repositório de Pagamento PIX

Este repositório fornece uma implementação em Python para gerar QR codes para pagamentos PIX. O código cria uma string de payload seguindo o padrão BR Code e gera uma imagem de QR code que pode ser escaneada para realizar pagamentos.

## Funcionalidades

- Gerar QR codes para pagamento PIX.
- Criar uma string de payload para pagamentos PIX seguindo o padrão BR Code.
- Salvar o QR code gerado como um arquivo de imagem.

## Requisitos

- Python 3.x
- Biblioteca `crcmod`
- Biblioteca `qrcode`

## Instalação

Para instalar as bibliotecas necessárias, execute:

```sh
pip install crcmod qrcode
```

## Uso

A função principal deste repositório é `Payload`, que recebe os parâmetros necessários e gera um QR code para pagamento PIX.

### Parâmetros

- `nome`: Nome do comerciante.
- `chavepix`: Chave PIX (CPF, email, número de telefone ou chave aleatória).
- `valor`: Valor da transação.
- `cidade`: Cidade do comerciante.
- `txtId`: Descrição ou ID da transação.
- `fileNameQrcode`: Nome do arquivo onde o QR code será salvo.

### Exemplo

Aqui está um exemplo de como usar a função `Payload`:

```py
import crcmod
import qrcode

def Payload(nome, chavepix, valor, cidade, txtId, fileNameQrcode):
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
        
    return payload_completa


# Parâmetros necessários
nome = "NOME SOBRENOME"
chavepix = "CHAVE PIX"
valor = '1.00'
cidade = "CIDADE"
txtId = "DESCRIÇÃO"
fileNameQrcode = "teste.png"

# Gerar QR code para pagamento PIX
payload = Payload(nome, chavepix, valor, cidade, txtId, fileNameQrcode)

print("chave copia e cola: ", payload)
```

### Resultado

A saída será uma string representando a chave "copia e cola" para o pagamento PIX e uma imagem de QR code salva no arquivo especificado.

### Observação

O QR code gerado é salvo no diretório de desenvolvimento. Além disso, há um manual do BR Code disponível que fornece diretrizes para a geração de QR codes PIX. [Manual PDF](https://github.com/LuisSilvah/pagamento_pix/blob/main/ManualBRCode.pdf)
