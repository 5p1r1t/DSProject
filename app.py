# -*- coding: utf-8 -*-

# Загрузим необходимые пакеты
import pandas as pd
import plotly.express as px
#from jupyter_dash import JupyterDash
from dash import Dash, dcc, html, Input, Output, State, no_update
from dash.exceptions import PreventUpdate
from catboost import CatBoostRegressor
import json
import dash_bootstrap_components as dbc

# https://dash-bootstrap-components.opensource.faculty.ai
# https://hellodash.pythonanywhere.com

#path = 'drive/MyDrive/DSProject/'
path = ''

# Загрузка параметров приложения
with open(path+'params.json') as fp:
    params = json.load(fp)

# Загрузка геоданных муниципальных образований Москвы https://gis-lab.info/qa/moscow-atd.html
with open(path+'mo.geojson') as gj:
    mo = json.load(gj)
# Загрузка таблицы для связи sub_area и mo
df = pd.read_csv(path+'mo_info.csv')

# Загрузка модели
cat_load = CatBoostRegressor()
CatBoostRegressor.load_model(cat_load, path+'cb_top12')

# Конструктор приложения, указываем тему dbc
#app = JupyterDash(__name__, external_stylesheets=[dbc.themes.MATERIA])
app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA, dbc.icons.BOOTSTRAP])


################################################# ЭЛЕМЕНТЫ УПРАВЛЕНИЯ ###################################################
header = html.H4(
    "Предсказание цен на недвижимость", className="bg-primary text-white p-2 mb-2 text-center"
)

sub_area = html.Div(
    [
        dbc.Label("Район"),
        dcc.Dropdown(
            id='sub_area',
            clearable=False,
            options=
                {df['MO'][i]: df['MO_ru'][i] for i in range (0, len(df['MO']))},
            value=df['MO'][0],
            className="p-0",
        ),
    ],
    style={"display": "grid", "grid-template-columns": "20% 80%"},
    className="mb-2",
)

full_sq = html.Div(
    [
        dbc.Label("Общая площадь",
            className="mb-0"),
        dbc.Input(
            id='full_sq',
            placeholder='Enter a value...',
            type='number',
            value='50',
            className="p-0",
            min = 0
        ),
        dcc.Slider(
            id='full_sq_sl',
            min=0,
            max=300,
            marks=None,
            value=50,
            className="p-0",
        ),
    ],
    className="mb-2",
)

life_sq = html.Div(
    [
        dbc.Label("Жилая площадь",
            className="mb-0"),
        dbc.Input(
            id='life_sq',
            placeholder='Enter a value...',
            type='number',
            value='40',
            className="p-0",
            min = 0
        ),
        dcc.Slider(
            id='life_sq_sl',
            min=0,
            max=300,
            marks=None,
            value=40,
            className="p-0",
        ),
    ],
    className="mb-2",
)

kitch_sq = html.Div(
    [
        dbc.Label("Площадь кухни",
            className="mb-0"),
        dbc.Input(
            id='kitch_sq',
            placeholder='Enter a value...',
            type='number',
            value='8',
            className="p-0",
            min = 0
        ),
        dcc.Slider(
            id='kitch_sq_sl',
            min=0,
            max=300,
            marks=None,
            value=8,
            className="p-0",
        ),
    ],
    className="mb-2",
)

num_room = html.Div(
    [
        dbc.Label("Кол-во комнат",
            className="mb-0"),
        dbc.Input(
            id='num_room',
            placeholder='Enter a value...',
            type='number',
            value='2',
            className="p-0",
            min=1
        ),
        dcc.Slider(
            id='num_room_sl',
            min=0,
            max=20,
            marks=None,
            step=1,
            value=2,
            className="p-0",
        ),
    ],
    className="mb-2",
)

floor = html.Div(
    [
        dbc.Label("Этаж",
            className="mb-0"),
        dbc.Input(
            id='floor',
            placeholder='Enter a value...',
            type='number',
            value='7',
            className="p-0",
            min=0
        ),
        dcc.Slider(
            id='floor_sl',
            min=0,
            marks=None,
            step=1,
            value=7,
            className="p-0",
        ),
    ],
    className="mb-2",
)

max_floor = html.Div(
    [
        dbc.Label("Всего этажей в доме",
                  className="mb-0"),
        dbc.Input(
            id='max_floor',
            placeholder='Enter a value...',
            type='number',
            value='14',
            className="p-0",
            min=0
        ),
        dcc.Slider(
            id='max_floor_sl',
            min=0,
            marks=None,
            step=1,
            value=14,
            className="p-0",
        ),
    ],
    className="mb-2",
)

build_year = html.Div(
    [
        dbc.Label("Год постройки дома",
                  className="mb-0"),
        dbc.Input(
            id='build_year',
            placeholder='Enter a value...',
            type='number',
            value='1981',
            className="p-0",
            min = 1950,
            max = 2030
        ),
        dcc.Slider(
            id='build_year_sl',
            min=1950,
            max=2030,
            marks=None,
            step=1,
            value=1981,
            className="p-0",
        ),
    ],
    className="mb-2",
)

