#!/usr/bin/env python

# pre-commit for git, which handles:
#   - Incrementing the version number
#   - Rebuilding and adding the main pdf
#   - Recording word and figure counts
#   - Updating the progress figure

import os
import re
import sys
import json
import subprocess

import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from functools import wraps

# ----------------------------------------
# Plot Style
# ----------------------------------------

# Normally handle this through a small module but for portability I've reproduced plot styling here.
# This will require a working xelatex installation and 'Source Sans Pro'
# installed on the system.
plt.style.use('utility/minimal.mplstyle')
# This one is incompatible with the style sheet:
plt.rcParams['pgf.preamble'] = [r"\usepackage{mathspec}", r"\setallmainfonts(Digits,Latin,Greek){Source Sans Pro Light}"]


def _despined(init):
    """
    Decorator to make the constructor of pyplot.Axes
    return an axes without left right or top spines.
    """
    @wraps(init)
    def despined_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        for spine in ["left", "right", "top"]:
            self.spines[spine].set_visible(False)
        self.xaxis.tick_bottom()
        self.yaxis.tick_right()
        for tick in self.xaxis.get_major_ticks():
            tick.gridline.set_visible(False)
    return despined_init

# Patch matplotlib to turn off the left/right/top spines of the axes
matplotlib.axes.Axes.__init__ = _despined(matplotlib.axes.Axes.__init__)


def progress(counts):
    index = pd.to_datetime(counts.pop('time'))
    df = pd.DataFrame(counts, index=index)

    # Set relative to goals
    goals = dict(words=20000, pages=170, figures=60)
    for col, goal in goals.items():
        df[col] /= goal

    fig, ax = plt.subplots()
    ax.set_title('Fraction Done'.upper(),loc='left',y=1.1)
    ax.set_ylim(0,1.0)
    df.plot(ax=ax)
    fig.savefig('figures/progress.png', dpi=300, bbox_inches='tight')


def main():
    # Increment version number. 
    with open('classicthesis-config.tex', 'r', encoding='utf-8') as infile:
        content = infile.read()
    version = r'\\newcommand{\\myVersion}{Version ([0-9]+).([0-9]+)\\xspace}'
    major, minor = (int(n) for n in re.search(version, content).group(1,2))
    if minor == 99:
        major += 1
    else:
        minor += 1
    content = re.sub(version, version.replace(r'([0-9]+)',str(major),1).replace(r'([0-9]+)',str(minor),1), content)
    with open('classicthesis-config.tex', 'w', encoding='utf-8') as outfile:
        outfile.write(content)

    # Load recorded counts
    with open('utility/counts.json','r') as infile:
        counts = json.load(infile)
    # Rebuild the pdf and update counts. Fail with non-zero error code
    # if it doesn't build!
    error = subprocess.call(['latexmk', '-xelatex', "-latexoption='-interaction=nonstopmode'", 'axen_thesis.tex'])
    if error:
        raise ValueError('latexmk failed, check for errors!')

    # Get the counts and time
    out, _ = subprocess.Popen(['texcount', '-sum', '-total', '-merge', 'axen_thesis.tex'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    wc = int(re.search(b'Words in text: ([0-9]+)',out).group(1))
    fc = int(re.search(b'Number of floats/tables/figures: ([0-9]+)',out).group(1))

    out, _ = subprocess.Popen(['pdfinfo', 'axen_thesis.pdf'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    pc = int(re.search(b'Pages:\s*([0-9]+)',out).group(1))
    
    time = pd.to_datetime('now')

    # Save them to the json
    counts['words'].append(wc)
    counts['pages'].append(pc)
    counts['figures'].append(fc)
    counts['time'].append(str(time))

    with open('utility/counts.json', 'w') as outfile:
        json.dump(counts, outfile)

    # Update the progress plot
    progress(counts)
    
    

if __name__ == "__main__":
    main()
