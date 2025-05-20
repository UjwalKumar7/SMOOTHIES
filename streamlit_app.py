# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the furits you want in your custom smoothie!
  """
)



name_on_order = st.text_input("Name on smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.FRUIT_OPTIONS").select(col('Fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()
ingredients_list=st.multiselect( 'Choose up to 5 intgredients: '
                                  ,my_dataframe
)
if ingredients_list and name_on_order:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ', '

        # Safe lookup for search_on
        match = pd_df[pd_df['fruit_name'] == fruit_chosen]
        if not match.empty:
            search_on = match['search_on'].iloc[0]
        else:
            search_on = fruit_chosen  # fallback

        st.subheader(fruit_chosen + " Nutrition Information")
        response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)

        if response.status_code == 200:
            try:
                st.dataframe(data=response.json(), use_container_width=True)
            except Exception as e:
                st.error(f"Invalid JSON for {fruit_chosen}: {e}")
        else:
            st.error(f"API failed for {fruit_chosen} ({search_on}) - Status: {response.status_code}")


time_to_insert = st.button('Submit Order')


if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, ' +name_on_order+ '!', icon="✅")
    st.write(my_insert_stmt)
    st.stop()


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

