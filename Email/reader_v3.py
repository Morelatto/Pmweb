import email, imaplib, os

detach_dir = '.'

EMAIL_ACCOUNT = "mito.mitado.mitando@gmail.com"
EMAIL_PASSWORD = ""

m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
m.select("inbox")

resp, items = m.search(None, "ALL") # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items = items[0].split() # getting the mails id

for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    email_body = data[0][1] # getting the mail content
    mail = email.message_from_bytes(email_body) # parsing the mail content to get a mail object

    # Check if any attachments at all
    if mail.get_content_maintype() != 'multipart':
        continue

    print("["+mail["From"]+"] :" + mail["Subject"])

    # we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
    for part in mail.walk():
        # multipart are just containers, so we skip them
        if part.get_content_maintype() == 'multipart':
            continue

        # is this part an attachment ?
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        counter = 1

        # if there is no filename, we create one with a counter to avoid duplicates
        if not filename:
            filename = 'part-%03d%s' % (counter, 'bin')
            counter += 1

        att_path = os.path.join(detach_dir, filename)

        #Check if its already there
        if not os.path.isfile(att_path) :
            # finally write the stuff
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()