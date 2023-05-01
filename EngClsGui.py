###############################################################################################################################################################
#
# Módulo : ENG Cls Gui           Data de Criação: 17/10/2022
#
# Objetivo: Módulo para geração da tela de vizualização.
#
# Ultimas alterações: Criação
#
# Data da ultima alteração: 17/10/2022
#
# Desenvolvedor: Francisco J. E. de Sousa
#
# Contato: e-mail: francisco.sousa1993@outlook.com      tel: (21) 96965-6759
#
###############################################################################################################################################################

# Imports:
from datetime import datetime

from GuiFuncs import *
from Dashboards import *
from flask import Flask

#Server
server=Flask(__name__)

#Constants:
main_title="BI Manutenção"
sub_title="Controle de indicadores: " + datetime.today().__str__()[0:10]

web_pages_title={'':'Home'}
web_pages_content={'':[]}

#Main applications (DASH):
main_app=DashProxy(server=server,name=__name__,routes_pathname_prefix='/',external_scripts=external_scripts,external_stylesheets=external_stylesheets,transforms=[MultiplexerTransform()])
main_app.config.suppress_callback_exceptions=True   

#Imported Charts

#Aggman:
ds_aggman=Dash_Aggman()
#columns=ds_aggman.main_columns
df=ds_aggman.df.copy(deep=True)
dff=ds_aggman.df.copy(deep=True)

dash_atraso=[ds_aggman.Chart_Atraso(),ds_aggman.Chart_Tempo_Aggman()]
dash_criticidade=[ds_aggman.Chart_Criticidade_Equipamento(),ds_aggman.Chart_Criticidade_Plano(),ds_aggman.Chart_Prioridade()]
dash_comp=[ds_aggman.Chart_Percent(),ds_aggman.Chart_AggmanxDemaisSatatus()]

#Disponibilidade
ds_disponibilidade=Dash_Disponibilidade()


#callback functions:

#Pages:
@main_app.callback(Output("page-content", "children"),[Input("url", "pathname")])
def render_page_content(pathname):
    for it in web_pages_title.keys():
        if pathname=="/" +it:
            return web_pages_content[it]               
    else:
        return dbc.Col(
        [
            html.Div(style={'margin-top':'6rem','margin-left':'21rem'},children=[
                html.H1("404: Not found", className="text-danger", style={"font-size":"6rem"}),
                html.Hr(),
                html.P("The pathname '{1}' was not recognised...".format(1,pathname),className="text text-light",style={"font-size":"3rem"}),
            ])
        ])

##############################################################################################################################################
#                                                   Indicador AGGMAN                                                                         #
##############################################################################################################################################
#
#   Descrição: Callbacks do Indicador Aggman
#
#

@main_app.callback(Output('tabs-atraso-id-content', 'children'),
                   Input('tabs-atraso-id', 'value'))
def render_content_Dash_Atraso(tab):
    if tab == 'tab-atraso-0':
        return html.Div([
           dash_atraso[0]
        ])
    elif tab == 'tab-atraso-1':
        return html.Div([
            dash_atraso[1]
        ])


@main_app.callback(Output('tabs-comp-id-content', 'children'),
                   Input('tabs-comp-id', 'value'))
def render_content_Dash_Atraso(tab):
    if tab == 'tab-comp-0':
        return html.Div([
           dash_comp[0]
        ])
    elif tab == 'tab-comp-1':
        return html.Div([
            dash_comp[1]
        ])

###################################  Tab Events: ###################################
#Criticidades:
@main_app.callback([eOutput('ds-crit-pla','style'),eOutput('ds-crit-eqp', 'style'),eOutput('ds-crit-pri','style'),eOutput('ds-tornou-se-aggman','style')],
                   eInput('bt-criticidade-2', 'n_clicks'),
                   eInput('bt-criticidade-1', 'n_clicks'),
                   eInput('bt-criticidade-3', 'n_clicks'),
                   prevent_initial_call=True)
