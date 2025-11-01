import streamlit as st

st.title('My To-Do List')

# Initialize session state if not already initialized
if 'my_todo_list' not in st.session_state:
    st.session_state.my_todo_list = []

# Input box for new to-do item
new_todo = st.text_input("What do you need to do?")

# Add new item to to-do list
if st.button("Add a new item"):
    if new_todo:  # Check if input is not empty
        st.session_state.my_todo_list.append(new_todo)
    else:
        st.warning("Please enter a task to add!")

# Selectbox to choose a task to remove (only show if there are tasks)
if len(st.session_state.my_todo_list) > 0:
    remove_item = st.selectbox("What have you done?", options=st.session_state.my_todo_list)

    # Remove item from to-do list
    if st.button("Remove an item"):
        if remove_item:  # Ensure an item is selected
            st.session_state.my_todo_list.remove(remove_item)
            st.experimental_rerun()  # Force the app to rerun and update the options in the selectbox
        else:
            st.warning("Please select a task to remove!")
else:
    st.write("No tasks available to remove.")

# Display the current to-do list
st.write('My To-Do list is:')
for k,v in enumerate(st.session_state.my_todo_list):
    st.write(f"{k+1}: {v}")

