import requests
import json
import uuid
import base64

ACCESS_TOKEN = "TEST-6310058720351952-100822-e567773f1a6b76ebfc89a9376427a402-1957499458"

# Cabeçalhos para a requisição
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "X-Idempotency-Key": str(uuid.uuid4())  # Gerando um UUID único para cada requisição
}

# Dados do pagamento
data = {
    "transaction_amount": 100.00,  # Valor do pagamento
    "description": "Compra de produto X",  # Descrição do pagamento
    "payment_method_id": "pix",  # Método de pagamento: PIX
    "payer": {  # Informações do pagador
        "email": "email_do_comprador@exemplo.com"
    },
    "notification_url": "https://minha-url-de-notificacao.com",  # URL para notificações (opcional)
    "external_reference": "REF1234"  # Referência externa (pode ser um ID do pedido)
}

# Fazendo a requisição POST para criar o pagamento
response = requests.post(
    "https://api.mercadopago.com/v1/payments", 
    headers=headers, 
    data=json.dumps(data)
)

# Verificando se a requisição foi bem sucedida
if response.status_code == 201:
    payment_data = response.json()
    
    # Extraindo o QR Code base64 e o código de pagamento PIX (copia e cola)
    qr_code = payment_data['point_of_interaction']['transaction_data']['qr_code']
    qr_code_base64 = payment_data['point_of_interaction']['transaction_data'].get('qr_code_base64')

    print("Pagamento criado com sucesso!")
    print(f"PIX Copia e Cola: {qr_code}")
    
    # Verificando se qr_code_base64 existe e não está vazio
    if qr_code_base64:
        print("QR Code Base64 encontrado.")
        try:
            # Salvando o QR Code como uma imagem
            with open("qrcode_pix.png", "wb") as f:
                # A string pode não ter a vírgula, então, vamos apenas decodificar diretamente
                if qr_code_base64.startswith("data:image/png;base64,"):
                    f.write(base64.b64decode(qr_code_base64.split(",")[1]))
                else:
                    f.write(base64.b64decode(qr_code_base64))  # Se não tiver a parte da string, apenas decodificamos
            print("QR Code salvo como qrcode_pix.png")
        except Exception as e:
            print("Erro ao salvar o QR Code:", e)
    else:
        print("QR Code Base64 não encontrado na resposta.")
else:
    print("Erro ao criar pagamento:", response.status_code, response.text)
