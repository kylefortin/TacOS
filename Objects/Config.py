"""
===================
TacOS Configuration
===================

Contains various environment configuration variables for the TacOS application.

"""

import os
from AnyQt.QtGui import QIcon

# Define working directories
cwd = os.path.dirname(os.path.realpath(__file__ + '/../'))
data = cwd + r'/Data'
graphics = cwd + r'/Graphics'
lightIcons = graphics + '/Lights'
obaIcons = graphics + '/OBA'
tracControlIcons = graphics + '/TracControl'
cssIcons = graphics + '/CSS'
faLibrary = graphics + '/fa/solid'

# Define config files
css = data + '/tacos.css'
lightConfig = data + '/lightcfg.tacos'
obaConfig = data + '/obacfg.tacos'
tracConfig = data + '/traccfg.tacos'
prefs = data + '/prefs.tacos'
logFile = data + '/log.tacos'

# Application geometry
geometry = (100, 100, 800, 600)
controlWidth = 200
controlHeight = 100
camHeight = 250

# Global constants
outputPinList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
busList = ['1', '2']
lightColumns = 3
obaColumns = 2
tracColumns = 2
iconSize = 50
dayBright = 255
nightBright = 63
camFrameRate = 30
strobeRate = 0.5

icons = {
    'logos': {
        'logo': {
            'name': 'TacOS Logo', 'path': graphics + '/TacOS.png'
        }
    },
    'oba': {
        'compressor': {
            'name': 'Compressor', 'path': obaIcons + '/cprsr.png'
        },
        'airhose': {
            'name': 'Air Hose', 'path': obaIcons + '/airhs.png'
        },
        'valve': {
            'name': 'Valve', 'path': obaIcons + '/valve.png'
        }
    },
    'lights': {
        'downlight': {
            'name': 'Down Light', 'path': lightIcons + '/dnlgt.png'
        },
        'light': {
            'name': 'Light', 'path': lightIcons + '/lgt.png'
        },
        'lightbar': {
            'name': 'Light Bar', 'path': lightIcons + '/lgtbar.png'
        },
        'spotlight': {
            'name': 'Spot Light', 'path': lightIcons + '/sptlgt.png'
        }
    },
    'tracControl': {
        'frontDiff': {
            'name': 'Front Diff Lock', 'path': tracControlIcons + '/fdiff.png'
        },
        'rearDiff': {
            'name': 'Rear Diff Lock', 'path': tracControlIcons + '/rdiff.png'
        }
    },
    'css': {
        'checkbox': {
            'name': 'Check Box', 'path': cssIcons + '/checkbox.png'
        },
        'down_arrow': {
            'name': 'Down Arrow', 'path': cssIcons + '/down_arrow.png'
        },
        'handle': {
            'name': 'Handle', 'path': cssIcons + '/handle.png'
        }
    }
}

# Version info
version = '1.4.1'


def faIcon(name):
    return QIcon(faLibrary + '/' + name + '.svg')


def icon(branch, name):
    if name in icons[branch].keys():
        return icons[branch][name]
    else:
        raise KeyError('Requested icon (%s/%s) not available.' % (branch, name))
