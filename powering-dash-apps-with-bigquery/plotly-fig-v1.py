import plotly.express as px
df = px.data.gapminder()
fig = px.scatter(
	df.query('year==2007'),
	x='gdpPercap',
	y='lifeExp',
	size='pop',
	color='continent',
	hover_name='country',
	log_x=True,
	size_max=60
)
fig.show()
