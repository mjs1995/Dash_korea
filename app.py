import json
import pandas as pd
import plotly
import plotly.graph_objects as go
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#server = app.server

# Import data 
df = pd.read_csv('https://raw.githubusercontent.com/mjs1995/Dash_korea/main/2018%EB%85%84%EC%86%8C%EB%A9%B8%EC%9C%84%ED%97%98%EC%A7%80%EC%88%98.csv', encoding='cp949')
df['sigun_code']=df['sigun_code'].astype(str)

new_df = df[['sido_nm', 'sigun_nm','소멸위험지수','출생아수','평균연령','종합병원','부동산업_사업체수']]

state_geo ='map (7).zip.geojson'
state_geo1 = json.load(open(state_geo, encoding='utf-8'))
for idx, sigun_dict in enumerate(state_geo1['features']):
    sigun_id = sigun_dict['properties']['merged']
    sigun_nmm = df.loc[(df.sigun_code == sigun_id), 'sigun_nm'].iloc[0]
    risk = df.loc[(df.sigun_code == sigun_id), '총인구_여자(명)'].iloc[0]
    people = df.loc[(df.sigun_code == sigun_id),  '총인구_65세이상(명)'].iloc[0]
    people_w = df.loc[(df.sigun_code == sigun_id),  '소멸위험지수'].iloc[0]
    txt = f'<b><h4>{sigun_nmm}</h4></b>총인구_여자(명) :{risk:.2f}<br>총인구_65세이상(명) : {people}<br>소멸위험지수 : {people_w}'
    
    state_geo1['features'][idx]['properties']['tooltip1'] = txt
    state_geo1['features'][idx]['properties']['risk'] = people_w

# mapbox token
#mapbox_accesstoken = 

# plotly fig 
suburbs = df['sigun_nm'].str.title().tolist()

color_deep=[[0.0, 'rgb(253, 253, 204)'],
            [0.1, 'rgb(201, 235, 177)'],
            [0.2, 'rgb(145, 216, 163)'],
            [0.3, 'rgb(102, 194, 163)'],
            [0.4, 'rgb(81, 168, 162)'],
            [0.5, 'rgb(72, 141, 157)'],
            [0.6, 'rgb(64, 117, 152)'],
            [0.7, 'rgb(61, 90, 146)'],
            [0.8, 'rgb(65, 64, 123)'],
            [0.9, 'rgb(55, 44, 80)'],
            [1.0, 'rgb(39, 26, 44)']]


Types = ['소멸위험지수','출생아수', '평균연령', '종합병원','부동산업_사업체수' ]

trace1 = [] 

for Type in Types:
    trace1.append(go.Choroplethmapbox(
    geojson=state_geo1, 
    locations=df['sigun_code'].tolist(), 
    z=df[Type].tolist(),
    text = suburbs,
    featureidkey = 'properties.merged',
    colorscale= color_deep, 
    colorbar = dict(thickness=20, ticklen=3),
    zmin=0, 
    zmax=df[Type].max() + 0.5 ,
    marker_opacity=0.5, marker_line_width=0,
    visible=False,
    subplot='mapbox1',        
    hovertemplate = "<b>%{text}</b><br><br>" +
                        "value: %{z}<br>" +
                        "<extra></extra>"))
    
trace1[0]['visible'] = True
#
trace2 = []

for Type in Types:
    trace2.append(go.Bar(
        x=df.sort_values([Type], ascending=False).head(10)['소멸위험지수'],
        y=df.sort_values([Type], ascending=False).head(10)['sigun_nm'].str.title().tolist(),
        xaxis='x2',
        yaxis='y2',
        marker=dict(
            color='rgba(91, 207, 135, 0.3)',
            line=dict(
                color='rgba(91, 207, 135, 2.0)',
                width=0.5),
        ),
        visible=False,
        name='Top 10 sigun with the highest {} value'.format(Type),
        orientation='h',
    ))

trace2[0]['visible'] = True

latitude = 35.565
longitude = 127.986


layout = go.Layout(
    title = {'text': 'Number of people in Korea / Local extinction in 2018',
             'font' :  {'size':28, 
                        'family':'Arial'}},
    autosize = True,
    
    mapbox1 = dict(
        domain = {'x': [0.3, 1],'y': [0, 1]},
        center = dict(lat=latitude, lon=longitude),
        style="open-street-map",        
        #accesstoken = mapbox_accesstoken, 
        zoom = 5),
    
    xaxis2={
        'zeroline': False,
        "showline": False,
        "showticklabels":True,
        'showgrid':True,
        'domain': [0, 0.25],
        'side': 'left',
        'anchor': 'x2',
    },
    yaxis2={
        'domain': [0.4, 0.9],
        'anchor': 'y2',
        'autorange': 'reversed',
    },
    margin=dict(l=100, r=20, t=70, b=70),
    paper_bgcolor='rgb(204, 204, 204)',
    plot_bgcolor='rgb(204, 204, 204)',
)
Types = ['소멸위험지수','출생아수', '평균연령', '종합병원','부동산업_사업체수' ]
layout.update(updatemenus=list([
    dict(x=0,
         y=1,
         xanchor='left',
         yanchor='middle',
         buttons=list([
             dict(
                 args=['visible', [True, False, False,False,False]],
                 label='type: 소멸위험지수',
                 method='restyle'
                 ),
             dict(
                 args=['visible', [False, True, False,False,False]],
                 label='type: 출생아수',
                 method='restyle'
                 ),
             dict(
                 args=['visible', [False, False, True,False,False]],
                 label='type: 평균연령',
                 method='restyle'
                 ),
             dict(
                 args=['visible', [False, False, False,True,False]],
                 label='type: 종합병원',
                 method='restyle'
                 ),
             dict(
                 args=['visible', [False, False, False,False,True]],
                 label='type: 부동산업_사업체수',
                 method='restyle'
                 )
            ]),
        )]))

fig=go.Figure(data=trace2 + trace1, layout=layout)


#####################
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "한국 지방소멸"

#####################
app.layout = html.Div([
    html.Div(children=[
        html.H1(children='한국 지방자치단체 지방소멸위험',
                style={"fontSize": "48px"},
                className="header-title"
                ),
        html.P(
                children="Analyze the "
                " number of people / Local extinction sold in the Korea"
                " between 2015 and 2018",
                className="header-description"
            ),

        dcc.Graph(
            id='example-graph-1',
            figure=fig
        ),

        html.Div(children='''
            Data source from https://github.com/mjs1995/yeonsei_project @Oct 2020
        ''')]),
    
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=new_df.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in new_df.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 6,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in ['Date', 'Region']
            ],
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },


#            style_cell_conditional=[
#                {'if': {'column_id': 'sigun_nm'},
#                 'width': '40%', 'textAlign': 'left'},
#                {'if': {'column_id': '소멸위험지수'},
#                 'width': '30%', 'textAlign': 'left'},
#                {'if': {'column_id': '출생아수'},
#                 'width': '30%', 'textAlign': 'left'},
#            ],
        ),
    ],
            className='row'),    
    
    ])



#@app.callback(
#    Output('graph','figure'),
#    [Input('dropdown', 'value')]
#)



#####################
if __name__ == '__main__':
    app.run_server()
       
