import numpy as np
import streamlit as st
import plotly.graph_objects as go
import time

# Custom CSS for Themed Styling
custom_css = '''
<style>
body {
    background-color: #f5f5f5; /* Light gray background */
    font-family: "Arial", sans-serif;
}
h1 {
    color: #4CAF50; /* Green title */
    text-align: center;
}
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 5px;
    padding: 5px 20px;
    font-size: 16px;
}
.stButton > button:hover {
    background-color: #45a049; /* Hover effect */
}
</style>
'''
st.markdown(custom_css, unsafe_allow_html=True)

# Initialize session state for slope and intercept
if "slope" not in st.session_state:
    st.session_state.slope = 1.0
if "intercept" not in st.session_state:
    st.session_state.intercept = 1.0

# Streamlit App Title
st.title("📈 Interactive Linear Regression App")

# Introduction with divider
st.write("### Welcome to the Linear Regression Visualizer")
st.markdown("---")

st.write("""
Linear regression is a fundamental technique in data analysis and machine learning.
This app lets you interactively adjust the parameters of a regression line, visualize the impact on the total error, 
and compare your adjustments with the best-fit line computed automatically.
""")

# Add a section divider
st.markdown("---")

# Generate data
np.random.seed(42)
x = np.linspace(0, 10, 50)
y = 3 * x + 5 + np.random.normal(0, 2, size=x.shape)

# Customizable line using number inputs
st.write("### Adjust Slope and Intercept")
slope = st.number_input(
    "Slope", value=st.session_state.slope, step=0.1, min_value=-10.0, max_value=10.0
)
intercept = st.number_input(
    "Intercept", value=st.session_state.intercept, step=0.1, min_value=-20.0, max_value=20.0
)

# Update session state with current values
st.session_state.slope = slope
st.session_state.intercept = intercept

# Regression line based on user input
y_pred = slope * x + intercept

# Total error calculation
total_error = np.sum((y - y_pred) ** 2)

# Add progress bar while processing
with st.spinner("Processing your inputs..."):
    time.sleep(1)
st.success("Done!")

# Plotly figure for the main plot
fig = go.Figure()

# Scatter plot of data points
fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Data Points'))

# Line for user-adjusted regression
fig.add_trace(
    go.Scatter(
        x=x,
        y=y_pred,
        mode='lines',
        line=dict(color='red', width=3),
        name=f"Your Line (y = {slope:.2f}x + {intercept:.2f})"
    )
)

# Best-fit line
best_slope, best_intercept = np.polyfit(x, y, 1)
fig.add_trace(
    go.Scatter(
        x=x,
        y=best_slope * x + best_intercept,
        mode='lines',
        line=dict(color='purple', dash='dash'),
        name=f"Best Fit Line (y = {best_slope:.2f}x + {best_intercept:.2f})"
    )
)

# Layout updates to enlarge the graph
fig.update_layout(
    title="Interactive Regression Plot",
    xaxis_title="X",
    yaxis_title="Y",
    showlegend=True,
    height=600,  # Increased height
    width=900,   # Increased width
)

# Show Plotly chart with a unique key
st.plotly_chart(fig, key="main_plot")

# Add section for Total Error
st.markdown("---")
st.write("### Total Error")
st.metric(label="Total Error", value=f"{total_error:.2f}", delta="Lower is better")

# Total error plot
fig_error = go.Figure()

# Total error as a single horizontal bar
fig_error.add_trace(
    go.Bar(
        x=[total_error],  # Bar length corresponds to the error value
        y=["Total Error"],  # Label for the bar
        orientation='h',  # Horizontal orientation
        marker=dict(color='green')  # Bar color
    )
)

# Layout update for error plot
fig_error.update_layout(
    title="Total Error Bar Chart",
    xaxis_title="Error Value",
    yaxis_title="",
    height=250,  # Adjusting height for error plot
    width=900,   # Same width as the main plot for consistency
    xaxis=dict(range=[0, max(total_error + 50, total_error * 1.2)])  # Dynamic range
)

# Show the error plot with a unique key
st.plotly_chart(fig_error, key="error_plot")

# Tabs for organization
tab1, tab2 = st.tabs(["📊 Interactive Plot", "📚 About Linear Regression"])
with tab1:
    st.write("### Interactive Plot Section")
    st.plotly_chart(fig, key="tab_plot")

with tab2:
    st.write("### About Linear Regression")
    st.write("""
    Linear regression is a method for modeling the relationship between an independent variable (X) and a dependent variable (Y) by fitting a straight line.
    The equation for the line is:

    **y = mx + b**

    where:
    - **m** is the slope.
    - **b** is the y-intercept.

    The total error measures how well the line fits the data and is minimized in the best-fit line.
    """)
