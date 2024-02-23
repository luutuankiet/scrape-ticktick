import time
import streamlit as st

def retry(retry_delay=15):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    st.toast(f":exclamation: {e}")
                    st.toast(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)

        return wrapper
    return decorator


