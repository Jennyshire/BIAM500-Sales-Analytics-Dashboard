# -*- coding: utf-8 -*-
#****************************************************
# Spyder Editor
#
# BIAM500 - Business Intelligence, Analytics, and AI
# 
# LAB 8 CAPSTONE PROJECT - INTERACTIVE EXECUTIVE DASHBOARD
#
# This is Week 8 Lab - - Business Case Analytics Project
# By Jeanette Shire.
#  Option A: Sales Analytics
#
#  Analyze:
#
#  * Revenue performance
#  * Product or regional trends
#  * Sales efficiency
#
# Step 2: Access DeVry Desktop and Create and Set Working Directory in Pythnon
# Step 3: Open Spyder and Set and confirm the Working Directory
#
#*****************************************************

# ============================================================
# INTERACTIVE SALES ANALYTICS DASHBOARD
# Streamlit + Plotly
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title(
    "Sales Analytics Executive Dashboard: "
    "Seasonality and Product Trends"
)

st.caption(
    "Interactive analysis of revenue patterns, seasonality, "
    "regional performance, and product-line trends."
)


# ============================================================
# LOAD DATA
# ============================================================

# Change this path if necessary
file_path = "week8_business_case_data.xlsx"

df = pd.read_excel(file_path)


# ============================================================
# PREPARE DATA
# ============================================================

df["TransactionDate"] = pd.to_datetime(
    df["TransactionDate"]
)

df["Year"] = df["TransactionDate"].dt.year
df["MonthNumber"] = df["TransactionDate"].dt.month
df["MonthName"] = df["TransactionDate"].dt.strftime("%b")
df["Quarter"] = df["TransactionDate"].dt.quarter

df["QuarterLabel"] = (
    "Q" + df["Quarter"].astype(str)
)

# ------------------------------------------------------------
# Working assumption:
# TotalCost is being used as Revenue for this analysis.
# ------------------------------------------------------------


# ============================================================
# SIDEBAR FILTERS / SLICERS
# ============================================================

st.sidebar.header("Dashboard Filters")

# ------------------------------------------------------------
# YEAR FILTER
# ------------------------------------------------------------

year_options = sorted(
    df["Year"].dropna().unique()
)

selected_years = st.sidebar.multiselect(
    "Year",
    options=year_options,
    default=year_options
)

# ------------------------------------------------------------
# QUARTER FILTER
# ------------------------------------------------------------

quarter_options = [
    "Q1",
    "Q2",
    "Q3",
    "Q4"
]

selected_quarters = st.sidebar.multiselect(
    "Quarter",
    options=quarter_options,
    default=quarter_options
)

# ------------------------------------------------------------
# REGION FILTER
# ------------------------------------------------------------

region_options = sorted(
    df["Region"].dropna().unique()
)

selected_regions = st.sidebar.multiselect(
    "Region",
    options=region_options,
    default=region_options
)

# ------------------------------------------------------------
# PRODUCT FILTER
# ------------------------------------------------------------

product_options = sorted(
    df["ProductLine"].dropna().unique()
)

selected_products = st.sidebar.multiselect(
    "Product Line",
    options=product_options,
    default=product_options
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["Year"].isin(selected_years))
    &
    (df["QuarterLabel"].isin(selected_quarters))
    &
    (df["Region"].isin(selected_regions))
    &
    (df["ProductLine"].isin(selected_products))
].copy()


# ============================================================
# VALIDATE FILTER RESULT
# ============================================================

