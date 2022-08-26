with open("icao-to-aircraft-clean.json") as f:
    lines = f.readlines()

def toupper(lines):
    out = []
    for l in lines:
        kvs = l.split(',')
        icao = kvs[0].split(':')
        icao[1] = icao[1].upper()
        kvs = [':'.join(icao)] + kvs[1:]
        newl = ','.join(kvs)
        out.append(newl)
    return out

newlines = toupper(lines)
with open("icao-to-aircraft-clean.json.new", "w") as f:
    for l in newlines:
        f.write(l)

