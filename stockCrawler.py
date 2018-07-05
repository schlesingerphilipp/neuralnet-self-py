import urllib.request

def getNASQIds():
    rawNasdaq = urllib.request.urlopen("http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt").read().decode('utf-8')
    rawlines = rawNasdaq.split("\n")
    lines = [rawline.split("|") for rawline in rawlines]
    parsed = [{"symbol":line[0], "name":line[1],"category":line[2]} for line in lines if len(line) == 8]
    return parsed
