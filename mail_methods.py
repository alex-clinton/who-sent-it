import matplotlib.pyplot as plt
from wordcloud import WordCloud

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
    body_list = []

    for message in mail_list:
        messy_body = message.get_payload()[0].get_payload(decode=True)
        # Discard null messages
        if messy_body:
            body = messy_body.decode('utf-8').strip()
            bad_characters = ['\r\n', '\n\n', '\n', ',' , ';' , ':' , '!' , '"' , '?' , '.' , '(' , ')' , '*']

            for char in bad_characters:
                body = body.replace(char, ' ')

            if len(body):
                body_list.append(body.lower())

    return body_list 

def unknown_email_words(path='mail_data/new_message.txt'):
    unknown_email_words = []

    with open(path) as new_message:
        clean_lines = [line.strip() for line in new_message]
        for line in clean_lines:
            unknown_email_words += line.split()
    
    return unknown_email_words

def create_word_cloud(email_bodies, output_path=None):
    '''Generate a word cloud from a list of email bodies. If no output path is specified display the image, otherwise save it to a file.'''
    word_list = []
    for body in email_bodies:
        word_list += body.split()

    word_cloud = WordCloud(background_color='white', width=800, height=400).generate(' '.join(word_list))
    plt.axis('off')
    plt.imshow(word_cloud)

    if not output_path:
        plt.show()
    else:
        plt.savefig(output_path)