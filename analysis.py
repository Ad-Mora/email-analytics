import pandas as pd
import statsmodels.api as sm


def get_data_frame(data, subject_title=False):
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.max_columns', 1000)

    labels = ['# words in subject', 'avg subject word length', 'hour sent', 'day of week',

              '(Email From Address) Could Not Parse Name', '(Email From Address) Is Gmail',
              '(Email From Address) Is Yahoo', '(Email From Address) Is Other',
              '(Email From Address) Could Not Parse Top Domain', '(Email From Address) Is .com',
              '(Email From Address) Is .org', '(Email From Address) Is .edu', '(Email From Address) Domain Is Other',

              '(Email To Address) Could Not Parse Name', '(Email To Address) Is Gmail',
              '(Email To Address) Is Yahoo', '(Email To Address) Is Other',
              '(Email To Address) Could Not Parse Top Domain', '(Email To Address) Is .com',
              '(Email To Address) Is .org', '(Email To Address) Is .edu', '(Email To Address) Domain Is Other',

              '# lines in message,', '# words in message', 'avg message word length', 'word length std dev', '# question marks',
              'replied to']

    if subject_title:
        labels.insert(0, 'Subject Title')

    df = pd.DataFrame.from_records(data, columns=labels)
    return df

def logit_regression(data):
    df = get_data_frame(data)

    del df['(Email From Address) Could Not Parse Name']
    del df['(Email From Address) Is Yahoo']
    del df['(Email From Address) Could Not Parse Top Domain']
    del df['(Email From Address) Is .com']
    del df['(Email From Address) Is .org']
    del df['(Email From Address) Is .edu']
    del df['(Email From Address) Is Other']
    del df['(Email From Address) Domain Is Other']
    del df['(Email To Address) Could Not Parse Name']
    del df['(Email To Address) Is Yahoo']
    del df['(Email To Address) Is Other']
    del df['(Email To Address) Could Not Parse Top Domain']
    del df['(Email To Address) Is .org']
    del df['(Email To Address) Is .com']
    del df['(Email To Address) Is .edu']
    del df['(Email To Address) Domain Is Other']

    df['intercept'] = 1.0
    train_cols = df.columns[:11]
    logit = sm.Logit(df['replied to'], df[train_cols])
    result = logit.fit()

    return result


def get_predictions(data, model):
    df = get_data_frame(data, True)

    del df['(Email From Address) Could Not Parse Name']
    del df['(Email From Address) Is Yahoo']
    del df['(Email From Address) Could Not Parse Top Domain']
    del df['(Email From Address) Is .com']
    del df['(Email From Address) Is .org']
    del df['(Email From Address) Is .edu']
    del df['(Email From Address) Is Other']
    del df['(Email From Address) Domain Is Other']
    del df['(Email To Address) Could Not Parse Name']
    del df['(Email To Address) Is Yahoo']
    del df['(Email To Address) Is Other']
    del df['(Email To Address) Could Not Parse Top Domain']
    del df['(Email To Address) Is .org']
    del df['(Email To Address) Is .com']
    del df['(Email To Address) Is .edu']
    del df['(Email To Address) Domain Is Other']

    df['intercept'] = 1.0
    test_cols = df.columns[1:12]
    df['predictions'] = model.predict(df[test_cols])

    return df
