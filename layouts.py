import PySimpleGUI as sg
sg.theme("Default 1")

menu_def = [["File", ["Sätted", "Info"]]]

# Põhiaken
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

tooandja_nimetuste_veerg = [[sg.Text("Tööandja kulu:")],
                            [sg.Text("Sotsiaalmaks:")],
                            [sg.Text("Töötuskindlustus:")]]

tooandja_arvude_veerg = [[sg.Text(key="-TOOANDJA_KULU-", size=(10,1))],
                         [sg.Text(key="-SOTSIAALMAKS-", size=(10,1))],
                         [sg.Text(key="-TOOTUS_TOOANDJALT-", size=(10, 1))]]

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

# Sätete aken
satted_nimetused = [[sg.Text("Tulumaksuvaba")],
                    [sg.Text("Tulumaks")],
                    [sg.Text("Töötuskindlustus")],
                    [sg.Text("Kogumispension")]]

satted_sisendid = [[sg.Input(key="-SATTED_C_TMVABA-", size=(12,1)), sg.Text("€")],
                   [sg.Input(key="-SATTED_C_TULUMAKS-", size=(12,1)), sg.Text("%")],
                   [sg.Input(key="-SATTED_C_TOOTUS-", size=(12,1)), sg.Text("%")],
                   [sg.Input(key="-SATTED_C_KOGUMIS-", size=(12,1)), sg.Text("%")]]

# Infoaken
info_layout = [[sg.Multiline("Programmi on loonud Hans Andre Kiigemägi.\nProgramm loodi Nõo Reaalgümnaasiumi arvutiõpetuse kvalifikatsioonikursuse raames.\nProgramm on suhteliselt töökindel, kuid ei ole sobilik asendus reaalsete raamatupidamisprogrammide kasuks.", wrap_lines=True, size=(80, 6))],
               [sg.Button(button_text="Sulge", key="-INFO_SULGE-")]]
