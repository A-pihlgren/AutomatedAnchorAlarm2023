import json

positions = []

i = 201
while i < 272:
    f = open(f'/Users/adrianpihlgren/cs408/testGo/jsonfiles/data{i}.json')
    if i == 26:
        i = 29
    
    print(i)
    i += 1
    #'/Users/adrianpihlgren/CS408/testGo/gui/data1.json')
    
    data = json.load(f)
    
    for obj in data:
        mmsi = obj['AIS']['MMSI']
        if (mmsi == 355249000):
            lat = obj['AIS']['LATITUDE']
            lon = obj['AIS']['LONGITUDE']
            pair = (lon, lat)
            exists = False
            for pos in positions:
                if pos == pair:
                    exists = True
            if exists == False:
                positions.append(pair)
            print(f'MMSI: {mmsi}, Latitude: {lat}, Longitude: {lon}')
    
    f.close()
print(positions)
