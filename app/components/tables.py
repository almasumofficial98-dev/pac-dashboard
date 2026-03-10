import streamlit as st

def render_styled_dataframe(df, max_height=400):
    """
    Renders a pandas dataframe using Streamlit's native dataframe,
    which we will style globally using CSS.
    """
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=max_height
    )

def render_recruiter_leaderboard(df):
    """
    Creates a custom HTML/CSS leaderboard table for recruiters.
    Assumes df has columns like 'Recruiter Name', 'Closures', 'Score', 'Performance Category'
    """
    
    # Try to map columns generically if exact names aren't present
    cols = list(df.columns)
    
    # We'll just build a clean HTML table and style it
    html = """
    <div class="leaderboard-container">
        <table class="modern-table">
            <thead>
                <tr>
    """
    
    for col in cols:
        html += f"<th>{col}</th>"
    
    html += """
                </tr>
            </thead>
            <tbody>
    """
    
    # Limit to top 10 for the leaderboard
    display_df = df.head(10)
    
    for _, row in display_df.iterrows():
        html += "<tr>"
        for i, col in enumerate(cols):
            val = row[col]
            
            # Add some color coding for categories if it exists
            if isinstance(val, str) and ("Excellent" in val or "High" in val):
                html += f'<td><span class="badge badge-success">{val}</span></td>'
            elif isinstance(val, str) and ("Average" in val or "Medium" in val):
                html += f'<td><span class="badge badge-warning">{val}</span></td>'
            elif isinstance(val, str) and ("Poor" in val or "Low" in val):
                html += f'<td><span class="badge badge-danger">{val}</span></td>'
            else:
                html += f"<td>{val}</td>"
                
        html += "</tr>"
        
    html += """
            </tbody>
        </table>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
