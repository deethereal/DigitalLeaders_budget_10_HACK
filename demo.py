import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from template2df import template2df as t2df
from datetime import date

from max_expenditure_calculator import calculate_max_expendature

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
color_dict = {'preds':'r-o', 'true': 'g-o', 'future': 'b-o'}

@st.cache
def get_data(filename):
    data = {'preds' : [6399038000, 8240000000,11310237000,12208281000,11361323000,10803387000,
                       12348385000,13074100000, 12857667000,17743400000,21145200000,None,None],
            'true' : [8613483384.46, 11334538970.16,10813732699.53, 8101885886.87,8916328469.16,
                      9962889434.44, 11518070774.48,11700807336.31,16900358608,17336881098.56,15165765187.88, None,None],
            'years' : range(2010,2023),
            'future': [None,None,None,None,None,None,None,None,None,None,None,1.82699107e+10, 1.88647391e+10]}
    data = pd.DataFrame.from_dict(data)
    return data

@st.cache
def get_model():
    model = joblib.load('model.pkl')
    return model

def get_plot(data, x_column, y_columns):
    fig = plt.figure(figsize=(10,5))
    fig.set_size_inches(8, 6)
    #plt.title('Доход с налогов на прибыль и доход')
    for col in y_columns:
        plt.plot(data[x_column], data[col], color_dict[col])
    plt.ylabel('Рубли (10^10 ₽)')
    plt.xlabel('Время')
    plt.legend(y_columns)
    return fig

model = get_model()

with header:
    st.title('Welcome to demo of budget 10 hack!')
    st.markdown('In this demo stand you can read the data and see the dependencies.')

data = get_data(None)


with st.form('graphs'):
    st.markdown('__Доход с налогов на прибыль и доход__')
    c1, c2, c3, bt = st.columns([1, 1, 1, 5])
    cb1 = c1.checkbox(label='preds', value = True)
    cb2 = c2.checkbox(label='true')
    сb3 = c3.checkbox(label='future')
    sumbit_button = st.form_submit_button('Show')
    y_columns = []
    x_column = ['years']
    if cb1:
        y_columns.append('preds')
    if cb2:
        y_columns.append('true')
    if сb3:
        y_columns.append('future')
    try:
        fig = get_plot(data, x_column, y_columns)
        st.pyplot(fig)
    except :
        st.markdown('Choose variable')

with st.form('predict'):
    st.write('__You can try our model on your own data!__')
    uploaded_file = st.file_uploader("Upload a xlsx file", ["xlsx"])
    file_button = st.form_submit_button('Predict labels')
    if uploaded_file is not None:
            #df = pd.read_excel(uploaded_file)
        years, df = t2df(uploaded_file)


    if file_button:
        pred = model.predict(df)
        st.write('predict: ', pred)

with st.form('calc'):
    st.markdown('__Расчет расходов бюджета__')
    st.markdown('Исходя из планируемого бюджета доходов, и максимально допустимого дефицита бюджета '
                'мы можем вычислить максимально допустимые бюджетные расходы за конкретный год')

    year = st.date_input(label="Год", min_value=date(2000, 1, 1), max_value=date(2023, 1, 1))
    percent = st.number_input(label= "Процент",min_value=0.)
    calc_button = st.form_submit_button('Calculate')


    if calc_button:
        res = calculate_max_expendature(year.year, percent)
        st.write(res)



