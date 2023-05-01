
###############################################################################################################################################################
#
# M�dulo : Dashboards          Data de Cria��o: 01/12/2022
#
# Objetivo: M�dulo para cria��o dos dashboards
#
# Ultimas altera��es: Cria��o
#
# Data da ultima altera��o: 01/12/2022
#
# Desenvolvedor: Francisco J. E. de Sousa
#
# Contato: e-mail: francisco.sousa1993@outlook.com      tel: (21) 96965-6759
#
###############################################################################################################################################################

# Imports:


from ConstantsGui import *
from GuiFuncs import *
import math

height_ref=180
width_ref=200
title_font_size='12px'

#Dash_Manutencao_Atrasada
class Dash_Manutencao_Atrasada():
    def __init__(self):
        self.config=Read_Config()
        self.path=self.config["base_indicador"]["manutencao_atrasada"]
        self.df=pd.read_excel(self.path)
        self.Uniformizar_Df()
        self.Card_total_properties={'div':{'left':'1rem','top':'4rem','class':'three columns','width':'8rem'},'object':{'name':'Total'}}

    def Uniformizar_Df(self):
        df=self.df.copy(deep=True)
        conditions=[(df['TAGEQUIP'].str.contains('-PRO-MCP')>0),(df['TAGEQUIP'].str.contains('-GER-MA')>0),(df['TAGEQUIP'].str.contains('-GER-EME')>0),
            (df['TAGEQUIP'].str.contains('-GOV-BOW')>0),(df['TAGEQUIP'].str.contains('-ACP-CA')>0),(df['TAGEQUIP'].str.contains('-SOC-PUC-P')>0),
            (df['TAGEQUIP'].str.contains('-LUB-PM')>0),(df['TAGEQUIP'].str.contains('-SAS-AAS-B')>0),(df['TAGEQUIP'].str.contains('-SCI-SFA-B')>0),
            (df['TAGEQUIP'].str.contains('-LAS-BWTS')>0),(df['TAGEQUIP'].str.contains('-SSG-SEP')>0),
            (df['TAGEQUIP'].str.contains('-LUB-PUR-PM')>0),(df['TAGEQUIP'].str.contains('-SAS-DES-DES')>0)]
        df['GRUPO_EQUIP_CHOSEN'] = np.select(conditions,[True]*len(conditions))

        grupo_equip=['MCP','MCA','DGE','BOW','COMPRESSOR','PUROC','PUROL','BOMBA AS','BOMBA IE','BWTS','SEPARADOR AO','PUROL','DESTILADOR']

        df['GRUPO_EQUIP'] = np.select(conditions,grupo_equip)


        conditions=[(df['TEMPO VENCIDO']<=30),(df['TEMPO VENCIDO']>30) & (df['TEMPO VENCIDO']<=60),
                    (df['TEMPO VENCIDO']>60) & (df['TEMPO VENCIDO']<=90),(df['TEMPO VENCIDO']>90) &
                    (df['TEMPO VENCIDO']<=180),(df['TEMPO VENCIDO']>180) & (df['TEMPO VENCIDO']<=365),
                    (df['TEMPO VENCIDO']>365) & (df['TEMPO VENCIDO']<=730),(df['TEMPO VENCIDO']>730) &
                    (df['TEMPO VENCIDO']<=365*5),(df['TEMPO VENCIDO']>365*5)]

        tempos_atraso=['Mês','Bimestre','Trimestre','Semestre','Ano','Biênio','Quinquênio','Acima de 5anos']
        df['TEMPO_ATRASO'] = np.select(conditions,tempos_atraso)       

        df2=df.loc[(df['TIPO_PLANO']=='ACUMULATIVO') & (df['PERIODICIDADE']>=2000)| (df['TIPO_PLANO']=='PERIODICO') & (df['PERIODICIDADE']>=365)]
        self.df=df2.loc[df2['GRUPO_EQUIP']!=0]
        
    def Chart_NavioxAtraso(self,style={'margin-left':'1rem'}):
        pivot_table=pd.pivot_table(self.df,values='TAGPLANO',index='NAVIO',columns='PRAZO DO PLANO',aggfunc='count')
        df_pivot=pivot_table.reset_index()
        
        x=df_pivot['NAVIO'].values.tolist()
        y=df_pivot['VENCIDO'].values.tolist()
        max_x=max(y)
        max_x=round(1.2*max_x,0)
        
        chart_obj=Chart(y,x)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.chart_types=(CHART_TYPE.HORIZONTAL_BAR)
        chart_obj.title=None #'Manutenções em atraso por Navio'
        chart_obj.Create()
        chart_obj.Update_Layout(autosize=True,width=2*width_ref,height=height_ref)
        chart_obj.Update_XAxis(x_range=[0,max_x])
        chart_obj.Update_YAxis(y_range=None)
        return  html.Div([  html.Div(children=['Manutenções em atraso por Navio'],
                                     style={'margin-left':'0rem','color':'white','font-size':title_font_size,'white-space': 'nowrap'},
                                     className="sammy-nowrap-1"),
                            html.Br(),
                            chart_obj.content,
                         ],style=style,className='container')

    def Chart_CriticidadeEquipamento(self):
        pivot_table=pd.pivot_table(self.df,values='TAGPLANO',index='CRITICIDADE_EQUIPAMENTO',aggfunc='count')
        df_pivot=pivot_table.reset_index()

        x=df_pivot['CRITICIDADE_EQUIPAMENTO'].values.tolist()
        y=df_pivot['TAGPLANO'].values.tolist()

        chart_obj=Chart(x,y)
        chart_obj.chart_types=(CHART_TYPE.PIE)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None #'Criticidade dos equipamentos'        
        chart_obj.Create()
        chart_obj.Update_Trace(dict(colors=['#990000', '#999900', '#006600','#a3a3c2'],line=dict(color='#000000', width=2)))
        chart_obj.Update_Layout(False,height_ref*0.8,height_ref*0.8)
        return html.Div([
                        html.Div(['Criticidade dos equipamentos'],
                                 style={'margin-left':'0rem','color':'white','font-size':title_font_size,'white-space': 'nowrap'}),
                        html.Br(),
                        chart_obj.content],style={'margin-left':'0rem'},className='container div_table')


    def Chart_CriticidadePlano(self):
        pivot_table=pd.pivot_table(self.df,values='TAGPLANO',index='CRITICIDADE_PLANO',aggfunc='count')
        df_pivot=pivot_table.reset_index()

        x=df_pivot['CRITICIDADE_PLANO'].values.tolist()
        y=df_pivot['TAGPLANO'].values.tolist()
        y=[a if str(a) != '0' else 'Outros' for a in y]

        chart_obj=Chart(x,y)
        chart_obj.chart_types=(CHART_TYPE.PIE)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None #'Criticidade dos planos'        
        chart_obj.Create()
        chart_obj.Update_Trace(dict(colors=['#990000', '#999900', '#006600','#a3a3c2'],line=dict(color='#000000', width=2)))
        chart_obj.Update_Layout(False,height_ref*0.8,height_ref*0.8)
        return html.Div([
                        html.Div(['Criticidade dos planos'],
                                 style={'margin-left':'0rem','color':'white','font-size':title_font_size,'white-space': 'nowrap'}),
                        html.Br(),
                        chart_obj.content],style={'margin-left':'0rem'},className='container div_table')

    def Chart_GrupoEquipamento(self,style={'margin-left':'1rem'}):
        pivot_table=pd.pivot_table(self.df,values='TAGPLANO',index='GRUPO_EQUIP',aggfunc='count')
        df_pivot=pivot_table.reset_index()

        x=df_pivot['GRUPO_EQUIP'].values.tolist()
        y=df_pivot['TAGPLANO'].values.tolist()

        max_x=max(y)
        max_x=int(1.2*max_x)

        chart_obj=Chart(y,x)
        chart_obj.chart_types=(CHART_TYPE.HORIZONTAL_BAR)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None #'Grupo de Equipamentos'   
        chart_obj.Create()
        chart_obj.Update_Layout(autosize=False,width=width_ref*1.7,height=height_ref*1.7)
        chart_obj.Update_XAxis(x_range=[0,max_x])
        return  html.Div([  html.Div(children=['Grupo de Equipamentos'],
                                     style={'margin-left':'0rem','color':'white','font-size':title_font_size,'white-space': 'nowrap'},
                                     className="sammy-nowrap-1"),
                            html.Br(),
                            chart_obj.content,
                         ],style=style,className='container')

    def Chart_Disciplina(self):
        pivot_table=pd.pivot_table(self.df,values='TAGPLANO',index='DISCIPLINA',aggfunc='count')
        df_pivot=pivot_table.reset_index()

        x=df_pivot['DISCIPLINA'].values.tolist()
        y=df_pivot['TAGPLANO'].values.tolist()

        max_x=max(y)
        max_x=int(1.2*max_x)

        chart_obj=Chart(y,x)
        chart_obj.chart_types=(CHART_TYPE.HORIZONTAL_BAR)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None #'Disciplina'   
        chart_obj.Create()
        chart_obj.Update_Layout(autosize=True,width=width_ref*1.5,height=height_ref)
        chart_obj.Update_XAxis(automargin="height+width+left+top+right+bottom",x_range=[0,max_x])
        chart_obj.Update_YAxis(y_range=None)
        return html.Div([  html.Div(children=['Disciplina'],
                                     style={'margin-left':'0rem','color':'white','font-size':title_font_size,'white-space':'nowrap'},
                                     className="sammy-nowrap-1"),
                            html.Br(),
                            chart_obj.content,
                         ],style={'margin-left':'1rem'},className='container')


    def Card_Total(self):
        total=self.df['TAGPLANO'].count()
        card_obj=Card(self.Card_total_properties['object']['name']
                      ,value=total)
        return card_obj.content

    def Chart_PossuiOS(self,style={'margin-left':'1rem'}):
        
        total_OS=self.df['NUMOS'].dropna().count()
        total=self.df['TAGPLANO'].count()
        total_sem_OS=total-total_OS
        x=['Sim','Não','Total']
        y=[total_OS,total_sem_OS,total]

        max_y=round(y[2]*1.2)
        chart_obj=Chart(x,y)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None
        chart_obj.Create()
        chart_obj.Update_Layout(autosize=False,width=width_ref,height=height_ref)
        chart_obj.Update_YAxis(y_range=[0,max_y])
        return  html.Div([  html.Div(children=['Manuenções Possuem OS'],
                                     style={'margin-left':'0rem','color':'white','font-size':title_font_size,'white-space': 'nowrap'},
                                     className="sammy-nowrap-1"),
                            html.Br(),
                            chart_obj.content,
                         ],style=style,className='container')

    def Chart_Atraso(self):
        pivot_table=pd.pivot_table(self.df,values='TAGPLANO',index='TEMPO VENCIDO',aggfunc='count')
        df_pivot=pivot_table.reset_index()

        x=df_pivot['TEMPO VENCIDO'].values.tolist()
        y=df_pivot['TAGPLANO'].values.tolist()

        max_y=max(y)
        max_y=round(1.2*max_y)

        max_x=max(x)
        max_x=round(1.2*max_x)

        chart_obj=Chart(x,y)
        chart_obj.chart_types=(CHART_TYPE.HISTOGRAM)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None #'Disciplina'   
        chart_obj.Create()
        chart_obj.Update_Layout(autosize=True,width=width_ref*2.2,height=height_ref*1.5)
        chart_obj.Update_YAxis(automargin="height+width+left+top+right+bottom",y_range=None)
        chart_obj.Update_XAxis(x_range=None,tickmode='array')

        return html.Div([  html.Div(children=['Quantidade em atraso x tempo'],
                                     style={'margin-left':'0rem','color':'white','font-size':title_font_size,'white-space':'nowrap'},
                                     className="sammy-nowrap-1"),
                            html.Br(),
                            chart_obj.content,
                         ],style={'margin-left':'1rem'},className='container')
    
    def Table_Element(self):
        selected_df=self.df[['NAVIO','TAGPLANO','CRITICIDADE_PLANO','TAGEQUIP','DISCIPLINA']]
        table=dbc.Container([dash.dash_table.DataTable(data=selected_df.to_dict('records'),
                                                       columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in selected_df.columns],
                                                       editable=True
                                                       ), 
                             dbc.Alert(id='tbl_out')
                             ])

        return html.Div([  html.Div(children=['Tabela'],
                                     style={'margin-left':'0rem','color':'white','font-size':title_font_size,'white-space':'nowrap'},
                                     className="sammy-nowrap-1"),
                            html.Br(),
                            table,
                         ],style={'margin-left':'0rem'},className='container')


    def Create(self):
        
        ds=html.Div(className='container',style={'margin-left':'18rem'},children=[
               html.Div(className='row',children=[
                   html.Div(className=self.Card_total_properties['div']['class'], children=[self.Card_Total()],
                            style={'width':self.Card_total_properties['div']['width'],'margin-left':self.Card_total_properties['div']['left'],
                                   'margin-top':self.Card_total_properties['div']['top']}),
                   html.Div(className='three columns', children=[self.Chart_NavioxAtraso()],style={'margin-left':'0rem'}),
                   html.Div(className='two columns', children=[self.Chart_Disciplina()],style={'margin-left':'20rem'}),
                   html.Div(className='two columns', children=[self.Chart_PossuiOS()],style={'margin-left':'18rem'})
                        
               ],style={'width':'100rem'}),
               html.Br(),
               html.Div(className='row',children=[
                   html.Div(className='three columns', children=[self.Chart_GrupoEquipamento()]),
                   html.Div(className='three columns',children=[
                            html.Div([
                                    self.Chart_CriticidadeEquipamento(),
                                    html.Br(),
                                    self.Chart_CriticidadePlano()
                                ],style={'margin-left':'12rem'})
                       ]),
                   html.Div(className='two columns',children=[self.Chart_Atraso()],style={'margin-left':'7rem'})
               ]),
               html.Br(),
               html.Div(className='table',children=[DataTable(self.df,'Total').Load()],style={'margin-left':'0rem'})
           ])
        
        return [ds]

