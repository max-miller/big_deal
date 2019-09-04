import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np
import pandas as pd

from dash.dependencies import Input, Output

from scipy import stats

city_names = sorted(['Washington D.C.','New York, NY','Los Angeles, CA','Chicago, IL','Houston, TX', 'Phoenix, AZ',
             'Philadelphia, PA', 'San Antonio, TX','San Diego, CA','Dallas, TX','San Jose, CA','Austin, TX',
             'Jacksonville, FL','Fort Worth, TX','Columbus, OH', 'San Francisco, CA','Charlotte, NC',
             'Indianapolis, IN', 'Seattle, WA','Denver, CO','Boston, MA','El Paso, TX','Detroit, MI',
             'Nashville, TN','Portland, OR','Memphis, TN','Oklahoma City, OK','Las Vegas, NV','Louisville, KY',
             'Baltimore, MD','Milwaukee, WI','Albuquerque, NM','Tucson, AZ','Fresno, CA','Mesa, AZ',
             'Sacramento, CA','Atlanta, GA','Kansas City, MO','Colorado Springs, CO','Miami, FL', 'Raleigh, NC',
             'Long Beach, CA','Virginia Beach, VA','Oakland, CA','Minneapolis, MN','Tulsa, OK',
             'Arlington, TX','Tampa, FL', 'New Orleans, LA','Wichita, KS','Cleveland, OH','Bakersfield, CA',
             'Honolulu, HI','Santa Ana, CA','Riverside, CA','Corpus Christi, TX','Lexington, KY','Stockton, CA',
             'Saint Paul, MN','St. Louis, MO','Cincinnati, OH','Pittsburgh, PA','Greensboro, NC','Anchorage, AK',
             'Plano, TX','Lincoln, NE','Orlando, FL','Newark, NJ','Toledo, OH','Durham, NC','Fort Wayne, IN',
             'Jersey City, NJ','St. Petersburg, FL','Laredo, TX','Madison, WI','Buffalo, NY','Lubbock, TX',
             'Winston-Salem, NC','Norfolk, VA','Chesapeake, VA','Boise, ID','Richmond, VA',
             'Baton Rouge, LA','Spokane, WA','Des Moines, IA','Tacoma, WA'])

