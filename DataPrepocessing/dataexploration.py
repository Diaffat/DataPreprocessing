import streamlit as st
import pandas as pd
import dataframefunctions
import plots
import featuresanalysis
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import plots

POSSIBLE_DATAEXP_ACTIONS = ["Null Values", "Outliners","Personalize","Data Mining","Normalization"]


def load_page(dataframe):
    if dataframe is None:
        st.error("Please upload your dataset!")
    else:
        dataexp_action = st.sidebar.selectbox("What do you want to explore?", POSSIBLE_DATAEXP_ACTIONS)

        
    if dataexp_action=="Null Values": 
        st.sidebar.markdown("## **Null Values :computer:** ##")
        rd = st.sidebar.radio("Choose",["Describe","Compute missing values","Compute linear correlation","Remove NaN","Replace NaN with Mean","Replace NaN with Mediane"])
        if rd=="Describe":
            render_first_look(dataframe)
            st.markdown("## **Description :computer:** ##")
            st.dataframe(dataframe.describe())
            st.header("Infos")
            st.dataframe(dataframe.info())

        if rd=="Compute missing values":
            render_missing_data(dataframe)
        if rd=="Compute linear correlation":
            render_linear_correlation(dataframe)
        if rd=="Remove NaN":
            col1,col2,col3,col4,col5 = st.columns(5)
            
            if col1.button("Remove NaN"):
                dataframe.dropna()
                st.dataframe(dataframe.describe( ))
            
            col2.button("NaN by Mean")
            col3.button("Result")
            col4.button("Save")
            col5.button("Dowload")
            


        # elif dataexp_action == "Plots":
        #     plots.load_page(dataframe)

        # elif dataexp_action == "Features":
        #     featuresanalysis.load_page(dataframe)
    if dataexp_action=="Outliners":
        st.sidebar.markdown("## **Outliners :computer:** ##")
     
        plots.render_boxplot(dataframe)

    # if dataexp_action=="Normalization":
    #     st.sidebar.markdown("## **Normalization :computer:** ##")
    #     rd2 = st.sidebar.radio("Choose",["MinMax","Standard"])
    
    if dataexp_action=="Data Mining":
        st.sidebar.markdown("## **Data Mining:computer:** ##")
        st.sidebar.number_input("How many features",min_value=2,max_value=dataframe.shape[1])


def render_missing_data(dataframe):
    """Renders the missing values and the missing percentages for each column."""

    missing_values, missing_percentage = dataframefunctions.get_missing_values(dataframe)
    st.markdown("## **Missing values :mag:** ##")
    st.dataframe(pd.concat([missing_values, missing_percentage], axis=1, keys=["Total", "percent"]))


def render_first_look(dataframe):
    """Renders the head of the dataset (with nan values colored in red),
     and comments regarding instances, columns, and missing values."""

    number_of_rows = st.sidebar.slider('Number of rows', 1, dataframe.shape[0], 10)
    st.markdown("## **Exploring the dataset :mag:** ##")
    if st.sidebar.checkbox("Color NaN values in red", value=True):
        st.dataframe(dataframe.head(number_of_rows).style.applymap(dataframefunctions.color_null_red))
    else:
        st.dataframe(dataframe.head(number_of_rows))
    render_firstlook_comments(dataframe)
    # fig,ax =plt.subplots(figsize=(10,10))
    # st.dataframe(dataframe.dtypes.value_counts())
    # sns.heatmap(dataframe.isna())
    # st.pyplot(fig)


# TODO improve such that all the type of columns are considered
def render_firstlook_comments(dataframe):
    """Makes a first analysis of the dataset and shows comments based on that."""

    num_instances, num_features = dataframe.shape
    categorical_columns = dataframefunctions.get_categorical_columns(dataframe)
    numerical_columns = dataframefunctions.get_numeric_columns(dataframe)
    cat_column = categorical_columns[0] if len(categorical_columns) > 0 else ""
    num_column = numerical_columns[0] if len(numerical_columns) > 0 else ""
    total_missing_values = dataframe.isnull().sum().sum()

    st.write("* The dataset has **%d** observations and **%d** variables. \
             Hence, the _instances-features ratio_ is ~**%d**."
             % (num_instances, num_features, int(num_instances/num_features)))

    st.write("* The dataset has **%d** categorical columns (e.g. %s) and **%d** numerical columns (e.g. %s)."
             % (len(categorical_columns), cat_column, len(numerical_columns), num_column))

    st.write("* Total number of missing values: **%d** (~**%.2f**%%)."
             % (total_missing_values, 100*total_missing_values/(num_instances*num_features)))


def render_linear_correlation(dataframe):
    """If the label is not categorical, renders the linear correlation between the features and the label."""

    st.markdown("## **Linear correlation ** ##")
    df_columns = list(dataframe.columns.values)
    label_name = df_columns[len(df_columns) - 1]

    # If the label is not categorical, show an error
    if dataframefunctions.is_categorical(dataframe[label_name]):
        display_correlation_error()
        return

    positive_corr = dataframefunctions.get_linear_correlation(dataframe, label_name, positive=True)
    negative_corr = dataframefunctions.get_linear_correlation(dataframe, label_name, positive=False)
    st.write('Positively correlated features :chart_with_upwards_trend:', positive_corr)
    st.write('Negatively correlated features :chart_with_downwards_trend:', negative_corr)


def display_correlation_error():
    st.write(":no_entry::no_entry::no_entry:")
    st.write("It's **not** possible to determine a linear correlation with a categorical label.")
    st.write("For more info, please check [this link.]\
             (https://stackoverflow.com/questions/47894387/how-to-correlate-an-ordinal-categorical-column-in-pandas)")

