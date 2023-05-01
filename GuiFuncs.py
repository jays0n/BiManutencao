
from datetime import datetime
from email import header
from tkinter.ttk import Style
from xmlrpc.client import DateTime
from ConstantsGui import *

#Sidebar
class SideBar():
    def __init__(self,title=None,description=None, resume_items={},style_sidebar=SIDEBAR_STYLE,style_links=SIDEBAR_LINKS_STYLE, sidebar_is_vertical=True):
        self.title=title
        self.description=description
        self.resume_items=resume_items
        self.style_sidebar=style_sidebar
        self.style_links=style_links
        self.sidebar_is_vertical=sidebar_is_vertical
        self.__html_structure__()
    
    def __html_structure__(self):
        self.element=html.Div([
                                html.H2(self.title, className="display-4 text-light", style={"font-size":"2.6rem"}),
                                html.Hr(),
                                html.P(self.description, className="lead text-light"),
                                html.Hr(),
                                dbc.Nav(
                                        [dbc.NavLink(value, href='/' + str(key), active="exact",style=self.style_links) 
                                                     for value,key in zip(self.resume_items.values(),self.resume_items.keys())
                                         ],
                                        vertical=self.sidebar_is_vertical,
                                        pills=True
                                )
                               ],
                               style=self.style_sidebar
                    )

#Main Layout
class MainLayout():
    def __init__(self,sidebar_html=None,main_content_html=None,style=MAIN_LAYOUT_STYLE):
        self.sidebar=sidebar_html
        self.main_content=main_content_html
        self.style=style
        self.__html_structure__()

    def __html_structure__(self):
        self.element=html.Div(className="content", 
                style=self.style,
                children=[
                            dcc.Location(id="url"),html.Div(className='main-page',children=[
                                html.Table(className='table-container',id='tbl-mp-1993', children=[
                                    html.Tbody(className='tbody-container', children=[
                                        html.Tr(id='tr-row1', children=[
                                            html.Td(id='td-row-col-11',children=[self.sidebar]),
                                            html.Td(id='td-row-col-12',children=[self.main_content])                                                                
                                        ])
                                    ])
                                ])
                            ])    
                ])
       
#Html Table
class Html_Table():
    def __init__(
                    self,data=[],nRows=1,nColumns=1,idRows='tab-row',idColumns='tab-column',idTable='tab-body',
                    classRow='tab-tr',classColumn='tab-td',classTable='tab-main'
                 ):
        self.data=data
        self.n_rows=nRows
        self.n_columns=nColumns
        self.id_rows=idRows
        self.id_columns=idColumns
        self.id_table=idTable
        self.class_row=classRow
        self.class_column=classColumn
        self.class_table=classTable
        self.__html_structure__()

    def __html_structure__(self):
        tag=None
        rows=[]   
        k=0
        for i in range(self.n_rows):
            columns=[]
            for j in range(self.n_columns):
                tag='-' + str(i) + 'X' + str(j)
                if k>=len(self.data):
                    break
                columns.append(
                        html.Td(
                            id=self.id_columns + tag,
                            className=self.class_column,
                            children=[
                                  self.data[k]
                            ]
                        )
                )
                k+=1
            tag='-' + str(i)
            rows.append(
                html.Tr(
                    id=self.id_rows + tag,
                    className=self.class_row,
                    children=columns
                )
            )
        self.element=html.Table(id=self.id_table,className=self.class_table,children=[
                                html.Tbody(children=rows)
                     ])

#Home Page
class Home_Page():
    def __init__(self,title=None,text=None):
        self.title=title
        self.text=text
        self.__html_structure__()

    def __html_structure__(self):
        element=Html_Table(
            [[html.Div(className="Row",children=[html.Img(src='data:image/png;base64,{}'.format(img_n4_introducao_encoded))]),
            html.Div(className="text",style={"margin-top":"2rem","margin-left":"1rem"},children=[
                html.P(className="text text-light", style={"font-size":"2rem"},children=[
                    self.text.split('.')[0],
                    html.Br(),
                    self.text.split('.')[1]
                ])
            ])]],1,2
        ).element

        self.element=[html.H1(self.title,style={"margin-left": "2rem",'textAlign':'center'},className="text-light"),
                      html.Div(className="container",style={"background-color":"#2a1c4a","margin-top":"2rem","margin-left": "21rem","margin-right": "1rem"},
                        children=[html.Div(className="column",children=[html.Div(className="container",
                             style={"margin-top":"2rem","margin-bottom":"2rem"},children=[element])                       
                        ])
                    ])
               ]

