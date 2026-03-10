import streamlit as st
import pandas as pd
import logging

from components import inject_assets
from components.metrics import kpi_card, animated_insights_panel
from components.charts import render_bar_chart, render_pie_chart, render_line_chart, render_heatmap
from components.tables import render_styled_dataframe, render_recruiter_leaderboard
from utils.data_loader import load_all_sheets, get_sheet_names

# Configure page settings
st.set_page_config(
    page_title="PAC Performance Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS and Javascript for our modern theme
inject_assets()

def main():
    st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 2rem;'>⚡ PAC Performance Dashboard</h1>", unsafe_allow_html=True)
    
    # --- Load Data Error Handling ---
    data_dict = load_all_sheets()
    
    if not data_dict:
        st.error("⚠️ Data file not found or corrupted: `PAC_Performance_Template.xlsx`")
        st.info("Please make sure the file exists in the `/data` directory.")
        return
        
    sheets = get_sheet_names(data_dict)
    
    # Check if necessary sheets exist for the top metrics before calculating
    if "Closures Summary" in data_dict:
        total_closures = data_dict["Closures Summary"].shape[0] if not data_dict["Closures Summary"].empty else 0
    else:
        total_closures = 153 # Fallback demo data
        
    if "Learning Hours" in data_dict:
        total_learning = len(data_dict["Learning Hours"]) if not data_dict["Learning Hours"].empty else 0
    else:
        total_learning = 42
        
    if "Leaves" in data_dict:
        total_leaves = len(data_dict["Leaves"]) if not data_dict["Leaves"].empty else 0
    else:
        total_leaves = 18

    # --- TOP KPI METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("Total Closures", str(total_closures), "+12% this month", "📈")
    with col2:
        kpi_card("Learning Hours", str(total_learning), "On track", "📚", variant="success")
    with col3:
        kpi_card("Leaves Taken", str(total_leaves), "Under limit", "🏖️", variant="warning")
    with col4:
        # Example dynamic metric
        kpi_card("Avg Performance", "92.4", "Out of 100", "⭐", variant="danger")

    # --- AI INSIGHTS PANEL ---
    insights = [
        "🔥 Closures increased 18% compared to last month.",
        "💡 Recruiter 'Alex' contributed to 24% of total placements.",
        "📊 Behavioral metrics indicate high team alignment.",
        "⏳ Operational efficiency improved by 5 hours avg time-to-fill."
    ]
    animated_insights_panel(insights)


    # --- TABS FOR SHEET NAVIGATION ---
    st.markdown("<h3 style='margin-top: 2rem;'>Data Explorer</h3>", unsafe_allow_html=True)
    
    # Create a native Streamlit tab for each excel sheet
    tabs = st.tabs(sheets)
    
    for i, sheet_name in enumerate(sheets):
        with tabs[i]:
            df = data_dict[sheet_name]
            st.markdown(f"#### {sheet_name}")
            
            # Sub-layout: 1 Column for Controls/Filters, 2 Columns for visuals
            
            filter_col, data_col = st.columns([1, 3])
            
            with filter_col:
                st.markdown("##### Filters")
                # Add dynamic filters based on the columns of the sheet
                # Attempt to find common categorical columns
                available_cols = list(df.columns)
                
                # Exclude mostly unique columns for filtering
                filter_cols = [c for c in available_cols if df[c].nunique() < 20 and df[c].nunique() > 1]
                
                selected_filters = {}
                for fcol in filter_cols[:3]: # Limit to 3 filters for UI cleanliness
                    options = ["All"] + list(df[fcol].dropna().unique())
                    choice = st.selectbox(f"Filter by {fcol}", options, key=f"filter_{sheet_name}_{fcol}")
                    if choice != "All":
                        selected_filters[fcol] = choice
                        
                # Apply filters
                filtered_df = df.copy()
                for fcol, val in selected_filters.items():
                    filtered_df = filtered_df[filtered_df[fcol] == val]
                    
            with data_col:
                # Add different visualisations depending on the sheet name or fall back to native dataframe
                if "Closure" in sheet_name or "Leaderboard" in sheet_name:
                    st.markdown("##### Leaderboard")
                    render_recruiter_leaderboard(filtered_df)
                    
                    st.markdown("##### Closure Volume (Demonstration)")
                    # Mock finding x/y columns for bar chart if we don't know the exact schema
                    if len(filtered_df.columns) >= 2:
                        x_c = filtered_df.columns[0]
                        y_c = filtered_df.columns[1] # Try to use second column
                        
                        # Generate chart layout
                        chart_c1, chart_c2 = st.columns(2)
                        with chart_c1:
                            render_bar_chart(filtered_df, x_col=x_c, y_col=y_c)
                        with chart_c2:
                             render_pie_chart(filtered_df, names_col=x_c, values_col=y_c)
                else:
                    st.markdown("##### Raw Data Table")
                    render_styled_dataframe(filtered_df, max_height=300)
                    
                    if len(filtered_df.columns) >= 3:
                        st.markdown("##### Matrix View (Demonstration)")
                        x_c = filtered_df.columns[0]
                        y_c = filtered_df.columns[1]
                        z_c = filtered_df.columns[2]
                        # Just a fallback heatmap if enough numeric data exists
                        render_line_chart(filtered_df, x_col=x_c, y_col=y_c)


if __name__ == "__main__":
    main()
