import streamlit as st

def get_user_session():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    return st.session_state

def set_user_session(authenticated, user):
    st.session_state['authenticated'] = authenticated
    st.session_state['user'] = user

def clear_user_session():
    st.session_state['authenticated'] = False
    st.session_state['user'] = None
