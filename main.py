# import numpy as np
# import pandas as pd
# import plotly.express as px
# import streamlit as st

# # ---------------- Page Config ----------------
# st.set_page_config(
#     page_title="Video Game Sales Dashboard",
#     page_icon="🎮",
#     layout="wide",
# )

# # ---------------- Load Dataset ----------------
# @st.cache_data
# def load_data():
#     try:
#         vg_data = pd.read_csv("vgchartz-2024.csv")
#         # ✅ Parse release_date safely
#         vg_data["year_new"] = pd.to_datetime(
#             vg_data["release_date"], errors="coerce", dayfirst=True
#         ).dt.year
#         # ✅ Keep only important columns to speed up dashboard
#         columns_to_keep = [
#             "title", "console", "year_new", "genre", "publisher",
#             "na_sales", "jp_sales", "pal_sales", "other_sales", "total_sales"
#         ]
#         vg_data = vg_data[columns_to_keep]
#         # ✅ Sample 50% of dataset to reduce load (optional)
#         vg_data = vg_data.sample(frac=0.5, random_state=42)
#     except FileNotFoundError:
#         st.error("❌ vgchartz-2024.csv not found. Please upload the file.")
#         vg_data = pd.DataFrame()
#     return vg_data

# vg_data = load_data()

# if vg_data.empty:
#     st.error("❌ Dataset is empty. Please upload 'vgchartz-2024.csv'.")
#     st.stop()

# # ---------------- Sidebar Filters ----------------
# st.sidebar.header("🔍 Filters")

# with st.sidebar.form("filter_form"):
#     # ----- Genre Filter -----
#     genres = st.multiselect(
#         "Select Genre(s)",
#         options=sorted(vg_data["genre"].dropna().unique()),
#         default=None,
#     )

#     # ----- Dynamic Publisher Filter -----
#     def get_filtered_publishers(vg_data, genres):
#         if genres:
#             return sorted(vg_data[vg_data["genre"].isin(genres)]["publisher"].dropna().unique())
#         else:
#             return sorted(vg_data["publisher"].dropna().unique())

#     filtered_publishers = get_filtered_publishers(vg_data, genres)
#     publishers = st.multiselect(
#         "Select Publisher(s)",
#         options=filtered_publishers,
#         default=None,
#     )

#     # ----- Dynamic Console Filter -----
#     def get_filtered_consoles(vg_data, genres):
#         if genres:
#             return sorted(vg_data[vg_data["genre"].isin(genres)]["console"].dropna().unique())
#         else:
#             return sorted(vg_data["console"].dropna().unique())

#     filtered_consoles = get_filtered_consoles(vg_data, genres)
#     consoles = st.multiselect(
#         "Select Console(s)",
#         options=filtered_consoles,
#         default=None,
#     )

#     # ----- Year Range Filter -----
#     year_min, year_max = int(vg_data["year_new"].min()), int(vg_data["year_new"].max())
#     year_range = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))

#     submit_button = st.form_submit_button(label="Apply Filters 🔍")

# # ---------------- Filter Data Function ----------------
# @st.cache_data
# def filter_data(vg_data, genres, publishers, consoles, year_range):
#     df = vg_data.copy()
#     if genres:
#         df = df[df["genre"].isin(genres)]
#     if publishers:
#         df = df[df["publisher"].isin(publishers)]
#     if consoles:
#         df = df[df["console"].isin(consoles)]
#     df = df[(df["year_new"] >= year_range[0]) & (df["year_new"] <= year_range[1])]
#     return df

# df = filter_data(vg_data, genres, publishers, consoles, year_range) if submit_button else vg_data.copy()

# # ---------------- Main Dashboard ----------------
# st.title("🎮 Interactive Video Game Sales Dashboard")

# if not df.empty:
#     # ----- KPI Metrics -----
#     avg_year = int(df["year_new"].mean())
#     total_sales = df["total_sales"].sum()
#     count_games = df.shape[0]

#     kpi1, kpi2, kpi3 = st.columns(3)
#     kpi1.metric("📅 Avg Release Year", avg_year)
#     kpi2.metric("🎮 Number of Games", count_games)
#     kpi3.metric("💰 Total Sales (M)", f"{round(total_sales, 2)} M")

#     # ----- Charts -----
#     fig_col1, fig_col2 = st.columns(2)

#     # 📈 Yearly Sales Trend
#     with fig_col1:
#         st.markdown("### 📈 Yearly Sales Trend")
#         yearly_sales = df.groupby("year_new", as_index=False)["total_sales"].sum()
#         fig_line = px.line(yearly_sales, x="year_new", y="total_sales", markers=True)
#         st.plotly_chart(fig_line, use_container_width=True)

#     # 🥧 Sales Share by Console with custom colors
#     with fig_col2:
#         st.markdown("### 🥧 Sales Share by Console")
#         custom_colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3", "#FF6692"]
#         fig_pie = px.pie(
#             df,
#             names="console",
#             values="total_sales",
#             hole=0.4,
#             color_discrete_sequence=custom_colors
#         )
#         fig_pie.update_traces(textinfo="percent+label")
#         fig_pie.update_layout(showlegend=True)
#         st.plotly_chart(fig_pie, use_container_width=True)