city_backgrounds = {'Washington D.C.':'https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Aerial_view_of_Federal_Triangle_-_facing_west.jpg/1920px-Aerial_view_of_Federal_Triangle_-_facing_west.jpg',
                    'New York, NY':'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Above_Gotham.jpg/1920px-Above_Gotham.jpg',
                    'Los Angeles, CA':'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Los_Angeles%2C_Winter_2016.jpg/2560px-Los_Angeles%2C_Winter_2016.jpg',
                    'Chicago, IL':'https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Chicago_River_ferry.jpg/1920px-Chicago_River_ferry.jpg',
                    'Houston, TX':'https://upload.wikimedia.org/wikipedia/commons/4/44/Panoramic_Houston_skyline.jpg',
                    'Phoenix, AZ':'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Downtown_Phoenix_Aerial_Looking_Northeast.jpg/1920px-Downtown_Phoenix_Aerial_Looking_Northeast.jpg',
                    'Philadelphia, PA':'https://upload.wikimedia.org/wikipedia/commons/6/62/BenjaminFranklinParkway2017.jpg',
                    'San Antonio, TX':'https://upload.wikimedia.org/wikipedia/commons/b/b4/The_Pearl_San_Antonio_2019.jpg',
                    'San Diego, CA':'https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Harbor_Drive%2C_San_Diego.jpg/1920px-Harbor_Drive%2C_San_Diego.jpg',
                    'Dallas, TX':'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Dallas_Skyline_with_Arts_District.jpg/2560px-Dallas_Skyline_with_Arts_District.jpg',
                    'San Jose, CA':'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/McKinley_memorial%2C_St._James_Park%2C_San_Jose%2C_California.jpg/2560px-McKinley_memorial%2C_St._James_Park%2C_San_Jose%2C_California.jpg',
                    'Austin, TX':'https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Austin_Texas_Sunset_Skyline_2011.jpg/1920px-Austin_Texas_Sunset_Skyline_2011.jpg',
                    'Jacksonville, FL':'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/JaxFLSouthbank2014.jpg/1920px-JaxFLSouthbank2014.jpg',
                    'Fort Worth, TX':'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/0011Fort_Worth_Stockyards_Exchange_Ave_E_Texas.jpg/1920px-0011Fort_Worth_Stockyards_Exchange_Ave_E_Texas.jpg',
                    'Columbus, OH':'https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Columbus-ohio-skyline.jpg/1920px-Columbus-ohio-skyline.jpg',
                    'San Francisco, CA':'https://upload.wikimedia.org/wikipedia/commons/1/1e/San_Francisco_from_the_Marin_Headlands_in_March_2019.jpg',
                    'Charlotte, NC':'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Saint_Peter_Catholic_Church_%28Charlotte%2C_North_Carolina%29_-_view_from_Mint_Museum.jpg/2560px-Saint_Peter_Catholic_Church_%28Charlotte%2C_North_Carolina%29_-_view_from_Mint_Museum.jpg',
                    'Indianapolis, IN':'https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Indianapolis-1872528.jpg/1920px-Indianapolis-1872528.jpg',
                    'Seattle, WA':'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Seattle_Kerry_Park_Skyline.jpg/2560px-Seattle_Kerry_Park_Skyline.jpg',
                    'Denver, CO':'https://upload.wikimedia.org/wikipedia/commons/a/a9/2006-03-26_Denver_Skyline_I-25_Speer.jpg',
                    'Boston, MA':'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Boston_skyline_from_Longfellow_Bridge_September_2017_panorama_2.jpg/2880px-Boston_skyline_from_Longfellow_Bridge_September_2017_panorama_2.jpg',
                    'El Paso, TX':'https://upload.wikimedia.org/wikipedia/commons/6/6d/Downtown_El_Paso_at_sunset.jpeg',
                    'Detroit, MI':'https://upload.wikimedia.org/wikipedia/commons/2/24/ChaseBuildingDetroit.JPG',
                    'Nashville, TN':'https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Peabodyvu.JPG/1920px-Peabodyvu.JPG',
                    'Portland, OR':'https://upload.wikimedia.org/wikipedia/commons/f/f5/Downtown_Portland%2C_OR_by_Paul_Nelson.jpg',
                    'Memphis, TN':'https://upload.wikimedia.org/wikipedia/commons/b/b4/Memphis_Skyline_from_Poplar_Ave.jpg',
                    'Oklahoma City, OK':'https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Downtown_Oklahoma_City_skyline_at_twilight.jpg/1920px-Downtown_Oklahoma_City_skyline_at_twilight.jpg',
                    'Las Vegas, NV':'https://upload.wikimedia.org/wikipedia/commons/1/15/Las_Vegas_%2822096744189%29.jpg',
                    'Louisville, KY':'https://upload.wikimedia.org/wikipedia/commons/d/de/WaterfrontPkDwnt.jpg',
                    'Baltimore, MD':'https://upload.wikimedia.org/wikipedia/commons/4/42/Sunset%40Baltimore_II.JPG',
                    'Milwaukee, WI':'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Downtown_Milwaukee_from_the_Milwaukee_River.jpg/1920px-Downtown_Milwaukee_from_the_Milwaukee_River.jpg',
                    'Albuquerque, NM':'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Old_Main_Library%2C_Albuquerque_NM.jpg/1920px-Old_Main_Library%2C_Albuquerque_NM.jpg',
                    'Tucson, AZ':'https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/TucsonDowntownView1.jpg/2560px-TucsonDowntownView1.jpg',
                    'Fresno, CA':'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/H._H._Brix_Mansion.JPG/1920px-H._H._Brix_Mansion.JPG',
                    'Mesa, AZ':'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Downtown_Mesa_Arizona.jpg/2560px-Downtown_Mesa_Arizona.jpg',
                    'Sacramento, CA':'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Sacramento%2C-California---State-Capitol_%28cropped%29.jpg/2560px-Sacramento%2C-California---State-Capitol_%28cropped%29.jpg',
                    'Atlanta, GA':'https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Midtown_HDR_Atlanta.jpg/1920px-Midtown_HDR_Atlanta.jpg',
                    'Kansas City, MO':'https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Kansas_City_Skyline_2.JPG/1920px-Kansas_City_Skyline_2.JPG',
                    'Colorado Springs, CO':'https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/CC_COSPRINGS.jpg/1920px-CC_COSPRINGS.jpg',
                    'Miami, FL':'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Downtown_Miami_aerial_2008.jpg/1920px-Downtown_Miami_aerial_2008.jpg',
                    'Raleigh, NC':'https://upload.wikimedia.org/wikipedia/commons/9/9c/Raleigh_skyline_along_S_Saunders_st.jpg',
                    'Omaha, NE':'https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Interstate_leaving_Omaha.jpg/2560px-Interstate_leaving_Omaha.jpg',
                    'Long Beach, CA':'https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/LongBeachLongView.jpg/1920px-LongBeachLongView.jpg',
                    'Virginia Beach, VA':'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/VirginiaBeach.jpg/1920px-VirginiaBeach.jpg',
                    'Oakland, CA':'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/OAKLAND%2C_CA%2C_USA_-_Skyline_and_Bridge.JPG/1920px-OAKLAND%2C_CA%2C_USA_-_Skyline_and_Bridge.JPG',
                    'Minneapolis, MN':'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Minneapolis_skyline_from_Prospect_Park_Water_Tower%2C_July_2014.jpg/2880px-Minneapolis_skyline_from_Prospect_Park_Water_Tower%2C_July_2014.jpg',
                    'Tulsa, OK':'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Downtown_Tulsa_Skyline.jpg/1920px-Downtown_Tulsa_Skyline.jpg',
                    'Arlington, TX':'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Cowboys_Stadium%2C_a_domed_stadium_with_a_retractable_roof_in_Arlington%2C_Texas_LCCN2013650777.tif/lossy-page1-1920px-Cowboys_Stadium%2C_a_domed_stadium_with_a_retractable_roof_in_Arlington%2C_Texas_LCCN2013650777.tif.jpg',
                    'Tampa, FL':'https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Tampa_Convention_Center_from_Bayshore.JPG/1920px-Tampa_Convention_Center_from_Bayshore.JPG',
                    'New Orleans, LA':'https://upload.wikimedia.org/wikipedia/commons/e/ef/Cafe_du_Monde_New_Orleans.jpg',
                    'Wichita, KS':'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Wichita_City_Carnegie_Library_Building.jpg/2560px-Wichita_City_Carnegie_Library_Building.jpg',
                    'Cleveland, OH':'https://upload.wikimedia.org/wikipedia/en/0/0f/Cleveland-Panorama-JasonRene.jpg',
                    'Bakersfield, CA':'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/2008-0621-Bakersfield-pan.JPG/2880px-2008-0621-Bakersfield-pan.JPG',
                    'Honolulu, HI':'https://upload.wikimedia.org/wikipedia/commons/2/21/Waikiki_view_from_Diamond_Head.JPG',
                    'Santa Ana, CA':'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Santa_Ana_Amtrak_Station_%28cropped%29.jpg/1920px-Santa_Ana_Amtrak_Station_%28cropped%29.jpg',
                    'Riverside, CA':'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/MissionInn_SpanishWing.jpg/1920px-MissionInn_SpanishWing.jpg',
                    'Corpus Christi, TX':'https://en.wikipedia.org/wiki/Texas_State_Aquarium#/media/File:Texas_State_Aquarium_Exterior.jpg',
                    'Lexington, KY':'https://upload.wikimedia.org/wikipedia/commons/0/0b/LexingtonDowntown.JPG',
                    'Stockton, CA':'https://en.wikipedia.org/wiki/University_of_the_Pacific_(United_States)#/media/File:UOP-burnstower.jpg',
                    'Saint Paul, MN':'https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Saint_paul_mn.jpg/1920px-Saint_paul_mn.jpg',
                    'St. Louis, MO':'https://upload.wikimedia.org/wikipedia/commons/9/9f/STL_Skyline_2007_edit_cropped.jpg',
                    'Cincinnati, OH':'https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Downtown_Cincinnati_viewed_from_Mt._Adams.jpg/1920px-Downtown_Cincinnati_viewed_from_Mt._Adams.jpg',
                    'Pittsburgh, PA':'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Downtown_Pittsburgh_from_Duquesne_Incline_in_the_morning.jpg/1920px-Downtown_Pittsburgh_from_Duquesne_Incline_in_the_morning.jpg',
                    'Greensboro, NC':'https://upload.wikimedia.org/wikipedia/commons/e/e5/Greensboro_Skyline.jpg',
                    'Anchorage, AK':'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Anchorage_on_an_April_evening.jpg/2560px-Anchorage_on_an_April_evening.jpg',
                    'Plano, TX':'https://upload.wikimedia.org/wikipedia/commons/0/02/Plano_Skyline.jpg',
                    'Lincoln, NE':'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Skyline_of_Downtown_Lincoln%2C_Nebraska%2C_U.S._%282015%29.jpg/2880px-Skyline_of_Downtown_Lincoln%2C_Nebraska%2C_U.S._%282015%29.jpg',
                    'Orlando, FL':'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Orlando_downtown_2011.jpg/1920px-Orlando_downtown_2011.jpg',
                    'Newark, NJ':'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Military_Park.JPG/1920px-Military_Park.JPG',
                    'Toledo, OH':'https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/COSI_Toledo_located_at_1_Discovery_Way.JPG/1920px-COSI_Toledo_located_at_1_Discovery_Way.JPG',
                    'Durham, NC':'https://upload.wikimedia.org/wikipedia/commons/1/1e/Durham_NC_downtown_skyline.jpg',
                    'Fort Wayne, IN':'https://upload.wikimedia.org/wikipedia/commons/2/21/Downtown_Fort_Wayne%2C_Indiana_Skyline_from_Old_Fort%2C_May_2014.jpg',
                    'Jersey City, NJ':'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/DowntownJC2.JPG/1920px-DowntownJC2.JPG',
                    'St. Petersburg, FL':'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/S._H._Kress_and_Co._Building_%28St._Petersburg%2C_Florida%29.jpg/1920px-S._H._Kress_and_Co._Building_%28St._Petersburg%2C_Florida%29.jpg',
                    'Laredo, TX':'https://upload.wikimedia.org/wikipedia/commons/9/93/TA%26MIU.jpg',
                    'Madison, WI':'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Madisonskyline.jpg/1920px-Madisonskyline.jpg',
                    'Buffalo, NY':'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/20150827_61_NFTA_Light_Rail_at_Fountain_Plaza_%2821990211710%29.jpg/1920px-20150827_61_NFTA_Light_Rail_at_Fountain_Plaza_%2821990211710%29.jpg',
                    'Lubbock, TX':'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/LubbockSkyline2013.jpg/1920px-LubbockSkyline2013.jpg',
                    'Winston-Salem, NC':'https://upload.wikimedia.org/wikipedia/commons/d/db/WakeWaitChapel.jpg',
                    'Norfolk, VA':'https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Skyline_of_Downtown_Norfolk_Looking_Towards_Portsmouth.jpg/1920px-Skyline_of_Downtown_Norfolk_Looking_Towards_Portsmouth.jpg',
                    'Chesapeake, VA':'https://upload.wikimedia.org/wikipedia/commons/9/97/Great_Dismal_Swamp_Canal.jpg',
                    'Boise, ID':'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Idaho_Capitol_Building.JPG/1920px-Idaho_Capitol_Building.JPG',
                    'Richmond, VA':'https://upload.wikimedia.org/wikipedia/commons/6/69/Science_Museum_-_Broad_Street_Station_%282256100684%29.jpg',
                    'Baton Rouge, LA':'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Downtown_Baton_Rouge_from_Louisiana_State_Capitol.jpg/2560px-Downtown_Baton_Rouge_from_Louisiana_State_Capitol.jpg',
                    'Spokane, WA':'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Riverside%2C_Spokane%2C_WA%2C_USA_-_panoramio_%2816%29.jpg/2560px-Riverside%2C_Spokane%2C_WA%2C_USA_-_panoramio_%2816%29.jpg',
                    'Des Moines, IA':'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/View_from_the_Pappajohn_Sculpture_Park.jpg/1920px-View_from_the_Pappajohn_Sculpture_Park.jpg',
                    'Tacoma, WA':'https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Mount_Rainier_over_Tacoma.jpg/1920px-Mount_Rainier_over_Tacoma.jpg'}

