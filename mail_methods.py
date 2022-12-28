def filter_wrong_sender(mailbox):
    '''Filters emails from the wrong senders (ex: Fwd, Re). Returns list of emails, # of original emails, # of filtered emails'''
    senders = [message['from'] for message in mailbox]
    correct_sender = max(senders, key=senders.count).split('<')[0]
    filtered_mail = []

    filtered_count, total = 0, 0

    for message in mailbox:
        has_garbage = any(garbage in message['subject'] for garbage in ['Re:','Fwd:','=?UTF-8?'])
        from_correct_sender = message['from'].split('<')[0] == correct_sender
        total += 1

        # Remove messages with garbade headers and wrong senders
        if not has_garbage and from_correct_sender: 
            filtered_mail.append(message)
            filtered_count += 1 

    return filtered_mail, filtered_count, total

def message_cleanup(mail_list):
    '''Cleans up the email body text by removing new lines and punctuation. Returns a list of lowercase plaintext email bodies.'''
    content_list = []

    for message in mail_list:
        messy_content = message.get_payload()[0].get_payload(decode=True)
        # Discard null messages
        if messy_content:
            content = messy_content.decode('utf-8').strip()
            bad_characters = ['\r\n', '\n\n', '\n', ',' , ';' , ':' , '!' , '"' , '?' , '.' , '(' , ')' , '*']

            for char in bad_characters:
                content = content.replace(char, ' ')

            if len(content):
                content_list.append(content.lower())

    return content_list 