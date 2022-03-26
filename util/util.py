

def pick_options(df):
    valid_options = []
    for col in df:
        if df[col].dtype == float or df[col].dtype == int:
            valid_options.append(col)
    return valid_options
