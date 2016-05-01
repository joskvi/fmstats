
def month2num(month):

    month = month.lower()

    if month == 'jan':
        return '01'
    elif month == 'feb':
        return '02'
    elif month == 'mar':
        return '03'
    elif month == 'apr':
        return '04'
    elif month == 'may':
        return '05'
    elif month == 'jun':
        return '06'
    elif month == 'jul':
        return '07'
    elif month == 'aug':
        return '08'
    elif month == 'sep':
        return '09'
    elif month == 'oct':
        return '10'
    elif month == 'nov':
        return '11'
    elif month == 'dec':
        return '12'
    else:
        return 'NaN'