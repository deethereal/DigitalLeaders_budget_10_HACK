import pandas as pd
def template2df(file):
    test_df = pd.read_excel(file)
    drop_ids = []
    for i, value in enumerate(test_df.loc[1]):
        if pd.isna(value):
            drop_ids.append(i)
    test_df = test_df.drop([test_df.columns[i] for i in drop_ids], axis = 1)
    test_df = test_df.drop(['Единица измерения'],axis='columns').T.reset_index(drop=True)
    test_df = test_df.rename(columns=test_df.iloc[0]).drop(test_df.index[0],axis='index')
    years = test_df['Год'].astype(int)
    test_df = test_df.drop(['Год'],axis='columns')
    return years.values, test_df