def render_button_criticidades(b1,b2,b3):
    button_clicked=ctx.triggered_id
    if button_clicked=='bt-criticidade-2':    
        return {'display':'none'},{'margin-left':'-18rem','margin-top':'4rem','display':'inline'},{'display':'none'},{'margin-left':'2rem','margin-top':'2rem'}
    elif button_clicked=='bt-criticidade-3': 
        return {'display':'none'},{'display':'none'},{'margin-left':'-18rem','margin-top':'4rem','display':'inline'},{'margin-left':'2rem','margin-top':'2rem'}
    else:
        return {'margin-left':'-18rem','margin-top':'4rem','display':'inline'},{'display':'none'},{'display':'none'},{'margin-left':'2rem','margin-top':'2rem'}

#Atrasos:
@main_app.callback([eOutput('ds-atraso-bkl','style'),eOutput('ds-atraso-agg', 'style')],
                   eInput('bt-atraso-1', 'n_clicks'),
                   eInput('bt-atraso-2', 'n_clicks'),
                   prevent_initial_call=True)
def render_button_atraso(b1,b2):
    button_clicked=ctx.triggered_id
    if button_clicked=='bt-atraso-2':    
        return {'display':'none'},{'margin-left':'-18rem','margin-top':'4rem','width':0,'height':0,'display':'inline'}  
    else:
        return {'margin-left':'-18rem','margin-top':'4rem','width':0,'height':0,'display':'inline'},{'display':'none'}


###################################  Call Back Iteractions: ###################################

#Criticidade Plano:
@main_app.callback([eOutput('ds-total-media', 'children'),eOutput('ds-diciplina','children'),eOutput('ds-navios','children'),
                    eOutput('ds-atraso-bkl','children'),eOutput('ds-crit-eqp','children'),eOutput('ds-crit-pri','children'),
                    eOutput('ds-tornou-se-aggman','children'),eOutput('table-data-os','children'),eOutput('ds-crit-pla','children'),
                    eOutput('ds-atraso-agg','children')],
                    eInput('chart-criticidade-plano', 'clickData'),
                    prevent_initial_call=True
                   )    
def render_content_Dash_CritPlan(click_data):
    #global dash_atraso
    global dff

    if not click_data or click_data is None:
        #dash_atraso=[ds_aggman.Chart_Atraso(dff),ds_aggman.Chart_Tempo_Aggman(dff)]
        return (ds_aggman.Card_Total_E_Media(dff),ds_aggman.Chart_Disciplina(dff),ds_aggman.Chart_Navios(dff),ds_aggman.Chart_Atraso(dff),
                ds_aggman.Chart_Criticidade_Equipamento(dff),ds_aggman.Chart_Prioridade(dff),ds_aggman.Chart_Mudado_2_Aggman(dff),
                DataTable(dff,'Lista OS').Load(),ds_aggman.Chart_Criticidade_Plano(dff),ds_aggman.Chart_Tempo_Aggman(dff))
    else:
        criticidade_chosen=click_data['points'][0]['label']
        
        if dff['CRITICIDADE_PLANO'].nunique()==1:
            df2=df.copy(deep=True)
        else:        
            df2=dff.loc[df['CRITICIDADE_PLANO']==criticidade_chosen]  
            if df2 is None or df2.empty:
                dff=df.copy(deep=True)
                df2=dff.loc[df['CRITICIDADE_PLANO']==criticidade_chosen] 

        #dash_atraso=[ds_aggman.Chart_Atraso(df2),ds_aggman.Chart_Tempo_Aggman(df2)]
        dff=df2.copy(deep=True)
        return (ds_aggman.Card_Total_E_Media(df2),ds_aggman.Chart_Disciplina(df2),ds_aggman.Chart_Navios(df2),ds_aggman.Chart_Atraso(df2),
                ds_aggman.Chart_Criticidade_Equipamento(df2),ds_aggman.Chart_Prioridade(df2),ds_aggman.Chart_Mudado_2_Aggman(df2),
                DataTable(df2,'Lista OS').Load(),ds_aggman.Chart_Criticidade_Plano(df2),ds_aggman.Chart_Tempo_Aggman(df2))
        

