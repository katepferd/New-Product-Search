# Import python packages
import streamlit as st
from rapidfuzz import process, fuzz
import pandas as pd

# Write directly to the app
st.title("New Product Search Engine:")
st.write(
    """Let's build a better search engine to create a better user experience!
    """
)

# Product Information
df_product = pd.read_csv('product_names.csv')

# Use an interactive text field to get user input
search_term = st.text_input("Keyword you want to search: "
                            , value="lavender"
                            , max_chars=None
                            , key=None
                            , type="default"
                            , help=None
                            , autocomplete=None
                            , on_change=None
                            , args=None
                            , kwargs=None
                            , placeholder=None
                            , disabled=False
                            , label_visibility="visible"
                            )


def product_search_score(keyword=search_term, df=df_product, threshold=80, sort_by='sales'):
    if keyword == "":
        return None

    product_names = df['MASTER_PRODUCT_NAME'].str.lower().tolist()
    keyword = keyword.lower()

    # Calculate similarity scores
    scores = process.cdist([keyword], product_names, scorer=fuzz.partial_ratio)

    # Filter matches based on threshold
    matched_data = [
        (i, score) for i, score in enumerate(scores[0]) if score >= threshold
    ]

    # Extract matching results with scores
    results = df.iloc[[i for i, _ in matched_data]].copy()
    results['SCORE'] = [score for _, score in matched_data]

    # Sort by Score
    if sort_by == 'sales':
        results = results.sort_values(by=['SCORE', 'SALES'], ascending=[False, False])
    elif sort_by == 'alphabetical':
        results = results.sort_values(by=['SCORE', 'MASTER_PRODUCT_NAME'], ascending=[False, True])

    return results[['MASTER_PART_NUMBER', 'MASTER_PRODUCT_NAME']].head(10)


#  Create an example dataframe
#  Note: this is just some dummy data, but you can easily connect to your Snowflake data
#  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
created_dataframe = product_search_score()

# Execute the query and convert it into a Pandas dataframe
# queried_data = created_dataframe.to_pandas()

st.subheader("Search Results")
st.dataframe(created_dataframe, use_container_width=True)