#Dropdown
class Dropdown():
    def __init__(self,data=[],style={'width':'30rem'},className='dash-dropdown',
                 id_element='dp-element-'+str(dt.datetime.now()).replace('/','').replace('\\','').replace(':','').replace('-','').replace(' ',''),
                 placeholder='', rectangle={'margin-left':'1rem'}):
        self.data=data
        self.style=style
        self.id=id_element
        self.placeholder=placeholder
        self.rectangle=rectangle
        self.__contructor__()
        
    def __contructor__(self):
        self.content=html.Div([
                        dcc.Dropdown(
                            [{"label":html.H1([i]),"value":i} for i in self.data],
                            id=self.id,
                            placeholder=self.placeholder,
                            style=self.style
                        )],style=self.rectangle)  

#Card
class Card():
    def __init__(self,title='titulo',title_style={'color':'#ffffff','font-size':'2rem'},value='valor',value_style={'color':'#ffffff','font-size':'3rem'},
                 has_body=True,card_color='#2b1f47',card_style={'border-color':'#808080'},id_element=''):
        self.title=title
        self.title_style=title_style
        self.value=value
        self.value_style=value_style
        self.has_body=has_body
        self.card_color=card_color
        self.card_style=card_style
        self.id_element=id_element
        self.__constructor__()

    def __constructor__(self):
        self.content=dbc.Card([
                                html.Div(children=[                            
                                    html.Div([
                                        html.Span(self.title,style=self.title_style),
                                        html.H2([self.value], className="card-title", style=self.value_style),
                                    ],id=self.id_element,key=1)
                                ])
                        ], 
                        body=self.has_body,
                        color=self.card_color,
                        style=self.card_style
                    ) 

    def Load(self):
        self.__constructor__()

#Group
class Group():
    def __init__(self,data,dimension=(1,1)):
        self.content=Html_Table(nRows=dimension[0],nColumns=dimension[1],data=data).element

    def Load(self):
        return self.content

#Panel
class Panel():
    def __init__(self,data,dimension=(1,1),style={'margin-left':'1rem'}):
        nrows=dimension[0]
        ncols=dimension[1]

        agora=datetime.today().__str__().strip().replace('/','').replace('\\','').replace(':','').replace('.','').replace('-','').replace(' ','')

        k=0

        trs=[]

        number_of_columns=['one','two','three','four','five','six','seven','eight','nine','ten']
        class_name=number_of_columns[ncols-1] + ' columns'

        for i in range(nrows):
            tds=[]
            for j in range(ncols):
                
                if k>=len(data):
                    break
                div_col=html.Div(children=[data[k]],className=class_name,id='pnds'+agora+'L'+str(i)+'X'+str(j),style={'margin-left':'5rem'})
                tds.append(div_col)
                k+=1
            div_row=html.Div(children=tds,className='row',id='pnds'+agora+'L'+str(i))
            trs.append(div_row)

        self.content=html.Div(style=style,children=trs,id='pnds'+agora)
        
    def Load(self):
        return self.content