#Criticidade Equipamento:
@main_app.callback([eOutput('ds-total-media', 'children'),eOutput('ds-diciplina','children'),eOutput('ds-navios','children'),
                    eOutput('ds-atraso-bkl','children'),eOutput('ds-atraso-agg','children'),
                    eOutput('ds-crit-pla','children'),eOutput('ds-crit-pri','children'),eOutput('ds-tornou-se-aggman','children'),
                    eOutput('table-data-os','children'),eOutput('ds-crit-eqp','children')],
                   eInput('chart-criticidade-equipamento', 'clickData'),
                   prevent_initial_call=True
                   )
def render_content_Dash_CritEquip(click_data):
    #global dash_atraso
    global dff

    if not click_data:
        #dash_atraso=[ds_aggman.Chart_Atraso(dff),ds_aggman.Chart_Tempo_Aggman(dff)]
        return (ds_aggman.Card_Total_E_Media(dff),ds_aggman.Chart_Disciplina(dff),ds_aggman.Chart_Navios(dff),ds_aggman.Chart_Atraso(dff),
                ds_aggman.Chart_Tempo_Aggman(dff),
                ds_aggman.Chart_Criticidade_Plano(dff),ds_aggman.Chart_Prioridade(dff),ds_aggman.Chart_Mudado_2_Aggman(dff),
                DataTable(dff,'Lista OS').Load(),ds_aggman.Chart_Criticidade_Equipamento(dff))
    else:
        criticidade_chosen=click_data['points'][0]['label']
        
        if dff['CRITICIDADE_EQUIPAMENTO'].nunique()==1:
            df2=df.copy(deep=True)
        else:
            df2=dff.loc[df['CRITICIDADE_EQUIPAMENTO']==criticidade_chosen]  
            if df2 is None or df2.empty:
                dff=df.copy(deep=True)
                df2=dff.loc[df['CRITICIDADE_EQUIPAMENTO']==criticidade_chosen] 

        #dash_atraso=[ds_aggman.Chart_Atraso(df2),ds_aggman.Chart_Tempo_Aggman(df2)]
        dff=df2.copy(deep=True)
        
        return (ds_aggman.Card_Total_E_Media(df2),ds_aggman.Chart_Disciplina(df2),ds_aggman.Chart_Navios(df2),ds_aggman.Chart_Atraso(df2),
                ds_aggman.Chart_Tempo_Aggman(df2),
                ds_aggman.Chart_Criticidade_Plano(df2),ds_aggman.Chart_Prioridade(df2),ds_aggman.Chart_Mudado_2_Aggman(df2),
                DataTable(df2,'Lista OS').Load(),ds_aggman.Chart_Criticidade_Equipamento(df2))

#Prioridade:
@main_app.callback([eOutput('ds-total-media', 'children'),eOutput('ds-diciplina','children'),eOutput('ds-navios','children'),
                    eOutput('ds-atraso-bkl','children'),eOutput('ds-atraso-agg','children'),
                    eOutput('ds-crit-pla','children'),eOutput('ds-crit-eqp','children'),eOutput('ds-tornou-se-aggman','children'),
                    eOutput('table-data-os','children'),eOutput('ds-crit-pri','children')],
                   eInput('chart-prioridade', 'clickData'),
                   prevent_initial_call=True
                   )
