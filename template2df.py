def template2df(file):
    test_df = pd.read_excel(file)
    test_df = test_df.drop(['Единица измерения'],axis='columns').T.reset_index(drop=True)
    test_df = test_df.rename(columns=test_df.iloc[0]).drop(test_df.index[0],axis='index')
    years = test_df['Год'].astype(int)
    test_df = test_df.drop(['Год'],axis='columns')
    return years.values, test_df
