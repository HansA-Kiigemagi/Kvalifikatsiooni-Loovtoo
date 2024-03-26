import PySimpleGUI as sg

# Väga algne tulumaksu arvutaja, mis arvestab ainult arvestuslikku palka, II samba maksjal
def tulumaks1(arvestuslik_palk):
    if arvestuslik_palk < 1200:
        tulumaks = (arvestuslik_palk - (0.016 * arvestuslik_palk + 0.02 * arvestuslik_palk + 654)) * 0.2
        if tulumaks < 0:
            tulumaks = 0
    elif arvestuslik_palk <= 2100:
        tulumaks = 654 - (arvestuslik_palk - 1200) * 0.072667
    else:
        tulumaks = arvestuslik_palk * 0.2
    return round(tulumaks, 2)

# Akna kujundus

layout = [[sg.Text("Sisesta arvestuslik töötasu:"), sg.Input(key="-IN-",)],
          [sg.Text("Tulumaks"), sg.Text(key="-OUTPUT-")],
          [sg.Button("Arvuta")],
          [sg.Button("Sulge")]]

window = sg.Window("Tulumaksu kalkulaator v0.0.1", layout)

# Tegevustsükkel

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == "Sulge":
        break
    if event == "Arvuta":
        sisend = float(values["-IN-"])
        tulemus = tulumaks1(sisend)
        tulemus_tekst = str(tulemus) + "€"
        window["-OUTPUT-"].update(tulemus_tekst)