# Import python packages
import streamlit as st
import requests
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

ingredients_list=st.multiselect( 'Choose up to 5 intgredients: '
                                  ,my_dataframe
)
if ingredients_list:
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                        VALUES ('""" + ingredients_string.strip() + """', '""" + name_on_order + """')"""

    smoothiefroot_response = requests.get("https://smoothiefroot.com/api/fruit/all")
    all_fruits_data = smoothiefroot_response.json()
    selected_data = {fruit: all_fruits_data.get(fruit.lower()) for fruit in ingredients_list if fruit.lower() in all_fruits_data}

    for fruit, data in selected_data.items():
        st.subheader(fruit.capitalize() + " Nutrition Information")
        st.dataframe(data)


time_to_insert = st.button('Submit Order')


if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, ' +name_on_order+ '!', icon="✅")
    st.write(my_insert_stmt)
    st.stop()


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

