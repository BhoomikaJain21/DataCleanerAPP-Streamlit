import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.title('Data Cleaner')
file_type = st.selectbox('File Type', ['csv', 'xlsx'])

if file_type == 'csv':
    file = st.file_uploader('Upload a CSV file', type=['csv'])
elif file_type == 'xlsx':
    file = st.file_uploader('Upload an Excel file', type=['xlsx'])
else:
    st.write('Please select a file type')

if file is not None:
    if file_type == 'csv':
        df = pd.read_csv(file, on_bad_lines='skip')
    elif file_type == 'xlsx':
        df = pd.read_excel(file)
    
    if "df" not in st.session_state or st.session_state.get("file_name") != file.name:
        st.session_state.df = df.copy()
        st.session_state.file_name = file.name
        st.session_state.new_columns = {col: col for col in df.columns}

    df = st.session_state.df
    st.write('Preview of Data Uploaded')
    st.dataframe(df)

    choice = st.radio('Do you want to rename columns?', ['Yes', 'No'])
    if choice == 'Yes':
        columns = list(df.columns)
        if "new_columns" not in st.session_state:
            st.session_state.new_columns = {col: col for col in columns}
        else:
            st.session_state.new_columns = {
                col: st.session_state.new_columns.get(col, col)
                for col in columns
            }

        # Store renamed columns
        if "new_columns" not in st.session_state:
            st.session_state.new_columns = {col: col for col in columns}
        # Slider acts like carousel
        if "col_index" not in st.session_state:
            st.session_state.col_index = 0
        # prevent out-of-range after column changes
        if st.session_state.col_index >= len(columns):
            st.session_state.col_index = 0
        index = st.slider(
            "Select column",
            0,
            len(columns) - 1,
            st.session_state.col_index
        )
        st.session_state.col_index = index
        current_col = columns[index]
        st.write(f"Column {index+1} of {len(columns)}")
        new_name = st.text_input(
            f"Rename column: {current_col}",
            value=st.session_state.new_columns[current_col]
        )
        st.session_state.new_columns[current_col] = new_name
        # Apply button
        # if st.button("Apply Renaming"):
        #     st.session_state.df.rename(
        #         columns=st.session_state.new_columns,
        #         inplace=True
        #     )
        #     st.success("Done!")
        #     st.write(st.session_state.df.columns)

    details = ['None','Info of Data', 'Statistics of Data', 'Null values in each column']
    option = st.selectbox('Select an option', details)

    if option == 'Info of Data':
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        st.text(info_str)
    elif option == 'Statistics of Data':
        st.write(df.describe())
    elif option == 'Null values in each column':
        st.write(df.isnull().sum())
    
    # Sync dtype_map with current dataframe columns
    columns = list(df.columns)
    if "dtype_map" not in st.session_state:
        st.session_state.dtype_map = {col: "Keep" for col in columns}
    else:
        # Keep only existing columns, add new ones if any
        st.session_state.dtype_map = {
            col: st.session_state.dtype_map.get(col, "Keep")
            for col in columns
        }

    st.write("### Change Data Types")
    columns = list(df.columns)
    dtype_options = ["Keep", "Drop", "int", "float", "str", "datetime"]

    for col in columns:
        st.session_state.dtype_map[col] = st.radio(
            f"{col}",
            dtype_options,
            horizontal=True,
            index=dtype_options.index(st.session_state.dtype_map[col]),
            key=f"dtype_{col}"
        )

    # Apply changes
    # if st.button("Apply Changes"):
    #     # 1. Drop columns first
    #     cols_to_drop = [
    #         col for col, action in st.session_state.dtype_map.items()
    #         if action == "Drop"
    #     ]
    #     st.session_state.df.drop(columns=cols_to_drop, inplace=True)
    #     # 2. Apply datatype changes
    #     for col, action in st.session_state.dtype_map.items():
    #         if col in cols_to_drop:
    #             continue  # already removed
    #         try:
    #             if action == "int":
    #                 st.session_state.df[col] = pd.to_numeric(
    #                     st.session_state.df[col], errors='coerce'
    #                 ).astype("Int64")
    #             elif action == "float":
    #                 st.session_state.df[col] = pd.to_numeric(
    #                     st.session_state.df[col], errors='coerce'
    #                 ).astype(float)
    #             elif action == "str":
    #                 st.session_state.df[col] = st.session_state.df[col].astype(str)
    #             elif action == "datetime":
    #                 st.session_state.df[col] = pd.to_datetime(
    #                     st.session_state.df[col], errors='coerce'
    #                 )
    #         except Exception as e:
    #             st.warning(f"{col}: {e}")
    #     for col in cols_to_drop:
    #         st.session_state.dtype_map.pop(col, None)
    #     st.success("Changes applied!")
    #     st.rerun()

    st.write("### Handle Missing Values")
    columns = list(df.columns)
    null_options = [
        "Keep",
        "Drop Rows",
        "Fill Mean",
        "Fill Median",
        "Fill Mode",
        "Forward Fill",
        "Backward Fill",
        "Custom Value"
    ]
    # Initialize state
    if "null_map" not in st.session_state:
        st.session_state.null_map = {col: "Keep" for col in columns}
    if "custom_values" not in st.session_state:
        st.session_state.custom_values = {col: "" for col in columns}
    # Sync state with columns (VERY IMPORTANT)
    st.session_state.null_map = {
        col: st.session_state.null_map.get(col, "Keep")
        for col in columns
    }
    st.session_state.custom_values = {
        col: st.session_state.custom_values.get(col, "")
        for col in columns
    }
    # UI
    for col in columns:
        choice = st.radio(
            f"{col}",
            null_options,
            horizontal=True,
            index=null_options.index(st.session_state.null_map[col]),
            key=f"null_{col}"
        )
        st.session_state.null_map[col] = choice
        # Show input only for custom value
        if choice == "Custom Value":
            st.session_state.custom_values[col] = st.text_input(
                f"Enter value for {col}",
                value=st.session_state.custom_values[col],
                key=f"custom_{col}"
            )
    # if st.button("Apply Null Handling"):
    #     for col, action in st.session_state.null_map.items():
    #         try:
    #             if action == "Drop Rows":
    #                 st.session_state.df.dropna(subset=[col], inplace=True)
    #             elif action == "Fill Mean":
    #                 st.session_state.df[col].fillna(
    #                     st.session_state.df[col].mean(), inplace=True
    #                 )
    #             elif action == "Fill Median":
    #                 st.session_state.df[col].fillna(
    #                     st.session_state.df[col].median(), inplace=True
    #                 )
    #             elif action == "Fill Mode":
    #                 st.session_state.df[col].fillna(
    #                     st.session_state.df[col].mode()[0], inplace=True
    #                 )
    #             elif action == "Forward Fill":
    #                 st.session_state.df[col].fillna(method='ffill', inplace=True)
    #             elif action == "Backward Fill":
    #                 st.session_state.df[col].fillna(method='bfill', inplace=True)
    #             elif action == "Custom Value":
    #                 value = st.session_state.custom_values[col]
    #                 st.session_state.df[col].fillna(value, inplace=True)
    #         except Exception as e:
    #             st.warning(f"{col}: {e}")
    #     st.success("Null handling applied!")
    #     st.rerun()
    if st.button("Apply All Changes"):
    
        df = st.session_state.df

        # ✅ 1. Rename columns
        df.rename(columns=st.session_state.new_columns, inplace=True)

        # ✅ 2. Drop columns (from dtype_map)
        cols_to_drop = [
            col for col, action in st.session_state.dtype_map.items()
            if action == "Drop"
        ]
        df.drop(columns=cols_to_drop, inplace=True)

        # ✅ 3. Change datatypes
        for col, action in st.session_state.dtype_map.items():
            if col in cols_to_drop:
                continue

            try:
                if action == "int":
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

                elif action == "float":
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

                elif action == "str":
                    df[col] = df[col].astype(str)

                elif action == "datetime":
                    df[col] = pd.to_datetime(df[col], errors='coerce')

            except Exception as e:
                st.warning(f"{col}: {e}")

        # ✅ 4. Handle nulls
        for col, action in st.session_state.null_map.items():
            if col not in df.columns:
                continue

            try:
                if action == "Drop Rows":
                    df.dropna(subset=[col], inplace=True)

                elif action == "Fill Mean":
                    df[col].fillna(df[col].mean(), inplace=True)

                elif action == "Fill Median":
                    df[col].fillna(df[col].median(), inplace=True)

                elif action == "Fill Mode":
                    df[col].fillna(df[col].mode()[0], inplace=True)

                elif action == "Forward Fill":
                    df[col].fillna(method='ffill', inplace=True)

                elif action == "Backward Fill":
                    df[col].fillna(method='bfill', inplace=True)

                elif action == "Custom Value":
                    df[col].fillna(st.session_state.custom_values[col], inplace=True)

            except Exception as e:
                st.warning(f"{col}: {e}")

        st.session_state.df = df
        st.success("All changes applied successfully!")
        st.rerun()

