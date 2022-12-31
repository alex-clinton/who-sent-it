# who-sent-it
Code to identify which of two senders wrote a given email. Sample emails from both senders are given to a Naive Bayes classifier to make a prediction.

## Requirements

- Python 3
- Numpy
- Matplotlib
- Scikit-learn
- Wordcloud
- Mailbox

## Setup/Execution

1. Create a virtual enviornment and install the requirements by running.
```
python3 -m venv ./venv
source venv/Scripts/activate
pip -r requirements.txt
```
2. Run predict.py with the .mbox files for the two possible senders and the unknown plaintext message.
```
python3 predict.py sender1.mbox sender2.mbox unknown_message.txt
```

## Mail data
Many services represent mail data via the .mbox format. The program requires two .mbox files: one for the mail data of each sender. To obtain these files from Gmail you can add emails from a given sender to a label and then download all of the emails under that label.
