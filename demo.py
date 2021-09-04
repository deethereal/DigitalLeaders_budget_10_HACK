import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from template2df import template2df as t2df


#from model import RegressionModel as rm

header = st.container()
dataset = st.container()
interactive = st.container()

#st.markdown(
#    '''
#    <style>
#    .main {
#    background-color: #F5F5F5;
#    }
#    </style>
#    ''',
#    unsafe_allow_html=True
#)
background_color = '#F5F5F5'
#model = rm()

@st.cache
def get_data(filename):
    data = {'preds' : [6399038000, 8240000000,11310237000,12208281000,11361323000,10803387000,
                       12348385000,13074100000, 12857667000,17743400000,21145200000],
            'true' : [8613483384.46, 11334538970.16,10813732699.53, 8101885886.87,8916328469.16,
                      9962889434.44, 11518070774.48,11700807336.31,16900358608,17336881098.56,15165765187.88],
            'years' : range(2010,2021)}
    data = pd.DataFrame.from_dict(data)
    return data

@st.cache
def get_model():
    model = joblib.load('model.pkl')
    return model

def get_plot(data, x_column, y_columns):
    fig = plt.figure()
    fig.set_size_inches(8, 6)
    plt.title('text')
    plt.plot(data[x_column], data[y_columns])
    plt.ylabel('label y')
    plt.xlabel('Time')
    plt.legend(y_columns)
    return fig

model = get_model()

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
    cb1 = c1.checkbox(label='preds')
    cb2 = c1.checkbox(label='true')

    y_columns = []
    x_column = ['years']
    if cb1:
        y_columns.append('preds')
    if cb2:
        y_columns.append('true')
    try:
        fig = get_plot(data, x_column, y_columns)
        #st.plotly_chart(fig)
        st.pyplot(fig)
    except :
        st.markdown('Choose variable')

with st.form('predict'):
    st.write('__You can try our model on your own data!__')
    uploaded_file = st.file_uploader("Upload a xlsx file", ["xlsx"])
    file_button = st.form_submit_button('Predict labels')
    if uploaded_file is not None:
            #df = pd.read_excel(uploaded_file)
        _, df = t2df(uploaded_file)


    if file_button:
        pred = model.predict(df)
        st.write('predict: ', pred)

        #try:
        #    st.write(df)
        #    pred = model.predict(df)
        #    st.write('predict: ', pred)
        #except:
        #    st.markdown('__Fail to predict__')