state = html.Div(
    [
        dbc.Label("Состояние квартиры",
                  className="mb-0"),
        dcc.Slider(
            id='state',
            min=params['state_min'],
            max=params['state_max'],
            step=1,
            marks={i: f'{i}' for i in range(params['state_min'], params['state_max']+1)},
            value=3,
            className="p-1",
        ),
    ],
    className="mb-4",
)

product_type = html.Div(
    [
        dbc.Label("Сделка"),
        dcc.Dropdown(
            id='product_type',
            clearable=False,
            options=
                {params['product_type'][i]: params['product_type_ru'][i] for i in range(0, len(params['product_type']))},
            value=params['product_type'][0],
            className="p-0",
        ),
    ],
    style={"display": "grid", "grid-template-columns": "30% 70%"},
    className="mb-2",
)

green_zone_km = html.Div(
    [
        dbc.Label("Расстояние до парка, км",
                  className="mb-0"),
        dbc.Input(
            id='green_zone_km',
            placeholder='Enter a value...',
            type='number',
            value='1',
            className="p-0",
            min = 0
        ),
        dcc.Slider(
            id='green_zone_km_sl',
            min=0,
            max=2,
            marks=None,
            step=0.01,
            value=1,
            className="p-0",
        ),
    ],
    className="mb-2",
)

ttk_km = html.Div(
    [
        dbc.Label("Расстояние до ТТК, км",
                  className="mb-0"),
        dbc.Input(
            id='ttk_km',
            placeholder='Enter a value...',
            type='number',
            value='2',
            className="p-0",
            min = 0
        ),
        dcc.Slider(
            id='ttk_km_sl',
            min=0,
            max=70,
            marks=None,
            step=0.1,
            value=2,
            className="p-0",
        ),
    ],
    className="mb-2",
)

controls = dbc.Card(
    [
        sub_area, full_sq, life_sq, kitch_sq, num_room, floor, max_floor,
        build_year, state, product_type, green_zone_km, ttk_km
    ],
    body=True,
)

price = dbc.Card(
    html.Div(
        [
            dbc.Label('Стоимость квартиры, руб'),
            dbc.Alert(id='price'),
        ],
        className="mb-4",
    ),
    body=True,
    className="mb-4"
)

map = dbc.Card(
    html.Div(
        [
            dbc.Label('Муниципальные округа'),
            dcc.Graph(
                id='map',
                style={'width': '70vw', 'height': '65vh'}
            )
        ],
        className="mb-4",
    ),
    body=True,
)

################################################## Шаблон приложения ###################################################
app.layout = dbc.Container(
    [
        header,
        dbc.Row(
            [
                dbc.Col(
                    [
                        controls,
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        price,
                        map
                    ],
                    width=9
                ),
            ]
        ),
    ],
    fluid=True,
    className="dbc",
)

############################################ Синхронизация input и slider ##############################################

@app.callback(
    Output('full_sq_sl', 'value'), Input('full_sq', 'value'), State('full_sq_sl', 'value'))
