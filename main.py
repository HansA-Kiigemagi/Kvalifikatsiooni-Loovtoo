import PySimpleGUI as sg

# Tulumaksu arvutamise funktsioon
def tulumaks1(arvestuslik_palk, kogumispension):
    if arvestuslik_palk <= 1200:
        # Kas isikul on II sammas või mitte
        if kogumispension == True:
            tulumaks = (arvestuslik_palk - (0.016 * arvestuslik_palk + 0.02 * arvestuslik_palk + 654)) * 0.2
        else:
            tulumaks = (arvestuslik_palk - (0.016 * arvestuslik_palk + 654)) * 0.2
        # Vaatab et tulumaks poleks negatiivne
        if tulumaks < 0:
            tulumaks = 0
    elif arvestuslik_palk < 2100:
        tulumaks = (arvestuslik_palk - (654 - (arvestuslik_palk - 1200) * 0.72667)) * 0.2
        print(tulumaks)
    else:
        tulumaks = arvestuslik_palk * 0.2
    # Peab olema ümardatud 1 sendini
    return round(tulumaks, 2)

# Akna kujundus

layout = [[sg.Text("Sisesta arvestuslik töötasu:"), sg.Input(key="-ARVESTUSLIK-",)],
          [sg.Text("Kogumispension"), sg.Radio("On",key="ON", group_id=1), sg.Radio("Ei ole",key="POLE", group_id=1)],
          [sg.Text("Tulumaks"), sg.Text(key="-TULUMAKS-")],
          [sg.Text("Töötuskindlustus"), sg.Text(key="-TOOTUS_TOOTAJALT-")],
          [sg.Text("Kogumispension"), sg.Text(key="-KOGUMISPENSION-")],
          [sg.Text("Netopalk"), sg.Text(key="-NETOPALK-")],
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
        # Tulumaks andmete põhjal
        arvestuslik_sisend = float(values["-ARVESTUSLIK-"])
        if values["ON"] == True:
            tulemus = tulumaks1(arvestuslik_sisend, True)
        else:
            tulemus = tulumaks1(arvestuslik_sisend, False)
        tulemus_tekst = str(tulemus) + "€"
        window["-TULUMAKS-"].update(tulemus_tekst)
        # Töötuskindlustus
        tootuskindlustus = round(arvestuslik_sisend * 0.016, 2)
        tootus_valja = str(tootuskindlustus) + "€"
        window["-TOOTUS_TOOTAJALT-"].update(tootus_valja)
        # Kogumispension
        if values["ON"] == True:
            kogumispension = round(arvestuslik_sisend * 0.02, 2)
        else:
            kogumispension = 0
        kogumispension_valja = str(kogumispension) + "€"
        window["-KOGUMISPENSION-"].update(kogumispension_valja)
        # Netopalk
        netopalk = arvestuslik_sisend - tulemus - tootuskindlustus - kogumispension
        netopalk_valja = str(netopalk)
        window["-NETOPALK-"].update(netopalk_valja)