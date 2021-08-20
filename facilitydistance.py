import math, time
import pandas as pd
import sqlite3 as sq3
homes = sq3.connect('homes.db')


def distance(a: tuple, b: tuple) -> float:
    return math.sqrt(((b[0]-a[0]) ** 2) + ((b[1]-a[1]) ** 2))


def shortest_dist(hh: list, meds: list) -> tuple:
    home = hh[0]  # home address
    spot = hh[1]  # coordinates
    names = [x[0] for x in meds]  # name of facility
    adds = [x[1] for x in meds]  # address of facility
    coor = [x[2] for x in meds]  # coords of facility
    dists = [distance(spot, x) for x in coor]
    short = min(dists)
    place = names[dists.index(short)]
    addy = adds[dists.index(short)]
    point = coor[dists.index(short)]
    return home, place, addy, point


def get_info() -> list:
    cur = homes.cursor()
    cur.execute('SELECT address, addy_x, addy_y FROM addresses')
    rows = [x for x in cur.fetchall()]
    ret = [[x[0], (x[1], x[2])] for x in rows]
    return ret


def medfacs() -> list:
    df = pd.read_csv('medcoords.csv')
    dic = {}
    c = {}
    ret = []
    temp = [[row['Name'], row['Address'], (row['X'], row['Y'])] for index, row in df.iterrows()]
    for x in temp:
        if x[1] not in dic:
            dic[x[1]] = []
            c[x[1]] = x[2]
        dic[x[1]].append(x[0])
    for k, v in dic.items():
        if len(v) > 1:
            v = " + ".join(v)
        else:
            v = v[0]
        ret.append([v, k, c[k]])
    return ret


def get_rest(listy: list) -> list:
    temp = []
    cur = homes.cursor()
    for x in listy:
        cur.execute('SELECT npa, type, latitude, longitude FROM addresses where address = "{}"'.format(x[0]))
        obj = cur.fetchone()
        filler = (obj[0], x[0], obj[1], obj[2], obj[3], x[1], x[2], x[3][0], x[3][1])
        # obj[0] is npa, x[0] is home address, obj[1] is type, obj[2] is lat, obj[3] is long,
        # x[1] is facility, x[2] is facility address, x[3] is epsg2264 coords
        temp.append(filler)
    return temp


def matchy(listy: list) -> int:
    cur = homes.cursor()
    cur.execute('CREATE TABLE matched (npa integer, residence text, type text, latitude float, longitude float,'
                'facility text, address text, epsgNC_x text, espgNC_y text)')
    add = 'INSERT INTO matched values(?,?,?,?,?,?,?,?,?)'
    for x in listy:
        cur.execute(add, x)
    homes.commit()
    return cur.lastrowid


if __name__ == '__main__':
    out = []
    data = get_info()
    med = medfacs()
    print("distance started at ", time.time())
    for z in data:
        s = shortest_dist(z, med)
        out.append(s)
    print("distance ended at ", time.time())
    print("matching started at ", time.time())
    com = get_rest(out)
    print("matching ended at ", time.time())
    matchy(com)



