import streamlit as st
from mon_module.utils import say_hello

def main():
    """Lance l'application Streamlit."""
    st.title(" Projet Mangetamain – Analyse de recettes les moins notées")
    name = st.text_input("Entrez votre prénom :")
    if name:
        st.success(say_hello(name))

if __name__ == "__main__":
    main()
