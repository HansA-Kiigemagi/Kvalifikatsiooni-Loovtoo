import PySimpleGUI as sg
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from funktsioonid import *
from layouts import *

# Akna üldkujundus
sg.theme("Default 1")

# Akende elementide paigutus (tulbad vaata layouts.py)
layout = [[sg.Menu(menu_def)],
          [sg.Text("Sisesta arvestuslik töötasu:"), sg.Input(key="-ARVESTUSLIK-", size=(12,1))],
          [sg.Text("Maksuseaduse aasta"), sg.Combo(["2024", "2025"], readonly=True, default_value="2024", key="-AASTA-")],
          [sg.Text("Kogumispension"), sg.Radio("On", key="ON", group_id=1), sg.Radio("Ei ole", key="POLE", group_id=1), sg.Text("Tööandja maksud palgalehel"), sg.Checkbox(key="KAS_PALGALEHEL", text="")],
          [sg.Column(maksude_nimetuste_veerg), sg.Column(maksude_arvude_veerg), sg.VSeparator(), sg.Column(tooandja_nimetuste_veerg), sg.Column(tooandja_arvude_veerg), sg.VSeparator(), sg.Column(andmete_nimetuste_veerg), sg.Column(andmete_sisestuse_veerg)],
          [sg.Button("Arvuta", bind_return_key=True), sg.Button("Loo PDF", disabled=True, key="-PDFNUPP-")],
          [sg.Button("Sulge"), sg.Button("Sätted"), sg.Button("Info")]]

window = sg.Window("Tulumaksu kalkulaator v0.2.0", layout, finalize=True)

def ava_satete_window():
    satted_layout = [[sg.Text("Kasuta kohandatud andmeid"), sg.Checkbox(text="", key="-SATTED_KAS_KOHANDATUD-")],
                     [sg.Column(satted_nimetused), sg.Column(satted_sisendid)],
                     [sg.Button(button_text="Kinnita", key="-SATTED_KINNITA-"), sg.Button(button_text="Sulge sätted", key="-SATTED_SULGE-")]]
    window2 = sg.Window("Sätted", satted_layout, modal=True)
    while True:
        event2, values2 = window2.read()
        if event2 == sg.WIN_CLOSED or event2 == "-SATTED_SULGE-":
            break
        if event2 == "-SATTED_KINNITA-":
            kohandatud = values2["-SATTED_KAS_KOHANDATUD-"]
            c_tulumaksuvaba = int(values2["-SATTED_C_TMVABA-"])
            c_tulumaks = int(values2["-SATTED_C_TULUMAKS-"])
            c_tootuskindlustus = int(values2["-SATTED_C_TOOTUS-"])
            c_kogumispension = int(values2["-SATTED_C_KOGUMIS-"])
            window2.close()
            return kohandatud, c_tulumaksuvaba, c_tulumaks, c_tootuskindlustus, c_kogumispension
    window2.close()
    return None, None, None, None, None

def ava_info_window():
    info_layout = [[sg.Multiline("Programmi on loonud Hans Andre Kiigemägi.\nProgramm loodi Nõo Reaalgümnaasiumi arvutiõpetuse kvalifikatsioonikursuse raames.\nProgramm on suhteliselt töökindel, kuid ei ole sobilik asendus reaalsete raamatupidamisprogrammide kasuks.", wrap_lines=True, size=(80, 6))],
                   [sg.Button(button_text="Sulge", key="-INFO_SULGE-")]]
    window3 = sg.Window("Info", info_layout, modal=True)
    while True:
        event3, values3 = window3.read()
        if event3 == sg.WIN_CLOSED or event3 == "-INFO_SULGE-":
            break
    window3.close()

