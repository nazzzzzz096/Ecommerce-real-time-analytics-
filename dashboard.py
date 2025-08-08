import pandas as pd
import psycopg2
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Database connection details
DATABASE_URI = "postgresql+psycopg2://postgres:ecompassword@ecom-db.c0l260aqo4b2.us-east-1.rds.amazonaws.com:5432/ecom"

def load_data():
    try:
        conn = psycopg2.connect(
            dbname="#",
            user="#",
            password="####",
            host="######",
            port="##"
        )
        query = "SELECT * FROM orders;"
        df = pd.read_sql(query, con=conn)
        conn.close()
        if 'order_time' in df.columns:
            df['order_time'] = pd.to_datetime(df['order_time'], errors='coerce')
            print(f"Data loaded at {datetime.now().strftime('%H:%M:%S')}. Rows: {len(df)}")
            print(f"Sample data:\n{df.head()}")
        else:
            print("No 'order_time' column found in the data.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

# Load initial data
df = load_data()

# Create Dash App
app = dash.Dash(__name__)

# Styling
APP_STYLE = {
    'backgroundColor': '#f5f7fa',
    'fontFamily': 'Arial, sans-serif',
    'padding': '20px',
    'maxWidth': '1200px',
    'margin': '0 auto'
}

CARD_STYLE = {
    'backgroundColor': '#ffffff',
    'padding': '20px',
    'borderRadius': '8px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
    'marginBottom': '20px'
}

# Prepare initial data for visualizations
# 1. Sales by hour for today using order_time
if 'order_time' in df.columns and not df.empty:
    if df['order_time'].dt.time.min() != df['order_time'].dt.time.max():  # Check if time varies
        sales_by_hour = df.groupby(df['order_time'].dt.hour)['price'].sum().reset_index()
        print(f"Sales by hour data:\n{sales_by_hour}")
        line_fig = px.bar(
            sales_by_hour,
            x='order_time',
            y='price',
            title='Sales by Hour',
            labels={'order_time': 'Hour', 'price': 'Total Sales ($)'},
            color='price',
            color_continuous_scale='Blues'
        )
    else:
        print("No time variation in order_time. Using sales by product.")
        sales_by_product = df.groupby('product')['price'].sum().reset_index().sort_values('price', ascending=False)
        line_fig = px.bar(
            sales_by_product.head(10),
            x='product',
            y='price',
            title='Top  Products by Sales Today',
            labels={'product': 'Product', 'price': 'Total Sales ($)'},
            color='price',
            color_continuous_scale='Blues'
        )
else:
    print("No valid data for line chart. Using placeholder.")
    line_fig = go.Figure(data=go.Bar(x=[0], y=[0], name='No Data'))
    line_fig.update_layout(
        title='Sales by Hour Today (No Data Available)',
        xaxis_title='Hour',
        yaxis_title='Total Sales ($)',
        showlegend=False
    )

# 2. Sales by product (bar chart)
sales_by_product = df.groupby('product')['price'].sum().reset_index().sort_values('price', ascending=False)
bar_fig = px.bar(
    sales_by_product.head(10),
    x='product',
    y='price',
    title='Top 10 Products by Sales',
    labels={'product': 'Product', 'price': 'Total Sales ($)'},
    color='price',
    color_continuous_scale='Blues'
)

# 3. Sales by payment method (pie chart)
sales_by_payment = df.groupby('payment_method')['price'].sum().reset_index()
pie_fig = px.pie(
    sales_by_payment,
    names='payment_method',
    values='price',
    title='Sales Distribution by Payment Method',
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Dashboard layout
app.layout = html.Div(style=APP_STYLE, children=[
    html.H1("E-commerce Sales Dashboard", style={'textAlign': 'center', 'color': '#1f2a44'}),
    
    html.Div(style=CARD_STYLE, children=[
        html.Label("Select Time Period:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='time-filter',
            options=[
                {'label': 'Last 7 Days', 'value': 7},
                {'label': 'Last 30 Days', 'value': 30},
                {'label': 'Last 90 Days', 'value': 90},
                {'label': 'All Time', 'value': 'all'}
            ],
            value='all',
            style={'width': '50%', 'margin': '10px auto'}
        ),
        dcc.Interval(
            id='interval-component',
            interval=60*60*1000,  # Update every hour (3600 seconds in milliseconds)
            n_intervals=0
        )
    ]),
    
    html.Div(style=CARD_STYLE, children=[
        html.H2("Sales Trend", style={'color': '#1f2a44'}),
        dcc.Graph(id='line-chart', figure=line_fig)
    ]),
    
    html.Div(style=CARD_STYLE, children=[
        html.H2("Top Products by Revenue", style={'color': '#1f2a44'}),
        dcc.Graph(id='bar-chart', figure=bar_fig)
    ]),
    
    html.Div(style=CARD_STYLE, children=[
        html.H2("Sales by Payment Method", style={'color': '#1f2a44'}),
        dcc.Graph(id='pie-chart', figure=pie_fig)
    ])
])

# Callback to update charts
@app.callback(
    [Output('line-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('time-filter', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_charts(time_filter, n_intervals):
    # Reload data on each interval trigger
    global df
    df = load_data()
    
    filtered_df = df.copy()
    
    if time_filter != 'all' and 'order_time' in df.columns:
        cutoff_date = datetime.now() - timedelta(days=int(time_filter))
        filtered_df = df[df['order_time'] >= cutoff_date]
    
    # Update line chart
    if 'order_time' in filtered_df.columns and not filtered_df.empty:
        if filtered_df['order_time'].dt.time.min() != filtered_df['order_time'].dt.time.max():
            sales_by_hour = filtered_df.groupby(filtered_df['order_time'].dt.hour)['price'].sum().reset_index()
            line_fig = px.bar(
                sales_by_hour,
                x='order_time',
                y='price',
                title='Sales by Hour Today',
                labels={'order_time': 'Hour', 'price': 'Total Sales ($)'},
                color='price',
                color_continuous_scale='Blues'
            )
        else:
            sales_by_product = filtered_df.groupby('product')['price'].sum().reset_index().sort_values('price', ascending=False)
            line_fig = px.bar(
                sales_by_product.head(10),
                x='product',
                y='price',
                title='Top Products by Sales Today',
                labels={'product': 'Product', 'price': 'Total Sales ($)'},
                color='price',
                color_continuous_scale='Blues'
            )
    else:
        line_fig = go.Figure(data=go.Bar(x=[0], y=[0], name='No Data'))
        line_fig.update_layout(
            title='Sales by Hour Today (No Data Available)',
            xaxis_title='Hour',
            yaxis_title='Total Sales ($)',
            showlegend=False
        )
    
    # Update bar chart
    sales_by_product = filtered_df.groupby('product')['price'].sum().reset_index().sort_values('price', ascending=False)
    bar_fig = px.bar(
        sales_by_product.head(10),
        x='product',
        y='price',
        title='Top 10 Products by Sales',
        labels={'product': 'Product', 'price': 'Total Sales ($)'},
        color='price',
        color_continuous_scale='Blues'
    )
    
    # Update pie chart
    sales_by_payment = filtered_df.groupby('payment_method')['price'].sum().reset_index()
    pie_fig = px.pie(
        sales_by_payment,
        names='payment_method',
        values='price',
        title='Sales Distribution by Payment Method',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    return line_fig, bar_fig, pie_fig

if __name__ == "__main__":

    app.run(debug=True)