#Chart
class Chart():
    def __init__(self,x=None,y=None,y_trend=None,show_trend=True,chart_types=(CHART_TYPE.VERTICAL_BAR),series_names=[''],
                 plot_size=(500,300),coordinates_xy={'top':0,'left':0},labels={'title':'Title','x':'x_label','y':'y_label'},
                 template={'template':'simple_white','font_family':'Tw Cen MT','font_color':'white','paper_bgcolor':'#1f1537','plot_bgcolor':'#1f1537',
                           'markers':[dict(color = '#0099ff'),dict(color = '#003333')],'marker_trend':dict(color='#800000'),
                           'insidetextfont':dict(color='white'),'textposition':'outside'},id_obj=datetime.now().__str__()
                 ): 
        self.x=x
        self.y=y
        self.y_trend=y_trend
        self.show_trend=show_trend
        self.chart_types=chart_types
        self.series_names=series_names
        self.width=plot_size[0]
        self.height=plot_size[1]
        self.top=coordinates_xy['top']
        self.left=coordinates_xy['left']
        self.title=labels['title']
        self.x_label=labels['x']
        self.y_label=labels['y']
        self.template=template['template']
        self.font_family=template['font_family']
        self.font_color=template['font_color']
        self.paper_bgcolor=template['paper_bgcolor']
        self.plot_bgcolor=template['plot_bgcolor']
        self.markers=template['markers']
        self.marker_trend=template['marker_trend']
        self.insidetextfont=template['insidetextfont']
        self.textposition=template['textposition']
        self.id=id_obj
        self.figure=None
    
    def __Generate_Chart_List__(self):

        self.chart_list=[]

        if isinstance(self.y[0],list) or isinstance(self.y[0],tuple):
            n_y=np.array(self.y,dtype=object).shape[0]
        else:
            n_y=1
        
        if isinstance(self.x[0],list) or isinstance(self.x[0],tuple):
            n_x=np.array(self.x,dtype=object).shape[0]
        else:
            n_x=1
        
        if self.y_trend!=None:         
            if isinstance(self.y_trend[0],list) or isinstance(self.y_trend[0],tuple):
                n_yt=np.array(self.y_trend,dtype=object).shape[0]
            else:
                n_yt=1
        else:
            n_yt=0
        
       
        
        for i in range(n_y):

            if isinstance(self.chart_types,list) or isinstance(self.chart_types,tuple):
                chart_type_selected=self.chart_types[i]
            else:
                chart_type_selected=self.chart_types

            if n_x==1:
                x_selected=self.x
            elif n_x>i:
                x_selected=self.x[i]

            if n_y==1:
                y_selected=self.y
            else:
                y_selected=self.y[i]

            if n_yt==1:
                yt_selected=self.y_trend
            elif n_yt>i:
                yt_selected=self.y_trend[i]

            if i>=len(self.markers):
                marker_index=len(self.markers)-1
            else:
                marker_index=i

            if isinstance(self.series_names[0],list) or isinstance(self.series_names[0],tuple):
                serie_name_selected=self.series_names[i]
            elif isinstance(self.series_names,str):
                serie_name_selected=self.series_names
            elif isinstance(self.series_names,list):
                serie_name_selected=self.series_names[i]
            else:
                serie_name_selected=self.series_names[0]

            if chart_type_selected==CHART_TYPE.VERTICAL_BAR:
                chart_obj=graph_objects.Bar(name=serie_name_selected,y=y_selected,x=x_selected,marker=self.markers[marker_index],text=y_selected,insidetextfont=self.insidetextfont,textposition=self.textposition)

            elif chart_type_selected==CHART_TYPE.HORIZONTAL_BAR:
                chart_obj=graph_objects.Bar(name=serie_name_selected,y=y_selected,x=x_selected,marker=self.markers[marker_index],text=x_selected,
                                            insidetextfont=self.insidetextfont,textposition=self.textposition,orientation='h')

            elif chart_type_selected==CHART_TYPE.PIE:

                chart_obj=graph_objects.Pie(name=serie_name_selected,values=y_selected,labels=x_selected,textinfo='label+percent',insidetextorientation='horizontal',
                                            textfont=self.insidetextfont,marker_colors=self.markers)

            elif chart_type_selected==CHART_TYPE.SCATTER:
                chart_obj=graph_objects.Scatter(name=serie_name_selected,y=y_selected,x=x_selected,marker=self.markers[marker_index],mode='lines+markers')
                

            elif chart_type_selected==CHART_TYPE.HISTOGRAM:
                chart_obj=graph_objects.Histogram(name=serie_name_selected,y=y_selected,x=x_selected,marker=self.markers[marker_index])
                

            self.chart_list.append(chart_obj)

            if self.show_trend and self.y_trend!=None:                
                if i<n_yt:
                    chart_obj=graph_objects.Scatter(name='Tendencia ' + serie_name_selected,y=yt_selected,x=x_selected,marker=self.marker_trend,mode='lines')
                    self.chart_list.append(chart_obj)
    
    def Create_Subplots(self,rows,cols,column_widths=None):
        self.__Generate_Chart_List__()

        if column_widths==None:
            self.figure=make_subplots(rows=rows,cols=cols)
        else:
            self.figure=make_subplots(rows=rows,cols=cols,column_widths=column_widths)

        k=0
        for i in range(rows):
            for j in range(cols):
                self.figure.add_trace(self.chart_list[k],row=i+1,col=j+1)
                k+=1

        self.__update_layout__()
        self.content=dcc.Graph(figure=self.figure)
        return self.content
    
    def __update_layout__(self):
        self.figure.update_layout(template=self.template,title=self.title,font_family=self.font_family,font_color=self.font_color,
                                  width=self.width,height=self.height)
        self.figure.layout.paper_bgcolor = self.paper_bgcolor
        self.figure.layout.plot_bgcolor=self.plot_bgcolor
        self.figure.layout.title.font.color=self.font_color
        

        self.figure.update_xaxes(showline=True, linecolor=self.font_color)
        self.figure.layout.xaxis.color=self.font_color
        self.figure.layout.xaxis.minor.tickcolor=self.font_color
        self.figure.layout.xaxis.title=self.x_label

        self.figure.update_yaxes(showline=True, linecolor=self.font_color)
        self.figure.layout.yaxis.color=self.font_color
        self.figure.layout.yaxis.minor.tickcolor=self.font_color
        self.figure.layout.yaxis.title=self.y_label
    
    def Create(self):

        self.__Generate_Chart_List__()

        self.figure=graph_objects.Figure() #FigureWidget() 
    
        for chart in self.chart_list:
            self.figure.add_trace(chart)

        self.__update_layout__()
        self.content=dcc.Graph(id=self.id,figure=self.figure)
        return self.content

    def Add_Trace(self,chart):
        self.Create()
        self.figure.add_trace(chart)
        self.__update_layout__()
        self.content=dcc.Graph(id=self.id,figure=self.figure)
        return self.content

    def Update_Trace(self,markers=None,showlegend=False):
        self.figure.update_traces(marker=markers,showlegend=showlegend)
        self.content=dcc.Graph(id=self.id,figure=self.figure)
        return self.content

    def Update_Layout(self,autosize=True,width=500,height=500,margin=dict(l=10,r=10,b=10,t=10,pad=2),showlegend=False):
        self.figure.update_layout(autosize=autosize,width=width,height=height,margin=margin,showlegend=showlegend)
        self.content=dcc.Graph(id=self.id,figure=self.figure)
        return self.content

    def Update_XAxis(self,automargin="height+width",x_range=[0,100],tickmode=None,categoryorder='total ascending',tickwidth=2,ticklen=6,dtick=None):
        self.figure.update_xaxes(automargin=automargin,range=x_range,tickmode=tickmode,categoryorder=categoryorder,tickwidth=tickwidth,ticklen=ticklen,dtick=dtick)
        self.content=dcc.Graph(id=self.id,figure=self.figure)
        return self.content

    def Update_YAxis(self,automargin="height+width",y_range=[0,100],tickmode=None,categoryorder='total ascending'):
        self.figure.update_yaxes(automargin=automargin,range=y_range,tickmode=tickmode,categoryorder=categoryorder)
        self.content=dcc.Graph(id=self.id,figure=self.figure)
        return self.content

