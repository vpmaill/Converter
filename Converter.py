from tkinter import *
import tkinter.ttk as ttk
import urllib.request
import xml.dom.minidom
import matplotlib
import matplotlib.pyplot as plt

a = 'https://www.cbr.ru/scripts/XML_daily.asp'

response = urllib.request.urlopen(a)
dom = xml.dom.minidom.parse(response)
dom.normalize()
nodeArray = dom.getElementsByTagName("Valute")
data = {}
names = []
for node in nodeArray:
    arr = []
    name = ''
    arr.append(node.getAttribute('ID'))
    childList = node.childNodes
    for child in childList:
        if child.nodeName == 'Name':
            name = child.childNodes[0].nodeValue
            names.append(child.childNodes[0].nodeValue)
        elif child.nodeName == 'Value':
            arr.append(float(child.childNodes[0].nodeValue.replace(',', '.')))
        else:
            arr.append(child.childNodes[0].nodeValue)
    data[name] = arr


def chet():
    koef = data[combo.get()][-2] / data[combo2.get()][-2]
    lb1 = Label(tab1, text=f"{float(txt.get()) * koef}")
    lb1.grid(column=2, row=1)


combo_pediod_arr = [
    {'2 неделя апрель 2024': ('14/04/2024', '07/04/2024'),
     '3 неделя апрель 2024': ('21/04/2024', '14/04/2024'), },

    {'Апрель 2024': ('30/04/2024', '01/04/2024'), 'Март 2024': ('31/03/2024', '01/03/2024'),
     'Февраль 2024': ('29/02/2024', '01/02/2024'), },

    {'1 квартал 2024': ('31/03/2024', '01/01/2024'), '4 квартал 2023': ('31/12/2023', '01/09/2023'),
     '3 квартал 2024': ('30/09/2023', '01/06/2023')},

    {'2023': ('01/01/2024', '01/01/2023'), '2022': ('01/01/2023', '01/01/2022'), '2021': ('01/01/2022', '01/01/2021')}

]


def kak():
    a = lang.get()
    combo_pediod['value'] = [i for i in combo_pediod_arr[int(a)]]


def graf():
    id = data[combo_gr.get()][0]
    a = combo_pediod_arr[int(lang.get())][combo_pediod.get()]
    graf_data = f'https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={a[1]}&date_req2={a[0]}&VAL_NM_RQ={id}'
    response = urllib.request.urlopen(graf_data)
    dom = xml.dom.minidom.parse(response)
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Record")
    x = []
    y = []
    for node in nodeArray:
        y.append(node.getAttribute('Date')[:5])
        childList = node.childNodes
        for child in childList:
            if child.nodeName == 'Value':
                x.append(float(child.childNodes[0].nodeValue.replace(',', '.')))
                continue
    if len(x) > 100:
        x = x[::30]
        y = y[::30]
    elif len(x) > 50:
        x = x[::9]
        y = y[::9]
    elif len(x) > 10:
        x = x[::3]
        y = y[::3]
    matplotlib.use('TkAgg')
    fig = plt.figure()
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=tab2)
    plot_widget = canvas.get_tk_widget()
    fig.clear()
    plt.plot(y, x)
    plt.grid()
    plot_widget.grid(row=1, column=4, padx=32, pady=12)


window = Tk()
window.title("Title")  # Название окна window.geometry("100x100")
position = {"padx": 6, "pady": 6, "anchor": NW}
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Калькулятор валют")
tab_control.add(tab2, text="Динамика курса")
combo = ttk.Combobox(tab1)
combo["values"] = names

combo.grid(column=0, row=0, padx=12, pady=12)
combo2 = ttk.Combobox(tab1)
combo2['values'] = names
combo2.grid(column=0, row=1)
txt = Entry(tab1)
btn = Button(tab1, text="Конвертировать", command=chet)

txt.grid(column=2, row=0)
btn.grid(column=4, row=0, padx=12, pady=12)

combo_gr = ttk.Combobox(tab2)
combo_gr['values'] = names

combo_gr.grid(column=0, row=1, padx=12, pady=12)

header = ttk.Label(tab2, text='Выберите все, чтобы построить график')
header.grid(column=1, row=0, )
btn_gr = Button(tab2, text="Построить график", command=graf)
btn_gr.grid(column=3, row=3, padx=12, pady=12)

lang = StringVar()

a = ttk.Radiobutton(tab2, text='Неделя', value='0', command=kak, variable=lang)
a.grid(column=0, row=2)
b = ttk.Radiobutton(tab2, text='Месяц', value='1', command=kak, variable=lang)
b.grid(column=1, row=2)
c = ttk.Radiobutton(tab2, text='Квартал', value='2', command=kak, variable=lang)
c.grid(column=2, row=2)
d = ttk.Radiobutton(tab2, text='Год', value='3', command=kak, variable=lang)
d.grid(column=3, row=2)

combo_pediod = ttk.Combobox(tab2)

combo_pediod.grid(column=3, row=1, padx=12, pady=12)

tab_control.pack(expand=1, fill='both')
window.mainloop()
