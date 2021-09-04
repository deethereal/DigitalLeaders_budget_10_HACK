import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from template2df import template2df as t2df


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
color_dict = {'preds':'r-o', 'true': 'g-o', 'our model': 'b-o',
              'our model 2': '-o', 't_n_and_nn': '-o', 'p_n_and_nn':'-o'}

@st.cache
def get_data(filename):
    data = {'preds' : [6399038000, 8240000000,11310237000,12208281000,11361323000,10803387000,
                       12348385000,13074100000, 12857667000,17743400000,21145200000,None,None],
            'true' : [8613483384.46, 11334538970.16,10813732699.53, 8101885886.87,8916328469.16,
                      9962889434.44, 11518070774.48,11700807336.31,16900358608,17336881098.56,15165765187.88, None,None],
            'years' : range(2010,2023),
            'our model': [None,None,None,None,None,None,None,None,None,1.76669370e+10, 1.83427747e+10,1.82699107e+10,1.88647391e+10],
            'our model 2': [None,None,None,None,None,None,None,None,None,2.63422423e+10, 2.70974103e+10,2.71566655e+10, 2.79458983e+10],
            't_n_and_nn' : [15322132232.73, 18202689345.18, 17570424288.03, 15173763025.93, 15956764902, 17808163620.08,
                          19654412574.42, 20129196349.22, 26604349315.43, 27763981934.92, 27131141282.57, None, None],
            'p_n_and_nn' : [13231012000.00, 15240527000, 17322409000, 19883469000, 18466755000,
                  18722703000, 27372190971.69, 28234753941.5, 21533939000, 27185753100, 33317772000, None, None]
    }
    data = pd.DataFrame.from_dict(data)
    return data

@st.cache
def get_models():
    model = joblib.load('model.pkl')
    tant_model = joblib.load('tant_model.pkl')
    return model, tant_model

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

model, tant_model = get_models()

with header:
    st.title('Демо стенд команды 2πk')
    st.markdown('В данном демо вы можете ознакомиться с текущими данными доходов, предсказанными по СЭР.')

data = get_data(None)

mod = st.selectbox('', ["Налог на прибыль и доход", "Налоговый и неналоговый доходы"])
with st.form('graphs'):


    y_columns = []
    x_column = ['years']

    if mod == "Налог на прибыль и доход":
        st.markdown('__Доход с налогов на прибыль и доход__')
        c1, c2, c3 = st.columns([1, 1, 1])
        cb1 = c1.checkbox(label='preds', value=True)
        cb2 = c2.checkbox(label='true', value=True)
        сb3 = c3.checkbox(label='our model', value=True)
        if cb1:
            y_columns.append('preds')
        if cb2:
            y_columns.append('true')
        if сb3:
            y_columns.append('our model')
    else:
        st.markdown('__Налоговый и неналоговый доходы__')
        c4, c5, c6 = st.columns([1, 1, 1])
        cb4 = c4.checkbox(label='t_n_and_nn', value = True)
        cb5 = c5.checkbox(label='p_n_and_nn', value=True)
        cb6 = c6.checkbox(label='our model', value=True)
        if cb4:
            y_columns.append('t_n_and_nn')
        if cb5:
            y_columns.append('p_n_and_nn')
        if cb6:
            y_columns.append('our model 2')
    sumbit_button = st.form_submit_button('Show')
    try:
        fig = get_plot(data, x_column, y_columns)
        st.pyplot(fig)
    except :
        st.markdown('Выберите данные')

with st.form('predict'):
    st.write('__Загрузите ваш собственный файл!__')
    uploaded_file = st.file_uploader("Upload a xlsx file", ["xlsx"])
    file_button = st.form_submit_button('Predict')



    if file_button:
        try:
            if uploaded_file is not None:
                # df = pd.read_excel(uploaded_file)
                years, df = t2df(uploaded_file)
            model_pred = model.predict(df)
            tant_model_pred = tant_model.predict(df)
            st.write('Налог на прибыль и доход: ')
            res_1 = pd.DataFrame(index=years, data = model_pred, columns=['Результат'])
            st.write(res_1)
            st.write('Налоговый и неналоговый доходы: ')
            res_2 = pd.DataFrame(index=years, data=tant_model_pred, columns=['Результат'])
            st.write(res_2)
        except:
            st.markdown("Произошла ошибка, попробуйте другие данные")


with st.form('calc'):
    st.markdown('__Расчет расходов бюджета__')
    st.markdown('Исходя из планируемого бюджета доходов, и максимально допустимого дефицита бюджета '
                'мы можем вычислить максимально допустимые бюджетные расходы за конкретный год')

    year = st.number_input(label="Год", min_value=2010, max_value=2022)
    percent = st.number_input(label= "Ограничение по дефициту бюджета, %",min_value=0., value=15.)
    calc_button = st.form_submit_button('Calculate')


    if calc_button:
        res = calculate_max_expendature(year, percent)
        #st.markdown(res['actual'][1:-1] + ' - прогнозируемый доход' )
        st.markdown(res['plus_percent'][1:-1] + ' млн руб. - максимальный прогнозируемый расход с учетом дефицита')



