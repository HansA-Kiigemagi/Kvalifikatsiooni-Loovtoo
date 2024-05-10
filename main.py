import PySimpleGUI as sg
sg.theme("Default 1")

# Maksude arvutamise funktsioon(id)
def maksud2024(arvestuslik,kas_kogumis):
    # Lihtsad maksud
    # Kogumispension on valikuline
    if kas_kogumis:
        kogumispension = round(arvestuslik * 0.02, 2)
    else:
        kogumispension = 0
    tootuskindlustus = round(arvestuslik * 0.016, 2)
    # Tulumaksuvaba
    if arvestuslik <= 1200:
        tmvaba = 654
    elif arvestuslik < 2100:
        tmvaba = round(654 - 0.72667 * (arvestuslik - 1200))
    else:
        tmvaba = 0
    # Tulumaks
    tulumaks = round((arvestuslik - tmvaba - kogumispension - tootuskindlustus) * 0.2, 2)
    # Kätte
    netopalk = round(arvestuslik - kogumispension - tootuskindlustus - tulumaks, 2)

    return kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk


# Akna kujunduse veerud
maksude_nimetuste_veerg = [[sg.Text("Kogumispension:")],
                           [sg.Text("Töötuskindlustus:")],
                           [sg.Text("Tulumaksuvaba:")],
                           [sg.Text("Tulumaks:")],
                           [sg.Text("Netopalk:")]]

maksude_arvude_veerg = [[sg.Text(key="-KOGUMISPENSION-", size=(10,1))],
                        [sg.Text(key="-TOOTUS_TOOTAJALT-", size=(10,1))],
                        [sg.Text(key="-TMVABA-", size=(10,1))],
                        [sg.Text(key="-TULUMAKS-", size=(10,1))],
                        [sg.Text(key="-NETOPALK-", size=(10,1))]]

andmete_nimetuste_veerg = [[sg.Text("Isikukood:")],
                           [sg.Text("Eesnimi:")],
                           [sg.Text("Perenimi:")],
                           [sg.Text("Kuupäev:")]]

andmete_sisestuse_veerg = [[sg.Input(key="-ISIKUKOOD-")],
                           [sg.Input(key="-EESNIMI-")],
                           [sg.Input(key="-PERENIMI-")],
                           [sg.Input(key="-KUUPAEV-")]]
# Kogu kujundus

layout = [[sg.Text("Sisesta arvestuslik töötasu:"), sg.Input(key="-ARVESTUSLIK-",)],
          [sg.Text("Kogumispension"), sg.Radio("On",key="ON", group_id=1), sg.Radio("Ei ole",key="POLE", group_id=1)],
          [sg.Column(maksude_nimetuste_veerg), sg.Column(maksude_arvude_veerg), sg.VSeparator(), sg.Column(andmete_nimetuste_veerg), sg.Column(andmete_sisestuse_veerg)],
          [sg.Button("Arvuta", bind_return_key=True)],
          [sg.Button("Sulge")]]


window = sg.Window("Tulumaksu kalkulaator v0.0.3", layout, size=(1200, 400))

# Tegevustsükkel
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == "Sulge":
        break
    if event == "Arvuta":
        # Maksude arvutamine andmete põhjal
        arvestuslik_sisend = float(values["-ARVESTUSLIK-"])
        if values["ON"] == True:
            kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk = maksud2024(arvestuslik_sisend, True)
        else:
            kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk = maksud2024(arvestuslik_sisend, False)
        # Andmete kuvamine programmiaknas
        window["-KOGUMISPENSION-"].update(str(kogumispension) + "€")
        window["-TOOTUS_TOOTAJALT-"].update(str(tootuskindlustus) + "€")
        window["-TMVABA-"].update(str(tmvaba) + "€")
        window["-TULUMAKS-"].update(str(tulumaks) + "€")
        window["-NETOPALK-"].update(str(netopalk) + "€")
