from datetime import datetime
import math
import sqlite3 as sq3
from multiprocessing import pool

con = sq3.connect('homes.db')


def to_rad(deg: float) -> float:
    return deg * math.pi / 180


def circle_dist(ax: float, ay: float, bx: float, by: float) -> float:
    return 2 * math.asin(math.sqrt((math.sin((ax-bx)/2)) ** 2 + math.cos(ax) * math.cos(bx) * math.sin((ay-by)/2) ** 2))


def check(dist: float) -> float:
    if dist < 0:
        dist += math.pi
    dist *= 6371.2 # radius of earth in km
    return dist


def inmiles(km: float) -> float:
    km = km / 1.609
    return km


def calculate(x1: float, x2: float, x3: float, x4: float) -> tuple:
    dis = circle_dist(to_rad(x1), to_rad(x2), to_rad(x3), to_rad(x4))
    clean = check(dis)
    ret = inmiles(clean)
    return clean, ret


def fromdb() -> list:
    cur = con.cursor()
    cur.execute('SELECT * FROM wgs')
    rows = cur.fetchall()
    return rows


def get_coords(listy: list) -> list:
    return [(x[3], x[4], x[7], x[8]) for x in listy]


def combine(table: list, newdata: list) -> list:
    d1 = [(table[i] + newdata[i]) for i in range(len(table))] # makes list of tuples
    # don't index newdata because it's already being iterated through
    return d1


def out(data: list) -> int:
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS distance (npa integer, residence text, bldg_type text, latitude float, longitude float,'
                'facility text, address text, fac_lat float, fac_long float, great_circle_km float, '
                'great_circle_mi float)')
    add = 'INSERT INTO distance values(?,?,?,?,?,?,?,?,?,?,?)'
    for x in data:
        cur.execute(add, x)
    con.commit()
    return cur.lastrowid


if __name__ == '__main__':
    f = fromdb()
    g = get_coords(f)
    p = pool.Pool()
    print("calculating:", datetime.now())
    results = p.starmap(calculate, g)
    print("combining:", datetime.now())
    m = combine(f, results)
    print(m)
    print("adding to database:", datetime.now())
    out(m)
    p.close()