#Dash_Aggman
class Dash_Aggman():
    #Initial
    def __init__(self):
        self.config=Read_Config()
        self.path=self.config["base_indicador"]["aggman"]
        self.df0=pd.read_excel(self.path)
        #self.df=self.df0.loc[pd.to_numeric(self.df0['PERIODO EM BACKLOG'])>=1]
        self.df=self.df0.loc[self.df0['TEMPO EM BACKLOG']!='CARTEIRA']
        self.main_columns=['NUMERO OS','NAVIO','DESCRIÇÃO DA OS']
    #Create Chart
    def __Create_Chart__(self,valores,index,aggfunc='count',columns=None,chart_types=(CHART_TYPE.HORIZONTAL_BAR),width=400,height=180,
                     horizontal=False,y_label='',x_label='',id_obj='',pivot_table_data=None,df=None):

        if df is None:
            df=self.df.copy(deep=True)

        if pivot_table_data is None:
            pivot_table=pd.pivot_table(df,values=valores,index=index,aggfunc=aggfunc,columns=columns)
            df_pivot=pivot_table.reset_index()
        else:
            df_pivot=pivot_table_data.copy(deep=True)

        x=df_pivot[index].values.tolist()
        y=df_pivot[valores].values.tolist()

        max_x=max(x)
        max_y=max(y)
        min_x=min(x)
        min_y=min(y)

        if horizontal:
            chart_obj=Chart(y,x,id_obj=id_obj)
        else:
            chart_obj=Chart(x,y,id_obj=id_obj)

        chart_obj.chart_types=chart_types
        chart_obj.y_label=y_label
        chart_obj.x_label=x_label
        chart_obj.title=None
        chart_obj.Create()
        chart_obj.Update_Layout(autosize=True,width=width,height=height)
        return chart_obj,[min_x,max_x,min_y,max_y]
    #Create Dash
    def __Create_Dash__(self,title=None,chart_obj=[],style_title=None,title_class=None,div_style=None,div_class=None,other_obj=[]):
        if title==None:
            title='Titulo'    
            
        if style_title==None:
            style_title={'margin-left':'0rem','color':'white','font-size':title_font_size,'white-space':'nowrap'}

        if title_class==None:
            title_class="sammy-nowrap-1"

        if div_style==None:
            div_style={'margin-left':'1rem'}

        if div_class==None:
            div_class='container'

        return html.Div([
                            html.Div(children=[title],style=style_title,className=title_class),
                            html.Br(),
                            chart_obj.content,

                            other_obj
                        ],style=div_style,className=div_class)
    #Chart Disciplina
    def Chart_Disciplina(self,df=None):       
        
        if df is None:
            dff=self.df.copy(deep=True)
        else:
            dff=df.copy(deep=True)

        chart_obj,limites=self.__Create_Chart__(valores='NUMERO OS',index='DISCIPLINA',horizontal=True,width=320,id_obj='chart-disciplina',df=dff)
        x_range=[0,int(limites[3])+2]

        chart_obj.Update_XAxis(automargin="height+width+left+top+right+bottom",x_range=x_range)
        chart_obj.Update_YAxis(y_range=None)

        return self.__Create_Dash__('Disciplinas',chart_obj)

    #Chart Navios
    def Chart_Navios(self,df=None):
        chart_obj,limites=self.__Create_Chart__(valores='NUMERO OS',index='NAVIO',horizontal=True,width=320,id_obj='chart-navios',df=df)
        x_range=[0,int(limites[3]+2)]
        
        chart_obj.Update_XAxis(automargin="height+width+left+top+right+bottom",x_range=x_range)
        chart_obj.Update_YAxis(y_range=None)

        return self.__Create_Dash__('Navios',chart_obj)
    #Card Total e Media
    def Card_Total_E_Media(self,dff=None):

        if dff is None:
            data_frame=self.df.copy(deep=True)
        else:
            data_frame=dff.copy(deep=True)

        total=data_frame['NUMERO OS'].count()
        card_total=Card('Total',value=total,title_style={'color':'#ffffff','font-size':'1rem'},id_element='card-total')


        pivot_table=pd.pivot_table(data_frame,values='NUMERO OS',index='NAVIO',aggfunc='count')
        df_pivot=pivot_table.reset_index()
        media=round(df_pivot['NUMERO OS'].mean(),1)

        card_media=Card('Media Navio',value=media,title_style={'color':'#ffffff','font-size':'1rem'},id_element='card-media')

        return html.Div(className='row',children=[
                            html.Div(className='two columns',id='ds-card-total',style={'width':'10rem','margin-left':'0rem'},children=[card_total.content]),
                            html.Br(),
                            html.Div(className='two columns',id='ds-card-media',style={'width':'10rem','margin-left':'0rem','margin-top':'1rem'},children=[card_media.content])
                        ])
    #Chart Atraso
    def Chart_Atraso(self,df=None):

        if df is None:
            df_atraso=self.df.copy(deep=True)
        else:
            df_atraso=df.copy(deep=True)

        #Distribuição de frequencias - Fórmula de Fórmula de Sturges : K=1+3.332*ln(N) -> k=N° Grupos e N=N° total de elementos
        N=df_atraso['NUMERO OS'].count()
        if N<1:
            x=[0]
            y=[0]
        else:
            k=1+3.332*math.log10(N)
            k=int(round(k,0))

            #df_atraso=df.copy(deep=True) 
            if N>1:
                lower, higher = df_atraso['PERIODO EM BACKLOG'].min(), df_atraso['PERIODO EM BACKLOG'].max()
                edges=range(int(lower),int(higher),int(round((higher-lower)/k,0)))
                lbs=[str(i+1) +str('-') + '(%d, %d]'%(edges[i], edges[i+1]) for i in range(len(edges)-1)]   
            else:
                lbs=[df_atraso['PERIODO EM BACKLOG'].min()]

            df_atraso['BACKLOG TIME']=pd.cut(df_atraso["PERIODO EM BACKLOG"],len(lbs),labels=lbs,precision=0, include_lowest=True).astype(str)       
            df_atraso=df_atraso.groupby('BACKLOG TIME')['NUMERO OS'].count()
            df_atraso.reset_index()

            x=df_atraso.index.to_list()
            y=df_atraso.to_list()

        max_y=int(round(max(y)+3,0))

        chart_obj=Chart(x=x,y=y)
        chart_obj.y_label='N° OS em atraso'
        chart_obj.x_label='Periodo (dias)'
        chart_obj.title=None
        chart_obj.Create()
        chart_obj.Update_Layout(autosize=True,width=400,height=190)

        chart_obj.Update_XAxis(automargin="height+width+left+top+right+bottom",x_range=None,categoryorder=None)
        chart_obj.Update_YAxis(y_range=[0,max_y],categoryorder=None)        
        return self.__Create_Dash__('Quantidade de OS x Periodo em backlog',chart_obj)

    #Chart Tempo AGGMAN
    def Chart_Tempo_Aggman(self,dff=None):
        if dff is None:
            df=self.df.copy(deep=True)
        else:
            df=dff.copy(deep=True)

        #Distribuição de frequencias - Fórmula de Fórmula de Sturges : K=1+3.332*ln(N) -> k=N° Grupos e N=N° total de elementos
        N=df['NUMERO OS'].count()
        if N<1:
            x=[0]
            y=[0]
        else:
            k=1+3.332*math.log10(N)
            k=int(round(k,0))

            df_atraso=df.copy(deep=True) 
            if N>1:
                lower, higher = df_atraso['TEMPO_AGGMAN'].min(), df_atraso['TEMPO_AGGMAN'].max()
                edges=range(int(lower),int(higher),int((higher-lower)/k))
                lbs=[str(i+1) +str('-') + '(%d, %d]'%(edges[i], edges[i+1]) for i in range(len(edges)-1)]  
            else:
                lbs=[df_atraso['TEMPO_AGGMAN'].min()]

            df_atraso['TEMPO_AGGMAN']=pd.cut(df_atraso["TEMPO_AGGMAN"],len(lbs),labels=lbs,precision=0, include_lowest=True).astype(str)       
            df_atraso=df_atraso.groupby('TEMPO_AGGMAN')['NUMERO OS'].count()
            df_atraso.reset_index()

            x=df_atraso.index.to_list()
            y=df_atraso.to_list()

        max_y=int(round(max(y)+3,0))

        chart_obj=Chart(x=x,y=y)
        chart_obj.y_label='N° OS em atraso'
        chart_obj.x_label='Tempo em AGGMAN (Dias)'
        chart_obj.title=None
        chart_obj.Create()
        chart_obj.Update_Layout(autosize=True,width=400,height=190)

        chart_obj.Update_XAxis(automargin="height+width+left+top+right+bottom",x_range=None,categoryorder=None)
        chart_obj.Update_YAxis(y_range=[0,max_y],categoryorder=None)        
        return self.__Create_Dash__('Quantidade de OS x Tempo em AGGMAN',chart_obj)

    #Chart Percentual em AGGMAN
    def Chart_Percent(self, df=None):
        
        if df is None:
            df0=self.df0.copy(deep=True)
        else:
            df0=df.copy(deep=True)

        df0['AUX']=np.where(df0['TEMPO EM BACKLOG']!='CARTEIRA','BACKLOG','CARTEIRA')
        pivot_table=pd.pivot_table(df0,values='NUMERO OS',index='AUX',aggfunc='count').reset_index()
        
        x=pivot_table['AUX'].values.tolist()
        y=pivot_table['NUMERO OS'].values.tolist()
        
        chart_obj=Chart(x,y)
        chart_obj.chart_types=(CHART_TYPE.PIE)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None #'Criticidade dos planos'        
        chart_obj.Create()
        chart_obj.Update_Layout(False,170,170)

        return self.__Create_Dash__('Percentual de AGGMAN em atraso',chart_obj)
    #Chart Criticidade Equipamento:
    def Chart_Criticidade_Equipamento(self,dff=None):

        if dff is None:
            df=self.df.copy(deep=True)
        else:
            df=dff.copy(deep=True)
        
        #pivot_table=pd.pivot_table(df,values='NUMERO OS',index='CRITICIDADE_EQUIPAMENTO',aggfunc='count').reset_index()
        
        A=df['CRITICIDADE_EQUIPAMENTO'].loc[df['CRITICIDADE_EQUIPAMENTO']=='A'].count()
        B=df['CRITICIDADE_EQUIPAMENTO'].loc[df['CRITICIDADE_EQUIPAMENTO']=='B'].count()
        C=df['CRITICIDADE_EQUIPAMENTO'].loc[df['CRITICIDADE_EQUIPAMENTO']=='C'].count()
        N=df['CRITICIDADE_EQUIPAMENTO'].loc[df['CRITICIDADE_EQUIPAMENTO']=='N'].count()

        #x=pivot_table['CRITICIDADE_EQUIPAMENTO'].values.tolist()
        #y=pivot_table['NUMERO OS'].values.tolist()

        x=['A','B','C','N']
        y=[A,B,C,N]

        chart_obj=Chart(x,y,id_obj='chart-criticidade-equipamento')
        chart_obj.chart_types=(CHART_TYPE.PIE)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None       
        chart_obj.Create()
        chart_obj.Update_Trace(dict(colors=['#990000', '#999900', '#006600','#a3a3c2'],line=dict(color='#000000', width=2)))
        chart_obj.Update_Layout(False,190,170)

        return self.__Create_Dash__('Criticidade Equipamentos',chart_obj)

    #Chart Prioridade
    def Chart_Prioridade(self,df=None):
        
        if df is None:
            dff=self.df.copy(deep=True)
        else:
            dff=df.copy(deep=True)

        #pivot_table=pd.pivot_table(dff,values='NUMERO OS',index='PRIORIDADE',aggfunc='count').reset_index()        
        #x=pivot_table['PRIORIDADE'].values.tolist()
        #y=pivot_table['NUMERO OS'].values.tolist()

        p1=dff['PRIORIDADE'].loc[dff['PRIORIDADE']==1].count()
        p2=dff['PRIORIDADE'].loc[dff['PRIORIDADE']==2].count()
        p3=dff['PRIORIDADE'].loc[dff['PRIORIDADE']==3].count()
        #N=dff['PRIORIDADE'].count() - p1 - p2 - p3

        x=[1,2,3]
        y=[p1,p2,p3]
        
        chart_obj=Chart(x,y,id_obj='chart-prioridade')
        chart_obj.chart_types=(CHART_TYPE.PIE)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None        
        chart_obj.Create()
        chart_obj.Update_Trace(dict(colors=['#990000', '#999900', '#006600','#a3a3c2'],line=dict(color='#000000', width=2)))
        chart_obj.Update_Layout(False,190,180)
        '''
        buttons=[dbc.Button(str(i), id='prop-prioridade-'+str(i),className='three columns',
                            style={'width':'40px','height':'20px','padding':'5px 5px','margin-top':'1rem','color':'white','background-color':'#161023','border-color':'#7575a3'}) for i in x]
        '''
        element= self.__Create_Dash__('Prioridade da OS',chart_obj)

        return element

    #Chart Criticidade Plano
    def Chart_Criticidade_Plano(self,df_plano=None,selected_colors=None):
        
        if df_plano is None:
            df_plano=self.df.copy(deep=True)

        #pivot_table=pd.pivot_table(df_plano,values='NUMERO OS',index='CRITICIDADE_PLANO',aggfunc='count').reset_index()
        
        A=df_plano['CRITICIDADE_PLANO'].loc[df_plano['CRITICIDADE_PLANO']=='A'].count()
        B=df_plano['CRITICIDADE_PLANO'].loc[df_plano['CRITICIDADE_PLANO']=='B'].count()
        C=df_plano['CRITICIDADE_PLANO'].loc[df_plano['CRITICIDADE_PLANO']=='C'].count()
        NA=df_plano['NUMERO OS'].count() - A - B - C

        #x=pivot_table['CRITICIDADE_PLANO'].values.tolist()
        #y=pivot_table['NUMERO OS'].values.tolist()

        x=['A','B','C','N']
        y=[A,B,C,NA]
        
        chart_obj=Chart(x,y,id_obj='chart-criticidade-plano')
        chart_obj.chart_types=(CHART_TYPE.PIE)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None     
        chart_obj.Create()
        if selected_colors==None:
            colors=['#990000', '#999900', '#006600','#a3a3c2']
        else:
            colors=selected_colors

        chart_obj.Update_Trace(dict(colors=colors,line=dict(color='#000000', width=2)))
        chart_obj.Update_Layout(False,190,170)

        return self.__Create_Dash__('Criticidade Plano',chart_obj)
    #Tabs Atraso
    def Tabs_Atrasos(self):
        return Tabs('tabs-atraso-id','tab-atraso',['Backlog','Tempo']).Load()
    #Tabs Criticidade
    def Tabs_Criticidade(self):
        return Tabs('tabs-criticidade-id','tab-criticidade',['1','2','3']).Load()
    #Tabs Comparação
    def Tabs_Comparacao(self):
        return Tabs('tabs-comp-id','tab-comp',['1','2']).Load()
    #Chart AGGMAN x Demais Status
    def Chart_AggmanxDemaisSatatus(self):
        path=self.config['base_indicador']['relatorio_os']
        df=pd.read_excel(path)
        df1=df.loc[(df['Backlog']=='S') & (df['Situação']=='A')]

        pivot_table=pd.pivot_table(df1,values='NUMOS',index='Status',aggfunc='count').reset_index()

        total=pivot_table['NUMOS'].sum()
        aggman=pivot_table.loc[pivot_table['Status']=='AGGMAN','NUMOS'].sum()
        demais_status=total-aggman
        
        x=['AGGMAN','DEMAIS STATUS']
        y=[aggman,demais_status]

        chart_obj=Chart(x,y)
        chart_obj.chart_types=(CHART_TYPE.PIE)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None #'Criticidade dos planos'        
        chart_obj.Create()
        chart_obj.Update_Layout(False,170,170)

        return  self.__Create_Dash__('AGGMAN x Demais Status',chart_obj)
    #Char Mudança p/ AGGMAN
    def Chart_Mudado_2_Aggman(self,df=None):

        if df is None:
            df_atraso=self.df.copy(deep=True) 
        else:
            df_atraso=df.copy(deep=True) 

        
        df_atraso['DATA_MUDA_AG']=pd.to_datetime(df_atraso['DATA ENTROU EM AGGMAN'])
        df_atraso['DIA_AG']=df_atraso[ "DATA_MUDA_AG"].dt.day

        pivot_table=pd.pivot_table(data=df_atraso,values='NUMERO OS',index='DIA_AG',aggfunc='count').reset_index()

        x=pivot_table['DIA_AG'].to_list()
        y=pivot_table['NUMERO OS'].to_list()

        max_y=int(round(max(y)+2,0))
        max_x=int(round(max(x)*1.2,0))

        chart_obj=Chart(x=x,y=y)
        chart_obj.chart_types=(CHART_TYPE.SCATTER)
        chart_obj.y_label='N° OS em atraso'
        chart_obj.x_label='Dia entrou AGGMAN'
        chart_obj.title=None
        chart_obj.Create()
        chart_obj.Update_Layout(autosize=True,width=400,height=200)

        chart_obj.Update_XAxis(automargin="height+width+left+top+right+bottom",x_range=[0,max_x],categoryorder=None)
        chart_obj.Update_YAxis(y_range=[0,max_y],categoryorder=None)
        
        return self.__Create_Dash__('Mudança da OS para o Status AGGMAN',chart_obj)

    #Create 
    def Create(self):
        buttons_style={'background-color':'#161023','color':'white','width':'60px','height':'30px','margin-left':'3px','border':'1px solid #000066'}
 
        ds=html.Div(className='container',style={'margin-left':'20rem'},children=[
               html.Div(className='row',children=[
                   html.Div(className='two columns',id='ds-total-media',children=[self.Card_Total_E_Media()],style={'margin-left':'1rem','margin-top':'3rem'}),
                   html.Div(className='three columns',id='ds-diciplina', children=[self.Chart_Disciplina()],style={'margin-left':'-4rem'}),
                   html.Div(className='two columns',id='ds-navios',children=[self.Chart_Navios()],style={'margin-left':'11rem'}),
                   html.Div(className='two columns',id='ds-comparacao',children=[self.Tabs_Comparacao()],style={'margin-left':'23rem'})
                   
               ],style={'width':'100rem'}),
               html.Br(),
               html.Div(className='row',children=[
                        #html.Div(className='two columns',id='ds-atraso',children=[self.Tabs_Atrasos()],style={'margin-left':'-1rem'}),
                        My_Tab([self.Chart_Atraso(),self.Chart_Tempo_Aggman()],
                               'bt-atraso',['ds-atraso-bkl','ds-atraso-agg'],'6rem').Load(),
                        My_Tab([self.Chart_Criticidade_Plano(),self.Chart_Criticidade_Equipamento(),self.Chart_Prioridade()],
                               'bt-criticidade',['ds-crit-pla','ds-crit-eqp','ds-crit-pri'],'33rem').Load(),
                        html.Div(className='two columns',id='ds-tornou-se-aggman',children=[self.Chart_Mudado_2_Aggman()],style={'margin-left':'16rem','margin-top':'2rem'}),     
                   ]),
               html.Br(),
               html.Div(className='table',id='table-data-os',children=[DataTable(self.df,'Lista OS').Load()],style={'margin-left':'0rem'})
               
           ])        
        return [ds]

