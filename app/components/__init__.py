def inject_assets():
    """
    Reads CSS and JS files and injects them into the Streamlit app using markdown.
    """
    import os
    import streamlit as st
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Read CSS
    css_path = os.path.join(current_dir, '..', 'static', 'style.css')
    try:
        with open(css_path, 'r') as f:
            css = f"<style>{f.read()}</style>"
            st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    
    # Read JS
    js_path = os.path.join(current_dir, '..', 'static', 'script.js')
    try:
        with open(js_path, 'r') as f:
            js = f"<script>{f.read()}</script>"
            # For scripts to run in Streamlit via markdown, they sometimes need an HTML component wrapping
            import streamlit.components.v1 as components
            components.html(f"<script>{f.read()}</script>", height=0, width=0)
    except FileNotFoundError:
        pass
