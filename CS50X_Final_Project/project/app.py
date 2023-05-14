import streamlit as st
import subprocess
from hashlib import sha256
from cs50 import SQL
import requests
from streamlit_lottie import st_lottie
import pandas as pd
from streamlit_option_menu import option_menu
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from datetime import datetime

st.set_page_config("Heat DASHboard", layout="wide", initial_sidebar_state="auto")
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Sofia">', unsafe_allow_html=True)
today = datetime.today().strftime('%Y-%m-%d')

# run the data extractor python file only at first run of the extractor file
@st.cache_data
def extract():
    subprocess.call(r'start "" "C:\Users\glenn\anaconda3\envs\cs50xfinal\python.exe" "extract.py"', shell=True)
    return True
try:
    if extractor == True:
        pass
except:
    extractor = extract()

@st.cache_data
def load_lottie(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

house_lottie = load_lottie("https://assets1.lottiefiles.com/packages/lf20_r2gr83m9.json")
sun_lottie = load_lottie("https://assets4.lottiefiles.com/packages/lf20_iombyzfq.json")

db = SQL("sqlite:///web.db")

def get_table(query):
    query_results = db.execute(f"{query}")
    header = [col_name for _, col_name in enumerate(query_results[0])]
    body = [[item[1] for item in row.items()] for row in query_results]
    return (header, body)

col1, col2, col3 = st.columns(3)
header_cont = st.container()

main_cont = st.container()
login_cont = col2.container()
logout_cont = col3.container()
signin_cont = col2.container()

header, data = get_table("SELECT * FROM weather_data;")
df = pd.DataFrame(columns=header, data=data)
df = df.drop_duplicates()

def show_main_page():
    option_menu(
        menu_title=None,
        options=["Philippine HeatMap"],
        orientation="horizontal"
    )
    
    with st.sidebar:
        st_lottie(
            sun_lottie,
            height=200
              ) 
        st.button("LOGOUT", on_click=LoggedOut_Clicked)
        st.header("Dashboard `Parameters`")
        dt = st.selectbox(
            "Filter Date",
            options=df["date"].unique()
        )
        hr = st.selectbox(
            "Filter Hour",
            options=df["hour"].unique()
        )

    h1, h2, h3, h4 = st.columns([1,7,1,4])
    
    with h2:            
        dt_filtered_df = df[(df['date'] == dt) & (df['hour'] == hr)]
        dt_filtered_df.loc[:, 'new_temp'] = (dt_filtered_df['temp_max'] / 100) + 0.4
        
        dtm1_filtered_df = df[(df['date'] == dt) & (df['hour'] == hr - 1)]
        
        heat_map_df = dt_filtered_df[['lat', 'lon', 'new_temp']]
        
        heat_map = folium.Map(location=[12.118845, 123.201439], zoom_start=5.2, tiles="CartoDB positron")
        HeatMap(heat_map_df).add_to(heat_map)
        folium_static(heat_map)
    with h3:
        st.metric("Highest Temperature", f"{round(dt_filtered_df['temp_max'].max(), 2)} °C", 
            f"{round(dt_filtered_df['temp_max'].max()- dtm1_filtered_df['temp_max'].max(), 2)} °C")
        
        st.metric("Average Highest Temp", f"{round(dt_filtered_df['temp_max'].mean(), 2)} °C", 
            f"{round(dt_filtered_df['temp_max'].mean()  - dtm1_filtered_df['temp_max'].mean(), 2)} °C")
        
        st.metric("Lowest Temperature", f"{round(dt_filtered_df['temp_min'].min(), 2)} °C", 
            f"{round(dt_filtered_df['temp_min'].max() - dtm1_filtered_df['temp_min'].max(), 2)} °C")
        
        st.metric("Average Lowest Temp", f"{round(dt_filtered_df['temp_min'].mean(), 2)} °C", 
            f"{round(dt_filtered_df['temp_min'].mean() - dtm1_filtered_df['temp_min'].mean(), 2)} °C")

def show_login_page():
    with login_cont:
        st_lottie(
            house_lottie,
            height=200
              )
        st.markdown("<h1 style='text-align: center; color: blue; font-size: 50px;'>Heat Dash-PH</h1>", unsafe_allow_html=True)
        if st.session_state['loggedIn'] == False and st.session_state['signup'] == False:
            st.markdown("<h3 style='text-align: center; color: grey; font-size: 40px;'>LOGIN</h1>",  unsafe_allow_html=True)
            userName = st.text_input(label="Username", value="", placeholder="Enter your user name")
            password = st.text_input(label="Password", value="",placeholder="Enter password", type="password")
            login_btn_cont, signup_btn_cont = st.columns([5,1])
            login_btn_cont.button("LOGIN", on_click=LoggedIn_Clicked, args= (userName, password))
            signup_btn_cont.button("SIGNUP", on_click=show_signup_page_clicked)

def show_signup_page():
    if st.session_state['loggedIn'] == False and st.session_state['signup'] == True:
        with signin_cont:
            st_lottie(
            house_lottie,
            height=200
              )
            st.markdown("<h1 style='text-align: center; color: blue; font-size: 50px;'>Heat Dash-PH</h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; color: grey; font-size: 40px;'>SIGNUP</h1>",  unsafe_allow_html=True)
            username = st.text_input("Create Username", placeholder="Username")
            password = st.text_input("Create Password", placeholder="Password", type="password")
            password2 = st.text_input("Confirm Password", placeholder="Confirm Password", type="password")
            register_btn_cont, back_to_signin_btn_cont = st.columns([3,1])
            register_btn_cont.button("Register", on_click=register_clicked, args= (username, password, password2))
            back_to_signin_btn_cont.button("Back to Login", on_click=back_to_login_clicked)    
            
def register_clicked(username, password, password2):
    user = db.execute("SELECT username FROM users WHERE username = ?;", username)
    if not username:
        st.error("Please enter Username", icon="❌")
    elif not password:
        st.error("Please enter Password", icon="❌")
    elif not password2:
        st.error("Please confirm Password", icon="❌")
    elif password != password2:
        st.error("Passwords do not match", icon="❌")
    elif user:
        st.error("Username already exists", icon="❌")
    else:
        password_hash = sha256(password.encode()).hexdigest()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?);", username, password_hash)
        st.success("Registration Successful!", icon="✅")

def back_to_login_clicked():
    st.session_state['signup'] = False
    
def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    
def show_signup_page_clicked():
    st.session_state['signup'] = True
   
def LoggedIn_Clicked(username, password):
    if not username:
        st.error("Please enter Username", icon="❌")
    elif not password:
        st.error("Please enter Password", icon="❌")
    else:
        password_hash = sha256(password.encode()).hexdigest()
        user = db.execute("SELECT username FROM users WHERE username = ?;", username)
        pw = db.execute("SELECT password FROM users WHERE password = ?;", password_hash)

        if not user:
            st.error("User doesn't exist", icon="❌")
        elif not pw:
            st.error("Invalid Password", icon="❌")
        else:
            st.session_state["loggedIn"] = True
    
def main():
    
    
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        st.session_state['signup'] = False
        show_login_page() 
    else:
        if st.session_state['loggedIn']:
            show_main_page()
        elif st.session_state['signup']:
            show_signup_page()
        else:
            show_login_page()
            
            
if __name__ == "__main__":
    main()
