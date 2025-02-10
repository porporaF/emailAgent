import imaplib
import email
import ssl
import poplib
from email.header import decode_header



    
#Funzione per connettersi alla mailbox
def connect_to_mailbox(imap,door):
    # Connettersi al server IMAP di Alice.it
    try:
        
        context=ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(imap,port=door,timeout=30,ssl_context=context)  # Timeout impostato a 30 secondi
        mail.login(EMAIL, PASSWORD)
        return mail
    except Exception as e:
        print(f"Errore di connessione: {e}")
        return None
def connectpop_to_mailbox(pop_mail,door):
    # Connettersi al server IMAP di Alice.it
    try:
        
        context=ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(pop_mail,port=door,timeout=30,ssl_context=context)  # Timeout impostato a 30 secondi
        mail.login(EMAIL, PASSWORD)
        return mail
    except Exception as e:
        print(f"Errore di connessione: {e}")
        return None
#Connessione e lettura delle e-mail


def get_unread_emails(mail):
    try:
        mail.select("inbox")  # Seleziona la cartella Inbox
        status, messages = mail.search(None, 'UNSEEN')  # Trova le e-mail non lette
        email_ids = messages[0].split()  # Ottieni gli ID delle e-mail non lette
        return email_ids
    except Exception as e:
        print(f"Errore di lettura mails: {e}")
        return None

def get_read_emails(mail):
    mail.select(mailbox='INBOX', readonly=False)
    status,messages = mail.search(None,'SEEN') #Trova le e-mail lette
    email_ids = messages[0].split()
    return email_ids

#Funzione per leggere il contenuto delle e-mail
def read_email(mail, email_id):
    status, msg_data = mail.fetch(email_id, "(RFC822)")  # Ottieni il contenuto dell'e-mail
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])  # Decodifica l'e-mail
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            from_ = msg.get("From")
            print(f"Subject: {subject}")
            print(f"From: {from_}")
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        print(f"Body: {body}")
            else: body = msg.get_payload(decode=True).decode()
            print(f"Body: {body}")
           

def delete_read_emails(mail):
    
    mail.select(mailbox='INBOX', readonly=False)
    status,messages = mail.search(None,'SEEN') #Trova le e-mail lette
    if status=="OK":
        for msg_num in messages[0].split():
            mail.store(msg_num,'+FLAGS','\\Deleted')
            mail.expunge()
            print("Le mail lettte sonos state eliminate con successo")
        else:
            print("Nessuna mail letta da cancellare")
            


#connessione gmail alice
EMAIL = "porporaFp.@gmail.com"  # La tua email
PASSWORD = "fclr tjra bkho whze"  # La tua password (o app password se hai l'autenticazione a due fattori)

mail = connect_to_mailbox("imap.gmail.com",993)

#Connetti e ottieni le e-mail non lette
#mail = connect_to_mailbox()
unread_emails = get_unread_emails(mail)
print("unread",unread_emails)

#read_emails = get_read_emails(mail)
#print("read",read_emails)


if mail:
    print("Connessione riuscita!")
   
else:
    print("Connessione fallita.")

#for email_id in unread_emails:
#    read_email(mail, email_id)




#Cancella le mail lette
#delete_read_emails(mail)
