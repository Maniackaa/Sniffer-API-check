import re


def find_weth(text):
    res = re.findall('WETH liquidity: (\d+) ', text)
    return int(res[0])
