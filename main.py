
import PySimpleGUI as sg
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm

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
        if arvestuslik < 654:
            tmvaba = arvestuslik - kogumispension - tootuskindlustus
        else:
            tmvaba = 654
    elif arvestuslik < 2100:
        tmvaba = round(654 - 0.72667 * (arvestuslik - 1200))
    else:
        tmvaba = 0
    # Tulumaks
    tulumaks = round((arvestuslik - tmvaba - kogumispension - tootuskindlustus) * 0.2, 2)
    if tulumaks < 0:
        tulumaks = 0
    # Kätte
    netopalk = round(arvestuslik - kogumispension - tootuskindlustus - tulumaks, 2)

    return kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk

# Akna kujunduse veerud
sg.theme("Default 1")

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
                           [sg.Text("Kuupäev:")],
                           [sg.Text("Maksmise kuupäev")]]

andmete_sisestuse_veerg = [[sg.Input(key="-ISIKUKOOD-", size=(12,1))],
                           [sg.Input(key="-EESNIMI-", size=(12,1))],
                           [sg.Input(key="-PERENIMI-", size=(12,1))],
                           [sg.Input(key="-KUUPAEV-", size=(12,1))],
                           [sg.Input(key="-MAKSMISE_KP-", size=(12,1))]]
# Kogu kujundus

layout = [[sg.Text("Sisesta arvestuslik töötasu:"), sg.Input(key="-ARVESTUSLIK-", size=(12,1))],
          [sg.Text("Kogumispension"), sg.Radio("On",key="ON", group_id=1), sg.Radio("Ei ole",key="POLE", group_id=1)],
          [sg.Column(maksude_nimetuste_veerg), sg.Column(maksude_arvude_veerg), sg.VSeparator(), sg.Column(andmete_nimetuste_veerg), sg.Column(andmete_sisestuse_veerg)],
          [sg.Button("Arvuta", bind_return_key=True), sg.Button("Loo PDF")],
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
    if event == "Loo PDF":
        # Sisenditest andmete võtmine
        isikukood = str(values["-ISIKUKOOD-"])
        perenimi = str(values["-PERENIMI-"])
        eesnimi = str(values["-EESNIMI-"])
        kuupaev = str(values["-KUUPAEV-"])
        maksmise_kuupaev = str(values["-MAKSMISE_KP-"])
        kuupaev_failile = kuupaev.replace(".", "_", 2)
        # PDF-i loomine
        pealkiri = perenimi + kuupaev_failile + ".pdf"
        canvas = Canvas(pealkiri)
        # Pealkiri
        canvas.setFont("Helvetica", 20)
        canvas.drawString(2 * cm, 27.5 * cm, "Palgaleht")
        canvas.line(2 * cm, 27 * cm, 20 * cm, 27 * cm)
        # Sisu
        canvas.setFont("Helvetica", 12)
        canvas.drawString(2 * cm, 26 * cm, "Töötaja")
        canvas.drawString(5 * cm, 26 * cm, eesnimi + " " + perenimi)
        canvas.drawString(2 * cm, 25 * cm, "Isikukood")
        canvas.drawString(5 * cm, 25 * cm, isikukood)
        canvas.drawString(11 * cm, 26 * cm, "Bruto Töötasu")
        canvas.drawString(15 * cm, 26 * cm, str(arvestuslik_sisend) + "€")
        canvas.drawString(11 * cm, 25 * cm, "Kogumispension")
        canvas.drawString(15 * cm, 25 * cm, str(kogumispension) + "€")
        canvas.drawString(11 * cm, 24 * cm, "Töötuskindlustus")
        canvas.drawString(15 * cm, 24 * cm, str(tootuskindlustus) + "€")
        canvas.drawString(11 * cm, 23 * cm, "Tulumaksuvaba")
        canvas.drawString(15 * cm, 23 * cm, str(tmvaba) + "€")
        canvas.drawString(11 * cm, 22 * cm, "Tulumaks")
        canvas.drawString(15 * cm, 22 * cm, str(tulumaks) + "€")
        canvas.drawString(11 * cm, 21 * cm, "Neto töötasu")
        canvas.drawString(15 * cm, 21 * cm, str(netopalk) + "€")

        canvas.save()
