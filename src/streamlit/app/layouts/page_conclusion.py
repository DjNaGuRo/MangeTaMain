import streamlit as st


def show_conclusion_page():
    st.markdown(
        """Nous avons effectué une analyse entre la variable a expliquer "niveau d'insatisfaction des recettes" et les variables explicatives comme le temps de préparation ou les valeurs nutritionnelles. 
                Nous avons remarqué qu'il n'y a pas de forte corrélation. 
                Nous pouvons donc penser que les variables seules ne suffisent pas à expliquer le niveau d'insatisfactions des utilisateurs. 

**Ouverture pour la poursuite de l'étude**

-   Approfondir la relation entre les variables : On peut chercher à comprendre le niveau d'insatisfaction des utilisateurs avec la combinaison de plusieurs variables explicatives 
c'est à dire développer des modèles de machine learning pour capturer les interactions complexes entre les variables. 
On peut faire du clustering afin de regrouper des modèles selon certaines caractéristiques combinés et étudier le taux d'insatisfaction

-   On peut éventuellement créer par exemple une nouvelle variable "complexité" avec "minutes / n_steps" décrivant la compléxité d'une recette."""
    )
