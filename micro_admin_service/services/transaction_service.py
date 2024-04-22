from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from micro_admin_service.models import TransactionDetailsOfClient
from micro_auth_service.models import ClientCredentials
from decouple import config
from EmailServer.email import Mail

@parser_classes([JSONParser])
def transactionDetailsUpdate(request,client_id):
    try:
        client=ClientCredentials.objects.get(client_id=client_id)
        transaction_date=request.data['transaction_date']
        transaction_id=request.data['transaction_id']
        
        if TransactionDetailsOfClient.objects.filter(transaction_id=transaction_id).exists():
            return False,{"info":"transaction exists"}
        
        TransactionDetailsOfClient.objects.create(
            client=client,
            transaction_id=transaction_id,
            transaction_date=transaction_date
        )
        subject="Transaction Success"
        body="We would like to inform you that your payment for the tax filing service has been successfully processed. Thank you for choosing our services and entrusting us with your tax filing needs."
        mail_sender = config('EMAIL_HOST_USER')
        mail=Mail(
            subject=subject,
            body=body,
            mail_sender=mail_sender,
            mail_receiver=client.email
        )
        mail.mailWithTemplate(client_name=client.first_name+" "+client.last_name)
        return True,{"info":"transaction updated"}
    except:
        pass