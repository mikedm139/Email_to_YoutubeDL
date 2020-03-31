import requests, smtplib, youtube_dl, re, json, os
from imap_tools import MailBox, Q
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep

def LoadConfig():
  dir = os.getcwd()
  config_file = os.path.join(dir, "config")
  with open(config_file, 'r') as f:
    config = json.load(f)
  return config

def ConfirmArchive(config):
  if not os.path.exists(config['youtube-dl_options']['download_archive']):
    f = open(config['youtube-dl_options']['download_archive'], "w+")
    f.close()
  else:
    pass
  
def CheckMail():
  config = LoadConfig()
  ConfirmArchive(config)
  mailbox = MailBox(config['imap_ssl_host'], config['imap_ssl_port'])
  try:
    mailbox.login(config['email_address'], config['email_password'], initial_folder='Inbox')
  except:
    i=0
    while i < config['max_retries']:
      print("Failed to log in to mailbox to retrieve mail. Retrying...")
      print("Retry %d of max %d" % (i, config['max_retries']))
      sleep(1)
      try:
        mailbox.login(config['email_address'], config['email_password'], initial_folder='Inbox')
        break
      except:
        i=i+1
  
  for message in mailbox.fetch(Q(seen=False)):
    if config['allowed_senders']:
      sender = message.from_
      if sender not in config['allowed_senders']:
        continue
    subject = message.subject
    body = message.text
    video_url = body.strip()
    try:
      with youtube_dl.YoutubeDL(config['youtube-dl_options']) as ydl:
        ydl.download([video_url])
    except Exception as e:
      print("Reporting error to user via email.")
      ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
      error = ansi_escape.sub('', str(e))
      s= smtplib.SMTP(host=config['smtp_host'], port=config['smtp_port'])
      s.starttls()
      s.login(config['email_address'], config['email_password'])

      msg = MIMEMultipart()
      msg['From']=config['email_address']
      msg['To']=sender
      msg['Subject']="Re: %s" % subject
      msg.attach(MIMEText(error, 'plain'))
      s.send_message(msg)
      del msg
      s.quit()

  mailbox.logout()

LoadConfig()
CheckMail()