#Dash_Disponibilidade
class Dash_Disponibilidade:
    #initial
    def __init__(self):
        self.config=Read_Config()
        self.keys=list(self.config["base_indicador"]["disponibilidade"].keys())
        self.dfs={}        
        self.__get_keys__()

    #Get Keys:
    def __get_keys__(self):
        for key in self.keys:
            path=self.config["base_indicador"]["disponibilidade"][key]
            if len(os.listdir(path))<1:
                self.dfs[key]=pd.DataFrame()
            else:
                for arquivo in os.listdir(path):
                    if str(arquivo).find('.xls'):
                       fullpath=path + "\\" + arquivo
                       try:
                            df=pd.read_excel(fullpath,sheet_name='BASE')
                            self.dfs[key]=df.copy(deep=True)
                            break
                       except Exception as err:
                           print(err)

    #Create Dash
    def __Create_Dash__(self,title=None,chart_obj=[],style_title=None,title_class=None,div_style=None,div_class=None,other_obj=[]):
        if title==None:
            title='Titulo'    
            
        if style_title==None:
            style_title={'margin-left':'0rem','color':'white','font-size':title_font_size,'white-space':'nowrap'}

        if title_class==None:
            title_class="sammy-nowrap-1"

        if div_style==None:
            div_style={'margin-left':'1rem'}

        if div_class==None:
            div_class='container'

        return html.Div([
                            html.Div(children=[title],style=style_title,className=title_class),
                            html.Br(),
                            chart_obj.content,
                            other_obj
                        ],style=div_style,className=div_class)

    #Filter Box
    def Create_Filterbox(self):
        style={'width':'25rem','background-color':''}
        return dcc.Dropdown(list(map(str.upper, self.keys)),multi=True,style=style,id='dpShips') 

    #Total
    def Card_Total(self,ship=None):
        if ship==None:
            total=0
        else:
            total=0
            for dff,key in zip(self.dfs.values(),self.dfs.keys()): 
                if not dff.empty:   
                    if key.find(ship)>=0:

                        year_ref=datetime.now().year
                        month_ref=datetime.now().month

                        df=dff.copy(deep=True)
                        df=df.loc[(df['MES'].notna()) & (df['ANO'].notna())]   
                        df=df.loc[df['NAVIO'].str.contains(ship)]
                        df=df.loc[df['ANO']==float(year_ref)]
                        df=df.loc[df['MES'].astype('int')==month_ref]
                        df=df.loc[df['DIA'].astype('int')==1]

                        total = int(df['NAVIO'].count())

        return Card('Total equipamentos',value=total,title_style={'color':'#ffffff','font-size':'1rem'},id_element='card-total',
                    value_style={'color':'#ffffff','font-size':'3rem','margin-left':'2rem'},card_style={'border-color':'#808080','margin-top':'2rem','width':'20rem'}).content

    #Percentual Disponibilidade:
    def Disp_Percent(self,ship=None):
        if ship==None:
            disp=0
        else:
            disp=0
            for dff,key in zip(self.dfs.values(),self.dfs.keys()): 
                if not dff.empty:   
                    if key.find(ship)>=0:

                        year_ref=datetime.now().year
                        month_ref=datetime.now().month

                        df=dff.copy(deep=True)
                        df=df.loc[(df['MES'].notna()) & (df['ANO'].notna())]   
                        df=df.loc[df['NAVIO'].str.contains(ship)]
                        df=df.loc[df['ANO']==float(year_ref)]
                        df=df.loc[df['MES'].astype('int')==month_ref]
                        df=df.loc[df['DIA'].astype('int')==1]

                        disp=int(df[df['CODSITUACAO']==0]['NAVIO'].count())
                        total = int(df['NAVIO'].count())
                        disp=str(round(float(disp/total),0)) + "%"

        return Card('Percentual de disponibilidade',value=disp,title_style={'color':'#ffffff','font-size':'1rem'},id_element='ds-disp-perc',
                    value_style={'color':'#ffffff','font-size':'3rem','margin-left':'2rem'},card_style={'border-color':'#808080','margin-top':'2rem'}).content

    #Global Availability
    def Chart_Global_Availability(self,year=None,month=None,ship=None,selected_colors=None):
        if year==None:
            year_ref=datetime.now().year
        else:
            year_ref=year

        if month==None:
            month_ref=datetime.now().month
        else:
            month_ref=month
        
        x=['A','B','C','N']

        if ship==None:
            y=[0,0,0,0]            
        else:
            y=[0,0,0,0]  
            for dff,key in zip(self.dfs.values(),self.dfs.keys()):
 
                if not dff.empty:   
                    if key.find(ship)>=0:
                        df=dff.copy(deep=True)
                        df=df.loc[(df['MES'].notna()) & (df['ANO'].notna())]   
                        df=df.loc[df['NAVIO'].str.contains(ship)]
                        df['ANO']=pd.to_numeric(df['ANO'])
                        df['MES']=pd.to_numeric(df['MES'])
                        df=df.loc[df['ANO']==float(year_ref)]
                        df=df.loc[df['MES'].astype('int')==month_ref]
                        df['CRITICIDADE']=df['CRITICIDADE'].fillna('N')

                        A=int(df.loc[(df['CODSITUACAO'].astype('int')!=0) & (df['CRITICIDADE']=='A')]['CODSITUACAO'].count())
                        B=int(df.loc[(df['CODSITUACAO'].astype('int')!=0) & (df['CRITICIDADE']=='B')]['CODSITUACAO'].count())
                        C=int(df.loc[(df['CODSITUACAO'].astype('int')!=0) & (df['CRITICIDADE']=='C')]['CODSITUACAO'].count())
                        N=int(df.loc[(df['CODSITUACAO'].astype('int')!=0) & (df['CRITICIDADE']=='N')]['CODSITUACAO'].count())
                        y=[A,B,C,N]
                        break

        chart_obj=Chart(x,y,id_obj='ds-cht-disp-glob')
        chart_obj.chart_types=(CHART_TYPE.PIE)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None     
        chart_obj.Create()
        if selected_colors==None:
            colors=['#990000', '#999900', '#006600','#a3a3c2']
        else:
            colors=selected_colors

        chart_obj.Update_Trace(dict(colors=colors,line=dict(color='#000000', width=2)))
        chart_obj.Update_Layout(False,190,170)

        return self.__Create_Dash__('Indisponibilidade Global',chart_obj)

    #System Availability
    def Chart_System_Availability(self,year=None,month=None,ship=None):
        if year==None:
            year_ref=datetime.now().year
        else:
            year_ref=year

        if month==None:
            month_ref=datetime.now().month
        else:
            month_ref=month
        
        y=[2,3,4,5,6]   
        x=[1,2,3,4,5]

        if ship!=None:            
            for dff,key in zip(self.dfs.values(),self.dfs.keys()): 
                if not dff.empty:   
                    if key.find(ship)>=0:
                        df=dff.copy(deep=True)
                        df=df.loc[(df['MES'].notna()) & (df['ANO'].notna())]   
                        df=df.loc[df['NAVIO'].str.contains(ship)]
                        df['ANO']=pd.to_numeric(df['ANO'])
                        df['MES']=pd.to_numeric(df['MES'])
                        df=df.loc[df['ANO']==float(year_ref)]
                        df=df.loc[df['MES'].astype('int')==month_ref]
                        x=list(df['SISTEMA'].unique())
                        y=[]
                        for item_key in x:
                            val=df[df['SISTEMA']==item_key]['SISTEMA'].count() - df[(df['SISTEMA']==item_key) & (df['CODSITUACAO']!=0)]['SISTEMA'].count()
                            val=100*round(val/df[df['SISTEMA']==item_key]['SISTEMA'].count(),0)
                            y.append(val)
                        break

        max_x=max(y)
        max_x=round(1.2*max_x,0)

        chart_obj=Chart(y,x,id_obj='ds-system')
        chart_obj.chart_types=(CHART_TYPE.HORIZONTAL_BAR)
        chart_obj.y_label=''
        chart_obj.x_label=''
        chart_obj.title=None     
        chart_obj.Create()
        chart_obj.Update_Layout(autosize=True,width=3*width_ref,height=4*height_ref)
        chart_obj.Update_XAxis(x_range=[0,max_x])
        chart_obj.Update_YAxis(y_range=None)

        return self.__Create_Dash__('Sistemas',chart_obj)

    #Filter Box:
    def Create_Filter(self,ships=None,year=None,month=None):
                               
        criticidades=['A','B','C','N']
        navios=list(self.dfs.keys())

        return html.Div(children=[
                dcc.Checklist(options=criticidades,value=criticidades[0],style={'background-color':'#362759','color':'white'}),
                html.Br(),
                dcc.Checklist(options=navios,value=navios[0],style={'background-color':'#362759','color':'white'}),
                html.Br(),
        ])

    #Create
    def Create(self):
        ds=html.Div(className='container',style={'margin-left':'20rem'},children=[
               html.Div(className='row',children=[
                   html.Div(className='two columns',id='ds-filterbox-ship',children=[
                            html.Div(children=[self.Create_Filterbox()],id='ds-filter-ship'),
                            html.Div(className='two columns',children=[self.Card_Total()],id='ds-tot-eqp'),
                   ], style={'margin-left':'2rem','margin-top':'3rem'}),  
                   html.Div(className='two columns',id='ds-filter-geral',children=[self.Create_Filter()],style={'margin-left':'40rem'}),
               ],style={'width':'100rem'}),
               html.Div(className='row',children=[
                   html.Div(className='two columns',id='ds-glob-avlb',children=[self.Chart_Global_Availability()],
                            style={'margin-left':'1rem','margin-top':'2rem'}),
               ]),
               html.Div(className='row',children=[
                   html.Div(className='two columns scroll',id='ds-avlb-syst',children=[self.Chart_System_Availability()],
                            style={'margin-left':'1rem','margin-top':'2rem','width':'45rem','height':'30rem'}),
               ]),
           ])        
        return [ds]



                   


        