#Table Content
class Table_Content():
    def __init__(self,headers=None,cells=None,h_line_color='black',h_fill_color='grey',h_align='center',c_line_color='black',c_fill_color='lightgrey',
                 c_align='left',width=400,height=300,h_font=None,c_font=None,h_height=40,c_height=30,h_width=None,c_width=None) -> None:
        self.headers=headers
        self.cells=cells
        self.headers_line_color=h_line_color
        self.cells_line_color=c_line_color
        self.headers_fill_color=h_fill_color
        self.cells_fill_color=c_fill_color
        self.headers_align=h_align
        self.cells_align=c_align
        self.width=width
        self.height=height
        self.headers_font=h_font
        self.cells_font=c_font
        self.headers_height=h_height
        self.cells_height=c_height
        self.headers_width=h_width
        self.cells_width=c_width
                       

    def __structure__(self):
        self.table=graph_objects.Table(
                header=dict(values=self.headers,line_color=self.headers_line_color,fill_color=self.headers_fill_color,
                            align=self.headers_align,font=self.headers_font,height=self.headers_height),
                cells=dict(values=self.cells,line_color=self.cells_line_color,fill_color=self.cells_fill_color,
                            align=self.cells_align,font=self.cells_font,height=self.cells_height)
        )
        self.fig=graph_objects.Figure(data=self.table)
        self.fig.update_layout(width=self.width,height=self.height)


    def Create(self):
        self.__structure__()
        self.content=[self.fig]
        return self.content

    def Reload(self):
        return self.Create()

#Dashboard
class Dashboard():
    def __init__(self,chart_list=[],dimension=(1,1),panel_style={"background-color":'#1c1234'},className='container'):
        self.data=chart_list
        self.dimension=dimension
        self.style=panel_style
        self.class_name=className
        self.__contructor__()

    def __contructor__(self):
        if len(self.data)==1:
            nrows=1
            ncolumns=1
        else:
            nrows=self.dimension[0]
            ncolumns=self.dimension[1]

        self.content=html.Div(children=[Html_Table(nRows=nrows,nColumns=ncolumns,data=self.data).element],
                              style=self.style,className=self.class_name)

    def Load(self):
        self.__contructor__()