# Tegevustsükkel
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Sulge":
        break
    if event == "Arvuta":
        arvestuslik_sisend = float(values["-ARVESTUSLIK-"])
        if values["-AASTA-"] == "2024":
            kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk = maksud2024(arvestuslik_sisend, values["ON"])
        elif values["-AASTA-"] == "2025":
            kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk = maksud2025(arvestuslik_sisend, values["ON"])
        if values.get("-SATTED_KAS_KOHANDATUD-"):
            kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk = maksud_kohandatud(arvestuslik_sisend, c_tulumaksuvaba, c_tulumaks, c_tootuskindlustus, c_kogumispension)
        kogu_kulu, sotsiaalmaks, tooandja_tootuskindlustus = tooandja_maksud(arvestuslik_sisend)
        window["-KOGUMISPENSION-"].update(str(kogumispension) + "€")
        window["-TOOTUS_TOOTAJALT-"].update(str(tootuskindlustus) + "€")
        window["-TMVABA-"].update(str(tmvaba) + "€")
        window["-TULUMAKS-"].update(str(tulumaks) + "€")
        window["-NETOPALK-"].update(str(netopalk) + "€")
        window["-SOTSIAALMAKS-"].update(str(sotsiaalmaks) + "€")
        window["-TOOTUS_TOOANDJALT-"].update(str(tooandja_tootuskindlustus) + "€")
        window["-TOOANDJA_KULU-"].update(str(kogu_kulu) + "€")
        window["-PDFNUPP-"].update(disabled=False)
    if event == "-PDFNUPP-":
        isikukood = str(values["-ISIKUKOOD-"])
        perenimi = str(values["-PERENIMI-"])
        eesnimi = str(values["-EESNIMI-"])
        kuupaev = str(values["-KUUPAEV-"])
        maksmise_kuupaev = str(values["-MAKSMISE_KP-"])
        kuupaev_failile = kuupaev.replace(".", "_", 2)
        pealkiri = perenimi + kuupaev_failile + ".pdf"
        canvas = Canvas(pealkiri)
        canvas.setFont("Helvetica", 20)
        canvas.drawString(2 * cm, 27.5 * cm, "Palgaleht")
        canvas.line(2 * cm, 27 * cm, 20 * cm, 27 * cm)
        canvas.setFont("Helvetica", 12)
        x1 = 2 * cm
        y = 26 * cm
        taisnimi = eesnimi + " " + perenimi
        vasak_nimed = ["Töötaja", "Isikukood", "Kuupäev", "Maksmise kuupäev"]
        vasak_andmed = [taisnimi, isikukood, kuupaev, maksmise_kuupaev]
        for i in range(len(vasak_nimed)):
            canvas.drawString(x1, y, str(vasak_nimed[i]))
            canvas.drawString(x1 + 4 * cm, y, str(vasak_andmed[i]))
            y -= 1 * cm
        x2 = 11 * cm
        y = 26 * cm
        parem_nimed = ["Bruto Töötasu", "Kogumispension", "Töötuskindlustus", "Tulumaksuvaba", "Tulumaks", "Neto töötasu"]
        parem_andmed = [arvestuslik_sisend, kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk]
        for i in range(len(parem_nimed)):
            canvas.drawString(x2, y, parem_nimed[i])
            canvas.drawString(x2 + 4 * cm, y, str(parem_andmed[i]) + "€")
            y -= 1 * cm
        x3 = 11 * cm
        y = 18 * cm
        if values["KAS_PALGALEHEL"]:
            tooandja_nimed = ["Sotsiaalmaks", "Töötuskindlustus", "Tööandja kulu"]
            tooandja_andmed = [sotsiaalmaks, tooandja_tootuskindlustus, kogu_kulu]
            canvas.drawString(x3, 19 * cm, "Tööandja maksud")
            for i in range(len(tooandja_nimed)):
                canvas.drawString(x3, y, tooandja_nimed[i])
                canvas.drawString(x3 + 4 * cm, y, str(tooandja_andmed[i]) + "€")
                y -= 1 * cm
        canvas.showPage()
        canvas.save()
    if event == "Sätted":
        kohandatud, c_tulumaksuvaba, c_tulumaks, c_tootuskindlustus, c_kogumispension = ava_satete_window()
    if event == "Info":
        ava_info_window()
window.close()
