import streamlit as st

def kpi_card(title, value, subtitle="", icon="📊", variant="primary"):
    """
    Renders a custom glassmorphism KPI card using injected HTML.
    CSS classes are expected to be defined in style.css and loaded via main.py.
    """
    
    html = f"""
    <div class="kpi-card {variant}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-content">
            <h3 class="kpi-title">{title}</h3>
            <h2 class="kpi-value"><span class="counter" data-target="{value}">{value}</span></h2>
            <p class="kpi-subtitle">{subtitle}</p>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def animated_insights_panel(insights):
    """
    Renders an AI-style animated insight box.
    """
    html = """
    <div class="insights-panel">
        <div class="insights-header">
            <span class="insights-icon">✨</span> AI Insights
        </div>
        <div class="insights-content">
            <ul class="typing-list">
    """
    
    for insight in insights:
        html += f"<li>{insight}</li>"
        
    html += """
            </ul>
        </div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
