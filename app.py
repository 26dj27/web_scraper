import streamlit as st
import pandas as pd

data_file = "merged_data.csv" 
data = pd.read_csv(data_file)

tab1, tab2 = st.tabs(["Compare Products", "Search Product"])

with tab1:
    unique_products = data["ITEM"].unique()
    st.title("Product Comparison Website")
    selected_product = st.selectbox("Select a Product", unique_products)
    filtered_data = data[data["ITEM"] == selected_product]
    if not filtered_data.empty:
        st.subheader(f"Comparisons for {selected_product}")
        for _, row in filtered_data.iterrows():
            shop_name = row["shop_name"]
            price = row["price"]
            product_link = row["product_link"]
            
            st.markdown(f"""
            **Shop Name**: {shop_name}  
            **Price**: {price}  
            **[Product Link]({product_link})**
            """)
            st.markdown("---")
    else:
        st.warning("No data available for the selected product.")
with tab2:

    st.title("Search for a Product")
    search_term = st.text_input("Enter a Product Name or Keyword:")

    if search_term:

        search_results = data[data["ITEM"].str.contains(search_term, case=False, na=False)]

        if not search_results.empty:
            st.subheader(f"Search Results for: {search_term}")

            st.dataframe(search_results[["ITEM", "shop_name", "price", "product_link"]])
        else:
            st.warning("No products match your search.")
