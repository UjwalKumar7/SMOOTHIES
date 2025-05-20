# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the furits you want in your custom smoothie!
  """
)



name_on_order = st.text_input("Name on smoothie:")
st.write("The name on your smoothie will be:", name_on_order)



from snowflake.snowpark.functions import col,when_matched

session = get_active_session()
my_dataframe = session.table("smoothies.public.FRUIT_OPTIONS").select(col('Fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect( 'Choose up to 5 intgredients: '
                                  ,my_dataframe
)

if ingredients_list:
    
  
    ingredients_string=''
    for fruits_chosen in ingredients_list:
        ingredients_string +=fruits_chosen
        #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
time_to_insert = st.button('Submit Order')
#st.write(my_insert_stmt)

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, ' +name_on_order+ '!', icon="✅")
    st.stop()

        
