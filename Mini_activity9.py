import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber Pickups in NYC")


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Loading data...done!(using st.cache)')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

#st.markdown('Number of pickups by hour')

st.markdown("""
<style>
.big-font {
    font-size:25px;
    color:purple;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Number of pickups by hour: </p>', unsafe_allow_html=True)

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

st.markdown('<p class="big-font">Map of all pickups: </p>', unsafe_allow_html=True)

st.map(data)

hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.markdown(f'<p class="big-font">Map of all pickups at {hour_to_filter}:00</p>', unsafe_allow_html=True)
st.map(filtered_data)

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.markdown(f'<p class="big-font">Map of all pickups at {hour_to_filter}:00</p>', unsafe_allow_html=True)
st.map(filtered_data)