if filtered_df.empty:

    st.warning(
        "No records match the current filter selections."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = (
    filtered_df["TotalCost"].sum()
)

total_units = (
    filtered_df["Units"].sum()
)

if total_units > 0:

    average_revenue_per_unit = (
        total_revenue / total_units
    )

else:

    average_revenue_per_unit = 0


revenue_by_region = (
    filtered_df
    .groupby("Region")["TotalCost"]
    .sum()
    .sort_values(
        ascending=False
    )
)

revenue_by_product = (
    filtered_df
    .groupby("ProductLine")["TotalCost"]
    .sum()
    .sort_values(
        ascending=False
    )
)

top_region = (
    revenue_by_region.index[0]
)

top_region_revenue = (
    revenue_by_region.iloc[0]
)

top_product = (
    revenue_by_product.index[0]
)

top_product_revenue = (
    revenue_by_product.iloc[0]
)


# ============================================================
# KPI CARDS
# ============================================================

st.subheader(
    "Executive KPI Summary"
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        label="Total Revenue",
        value=f"${total_revenue:,.2f}"
    )

with col2:

    st.metric(
        label="Average Revenue per Unit",
        value=f"${average_revenue_per_unit:,.2f}"
    )

with col3:

    st.metric(
        label="Top Region",
        value=top_region,
        delta=f"${top_region_revenue:,.0f}"
    )

with col4:

    st.metric(
        label="Top Product Line",
        value=top_product,
        delta=f"${top_product_revenue:,.0f}"
    )


# ============================================================
# EXECUTIVE MESSAGE
# ============================================================

st.info(
    "Annual and quarterly totals can appear stable while "
    "product-level and seasonal analysis reveals important "
    "patterns, peaks, valleys, and opportunities."
)


# ============================================================
# ROW 1
# QUARTERLY REVENUE + REGION REVENUE
# ============================================================

left1, right1 = st.columns(2)


# ------------------------------------------------------------
# QUARTERLY REVENUE BY PRODUCT
# ------------------------------------------------------------

with left1:

    st.subheader(
        "Quarterly Revenue by Product Line"
    )

    quarterly_data = (
        filtered_df
        .groupby([
            "Quarter",
            "ProductLine"
        ])["TotalCost"]
        .sum()
        .reset_index()
    )

    quarterly_data[
        "QuarterLabel"
    ] = (
        "Q"
        + quarterly_data[
            "Quarter"
        ].astype(str)
    )

    fig_quarter = px.bar(
        quarterly_data,
        x="QuarterLabel",
        y="TotalCost",
        color="ProductLine",
        barmode="group",
        labels={
            "QuarterLabel": "Quarter",
            "TotalCost": "Revenue",
            "ProductLine": "Product Line"
        },
        title=(
            "Quarterly Revenue by Product Line"
        )
    )

    fig_quarter.update_layout(
        yaxis_tickprefix="$",
        yaxis_tickformat=",",
        legend_title_text=(
            "Product Line"
        )
    )

    st.plotly_chart(
        fig_quarter,
        use_container_width=True
    )


# ------------------------------------------------------------
# REVENUE BY REGION
# ------------------------------------------------------------

with right1:

    st.subheader(
        "Revenue by Region"
    )

    region_data = (
        filtered_df
        .groupby("Region")[
            "TotalCost"
        ]
        .sum()
        .reset_index()
        .sort_values(
            "TotalCost",
            ascending=False
        )
    )

    fig_region = px.bar(
        region_data,
        x="Region",
        y="TotalCost",
        labels={
            "TotalCost": "Revenue"
        },
        title="Revenue by Region"
    )

    fig_region.update_layout(
        yaxis_tickprefix="$",
        yaxis_tickformat=","
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


# ============================================================
# ROW 2
# MONTHLY SEASONALITY + PRODUCT TOTALS
# ============================================================

left2, right2 = st.columns(2)


# ------------------------------------------------------------
# MONTHLY SEASONALITY
# ------------------------------------------------------------

with left2:

    st.subheader(
        "Monthly Revenue Seasonality"
    )

    monthly_data = (
        filtered_df
        .groupby([
            "MonthNumber",
            "MonthName",
            "ProductLine"
        ])["TotalCost"]
        .sum()
        .reset_index()
        .sort_values(
            "MonthNumber"
        )
    )

    month_order = [
        "Jan", "Feb", "Mar",
        "Apr", "May", "Jun",
        "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec"
    ]

    fig_month = px.line(
        monthly_data,
        x="MonthName",
        y="TotalCost",
        color="ProductLine",
        markers=True,
        category_orders={
            "MonthName": month_order
        },
        labels={
            "MonthName": "Month",
            "TotalCost": "Revenue",
            "ProductLine": "Product Line"
        },
        title=(
            "Monthly Revenue by Product Line"
        )
    )

    fig_month.update_layout(
        yaxis_tickprefix="$",
        yaxis_tickformat=","
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )


# ------------------------------------------------------------
# PRODUCT TOTALS
# ------------------------------------------------------------

with right2:

    st.subheader(
        "Revenue by Product Line"
    )

    product_data = (
        filtered_df
        .groupby("ProductLine")[
            "TotalCost"
        ]
        .sum()
        .reset_index()
        .sort_values(
            "TotalCost",
            ascending=False
        )
    )

    fig_product = px.bar(
        product_data,
        x="ProductLine",
        y="TotalCost",
        labels={
            "ProductLine":
                "Product Line",
            "TotalCost":
                "Revenue"
        },
        title=(
            "Total Revenue by Product Line"
        )
    )

    fig_product.update_layout(
        yaxis_tickprefix="$",
        yaxis_tickformat=","
    )

    st.plotly_chart(
        fig_product,
        use_container_width=True
    )


# ============================================================
# DEEPER DIVE
# INTERACTIVE REGRESSION
# ============================================================

st.divider()

st.subheader(
    "Deeper Dive: "
    "Underlying Revenue Trends"
)


# ============================================================
# MONTHLY REGRESSION DATA
# ============================================================

regression_source = (
    filtered_df
    .groupby([
        pd.Grouper(
            key="TransactionDate",
            freq="MS"
        ),
        "ProductLine"
    ])["TotalCost"]
    .sum()
    .reset_index()
)

regression_results = []

fig_regression = go.Figure()


# ============================================================
# RUN REGRESSION BY PRODUCT
# ============================================================

for product in sorted(
    regression_source[
        "ProductLine"
    ].unique()
):

    product_data = (
        regression_source[
            regression_source[
                "ProductLine"
            ] == product
        ]
        .copy()
        .sort_values(
            "TransactionDate"
        )
    )

    # Need at least 2 observations
    if len(product_data) < 2:

        continue

    product_data["Time"] = np.arange(
        1,
        len(product_data) + 1
    )

    slope, intercept = np.polyfit(
        product_data["Time"],
        product_data["TotalCost"],
        1
    )

    product_data[
        "PredictedRevenue"
    ] = (
        intercept
        +
        slope
        * product_data["Time"]
    )

    actual = (
        product_data["TotalCost"]
    )

    predicted = (
        product_data[
            "PredictedRevenue"
        ]
    )

    ss_res = np.sum(
        (actual - predicted) ** 2
    )

    ss_tot = np.sum(
        (
            actual
            - actual.mean()
        ) ** 2
    )

    if ss_tot > 0:

        r_squared = (
            1
            - ss_res / ss_tot
        )

    else:

        r_squared = 0


    regression_results.append(
        {
            "Product Line":
                product,

            "Slope per Month":
                slope,

            "R Squared":
                r_squared
        }
    )


    # --------------------------------------------------------
    # Scatter
    # --------------------------------------------------------

    fig_regression.add_trace(

        go.Scatter(
            x=product_data[
                "TransactionDate"
            ],

            y=product_data[
                "TotalCost"
            ],

            mode="markers",

            name=product,

            hovertemplate=(
                f"<b>{product}</b><br>"
                "Month: %{x|%b %Y}<br>"
                "Revenue: $%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )


    # --------------------------------------------------------
    # Trend line
    # --------------------------------------------------------

    fig_regression.add_trace(

        go.Scatter(
            x=product_data[
                "TransactionDate"
            ],

            y=product_data[
                "PredictedRevenue"
            ],

            mode="lines",

            name=(
                f"{product} Trend"
            ),

            hovertemplate=(
                f"<b>{product} Trend</b><br>"
                "Predicted Revenue: "
                "$%{y:,.2f}"
                "<extra></extra>"
            )
        )
    )


# ============================================================
# REGRESSION CHART FORMAT
# ============================================================

fig_regression.update_layout(

    title=(
        "Monthly Revenue and "
        "Regression Trends"
    ),

    xaxis_title="Month",

    yaxis_title=(
        "Monthly Revenue"
    ),

    yaxis_tickprefix="$",

    yaxis_tickformat=",",

    hovermode="closest",

    height=550
)

st.plotly_chart(
    fig_regression,
    use_container_width=True
)


# ============================================================
# REGRESSION RESULTS TABLE
# ============================================================

regression_table = pd.DataFrame(
    regression_results
)

if not regression_table.empty:

    regression_table[
        "Slope per Month"
    ] = regression_table[
        "Slope per Month"
    ].map(
        lambda x:
        f"${x:+,.2f}"
    )

    regression_table[
        "R Squared"
    ] = regression_table[
        "R Squared"
    ].map(
        lambda x:
        f"{x:.4f}"
    )

    st.subheader(
        "Trend Strength Summary"
    )

    st.dataframe(
        regression_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# INTERPRETATION
# ============================================================

st.divider()

st.subheader(
    "Business Interpretation"
)

st.write(
    """
    The interactive dashboard allows leadership to move beyond
    company-wide revenue totals and examine how performance changes
    by year, quarter, region, and product line.

    Seasonal peaks and valleys can be isolated using the filters.
    This makes it possible to identify periods of strong demand,
    periods of underperformance, and differences in product behavior
    that may not be visible in annual totals.

    Leadership can use these findings to evaluate whether inventory,
    marketing campaigns, promotions, and regional strategies should
    be adjusted for specific products and time periods.
    """
)


# ============================================================
# OPTIONAL RAW DATA VIEW
# ============================================================

with st.expander(
    "View Filtered Data"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )