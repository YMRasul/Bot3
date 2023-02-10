from datetime import date
def knopki():
    today = date.today()
    #print(today)
    y = int(today.strftime("%Y"))
    m = int(today.strftime("%m"))
    i = 12
    mas = []
    while (i > 0):
        m = m - 1
        if m == 0:
            m = 12
            y = y - 1
        s = str(y) + '_' + str(m).rjust(2, '0')
        mas.append(s)
        i = i - 1
    mas.append("Qaytish")
    return(mas)