def update_full_sq_sl(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('full_sq', 'value'), Input('full_sq_sl', 'value'), State('full_sq', 'value'))
def update_full_sq(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('life_sq_sl', 'value'), Input('life_sq', 'value'), State('life_sq_sl', 'value'))
def update_life_sq_sl(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('life_sq', 'value'), Input('life_sq_sl', 'value'), State('life_sq', 'value'))
def update_life_sq(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('kitch_sq_sl', 'value'), Input('kitch_sq', 'value'), State('kitch_sq_sl', 'value'))
def update_kitch_sq_sl(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('kitch_sq', 'value'), Input('kitch_sq_sl', 'value'), State('kitch_sq', 'value'))
def update_kitch_sq(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('num_room_sl', 'value'), Input('num_room', 'value'), State('num_room_sl', 'value'))
def update_num_room_sl(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('num_room', 'value'), Input('num_room_sl', 'value'), State('num_room', 'value'))
def update_num_room(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('floor_sl', 'value'), Input('floor', 'value'), State('floor_sl', 'value'))
def update_floor_sl(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('floor', 'value'), Input('floor_sl', 'value'), State('floor', 'value'))
def update_floor(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('max_floor_sl', 'value'), Input('max_floor', 'value'), State('max_floor_sl', 'value'))
def update_max_floor_sl(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('max_floor', 'value'), Input('max_floor_sl', 'value'), State('max_floor', 'value'))
def update_max_floor(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('build_year_sl', 'value'), Input('build_year', 'value'), State('build_year_sl', 'value'))
def update_build_year_sl(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('build_year', 'value'), Input('build_year_sl', 'value'), State('build_year', 'value'))
def update_build_year(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('green_zone_km_sl', 'value'), Input('green_zone_km', 'value'), State('green_zone_km_sl', 'value'))
def update_green_zone_km_sl(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('green_zone_km', 'value'), Input('green_zone_km_sl', 'value'), State('green_zone_km', 'value'))
def update_green_zone_km(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('ttk_km_sl', 'value'), Input('ttk_km', 'value'), State('ttk_km_sl', 'value'))
def update_ttk_km_sl(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

@app.callback(
    Output('ttk_km', 'value'), Input('ttk_km_sl', 'value'), State('ttk_km', 'value'))
def update_ttk_km(v_in, v_st):
    if float(v_in) == float(v_st):
        raise PreventUpdate
    else:
        return float(v_in)

############################################## Расчет стоимости квартиры ###############################################

@app.callback(
    [
        Output('price', 'children'),
        Output('price', 'color')
    ],
    Input('sub_area', 'value'),
    Input('full_sq', 'value'),
    Input('life_sq', 'value'),
    Input('kitch_sq', 'value'),
    Input('num_room', 'value'),
    Input('floor', 'value'),
    Input('max_floor', 'value'),
    Input('build_year', 'value'),
    Input('state', 'value'),
    Input('product_type', 'value'),
    Input('green_zone_km', 'value'),
    Input('ttk_km', 'value')
)
def predict(sub_area, full_sq, life_sq, kitch_sq, num_room, floor, max_floor,
            build_year, state, product_type, green_zone_km, ttk_km):
    full_sq = float(full_sq)
    life_sq = float(life_sq)
    kitch_sq = float(kitch_sq)
    num_room = float(num_room)
    floor = float(floor)
    max_floor = float(max_floor)
    build_year = float(build_year)
    state = float(state)
    green_zone_km = float(green_zone_km)
    ttk_km = float(ttk_km)

    if (full_sq < life_sq):
        return [html.I(className="bi bi-x-octagon-fill me-2"),"Ошибка! Общая площадь меньше жилой"], "danger"
    elif (full_sq < kitch_sq):
        return [html.I(className="bi bi-x-octagon-fill me-2"),"Ошибка! Общая площадь меньше площади кухни"], "danger"
    elif (full_sq < life_sq + kitch_sq):
        return [html.I(className="bi bi-x-octagon-fill me-2"),"Ошибка! Общая площадь меньше суммы жилой площади и кухни"], "danger"
    elif (max_floor < floor):
        return [html.I(className="bi bi-x-octagon-fill me-2"),"Ошибка! Этаж больше кол-ва этажей в здании"], "danger"
    else:
        # Вариант 1: Просто считаем прогноз для набора параметров и возвращаем его
        data = {
            'full_sq': full_sq,
            'num_room': num_room,
            'build_year': build_year,
            'state': state,
            'floor': floor,
            'max_floor': max_floor,
            'life_sq': life_sq,
            'product_type': product_type,
            'sub_area': sub_area,
            'ttk_km': ttk_km,
            'green_zone_km': green_zone_km,
            'kitch_sq': kitch_sq
        }
        price_pred = cat_load.predict(pd.DataFrame(data, [0]))
        return [html.I(className="bi bi-check-circle-fill me-2"), '{0:,.2f}'.format(price_pred[0]).replace(',', ' ')], "success"


@app.callback(
    Output("sub_area", "value"),
    Input("map", "clickData"))
def update_sub_area(clickData):
    #print (clickData)
    if clickData == None:
        return df['MO'][0]
    else:
        return df.loc[df['MO_ru'] == clickData['points'][0]['location'], 'MO'].iloc[0]




@app.callback(
    Output("map", "figure"),
    Input("sub_area", "value"))
def display_choropleth(sub_area):
    #https://plotly.com/python/choropleth-maps/
    fig = px.choropleth_mapbox(df,
                        #title = 'Муниципальные районы',
                        geojson=mo,
                        color='density_popul',
                        locations='MO_ru',
                        featureidkey='properties.NAME',
                        #projection="mercator",
                        opacity=0.3,

                        range_color=[0, df['density_popul'].max()],
                        hover_data=df.columns[2:],
                        mapbox_style="open-street-map",

                        #mapbox_style="carto-positron",
                        center={"lat": 55.59, "lon": 37.5},
                        zoom=7.89,
                        #animation_frame='area_m',
                        labels={'MO_ru': 'Муниципальное образование ',
                                'area_m': 'Площадь района, км2 ',
                                'raion_popul': 'Население района, чел ',
                                'density_popul': 'Плотность населения, чел/км2 ',
                                'green_zone_part': '% озеленения ',
                                'indust_part': '% промзоны '
                                }
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        #mapbox_zoom=20.0,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )



    return fig


# Run app and display result inline in the notebook
#app.run_server(mode='inline')
if __name__ == '__main__':
    app.run_server(debug=True)