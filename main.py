import streamlit as st
import pandas as pd
from analysis import analyze_feedback

TEXT_COLUMN_PRIORITY = (
    "review",
    "text",
    "tweet_text",
    "full_text",
    "content",
    "comment",
    "message",
    "feedback",
)


def find_default_review_column(columns):
    normalized_columns = {str(column).strip().lower(): column for column in columns}
    for candidate in TEXT_COLUMN_PRIORITY:
        if candidate in normalized_columns:
            return normalized_columns[candidate]
    return None


def clean_feedback_rows(df, column_name):
    clean_df = df.dropna(subset=[column_name]).copy()
    clean_df[column_name] = clean_df[column_name].astype(str).str.strip()
    return clean_df[clean_df[column_name] != ""]


st.title("Customer Feedback Analyzer")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    #DataFrame preview
    st.write("### Uploaded Data Preview")
    st.dataframe(df.head())

    # Let the user select the column containing reviews after seeing the data
    columns = df.columns.tolist()
    if not columns:
        st.warning("The uploaded CSV file has no columns to analyze.")
        st.stop()

    default_column = find_default_review_column(columns)
    default_index = columns.index(default_column) if default_column else 0
    if default_column:
        st.info(f"Auto-selected review column: {default_column}")
    column_name = st.selectbox("Select the column containing reviews", columns, index=default_index)

    # Ask the user a few questions to customize the analysis
    st.write("### Customize Your Analysis")

    # Example questions for users to provide input
    analysis_focus = st.radio(
        "What would you like to focus on?",
        ('Sentiment Analysis', 'Theme Identification', 'Improvement Suggestions', 'All of the Above')
    )

    # If a column is selected and user inputs are given, proceed with analysis
    if column_name:
        clean_df = clean_feedback_rows(df, column_name)

        if st.button("Analyze Feedback"):
            if clean_df.empty:
                st.warning("No usable feedback rows found after removing blank values.")
            else:
                # Passing the user inputs to the analyze_feedback function
                result = analyze_feedback(clean_df[column_name].tolist(), analysis_focus)

                st.write("### Analysis Results")
                st.markdown(result)


#####TO RUN THIS TYPE THIS(streamlit run main.py)