def render_content_Dash_Prioridade(click_data):
    #global dash_atraso
    global dff

    if not click_data:
        #dash_atraso=[ds_aggman.Chart_Atraso(dff),ds_aggman.Chart_Tempo_Aggman(dff)]
        return (ds_aggman.Card_Total_E_Media(dff),ds_aggman.Chart_Disciplina(dff),ds_aggman.Chart_Navios(dff),ds_aggman.Chart_Atraso(dff),
                ds_aggman.Chart_Tempo_Aggman(dff),
                ds_aggman.Chart_Criticidade_Plano(dff),ds_aggman.Chart_Criticidade_Equipamento(dff),ds_aggman.Chart_Mudado_2_Aggman(dff),
                DataTable(dff,'Lista OS').Load(),ds_aggman.Chart_Prioridade(dff))
    else:
        criticidade_chosen=click_data['points'][0]['label']

        if dff['PRIORIDADE'].nunique()==1:
            df2=df.copy(deep=True)
        else:
            df2=dff.loc[df['PRIORIDADE'].astype('int')==int(criticidade_chosen)]  

            if df2 is None or df2.empty:
                dff=df.copy(deep=True)
                df2=dff.loc[df['PRIORIDADE'].astype('int')==int(criticidade_chosen)] 

        #dash_atraso=[ds_aggman.Chart_Atraso(df2),ds_aggman.Chart_Tempo_Aggman(df2)]
        dff=df2.copy(deep=True)
        
        return (ds_aggman.Card_Total_E_Media(df2),ds_aggman.Chart_Disciplina(df2),ds_aggman.Chart_Navios(df2),ds_aggman.Chart_Atraso(df2),
                ds_aggman.Chart_Tempo_Aggman(df2),
                ds_aggman.Chart_Criticidade_Plano(df2),ds_aggman.Chart_Criticidade_Equipamento(df2),ds_aggman.Chart_Mudado_2_Aggman(df2),
                DataTable(df2,'Lista OS').Load(),ds_aggman.Chart_Prioridade(df2))

#Navios:
@main_app.callback([eOutput('ds-total-media', 'children'),eOutput('ds-diciplina','children'),eOutput('ds-navios','children'),
                    eOutput('ds-atraso-bkl','children'),eOutput('ds-atraso-agg','children'),
                    eOutput('ds-crit-pla','children'),eOutput('ds-crit-eqp','children'),eOutput('ds-tornou-se-aggman','children'),
                    eOutput('table-data-os','children'),eOutput('ds-crit-pri','children')],
                   eInput('chart-navios', 'clickData'),
                   prevent_initial_call=True
                   )
def render_content_Dash_Navios(click_data):
    global dash_atraso
    global dff

    if not click_data:
        dash_atraso=[ds_aggman.Chart_Atraso(dff),ds_aggman.Chart_Tempo_Aggman(dff)]
        return (ds_aggman.Card_Total_E_Media(dff),ds_aggman.Chart_Disciplina(dff),ds_aggman.Chart_Navios(dff),ds_aggman.Chart_Atraso(dff),
                ds_aggman.Chart_Tempo_Aggman(dff),
                ds_aggman.Chart_Criticidade_Plano(dff),ds_aggman.Chart_Criticidade_Equipamento(dff),ds_aggman.Chart_Mudado_2_Aggman(dff),
                DataTable(dff,'Lista OS').Load(),ds_aggman.Chart_Prioridade(dff))
    else:
        filtered=click_data['points'][0]['label']

        if dff['NAVIO'].nunique()==1:
            df2=df.copy(deep=True)
        else:
            df2=dff.loc[df['NAVIO']==filtered]  

            if df2 is None or df2.empty:
                dff=df.copy(deep=True)
                df2=dff.loc[df['NAVIO']==filtered]  

        dash_atraso=[ds_aggman.Chart_Atraso(df2),ds_aggman.Chart_Tempo_Aggman(df2)]
        dff=df2.copy(deep=True)
        
        return (ds_aggman.Card_Total_E_Media(df2),ds_aggman.Chart_Disciplina(df2),ds_aggman.Chart_Navios(df2),ds_aggman.Chart_Atraso(df2),
                ds_aggman.Chart_Tempo_Aggman(df2),
                ds_aggman.Chart_Criticidade_Plano(df2),ds_aggman.Chart_Criticidade_Equipamento(df2),ds_aggman.Chart_Mudado_2_Aggman(df2),
                DataTable(df2,'Lista OS').Load(),ds_aggman.Chart_Prioridade(df2))