class Dash_Custos():
    def __init__(self):
        self.tendencia=mtx.CalcTrendPolinomial()
        self.ships=['LOG-IN JATOBA','LOG-IN JACARANDA','LOG-IN PANTANAL','LOG-IN POLARIS','LOG-IN RESILIENTE','LOG-IN ENDURANCE']

    def Custo_Total(self):        
        self.custo_kpi=Indicador_Custos()        
        self.custo_kpi.Get_Month()
        self.x_months=self.custo_kpi.meses
        self.custo_total_orcado=[round(v/1000,2) for v in self.custo_kpi.orcado]
        self.custo_total_real=[round(v/1000,2) for v in self.custo_kpi.real]

        self.cuto_total_real_sum=round(reduce(lambda v1,v2:v1+v2,self.custo_total_real),2)
        self.cuto_total_real_avg=round(self.cuto_total_real_sum/9,2)
        self.custo_total_real_trend=self.tendencia.CalcTrendYVector(x=self.x_months,y=self.custo_total_real[0:10],number_of_newElements=3,degree=2)
        self.ctrt=self.tendencia.CalcTrendFunction(x=self.x_months,y=self.custo_total_real[0:10],number_of_elements=12,degree=28)

        ds_Custos=Dashboard(x=self.x_months,y=[self.custo_total_real,self.custo_total_orcado],series_names=['real','orcado'],y_trend=self.ctrt,
                    labels={'title':'Custo Total','x':'Mes','y':'Custo R$ (MM)'})

        fig_Custos=ds_Custos.Create()

        dropdown_element=Dropdown(self.ships,id_element='dpShips').content
        card_ct=Card('Custo total',value=str(self.cuto_total_real_sum) + ' MM').content
        card_cm=Card('Custo M�dio',value=str(self.cuto_total_real_avg)+ " MM").content
        cards_c=Cards([card_ct,card_cm]).content

        panel_custos=Panel([dropdown_element,[],cards_c,fig_Custos],(2,2))
        panel_custos.style['margin-left']='18rem'
        panel_custos.Load()

        return panel_custos