#     # 📊 Regional Sales Breakdown
#     st.markdown("### 📊 Regional Sales Breakdown")
#     region_sales = df.melt(
#         id_vars=["title"],
#         value_vars=["na_sales", "jp_sales", "pal_sales", "other_sales"],
#         var_name="Region",
#         value_name="Sales"
#     )
#     fig_bar = px.bar(region_sales, x="Region", y="Sales", color="Region", barmode="group")
#     st.plotly_chart(fig_bar, use_container_width=True)

# else:
#     st.warning("⚠️ No data matches your selected filters. Try adjusting them.")


import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Video Game Sales Dashboard",
    page_icon="🎮",
    layout="wide",
)

# ---------------- Load Dataset ----------------
@st.cache_data
def load_data():
    try:
        vg_data = pd.read_csv("vgchartz-2024.csv")
        vg_data["year_new"] = pd.to_datetime(
            vg_data["release_date"], errors="coerce", dayfirst=True
        ).dt.year
        columns_to_keep = [
            "title", "console", "year_new", "genre", "publisher",
            "na_sales", "jp_sales", "pal_sales", "other_sales", "total_sales"
        ]
        vg_data = vg_data[columns_to_keep]
        vg_data = vg_data.sample(frac=0.5, random_state=42)
    except FileNotFoundError:
        st.error("❌ vgchartz-2024.csv not found. Please upload the file.")
        vg_data = pd.DataFrame()
    return vg_data

vg_data = load_data()

if vg_data.empty:
    st.error("❌ Dataset is empty. Please upload 'vgchartz-2024.csv'.")
    st.stop()

# ---------------- Sidebar Filters ----------------
st.sidebar.header("🔍 Filters")

with st.sidebar.form("filter_form"):

    # ----- Genre Filter -----
    genres = st.multiselect(
        "Select Genre(s)",
        options=sorted(vg_data["genre"].dropna().unique()),
        default=None,
    )

    # ----- Publisher Filter (depends on Genre) -----
    def get_filtered_publishers(vg_data, genres):
        df_filtered = vg_data.copy()
        if genres:
            df_filtered = df_filtered[df_filtered["genre"].isin(genres)]
        return sorted(df_filtered["publisher"].dropna().unique())

    filtered_publishers = get_filtered_publishers(vg_data, genres)
    publishers = st.multiselect(
        "Select Publisher(s)",
        options=filtered_publishers,
        default=None,
    )

    # ----- Console Filter (depends on Genre + Publisher) -----
    def get_filtered_consoles(vg_data, genres, publishers):
        df_filtered = vg_data.copy()
        if genres:
            df_filtered = df_filtered[df_filtered["genre"].isin(genres)]
        if publishers:
            df_filtered = df_filtered[df_filtered["publisher"].isin(publishers)]
        return sorted(df_filtered["console"].dropna().unique())

    filtered_consoles = get_filtered_consoles(vg_data, genres, publishers)
    consoles = st.multiselect(
        "Select Console(s)",
        options=filtered_consoles,
        default=None,
    )

    # ----- Year Range Filter -----
    year_min, year_max = int(vg_data["year_new"].min()), int(vg_data["year_new"].max())
    year_range = st.slider("Select Year Range", year_min, year_max, (year_min, year_max))

    submit_button = st.form_submit_button(label="Apply Filters 🔍")

# ---------------- Filter Data Function ----------------
@st.cache_data
def filter_data(vg_data, genres, publishers, consoles, year_range):
    df = vg_data.copy()
    if genres:
        df = df[df["genre"].isin(genres)]
    if publishers:
        df = df[df["publisher"].isin(publishers)]
    if consoles:
        df = df[df["console"].isin(consoles)]
    df = df[(df["year_new"] >= year_range[0]) & (df["year_new"] <= year_range[1])]
    return df

df = filter_data(vg_data, genres, publishers, consoles, year_range) if submit_button else vg_data.copy()

# ---------------- Main Dashboard ----------------
st.title("🎮 Interactive Video Game Sales Dashboard")

if not df.empty:
    # ----- KPI Metrics -----
    avg_year = int(df["year_new"].mean())
    total_sales = df["total_sales"].sum()
    count_games = df.shape[0]

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("📅 Avg Release Year", avg_year)
    kpi2.metric("🎮 Number of Games", count_games)
    kpi3.metric("💰 Total Sales (M)", f"{round(total_sales, 2)} M")

    # ----- Charts -----
    fig_col1, fig_col2 = st.columns(2)

    # 📈 Yearly Sales Trend
    with fig_col1:
        st.markdown("### 📈 Yearly Sales Trend")
        yearly_sales = df.groupby("year_new", as_index=False)["total_sales"].sum()
        fig_line = px.line(yearly_sales, x="year_new", y="total_sales", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

    # 🥧 Sales Share by Console
    with fig_col2:
        st.markdown("### 🥧 Sales Share by Console")
        custom_colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3", "#FF6692"]
        fig_pie = px.pie(
            df,
            names="console",
            values="total_sales",
            hole=0.4,
            color_discrete_sequence=custom_colors
        )
        fig_pie.update_traces(textinfo="percent+label")
        fig_pie.update_layout(showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

    # 📊 Regional Sales Breakdown
    st.markdown("### 📊 Regional Sales Breakdown")
    region_sales = df.melt(
        id_vars=["title"],
        value_vars=["na_sales", "jp_sales", "pal_sales", "other_sales"],
        var_name="Region",
        value_name="Sales"
    )
    fig_bar = px.bar(region_sales, x="Region", y="Sales", color="Region", barmode="group")
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.warning("⚠️ No data matches your selected filters. Try adjusting them.")
