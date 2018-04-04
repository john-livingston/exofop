import sys
try:
    # python 3
    from urllib.request import urlopen, urlretrieve
except ImportError:
    # Python 2
    from urllib2 import urlopen, urlretrieve
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

def get_phot(epic, verbose=True, savefp=None, return_str=False):

    PM = '±'

    url = 'https://exofop.ipac.caltech.edu/k2/edit_target.php?id={}'.format(epic)
    soup = BeautifulSoup(urlopen(url).read(), "html5lib")

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
        # import pdb; pdb.set_trace()
        if PM in vals:
            line_str = ' '.join([band, '=', ','.join(vals.split(PM))])
            res[band] = list(map(float, vals.split(PM)))
        else:
            line_str = ' '.join([band, '=', vals])
            res[band] = float(vals)
        out_str += line_str+'\n'

    if savefp:
        with open(savefp, 'w') as f:
            f.write(out_str)

    if verbose:
        print(out_str)
    if return_str:
        return out_str

    return res


def get_stellar(epic, verbose=True, rstar=False, savefp=None, return_str=False):

    PM = '±'

    url = 'https://exofop.ipac.caltech.edu/k2/edit_target.php?id={}'.format(epic)
    soup = BeautifulSoup(urlopen(url).read(), "html5lib")

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
        line_str = ' '.join([g, '=', ','.join(vals[idx].split(PM))])
        out_str += line_str+'\n'

    if savefp:
        with open(savefp, 'w') as f:
            f.write(out_str)

    if verbose:
        print(out_str)
    if return_str:
        return out_str

    res = {k:list(map(float, vals[keys.index(w)].split(PM))) \
        for k,w in zip(good, want)}

    return res


baseurl = "https://exofop.ipac.caltech.edu/"

def get_all_links(epic,mission='k2'):
    webpage = baseurl+mission+"/edit_target.php?id={}".format(epic)

    try:
        html_page = urlopen(webpage)
        html = urlopen(webpage)
        bsObj = BeautifulSoup(html.read(), "lxml");
    except Exception as e:
        print('Error: {}\n{} does not exist!\n'.format(e,webpage))
        sys.exit()
        
    links = []
    for link in bsObj.find_all('a'):
        links.append(link.get('href'))

    if len(links) == 0:
        print('No links fetched. Check EPIC number.\n')
        sys.exit()
    return links

def get_specific_ext(links,ext='csv',mission='k2'):
    wanted = []
    for link in links:
        try:
            if link.split('.')[-1] == ext:
                wanted.append(baseurl+mission+'/'+link)
        except:
            pass

    if len(wanted) == 0:
        print('No links fetched with file extension={}\n'.format(ext))
        sys.exit()
    return wanted

def save_to_file(epic, urls, ext):
    epic = str(epic)
    if not os.path.exists(epic):
        os.makedirs(epic)

    subfolder=os.path.join(epic,ext)
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    print('\n----------Saving .{} files----------\n'.format(ext))
    i =0
    for url in tqdm(urls):
        #save: e.g. epic/epic.csv
        # if len(urls) > 1:
        #     fname = epic+'_'+str(i)+'.'+ext
        # else:
        #     fname = epic+'.'+ext
        fname = url.split('/')[-1]
        destination = os.path.join(subfolder,fname)
        try:
            urlretrieve(url, destination)
            #print('Saved: {}\n'.format(url))
        except Exception as e:
            print('Error: {}\nNot saved: {}\n'.format(e,url))
        i+=1

    return None
