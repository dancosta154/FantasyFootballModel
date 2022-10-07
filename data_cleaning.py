def impute_special_char(df, char):
    """Remove special character from dataframe"""
    return df.replace(char, 0, inplace=True)


def change_col_types(df):
    numcols_to_change = df.columns
    numcols_to_change2 = []
    for col in numcols_to_change:
        try:
            df[col] = df[col].astype(int)
            print("success!")
        except:
            numcols_to_change2.append(col)
            print(f"need to clean column: {col}")
    return col

def drop_rows(position):
        for header in position.columns:
            index_list = position.loc[(position[header] == header)].index
            position.drop(labels=index_list, axis=0, inplace = True)
            return position