def rounder(number):
    if number < 1000:
        return number
    if number <2000:
        clean =  str((number // 250)*250)
        return clean[0]+','+clean[1:]
    digits =len(str(number))
    power = (10**(digits-1))
    clean = str((number//power)*power)
    n_commas = (digits-1)//3
    for position in range(n_commas,0,-1):
        clean = clean[:-(position*3)]+','+clean[-(position*3):]
    return clean

label_dict = {'TMAX':'Average Daily Maximum Temperature','TMIN':'Average Daily Minimum Temperature',
             't90':'Number of Days Above 90 Degrees','TMAX_rolling':'Rolling average',
              'TMIN_rolling':'Rolling average','t90_rolling':'Rolling average'}

def ttest(df, metric, city):
    diff = round(df['2009':'2018'][f'{metric}{city}'].mean()-df['1950':'2000'][f'{metric}{city}'].mean(),2)
    pvalue = stats.ttest_ind(df['2009':'2018'][f'{metric}{city}'],
                             df['1950':'2000'][f'{metric}{city}'],equal_var=False)[1]
    if pvalue == 0:
        if diff >0:
            return f'''The {label_dict[metric].lower()} was {diff} higher in the last ten years compared to the last half of the 20th century. The odds of this happening by chance are vanishingly small'''
        return f'''The {label_dict[metric].lower()} was {-diff} lower in the last ten years compared to the last half of the 20th century. The odds of this happening by chance are vanishingly small'''
    elif pvalue < .2:
        odds = rounder(int(round(1/pvalue)))
        if diff >0:
            return f'''The {label_dict[metric].lower()} was {diff} higher in the last ten years compared to the last half of the 20th century. The odds of this happening by chance are about 1 in {odds}'''

        return f'''The {label_dict[metric].lower()} was {-diff} lower in the last ten years compared to the last half of the 20th century. The odds of this happening by chance are about 1 in {odds}'''
    elif diff >0:
        return f'''The {label_dict[metric].lower()} was {diff} higher in the last ten years compared to the last half of the 20th century. This difference may well be due to chance'''
    return f'''The {label_dict[metric].lower()} was {-diff} lower in the last ten years compared to the last half of the 20th century. This difference may well be due to chance'''

def dataframe_prep(city):
    temp = pd.read_csv(f'master_data/{city}_master.csv')
    temp.drop(0,inplace=True)
    for metric in ['TMAX','TMIN','t90']:
        temp[f'{metric}_rolling'] = [temp[metric][0:n+1].mean() if n<10 else temp[metric][n-10:n+1].mean() for
                              n in range(0,len(temp))]
    temp['years'] = pd.to_datetime(temp['years'],format='%Y')
    temp.set_index('years',inplace=True)
    return temp

df = dataframe_prep('Washington D.C.')
for city in city_names:
    try:
        temp = dataframe_prep(city)
        df = df.join(temp,how='outer',rsuffix=f'{city}')
    except:
        pass

background_color = 'rgba(227,227,246,.5)'
header_text = '''Is Climate Change a Big Deal? How much have temperatures changed in cities across the US? Select a city and a metric to see historical numbers since 1950.
Average Maximum and Average Minimum temperatures are year by year averages of all daily maximums and minimums.
You may notice that warming trends are generally more noticeable in the daily minimums - nights have gotten warmer at a faster rate than days.
'''
app= dash.Dash()

app.layout = html.Div(html.Div([html.Div([html.Div(id='header',children=header_text,
                                                  style={'fontSize':24,'marginBottom':20}),

                                          dcc.Dropdown(id='city-dropdown',
                                            options=[{'label':city,'value':city} for city in city_names],
                                            value='New York, NY',style={'width':'50%','display':'inline-block'}),

                                 dcc.Dropdown(id='metric-dropdown',
                            options=[{'label':'Average Maximum Temp','value':'TMAX'},
                                    {'label':'Average Minimum Temp','value':'TMIN'},
                                    {'label':'Number of days above 90','value':'t90'}],
                            value='TMAX',style={'width':'50%','display':'inline-block'})
                                ]),

                       html.Div([html.Div(dcc.Graph(id='graph'),style={'width':'75%','display':'inline-block',
                                                                      'vertical-align': 'middle'}),
                                html.Div(id='ttest',style={'width':'25%','display':'inline-block',
                                                          'vertical-align': 'middle',
                                                          'fontSize':24
                                                          })])],
                                style={'backgroundColor':background_color},
                     ),id='picture',
                      style={'background-image':'url(https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/26_-_New_York_-_Octobre_2008.jpg/2880px-26_-_New_York_-_Octobre_2008.jpg)'}
                      )


@app.callback(Output('graph','figure'),
             [Input('metric-dropdown','value'),
             Input('city-dropdown','value')])

def update_figure(metric,city):
    temp_dict = {f'{metric}{city}':label_dict[metric],f'{metric}_rolling{city}':'Rolling average'}
    data = [go.Scatter(x=df.index, y=df[column], mode='lines', name=temp_dict[column],line={'width':3})
            for column in [f'{metric}{city}',f'{metric}_rolling{city}']]
    layout = go.Layout(title = go.layout.Title(text=f'{metric} and 10 year rolling average',font={'size':30}),
                       legend=go.layout.Legend(xanchor='center', x=0.5, orientation='h',font={'size':24}),
                        paper_bgcolor='rgba(227,227,246,0)',
                      plot_bgcolor='rgba(227,227,246,0)',
                        height=600,
                       yaxis=go.layout.YAxis(gridwidth=3,tickfont={'size':18}),
                       xaxis=go.layout.XAxis(tickfont={'size':18})
                      )
    return {'data':data,'layout':layout}

@app.callback(Output('ttest','children'),
             [Input('metric-dropdown','value'),
             Input('city-dropdown','value')])
def perform_ttest(metric,city):
    return(ttest(df,metric,city))

@app.callback(Output('picture','style'),
              [Input('city-dropdown','value')])
def switch_background(city):
    return {'background-image':f'url({city_backgrounds[city]})'}

app.run_server(host='0.0.0.0',debug=True, port=80)
