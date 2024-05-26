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

def maksud_kohandatud(arvestuslik, tmvaba, tulumaks_protsent, tootus_protsent, kogumis_protsent):
    # Eeldame, et ei ole mingeid erilisi valemeid nagu nt 2024 tulumaksuvaba arvutamine
    tootuskindlustus = round(arvestuslik * (tootus_protsent / 100), 2)
    kogumispension = round(arvestuslik * (kogumis_protsent / 100), 2)
    tulumaks = round((arvestuslik - tmvaba - tootuskindlustus - kogumispension) * (tulumaks_protsent / 100), 2)
    netopalk = round(arvestuslik - kogumispension - tootuskindlustus - tulumaks, 2)
    return kogumispension, tootuskindlustus, tmvaba, tulumaks, netopalk

def tooandja_maksud(arvestuslik):
    sotsiaalmaks = round(arvestuslik * 0.33, 2)
    tootuskindlustus = round(arvestuslik * 0.008, 2)
    kulu = arvestuslik + sotsiaalmaks + tootuskindlustus

    return kulu, sotsiaalmaks, tootuskindlustus