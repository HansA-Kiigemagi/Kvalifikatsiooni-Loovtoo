
import PySimpleGUI as sg
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm

# Maksude arvutamise funktsioon(id)
def maksud2024(arvestuslik,kas_kogumis):
    # Lihtsad maksud
    # Kogumispension on valikuline 2%
    if kas_kogumis:
        kogumispension = round(arvestuslik * 0.02, 2)
    else:
        kogumispension = 0
    # Töötuskindlustus 1,6%
    tootuskindlustus = round(arvestuslik * 0.016, 2)
    # Tulumaksuvaba maksimaalselt 654€, sõltub tulust
    if arvestuslik <= 1200:
        if arvestuslik - kogumispension - tootuskindlustus < 654:
            tmvaba = arvestuslik - kogumispension - tootuskindlustus
        else:
            tmvaba = 654
    elif arvestuslik < 2100:
        tmvaba = round(654 - 0.72667 * (arvestuslik - 1200))
    else:
        tmvaba = 0
    # Tulumaks 20%
    tulumaks = round((arvestuslik - tmvaba - kogumispension - tootuskindlustus) * 0.2, 2)
    if tulumaks < 0:
        tulumaks = 0
    # Kätte
    netopalk = round(arvestuslik - kogumispension - tootuskindlustus - tulumaks, 2)

    return kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk

def maksud2025(arvestuslik, kas_kogumis):
    # Valikuline kogumispension 2%
    if kas_kogumis:
        kogumispension = round(arvestuslik * 0.02, 2)
    else:
        kogumispension = 0
    # Tootuskindlustus 1,6%
    tootuskindlustus = tootuskindlustus = round(arvestuslik * 0.016, 2)
    # Tulumaksuvaba kõigil 700€
    if arvestuslik - kogumispension - tootuskindlustus < 700:
        tmvaba = arvestuslik - kogumispension - tootuskindlustus
    else:
        tmvaba = 700
    # Tulumaks 22%
    tulumaks = round((arvestuslik - tmvaba - kogumispension - tootuskindlustus) * 0.22, 2)
    # Netopalk
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
          [sg.Text("Maksuseaduse aasta"), sg.Combo(["2024", "2025"], readonly=True, default_value="2024", key="-AASTA-")],
          [sg.Text("Kogumispension"), sg.Radio("On",key="ON", group_id=1,), sg.Radio("Ei ole",key="POLE", group_id=1)],
          [sg.Column(maksude_nimetuste_veerg), sg.Column(maksude_arvude_veerg), sg.VSeparator(), sg.Column(andmete_nimetuste_veerg), sg.Column(andmete_sisestuse_veerg)],
          [sg.Button("Arvuta", bind_return_key=True), sg.Button("Loo PDF", disabled=True, key="-PDFNUPP-")],
          [sg.Button("Sulge")]]


window = sg.Window("Tulumaksu kalkulaator v0.0.3", layout, size=(1200, 400))

# Tegevustsükkel
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == "Sulge":
        break
    if event == "Arvuta":
        # Maksude arvutamine andmete põhjal, sõltuvalt valitud aastast
        arvestuslik_sisend = float(values["-ARVESTUSLIK-"])
        if values["-AASTA-"] == "2024":
            kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk = maksud2024(arvestuslik_sisend, values["ON"])
        elif values["-AASTA-"] == "2025":
            kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk = maksud2025(arvestuslik_sisend, values["ON"])
        # Andmete kuvamine programmiaknas
        window["-KOGUMISPENSION-"].update(str(kogumispension) + "€")
        window["-TOOTUS_TOOTAJALT-"].update(str(tootuskindlustus) + "€")
        window["-TMVABA-"].update(str(tmvaba) + "€")
        window["-TULUMAKS-"].update(str(tulumaks) + "€")
        window["-NETOPALK-"].update(str(netopalk) + "€")
        window["-PDFNUPP-"].update(disabled=False)
    if event == "-PDFNUPP-":
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
        # Vasakpoolne plokk - töötaja ja palgalehe info
        x1 = 2 * cm
        y = 26 * cm
        taisnimi = eesnimi + " " + perenimi
        vasak_nimed = ["Töötaja", "Isikukood", "Kuupäev", "Maksmise kuupäev"]
        vasak_andmed = [taisnimi, isikukood, kuupaev, maksmise_kuupaev]

        for i in range(len(vasak_nimed)):
            canvas.drawString(x1, y, str(vasak_nimed[i]))
            canvas.drawString(x1 + 4 * cm, y, str(vasak_andmed[i]))
            y -= 1 * cm

        # Parem plokk - töötaja palgaandmed
        x2 = 11 * cm
        y = 26 * cm
        parem_nimed = ["Bruto Töötasu", "Kogumispension", "Töötuskindlustus", "Tulumaksuvaba", "Tulumaks", "Neto töötasu"]
        parem_andmed = [arvestuslik_sisend, kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk]

        for i in range(len(parem_nimed)):
            canvas.drawString(x2, y, parem_nimed[i])
            canvas.drawString(x2 + 4 * cm, y, str(parem_andmed[i]) + "€")
            y -= 1 * cm

        # Faili salvestamine
        canvas.showPage()
        canvas.save()