#My own Tabs
class My_Tab:
    def __init__(self,children,bt_id,child_id,left='28rem'):
        self.children=children
        self.button_id=bt_id
        self.child_id=child_id
        self.left=left
        self.__structure__()

    def __structure__(self):
        N=len(self.children)
        buttons_style={'background-color':'#161023','color':'white','width':'60px','height':'30px','margin-left':'3px','border':'1px solid #000066'}
        buttons=html.Div(className='row',id=self.button_id,children=[
                          dbc.Button(str(i+1), id=self.button_id+'-'+str(i+1),className='two columns',style=buttons_style) for i in range(N)
                         ],style={'margin-left':'-1rem'})
        divs=[buttons]

        for i in range(N):
            if i==0:
                display='inline'
            else:
                display='none'

            if i%2==0:
                className='two columns'
            else:
                className='three columns'

            htmlDiv=html.Div(className=className,id=self.child_id[i],children=[self.children[i]],
                                        style={'margin-left':'-18rem','margin-top':'4rem','width':0,'height':0,'display':display})
            divs.append(htmlDiv)

        self.content=html.Div(className='row',children=divs,style={'margin-left':self.left})

    def Load(self):
        return self.content
        
class Own_Tab:
    def __init__(self,tbs_id,tag_value,labels,data,buttons_style=None):
        self.tbs_id=tbs_id
        self.tag_value=tag_value
        self.labels=labels
        self.data=data
        self.buttons_style=buttons_style
        self.__structure__()

    def __structure__(self):

        N=len(self.data)
        if N<=0:
            return html.Div([])

        if self.buttons_style==None:
            buttons_style={'background-color':'#161023','color':'white','width':'60px','height':'30px','margin-left':'3px','border':'1px solid #000066'}
        else:
            buttons_style=self.buttons_style

        if len(self.labels)!=N:
            if len(self.labels)>N:
                labels=self.labels[0:N]
            else:
                diff=N-len(self.labels)
                labels=self.labels
                for i in range(diff):
                    labels.append(self.labels[0])
        else:
            labels=self.labels

        divs=[]

        buttons=[dbc.Button(labels[i], id='bt-'+ self.tbs_id+str(i),className='two columns',style=buttons_style) for i in range(N)]
       
        divs.append(html.Div(className='row',children=buttons))
        cells=[]

        for i in range(N):
            if i==0:
                style={'display':'inline'}
            else:
                style={'display':'inline'}

            div=html.Div(className='two columns',id=self.tbs_id+str(i),children=[self.data[i]],style=style)
            cells.append(div)     
        
        divs.append(html.Div(className='row',children=cells))
        self.content=html.Div(className='container',children=divs)

    def Load(self):
        return self.content

#Tabs
class Tabs():

        def __init__(self,tbs_id,tag_values,labels):
            n=len(labels)
            if n<=0:
                return

            tab_list=[dcc.Tab(label=labels[i],style=TAB_STYLE,
                              selected_style=SELECTED_STYLE,value=tag_values + "-" + str(i)) for i in range(n)]

            self.content=html.Div(children=[
                            dcc.Tabs(id=tbs_id, value=tag_values + "-0",children=tab_list),
                            html.Div(id=tbs_id + "-content",style={'background-color':TAB_STYLE['background']})
                       ])

        def Load(self):
            return self.content

#Data Table
class DataTable():
    def __init__(self,df,title=''):
        self.df=df.copy(deep=True)
        self.title=title
    def Load(self):

        return html.Div(children=[
                        html.H1(children=[self.title],style={'color':'white'}),
                        html.Br(),
                        dash.dash_table.DataTable(
                                self.df.to_dict('records'),[{"name": i, "id": i} for i in self.df.columns],
                                style_cell={'background-color':'#34235c','color':'white','textAlign': 'left'},
                                style_header={'background-color':'#1f1537','color':'white','textAlign': 'center'},
                                style_table={'overflowX': 'scroll'},
                                style_filter={'color':'white','background-color':'white'},
                                page_size=15,
                                editable=True,
                                filter_action="native",
                                sort_action="native",
                                sort_mode="multi",
                                column_selectable="single",
                                row_selectable="multi",
                                row_deletable=True,
                                selected_columns=[],
                                selected_rows=[],
                                page_action="native",
                                page_current=0,
                                export_format='csv')
                         ],style={'width':1000})
