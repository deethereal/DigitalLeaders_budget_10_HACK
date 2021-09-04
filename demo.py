import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

from model import RegressionModel as rm

header = st.container()
dataset = st.container()
interactive = st.container()

st.markdown(
    '''
    <style>
    .main {
    background-color: #F5F5F5;
    }
    </style>
    ''',
    unsafe_allow_html=True
)
background_color = '#F5F5F5'
model = rm()

@st.cache
def get_data(filename):
    data = [(random.randint(0, 100), hash(str(i))%100 , i+2010) for i in range(10)]
    data = pd.DataFrame(data= data, columns= ['Value1', 'Value2', 'Year'])
    return data

def get_plot(data, x_column, y_columns):
    fig = plt.figure()
    fig.set_size_inches(8, 6)
    plt.title('text')
    plt.plot(data[x_column], data[y_columns])
    plt.ylabel('label y')
    plt.xlabel('Time')
    plt.legend(y_columns)
    return fig



with header:
    st.title('Welcome to demo of budget 10 hack!')
    st.text('In this demo stand you can read the data and see the dependencies.')


with dataset:
    st.header('Dataset')
    data = get_data(None)
    st.write(data)

with interactive:
    st.title('Simple graph')
    c1, plot = st.columns([1, 5])
    cb1 = c1.checkbox(label='Value1')
    cb2 = c1.checkbox(label='Value2')

    y_columns = []
    x_column = ['Year']
    if cb1:
        y_columns.append('Value1')
    if cb2:
        y_columns.append('Value2')
    try:
        fig = get_plot(data, x_column, y_columns)
        st.plotly_chart(fig)
        st.pyplot(fig)
    except :
        st.markdown('Choose variable')




