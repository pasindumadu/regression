import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

# Page Configuration
st.set_page_config(
    layout="wide", page_title="Interactive Linear Regression", page_icon="📈"
)

# Dark Theme Styling
custom_css = '''
<style>
body {
    background-color: #121212;
    color: #FFFFFF;
}
h1, h2, h3 {
    color: #FFFFFF;
}
.stButton > button {
    background-color: #1E88E5;
    color: white;
}
.stButton > button:hover {
    background-color: #1565C0;
}
</style>
'''
st.markdown(custom_css, unsafe_allow_html=True)

# Initialize session state for slope and intercept
if "slope" not in st.session_state:
    st.session_state.slope = 1.0
if "intercept" not in st.session_state:
    st.session_state.intercept = 1.0

# Tabs for interactive visualization and theory
tab1, tab2 = st.tabs(["📊 Interactive Regression", "📚 What is Linear Regression?"])

with tab1:
    # App Title
    st.title("📈 Interactive Linear Regression App")
    st.subheader("Explore Regression Models and Minimize Error")

    # Introduction Section
    st.markdown("""
    This app lets you:
    - Adjust the slope (**m**) and intercept (**b**) of a regression line.
    - Visualize your adjusted line and compare it to the optimal best-fit line.
    - View and minimize the **total error** dynamically.
    """)
    st.markdown("---")

    # Data Generation
    np.random.seed(42)
    x = np.linspace(0, 10, 50)
    y = 3 * x + 5 + np.random.normal(0, 2, size=x.shape)

    # Input Controls for Slope and Intercept
    st.markdown("### 🔧 Adjust Parameters")
    col1, col2 = st.columns(2)
    with col1:
        slope = st.number_input(
            "Slope (m)", value=st.session_state.slope, step=0.1, min_value=-10.0, max_value=10.0
        )
    with col2:
        intercept = st.number_input(
            "Intercept (b)", value=st.session_state.intercept, step=0.1, min_value=-20.0, max_value=20.0
        )

    # Update Session State
    st.session_state.slope = slope
    st.session_state.intercept = intercept

    # Regression Line Calculations
    y_pred = slope * x + intercept
    best_slope, best_intercept = np.polyfit(x, y, 1)
    y_best_fit = best_slope * x + best_intercept
    total_error = np.sum((y - y_pred) ** 2)

    # Scatter Plot with Regression Lines
    data = pd.DataFrame({"X": x, "Y": y, "Y_pred": y_pred, "Y_best_fit": y_best_fit})
    scatter = alt.Chart(data).mark_circle(size=70).encode(
        x="X", y="Y", tooltip=["X", "Y"]
    ).properties(width=800, height=400)

    user_line = alt.Chart(data).mark_line(color="red", strokeWidth=3).encode(
        x="X", y="Y_pred", tooltip=["X", "Y_pred"]
    )

    best_fit_line = alt.Chart(data).mark_line(color="purple", strokeDash=[5, 5], strokeWidth=2).encode(
        x="X", y="Y_best_fit", tooltip=["X", "Y_best_fit"]
    )

    chart = scatter + user_line + best_fit_line
    chart = chart.properties(
        title="📊 Regression Line Visualization",
    ).configure_title(
        fontSize=18, anchor="middle", color="lightgreen"
    )

    # Display Main Chart
    st.altair_chart(chart, use_container_width=True)

    # Dynamic Horizontal Total Error Bar Chart
    st.markdown("---")
    st.markdown("### 🔢 Total Error")

    error_data = pd.DataFrame({
        "Error Type": ["Current Error"],
        "Error Value": [total_error]
    })
    error_chart = alt.Chart(error_data).mark_bar(size=30).encode(
        x=alt.X("Error Value", axis=alt.Axis(title="Error Magnitude")),
        y=alt.Y("Error Type", axis=None),
        color=alt.condition(
            alt.datum["Error Value"] < 200,
            alt.value("green"),  # Green for low error
            alt.value("red")    # Red for high error
        ),
        tooltip=["Error Value"]
    ).properties(width=600, height=100)

    # Adjust columns for mobile view
    error_col1, error_col2 = st.columns([4, 1])
    with error_col1:
        st.altair_chart(error_chart, use_container_width=True)
    with error_col2:
        st.write(f"### **{total_error:.2f}**")

    # Error Evaluation
    if total_error < 50:
        st.success("Great Fit! 🎉")
    elif total_error < 200:
        st.warning("Good Fit! Could Improve 🧐")
    else:
        st.error("High Error! 🚨 Try Adjusting.")

    # Footer
    st.markdown("""
    ---
    <footer style="text-align: center; font-size: 12px; color: gray;">
        Developed by Pasindu Madhuranga | Powered by Streamlit
    </footer>
    """, unsafe_allow_html=True)

with tab2:
    st.write("### What is Linear Regression?")
    st.write("""
    Linear regression is a technique to model the relationship between two variables by fitting a straight line. 
    The line is represented by the equation:
    **y = mx + b**
    - **m**: Slope of the line
    - **b**: Intercept of the line

    The goal is to minimize the total error (sum of squared differences between predicted and actual values).

    In this app:
    - Adjust the slope (**m**) and intercept (**b**) manually and see how well your line fits.
    - Compare your adjustments to the **optimal best-fit line** computed automatically.
    - Watch the **total error** change dynamically as you make adjustments.
    """)

    st.markdown("---")
    with st.expander("Need Help?"):
        st.write("""
        - Use the **Slope (m)** and **Intercept (b)** sliders to adjust the line.
        - Observe how your line matches the data and how the error changes.
        """)
