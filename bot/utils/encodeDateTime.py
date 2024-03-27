

def encode_datetime(datetime):
    date, time = datetime.split(' ')
    d, m, y = date.split('.')
    return y + '-' + m + '-' + d + ' ' + time
