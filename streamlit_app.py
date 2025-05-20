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
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Safely get the corresponding search_on value
        match = pd_df[pd_df['FRUIT_NAME'] == fruit_chosen]
        if not match.empty:
            search_on = match['SEARCH_ON'].iloc[0]
        else:
            search_on = fruit_chosen  # fallback if not found

        # Show subheader and nutrition info
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)

        # Safely display the JSON response
        if smoothiefroot_response.status_code == 200:
            try:
                sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
            except Exception as e:
                st.error(f"Failed to parse JSON for {fruit_chosen}: {e}")
        else:
            st.error(f"API request failed for {fruit_chosen} with status {smoothiefroot_response.status_code}")

    # Prepare the insert statement
    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                        VALUES ('""" + ingredients_string.strip() + """','""" + name_on_order + """')"""

time_to_insert = st.button('Submit Order')


if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, ' +name_on_order+ '!', icon="✅")
    st.write(my_insert_stmt)
    st.stop()


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

