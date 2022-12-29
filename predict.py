import sys
import numpy as np
import mailbox as mb
import mail_methods as mm
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score

def create_word_mapping(first_bodies, second_bodies, unknown_email_words):
    '''Create a mapping from all words in the three inputs to unique numbers.'''
    word_mapping = {}

    for body in first_bodies + second_bodies:
        for word in body.split():
            if word not in word_mapping:
                word_mapping[word] = len(word_mapping)

    for word in unknown_email_words:
        if word not in word_mapping:
            word_mapping[word] = len(word_mapping)
    
    return word_mapping

def fill_out_mappings(first_bodies, first_mapping, second_bodies, second_mapping, unknown_words, unknown_mapping, word_mapping):
    '''Fill out the numeric mappings for the three inputs to be used with the Naive Bayes classifier.'''
    for i, body in enumerate(first_bodies):
        for word in body.split():
            first_mapping[i, word_mapping[word]] += 1

    for i, body in enumerate(second_bodies):
        for word in body.split():
            second_mapping[i, word_mapping[word]] += 1

    for word in unknown_words:
        unknown_mapping[word_mapping[word]] += 1

def main():
    # Mail data for the two candidate senders and the unknown sender
    first_sender = mb.mbox(sys.argv[1])
    second_sender = mb.mbox(sys.argv[2])
    unknown_email_words = mm.unknown_email_words(sys.argv[3])

    # Filter out emails from the wrong senders
    first_filtered, first_count, first_total = mm.filter_wrong_sender(first_sender)
    second_filtered, second_count, second_total = mm.filter_wrong_sender(second_sender)

    # Display count for filtered and original emails
    print(f'First sender (filtered/total) messages: {first_count}/{first_total}')
    print(f'Second sender (filtered/total) messages: {second_count}/{second_total}')

    # Remove problematic formatting from filtered emails
    first_bodies = mm.message_cleanup(first_filtered)
    second_bodies = mm.message_cleanup(second_filtered)

    word_mapping = create_word_mapping(first_bodies, second_bodies, unknown_email_words)

    # Create word clouds for both senders
    mm.create_word_cloud(first_bodies, 'first_word_cloud.png')
    mm.create_word_cloud(second_bodies, 'second_word_cloud.png')

    # Initialize array representation of word counts for all known emails
    first_bodies_mapping = np.zeros((len(first_bodies), len(word_mapping)))
    first_labels = np.array(len(first_bodies)*['first_sender'])

    second_bodies_mapping = np.zeros((len(second_bodies), len(word_mapping)))
    second_labels = np.array(len(second_bodies)*['second_sender'])

    unknown_mapping = np.zeros((len(word_mapping)))

    # Fill out word counts for first, second, and unknown sender
    fill_out_mappings(first_bodies, first_bodies_mapping, second_bodies, second_bodies_mapping, unknown_email_words, unknown_mapping, word_mapping)

    # Combine and shuffle the training data and labels
    combined_bodies_mapping = np.concatenate((first_bodies_mapping, second_bodies_mapping), axis=0)
    combined_labels = np.concatenate((first_labels, second_labels), axis=0)

    shuffle_perm = np.random.permutation(len(combined_labels))
    combined_bodies_mapping = combined_bodies_mapping[shuffle_perm]
    combined_labels = combined_labels[shuffle_perm]

    # Create multinomial naive bayes predictor 
    clf = MultinomialNB()

    # Calculate 5x cross validation scores
    scores = cross_val_score(clf, combined_bodies_mapping, combined_labels, cv=5, scoring='accuracy')
    print('Average cross-validation (5x) score: {:.4f}'.format(scores.mean()))

    # Generate and display guess for unknown email
    clf.fit(combined_bodies_mapping, combined_labels)
    print(f'Prediction: {clf.predict([unknown_mapping])[0]}')

if __name__ == '__main__':
    # Check input arguments
    if len(sys.argv) != 4 or sys.argv[1][-5:] != '.mbox' or sys.argv[2][-5:] != '.mbox':
        print('Usage: python predict.py sender1.mbox sender2.mbox')
    else:
        main()