import numpy as np


def xirr(df, guess=0.0001, date_column='date', amount_column='amount'):
    '''Calculates XIRR from a series of cashflows.
       Needs a dataframe with columns date and amount, customisable through parameters.
       Requires Pandas, NumPy libraries'''

    df = df.sort_values(by=date_column).reset_index(drop=True)

    amounts = df[amount_column].values
    dates = df[date_column].values

    years = np.array(dates-dates[0], dtype='timedelta64[D]').astype(int)/365

    step = 0.05
    epsilon = 0.0001
    limit = 1000
    residual = 1

    #Test for direction of cashflows
    disc_val_1 = np.sum(amounts/((1+guess)**years))
    disc_val_2 = np.sum(amounts/((1.05+guess)**years))
    mul = 1 if disc_val_2 < disc_val_1 else -1

    #Calculate XIRR
    for i in range(limit):
        prev_residual = residual
        residual = np.sum(amounts/((1+guess)**years))
        if abs(residual) > epsilon:
            if np.sign(residual) != np.sign(prev_residual):
                step /= 2
            guess = guess + step * np.sign(residual) * mul
        else:
            return guess