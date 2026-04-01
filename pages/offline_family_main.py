import streamlit as st

st.title("Family Booking")

family_ticket_orders_form_embed_link = '<iframe class="airtable-embed" src="https://airtable.com/embed/app1FPAjv4OEUJ5T4/pagtrSD4inJU17gHc/form" frameborder="0" onmousewheel="" width="100%" height="800" style="background: transparent; border: 1px solid #ccc;"></iframe>'

st.markdown(family_ticket_orders_form_embed_link, unsafe_allow_html=True)