#Disciplina:
@main_app.callback([eOutput('ds-total-media', 'children'),eOutput('ds-diciplina','children'),eOutput('ds-navios','children'),
                    eOutput('ds-atraso-bkl','children'),eOutput('ds-atraso-agg','children'),
                    eOutput('ds-crit-pla','children'),eOutput('ds-crit-eqp','children'),eOutput('ds-tornou-se-aggman','children'),
                    eOutput('table-data-os','children'),eOutput('ds-crit-pri','children')],
                   eInput('chart-disciplina', 'clickData'),
                   prevent_initial_call=True
                   )
def render_content_Dash_Navios(click_data):
    #global dash_atraso
    global dff

    if not click_data:
        #dash_atraso=[ds_aggman.Chart_Atraso(dff),ds_aggman.Chart_Tempo_Aggman(dff)]
        return (ds_aggman.Card_Total_E_Media(dff),ds_aggman.Chart_Disciplina(dff),ds_aggman.Chart_Navios(dff),ds_aggman.Chart_Atraso(dff),
                ds_aggman.Chart_Tempo_Aggman(dff),
                ds_aggman.Chart_Criticidade_Plano(dff),ds_aggman.Chart_Criticidade_Equipamento(dff),ds_aggman.Chart_Mudado_2_Aggman(dff),
                DataTable(dff,'Lista OS').Load(),ds_aggman.Chart_Prioridade(dff))
    else:
        filtered=click_data['points'][0]['label']

        if dff['DISCIPLINA'].nunique()==1:
            df2=df.copy(deep=True)
        else:
            df2=dff.loc[df['DISCIPLINA']==filtered]  

            if df2 is None or df2.empty:
                dff=df.copy(deep=True)
                df2=dff.loc[df['DISCIPLINA']==filtered]  

        #dash_atraso=[ds_aggman.Chart_Atraso(df2),ds_aggman.Chart_Tempo_Aggman(df2)]
        dff=df2.copy(deep=True)
        
        return (ds_aggman.Card_Total_E_Media(df2),ds_aggman.Chart_Disciplina(df2),ds_aggman.Chart_Navios(df2),ds_aggman.Chart_Atraso(df2),
                ds_aggman.Chart_Tempo_Aggman(df2),
                ds_aggman.Chart_Criticidade_Plano(df2),ds_aggman.Chart_Criticidade_Equipamento(df2),ds_aggman.Chart_Mudado_2_Aggman(df2),
                DataTable(df2,'Lista OS').Load(),ds_aggman.Chart_Prioridade(df2))

##############################################################################################################################################
#                                                   Indicador Disponibilidade                                                                      #
##############################################################################################################################################
#
#   Descrição: Callbacks do Indicador Disponibilidade
#
#

@main_app.callback([eOutput('ds-glob-avlb','children'),eOutput('ds-tot-eqp','children'),eOutput('ds-avlb-syst','children')],
                   eInput('dpShips', 'value'),
                   prevent_initial_call=True)
def render_button_criticidades(value):
    if type(value)=='str':
        ship=str(value).replace("LOGIN ","")[0:5]
    else:
        if len(value)>0:
            ship=str(value[0]).replace("LOGIN ","")[0:5]
        else:
            ship=None
    return (ds_disponibilidade.Chart_Global_Availability(ship=ship),ds_disponibilidade.Card_Total(ship=ship),
            ds_disponibilidade.Chart_System_Availability(ship=ship))


#Server:
@server.route('/A/')
def Big_Teste():
    return 'Teste'

# Main Class 
class GraficInterface():
    
    def __init__(self):
        self.external_scripts=None
        self.external_stylesheets=None    
        self.server=None
        

    def __set_layout__(self):      
        self.side_bar=SideBar(main_title,sub_title,web_pages_title).element
        self.content = html.Div(className='Container',children=[html.Div(id="page-content", children=[])])        
        main_app.layout = html.Div([MainLayout(self.side_bar,self.content).element],style={'background-color':"#120a29"}) 
        self.server=main_app.server 

    def Add(self,html_title,description,content):
        web_pages_content[html_title]=content
        web_pages_title[html_title]=description
        

    def __runner__(self):
        self.__set_layout__()             
        main_app.run_server()
     
    def Run(self):
        self.__runner__()

    