class Dash_Horimetros():
    def __init__(self):
        self.tendencia=mtx.CalcTrendPolinomial()
        self.ships=['LOG-IN JATOBA','LOG-IN JACARANDA','LOG-IN PANTANAL','LOG-IN POLARIS','LOG-IN RESILIENTE','LOG-IN ENDURANCE']

    def Get(self):
        self.kpi_horimetro=Indicador_Horimetros().Get()
        


def Load_Gui(chart_objects=[],incremental_tag='', objects_per_column=1):
    total_charts=len(chart_objects)
    n_rows=ceil(total_charts/objects_per_column)
    trs=[]
    k=0

    for i in range(n_rows):
        children=[]
        for j in range(objects_per_column):
            if k<total_charts:
                td=html.Td(id=incremental_tag +'-cell-'+str(i+1)+str(j+1),children=[dcc.Graph(figure=chart_objects[k])])
                children.append(td)
            else:
                break
            k+=1
        tr=html.Tr(id=incremental_tag +'-tr-'+ str(i),children=children)
        trs.append(tr)


    return [html.Div(children=[html.Table(id=incremental_tag + '-tbl',children=[
                html.Tbody(id=incremental_tag +'-tbody',children=trs)
                ])
            ],className="container",
                style={"background-color":"#2a1c4a","margin-top":"1rem","margin-left": "18rem","margin-right": "1rem"})
            ]


