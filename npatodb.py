import sqlite3 as sq3
import pandas as pd
from shapely.geometry import Point, Polygon


def get_bounds() -> dict:
    npas = pd.read_csv("/Users/nadiabey/Documents/Duke/Spring 2021/Data Journalism/healthfac/npa-coords.csv")
    bounds = {}
    areas = {}
    for index, row in npas.iterrows():  # loop through rows in csv
        current = row['NPA']
        spot = (row['X'], row['Y'])  # coordinates
        if current not in bounds:
            bounds[current] = []  # put if absent
        bounds[current].append(spot)  # add coordinates to list in dict
    for k, v in bounds.items():
        areas[k] = Polygon(v)
    return areas


def match_npas(bounds: dict) -> list:
    res = pd.read_csv('/Users/nadiabey/Documents/healthmap/residential.csv', dtype= {'txt_addr_u': str,
                                                                                     'num_parent': str,
                                                                                     'id_add_by': str})
    # coded as 'residential buildings' rather than households bc number of units is unknown
    ru = {}
    ret = []
    npa = [n for n in bounds.keys()]
    for index, row in res.iterrows():
        addy = row['full_addre']
        spot = (row['num_x_coor'], row['num_y_coor'])
        ru[addy] = [Point(spot), row['txt_cdeuse'], row['latitude'], row['longitude']]  # list containing coord and type
    for k, v in ru.items():
        comparisons = [v[0].distance(poly) for poly in bounds.values()]
        least = min(comparisons)
        area = npa[comparisons.index(least)]
        ret.append((area, v[0].x, v[0].y, k, v[1], v[2], v[3]))
    return ret


def insertdb(listy: list) -> int:
    conn = sq3.connect('/Users/nadiabey/Documents/healthmap/homes.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE addresses (npa integer, addy_x float, addy_y float, address text, type text,
     latitude float, longitude float)''')
    add = '''INSERT INTO addresses VALUES (?,?,?,?,?,?,?)'''
    for x in listy:
        cur.execute(add, x)
    conn.commit()
    return cur.lastrowid


if __name__ == '__main__':
    g = get_bounds()
    m = match_npas(g)
    insertdb(m)
