from runModel.interactive_conditional_samples import interact_model
from pathlib import Path
import arabic_reshaper
import streamlit as st
from bidi.algorithm import get_display
from streamlit_chat import message

st.set_page_config(
    page_title="Tabuk Uni Bot",
    page_icon="🤖",
    initial_sidebar_state="collapsed"
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

rtl = lambda w: get_display(f"{arabic_reshaper.reshape(w)}")
_, col1, _ = st.columns(3)
st.title("اسالني عن جامعة تبوك")

c=Path(__file__).parents[0]
pic = c / 'dependencies/Tabuk-Uni-Logo.png'
pic=str(pic)

with col1:
    st.image(pic, width=200)

st.markdown(
    """
<style>
p, div, input, label {
  text-align: right;
}
body {
    color: #fff;
    background-color: #111;
}
</style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("Info")
st.sidebar.header("بوت هو شات بوت يجيب على أسالة القبول و التسجيل لجامعة تبوك ١٤٤٤")

def query():
    with st.spinner("... جاري البحث "):
        response = interact_model(input = a)
        special_token='بوت :'
        prompt_text= response.split(special_token)[1]
        f_text= prompt_text.split("\n")[0]
    return f_text

def get_text():
    input_text = st.text_input("","من انت ؟ ")
    if "؟" not in input_text:
        input_text += "؟"
    global a    
    a = "الطالب : "
    a= a+input_text
    return input_text


user_input = get_text()
run_query = st.button("أجب")

if run_query:
    output = query()
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i),avatar_style="bottts")
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user',avatar_style="pixel-art")
    