# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Example Streamlit App :balloon:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)


name_on_order = st.text_input('Movie title', 'Life of Brian')
st.write('The name is',name_on_order)


from snowflake.snowpark.functions import col
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()


if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')


    if submitted:
        
    
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
    
        try:
                og_dataset.merge(edited_dataset
                                 , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                                 , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                                )
                st.success("Someone clicked the button:",icon = '👍')
    
        except:
            st.write('Something went wrong.')
else:
    st.success('There are no pending orders right now',icon = '👍')
            

# st.write(my_dataframe)

# session = get_active_session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)


# ingredients_list =st.multiselect(
#     'Choose up to 5 ingredients:'
#     , my_dataframe
# ) 

# if ingredients_list:
#     # st.write(ingredients_list)
#     # st.text(ingredients_list)

#     ingredients_string = ''
#     for fruit_choosen in ingredients_list:
#         ingredients_string += fruit_choosen

#     st.write(ingredients_string)
    
#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
#             values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

#     # st.write(my_insert_stmt)
#     time_to_insert = st.button('Submit Order')
#     if time_to_insert:
#     # if ingredients_string:
#             session.sql(my_insert_stmt).collect()
        
#             st.success('Your Smoothie is ordered!', icon="✅")
