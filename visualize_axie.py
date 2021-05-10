import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from datetime import datetime

import plotly.express as px
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html


# Set app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read Data
aqua = pd.read_csv('aqua_master - Copy.csv')
plant = pd.read_csv('plant_master - Copy.csv')
beast = pd.read_csv('beast_master - Copy.csv')
bird = pd.read_csv('bird_master - Copy.csv')

aqua['type'] = 'aqua'
plant['type'] = 'plant'
beast['type'] = 'beast'
bird['type'] = 'bird'

df = aqua.append(plant).append(beast).append(bird)

df['prices'] = [float(x.strip('$').replace(',','')) for x in df['price']]
date= [x.split('-') for x in df['date']]
x_axis = []
for i in date:
	x_axis.append(float(str(i[0]) +'.'+ str(i[1])))
df['date'] = [datetime.strptime(x, "%Y%m%d-%H%M") for x in df['date']]

print(df.head())

def get_options(list):
	dict_list = []
	for i in list:
		dict_list.append({'label': i, 'value': i})
	return dict_list

PARAMETER_OPTIONS = [
	{
		'label': 'Axie Type',
		'value': 'Number of Routes'
	},
	{
		'label': 'Aqua',
		'value': 'Value of Route'
	},
	{
		'label': 'Plant',
		'value': 'Popularity of route'
	}
]



app.layout = html.Div(
	children=[
			html.Div(
				className="row",
				children=[
						html.Div(
							className="four columns div-model-inputs",
							children=[
									html.H3('Where to Build Hydrogen Fueling Stations'),
									html.P(
										'We have developed a model that optimizes truck refueling centers based on the '
										'top 4674 routes in the US. You can choose which companies you would like to work '
										'with, along with the metrics that are most important to your decision.', 
										style={}
									),
									html.Br(),
									html.P([
											html.Strong('Number of Routes: '),
											'How many routes are enabled and supported by a station', html.Br(),
											html.Strong('Value of Goods: '),
											'Monetary value of the cargo transported along the route', html.Br(),
											html.Strong('Popularity of Route: '),
											'How much tonnage moves across the route', html.Br()
										], 
										style={}
									),
									html.Hr(className='hr-divider'),
									html.H6('How many stations would you like to build?'),

									html.Div(
										className="div-num-stations",
										children=[
												dcc.Input(
													id='nstations',
													placeholder='How many stations?',
													type='number',
													value=5
												),
										]
									),

									html.H6('What metric should be used to select stations?'),

									html.Div(
										className="div-entries",
										children=[
												dcc.RadioItems(
													className="radio-entry",
													id='metric',
													options=PARAMETER_OPTIONS,
													value='Number of Routes',
													labelStyle={
														'display': 'inline-block',
														'textAlign': 'center',
														'paddingLeft': '6px',
														'paddingRight': '6px',
													}
												),
										]
									),

									html.H6('What metric should determine the station icon size?'),
									
									html.Div(
											className="div-entries",
											children=[
													dcc.RadioItems(
														className="radio-entry",
														id='sec_metric',
														options=PARAMETER_OPTIONS,
														value='Number of Routes',
														labelStyle={
															'display': 'inline-block',
															'textAlign': 'center',
															'paddingLeft': '6px',
															'paddingRight': '6px',
														}
													),
											]
									),
									
									html.H6('Owner of Trucking Stations'),
									
									html.Div(
											className="div-station-companies",
											children=[
													dcc.Checklist(
														id='company',
														options=get_options(
																df['type'].unique()),
														value=['plant', 'aqua', "bird", 'beast'],
														labelStyle={
															'display': 'inline-block',
															'width': '100px',
															'textAlign': 'center',
															'paddingTop': '2px',
															'paddingBottom': '2px',
															'paddingLeft': '4px',
															'paddingRight': '4px',
														}
													)		
											]
									),			
							]
						),
				]
		),

		html.Div(
			className="row-divider",
			children=[
				html.Hr(className='hr-divider'),
			]
		),

		html.Div(
			className="row",
			children=[
					html.Div(
						className="one-third column app__left__section",
						children=[
								# TODO: Need to link this to a download function
								dcc.Graph(
									id='map_v2',
									figure={}
								),
						],
					)
			]
		)
	]
)
                

@app.callback(
    [
        Output('map_v2', 'figure')
    ],
    [
        Input('company', 'value')
    ]
)
def update_figure(selected_fuel):
		df_sub = df[df.type.isin(selected_fuel)]

		# Use Min-Max Normalization Rescaling to get a size metric for scatter plot based on the
		# chosen secondary metric. Has been used to normalize values where [a,b] = [0.5,1]
		# https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization)
		A = 0.05
		B = .5
		pri_plot = px.scatter(
			df_sub, 
			title='Axie Prices',
			x='date', 
			y='price', 
			color='type', 
			color_discrete_map={'bird': 'red', 'aqua': 'blue', "plant": 'green', 'beast': 'orange'}
		)


		figures = [pri_plot]
		[fig_.update_layout(paper_bgcolor='#879085', plot_bgcolor='#879085') for fig_ in figures]
		return figures


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=3001)






plt.scatter(date_time_obj, prices)
plt.xticks(rotation=90)
plt.xlim(min(date_time_obj), max(date_time_obj))
plt.show()
