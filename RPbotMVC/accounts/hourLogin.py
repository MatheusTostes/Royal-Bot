from datetime import datetime

def HourLogin():
    horas = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    print(horas)
    return horas