import os

filename = 'hdomar_1931-1932.txt'

days = ['Mánudaginn', 'Þriðjudaginn', 'Miðvikudaginn', 'Fimmtudaginn', 'Föstudaginn', 'Laugardaginn', 'Sunnudaginn']

with open(filename) as f:
    domur = ""
    collect = False
    for count, line in enumerate(f):
        if any(day in line for day in days):
            if domur != "":
                with open(os.path.join('out', str(count) + ".txt"), "w") as out:
                    out.write(domur)
            domur = ""
            domur = line
            collect = True
            continue
        if collect is True:
            domur = domur + line
    with open(os.path.join('out', str(count) + ".txt"), "w") as out:
        out.write(domur)

