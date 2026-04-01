import streamlit as st

st.title("Single Booking")

single_ticket_orders_form_embed_link = '<iframe class="airtable-embed" src="https://airtable.com/embed/app1FPAjv4OEUJ5T4/paggDj87JU5V1VSHD/form" frameborder="0" onmousewheel="" width="100%" height="800" style="background: transparent; border: 1px solid #ccc;"></iframe>'

st.markdown(single_ticket_orders_form_embed_link, unsafe_allow_html=True)
