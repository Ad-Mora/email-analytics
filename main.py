import imaplib
import getpass
import process_mail
import analysis

M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    username = raw_input("Enter gmail account: ")
    M.login(username, getpass.getpass())
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!!"

NUM_TRAINING_EMAILS = 300
NUM_EMAILS_TO_CHECK = 50
NUM_TOP_COLS = 20
INBOX = 'INBOX'

# train the model
all_emails = process_mail.package_all_emails(M, NUM_TRAINING_EMAILS, NUM_EMAILS_TO_CHECK, INBOX)
expanded_list = process_mail.expand_factors(all_emails)
model = analysis.logit_regression(expanded_list)
print ''

# get predictions for recent emails
test_emails = process_mail.package_mailbox(M, INBOX, NUM_EMAILS_TO_CHECK, 0)
expanded_list = process_mail.expand_factors(test_emails, True)
df = analysis.get_predictions(expanded_list, model)

# get sorted predictions values
df = df[['Subject Title', 'predictions']]
df = df.sort_values(by=['predictions'], ascending=[False])
df = df.reset_index()
del df['index']
df = df.head(NUM_TOP_COLS)

print df

M.logout()
