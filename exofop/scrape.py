import sys
import urllib2
from BeautifulSoup import BeautifulSoup


def get_phot(epic, verbose=True):

    PM = '&plusmn; '

    url = 'https://exofop.ipac.caltech.edu/k2/edit_target.php?id={}'.format(epic)
    soup = BeautifulSoup(urllib2.urlopen(url).read())

    table = soup.find(id='myTable1')

    res = {}
    for line in table.findAll('tr')[2:]:
        td = line.findAll('td')
        band = td[0].text
        if band == 'Kep':
            band = 'Kepler'
        vals = td[1].text
        if '&plusmn; ' in vals:
            if verbose:
                print band, '=', ', '.join(vals.split(PM))
            res[band] = map(float, vals.split(PM))
        else:
            if verbose:
                print band, '=', vals
            res[band] = float(vals)

    if not verbose:
        return res


def get_stellar(epic, verbose=True):

    PM = '&plusmn;'

    url = 'https://exofop.ipac.caltech.edu/k2/edit_target.php?id={}'.format(epic)
    soup = BeautifulSoup(urllib2.urlopen(url).read())

    table = soup.find(id='myTable2')

    line = table.findAll('tr')[1]
    keys = [th.text for th in line.findAll('th')]

    line = table.findAll('tr')[2]
    vals = [th.text for th in line.findAll('td')]

    want = 'Teff(K) log(g) [Fe/H]'.split()
    good = 'teff logg feh'.split()
    if verbose:
        for g,w in zip(good, want):
            idx = keys.index(w)
            print g, '=', ', '.join(vals[idx].split(PM))
    else:
        return {k:map(float, vals[keys.index(w)].split(PM)) \
            for k,w in zip(good, want)}
