import sys
import urllib2
from BeautifulSoup import BeautifulSoup


def get_phot(epic, verbose=True, savefp=None, return_str=False):

    PM = '&plusmn; '

    url = 'https://exofop.ipac.caltech.edu/k2/edit_target.php?id={}'.format(epic)
    soup = BeautifulSoup(urllib2.urlopen(url).read())

    table = soup.find(id='myTable1')

    res = {}
    out_str = ''
    for line in table.findAll('tr')[2:]:
        td = line.findAll('td')
        band = td[0].text
        if band == 'Kep':
            band = 'Kepler'
        elif band == 'WISE 3.4 micron':
            band = 'W1'
        elif band == 'WISE 4.6 micron':
            band = 'W2'
        elif band == 'WISE 12 micron':
            band = 'W3'
        elif band == 'WISE 22 micron':
            band = 'W4'

        vals = td[1].text
        if '&plusmn; ' in vals:
            line_str = ' '.join([band, '=', ', '.join(vals.split(PM))])
            res[band] = map(float, vals.split(PM))
        else:
            line_str = ' '.join([band, '=', vals])
            res[band] = float(vals)
        out_str += line_str+'\n'

    if savefp:
        with open(savefp, 'w') as f:
            f.write(out_str)

    if verbose:
        print out_str
    if return_str:
        return out_str
    else:
        return res


def get_stellar(epic, verbose=True, rstar=False, savefp=None, return_str=False):

    PM = '&plusmn;'

    url = 'https://exofop.ipac.caltech.edu/k2/edit_target.php?id={}'.format(epic)
    soup = BeautifulSoup(urllib2.urlopen(url).read())

    table = soup.find(id='myTable2')

    line = table.findAll('tr')[1]
    keys = [th.text for th in line.findAll('th')]

    line = table.findAll('tr')[2]
    vals = [th.text for th in line.findAll('td')]

    want = 'Teff(K) log(g) [Fe/H]'.split()
    good = 'Teff logg feh'.split()

    if rstar:
        want.append('Radius(R_Sun)')
        good.append('rstar')

    out_str = ''
    for g,w in zip(good, want):
        idx = keys.index(w)
        line_str = ' '.join([g, '=', ', '.join(vals[idx].split(PM))])
        out_str += line_str+'\n'

    if savefp:
        with open(savefp, 'w') as f:
            f.write(out_str)

    if verbose:
        print out_str
    if return_str:
        return out_str
    else:
        res = {k:map(float, vals[keys.index(w)].split(PM)) \
            for k,w in zip(good, want)}
        return res
