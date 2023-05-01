# -*- coding: latin-1 -*-
###############################################################################################################################################################
#
# M�dulo : Contants Gui           Data de Cria��o: 07/12/2022
#
# Objetivo: M�dulo base para as constantes de projeto.
#
# Ultimas altera��es: Cria��o
#
# Data da ultima altera��o: 07/12/2022
#
# Desenvolvedor: Francisco J. E. de Sousa
#
# Contato: e-mail: francisco.sousa1993@outlook.com      tel: (21) 96965-6759
#
###############################################################################################################################################################

# Imports:

import datetime as dt
from enum import Enum
from plotly.subplots import make_subplots
import dash
from dash import Dash, html, dcc,ctx
import dash_bootstrap_components as dbc
import pandas as pd
import datetime as dt
from dash.dependencies import Input, Output
from dash_extensions.enrich import Output as eOutput, DashProxy, Input as eInput, MultiplexerTransform
#import dash_extensions.enrich as dash_enrich #import Output, DashProxy, Input, MultiplexerTransform
from dash.exceptions import PreventUpdate
from plotly import express,graph_objects
import plotly.io as pio
import base64
import numpy as np
from Indicators import *
from functools import reduce
import EngClsMatrix as mtx
from EngSettings import *
import os
import json

# Constants:

month_int_ref=int(dt.datetime.today().month)
month_ref=["JANEIRO","FEVEREIRO","MARÇO","ABRIL","MAIO","JUNHO","JULHO","AGOSTO","SETEMBRO","OUTUBRO","NOVEMBRO","DEZEMBRO"][month_int_ref-1]
year_ref=str(dt.datetime.today().year) if month_ref.find('JAN')<0 else str(dt.datetime.today().year-1)


#img_n4_introducao_encoded = base64.b64encode(open(img_n4_introducao, 'rb').read()).decode('ascii')

# External Scripts/Styles:

external_scripts = [
            'https://www.google-analytics.com/analytics.js',
            {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
            {
                'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
                'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
                'crossorigin': 'anonymous'
            }
        ]

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

# Side bar
SIDEBAR_STYLE={
    'position':'fixed',
    'top':0,
    'left':0,
    'bottom':0,
    'width':'20rem',
    'padding':'2rem 1rem',
    'background-color':'#070713'
}

SIDEBAR_LINKS_STYLE={
    "font-size":"1.6rem",
    "text-align":"left"
}
                
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"
}

# main Layout
MAIN_LAYOUT_STYLE={
        'background-color':"#120a29",
        'width':'150rem',
        'height':'600rem'
}

TAB_STYLE = {
    'color':'white',
    'width': '15rem',
    'border': 'none',
    'boxShadow': 'inset 0px -1px 0px 0px white',
    'borderBottom': '2px white solid',
    'background': '#120a29',
    'paddingTop': 0,
    'paddingBottom': 0,
    'height': '30px'
}

SELECTED_STYLE = {
    'color':'white',
    'width': '18rem',
    'height': '30px',
    'boxShadow': 'none',
    'borderLeft': 'none',
    'borderRight': 'none',
    'borderTop': 'none',
    'borderBottom': '2px white solid',
    'background': '#23235c',
    'paddingTop': 0,
    'paddingBottom': 0
}


#Charts Type

class CHART_TYPE(Enum):
    PIE=1
    VERTICAL_BAR=2
    HORIZONTAL_BAR=3
    SCATTER=4
    HISTOGRAM=40
