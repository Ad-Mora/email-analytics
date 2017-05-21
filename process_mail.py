import email
import datetime
import copy
import extract_factors


def package_mailbox(M, mailbox, num_emails, offset, is_sent=False):
    email_data = {}
    rv, data = M.select(mailbox)
    if rv == 'OK':
        print "Processing " + mailbox + " mailbox..."

        # get emails from the given mailbox
        rv, data = M.search(None, "ALL")
        if rv != 'OK':
            print "No messages found!"
            return

        email_list = data[0].split()[::-1]
        email_list = email_list[offset:]

        # process an individual email
        counter = 0
        for num in email_list:

            # get raw single email
            rv, data = M.fetch(num, '(RFC822)')
            if rv != 'OK':
                print "ERROR getting message", num
                return
            msg = email.message_from_string(data[0][1])

            # extract data from email
            subject = msg['Subject']
            subject = email.Header.decode_header(subject)[0][0].strip()
            date = None
            try:
                from_field = msg['From'].lower()
                to_field = msg['To'].lower()
            except:
                continue

            date_tuple = email.utils.parsedate_tz(msg['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                date = local_date.strftime("%a, %d %b %Y %H:%M:%S")

            while msg.is_multipart():
                msg = msg.get_payload()[0]
            payload = msg

            # do not look at emails that are html or base64
            if payload['Content-Transfer-Encoding'] == 'base64':
                continue
            if payload.get_content_subtype() == 'html':
                continue


            # add on false flag if this is not an email from the sent mailbox
            email_data[subject] = (date, from_field, to_field, payload)
            if not is_sent:
                email_data[subject] = (date, from_field, to_field, payload, False)

            # increment counter
            counter += 1
            if counter >= num_emails:
                print 'Processed ' + str(num_emails) + ' emails\n'
                M.close()
                break

        return email_data
    else:
        print 'Could not process mailbox'
        return


def clean_sent_emails(sent_emails):

    clean_emails = copy.deepcopy(sent_emails)

    for subject in sent_emails:
        is_sent = False
        if len(subject) > 4 and subject.startswith('Re: '):
            is_sent = True
            clean_subject = subject[4:]
            clean_emails[clean_subject] = sent_emails[subject]
            del clean_emails[subject]

            # flag this email as having been replied to
            clean_emails[clean_subject] = clean_emails[clean_subject] + (True,)

        if not is_sent:
            del clean_emails[subject]

    return clean_emails


def package_all_emails(M, num_emails, offset, inbox):
    sent_mail = package_mailbox(M, '[Gmail]/Sent Mail', num_emails, 0, True)
    sent_mail = clean_sent_emails(sent_mail)
    inbox_mail = package_mailbox(M, inbox, num_emails, offset, False)

    # combine the two mail sets
    all_mail = copy.deepcopy(sent_mail)
    for subject in inbox_mail.keys():
        if subject not in all_mail:
            all_mail[subject] = inbox_mail[subject]

    return all_mail


def expand_factors(email_dict, include_subject=False):
    expanded_list = []
    for subject, vals in email_dict.items():
        email_vector = []
        subject_field = subject
        date = vals[0]
        from_field = vals[1]
        to_field = vals[2]
        message = vals[3]
        replied = vals[4]

        if include_subject:
            email_vector += [subject]

        email_vector += extract_factors.get_subject_factors(subject_field)
        email_vector += extract_factors.get_date_factors(date)
        email_vector += extract_factors.get_email_factors(from_field)
        email_vector += extract_factors.get_email_factors(to_field)
        email_vector += extract_factors.get_message_factors(message)
        email_vector += [int(replied)]

        expanded_list.append(email_vector)

    return expanded_list


