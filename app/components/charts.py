import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Custom Dark Theme Colors for Plotly matching the SaaS UI
CHART_THEME = {
    'layout': go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#e2e8f0', 'family': 'Inter, sans-serif'},
        title={'font': {'size': 18, 'color': '#ffffff'}},
        legend={'font': {'color': '#94a3b8'}, 'orientation': 'h', 'y': -0.2},
        xaxis={'gridcolor': '#334155', 'zerolinecolor': '#334155'},
        yaxis={'gridcolor': '#334155', 'zerolinecolor': '#334155'}
    )
}

COLOR_PALETTE = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']

def get_chart_kwargs():
    """Returns common styling arguments for plotly express charts"""
    return {
        "template": CHART_THEME,
        "color_discrete_sequence": COLOR_PALETTE
    }

def render_bar_chart(df, x_col, y_col, title="Closures per Recruiter"):
    """
    Renders a bar chart for categorical comparisons.
    """
    if df.empty or x_col not in df.columns or y_col not in df.columns:
        st.warning(f"Data not available for {title}.")
        return

    # Basic aggregation if needed, assuming the df is already aggregated or we sum
    try:
        grouped = df.groupby(x_col, as_index=False)[y_col].sum()
        grouped = grouped.sort_values(by=y_col, ascending=False)
        
        fig = px.bar(
            grouped, 
            x=x_col, 
            y=y_col,
            title=title,
            labels={x_col: "Recruiter", y_col: "Closures"},
            **get_chart_kwargs()
        )
        
        fig.update_traces(marker_line_width=0, opacity=0.9)
        fig.update_layout(margin=dict(t=50, l=10, r=10, b=10))
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering chart: {e}")

def render_pie_chart(df, names_col, values_col, title="Contribution Percentage"):
    """
    Renders a donut/pie chart.
    """
    if df.empty or names_col not in df.columns or values_col not in df.columns:
        st.warning(f"Data not available for {title}.")
        return
        
    try:
        grouped = df.groupby(names_col, as_index=False)[values_col].sum()
        
        fig = px.pie(
            grouped, 
            names=names_col, 
            values=values_col,
            title=title,
            hole=0.6,
            **get_chart_kwargs()
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(margin=dict(t=50, l=10, r=10, b=10))
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering chart: {e}")

def render_line_chart(df, x_col, y_col, color_col=None, title="Monthly Trends"):
    """
    Renders a line chart for time series or trends.
    """
    if df.empty or x_col not in df.columns or y_col not in df.columns:
        st.warning(f"Data not available for {title}.")
        return

    try:
        fig = px.line(
            df, 
            x=x_col, 
            y=y_col,
            color=color_col,
            title=title,
            markers=True,
            line_shape='spline', # Smooth lines
            **get_chart_kwargs()
        )
        
        fig.update_traces(line=dict(width=3))
        fig.update_layout(margin=dict(t=50, l=10, r=10, b=10))
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering chart: {e}")

def render_heatmap(df, x_col, y_col, z_col, title="Productivity Heatmap"):
    """
    Renders a density heatmap for correlation or productivity spread.
    """
    if df.empty or x_col not in df.columns or y_col not in df.columns or z_col not in df.columns:
        st.warning(f"Data not available for {title}.")
        return

    try:
        fig = px.density_heatmap(
            df, 
            x=x_col, 
            y=y_col, 
            z=z_col,
            title=title,
            color_continuous_scale="Viridis",
            **get_chart_kwargs()
        )
        
        fig.update_layout(margin=dict(t=50, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering chart: {e}")
