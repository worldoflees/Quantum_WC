import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Employee Attrition Analysis Dashboard")

st.title("Employee Attrition Analysis Dashboard")
st.markdown("""
This interactive dashboard provides a comprehensive analysis of employee attrition, leveraging various
demographic, job-related, and satisfaction metrics. Explore different factors influencing attrition
to identify key areas for retention strategies.
""")

# --- Data Loading and Transformations ---
@st.cache_data
def load_and_transform_data(path):
    """
    Loads the employee attrition data and performs necessary transformations.
    """
    df = pd.read_csv(path)

    # Encode Attrition column
    df['Attrition_encoded'] = df['Attrition'].map({'No': 0, 'Yes': 1})

    # Bin MonthlyIncome column
    min_income = df['MonthlyIncome'].min()
    max_income = df['MonthlyIncome'].max()
    # Define bin edges and labels for 5 bins
    bins = [min_income, 40000, 80000, 120000, 160000, max_income + 1] # Add 1 to max to ensure max value is included
    labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    df['MonthlyIncome_bin'] = pd.cut(df['MonthlyIncome'], bins=bins, labels=labels, right=False)

    return df

# Load data
df_employee = load_and_transform_data("DA314_S10_EmployeeAttrition_Data_Practice (1).csv")

# --- Sidebar for Filtering ---
st.sidebar.header("Filter Options")

# Department filter
selected_department = st.sidebar.multiselect(
    "Select Department(s)",
    options=df_employee['Department'].unique(),
    default=list(df_employee['Department'].unique())
)

# Job Role filter
selected_job_role = st.sidebar.multiselect(
    "Select Job Role(s)",
    options=df_employee['JobRole'].unique(),
    default=list(df_employee['JobRole'].unique())
)

# Age Group filter
selected_age_group = st.sidebar.multiselect(
    "Select Age Group(s)",
    options=df_employee['AgeGroup'].unique(),
    default=list(df_employee['AgeGroup'].unique())
)

# Apply filters
filtered_df = df_employee[
    (df_employee['Department'].isin(selected_department)) &
    (df_employee['JobRole'].isin(selected_job_role)) &
    (df_employee['AgeGroup'].isin(selected_age_group))
]

st.subheader("Filtered Data Overview")
st.write(f"Displaying data for **{len(filtered_df)}** employees out of **{len(df_employee)}** total employees after applying filters.")
st.dataframe(filtered_df.head())

# --- Visualizations ---

st.header("1. Employee Distribution by Key Categorical Features")

categorical_features_for_dist = ['Attrition', 'Department', 'JobRole']
for feature in categorical_features_for_dist:
    st.subheader(f"Distribution of {feature}")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=filtered_df, x=feature, palette='viridis',hue=feature, legend=False, ax=ax)
    ax.set_title(f'Distribution of {feature}')
    ax.set_xlabel(feature)
    ax.set_ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    plt.close(fig) # Close the figure to free up memory

    if feature == 'Attrition':
        st.markdown("""
        **Insight**: This chart shows the overall distribution of 'No' (remaining) versus 'Yes' (attritted) employees within the filtered dataset. It provides an immediate sense of the attrition severity.
        """)
    elif feature == 'Department':
        st.markdown("""
        **Insight**: This plot illustrates the distribution of employees across different departments. It can highlight which departments are most represented in the filtered data.
        """)
    elif feature == 'JobRole':
        st.markdown("""
        **Insight**: Displays the number of employees in each job role. This is useful for identifying high-volume roles that might require more attention regarding employee retention.
        """)

st.header("2. Overall Employee Attrition Rate")
attrition_counts = filtered_df['Attrition'].value_counts()
fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
ax_pie.pie(attrition_counts, labels=attrition_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightcoral'])
ax_pie.set_title('Overall Employee Attrition Rate')
ax_pie.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig_pie)
plt.close(fig_pie)
st.markdown("""
**Insight**: This pie chart offers a clear and concise view of the overall employee attrition rate within the filtered population, serving as a critical high-level performance indicator.
""")

st.header("3. Distribution of Job Satisfaction Levels")
fig_js, ax_js = plt.subplots(figsize=(8, 6))
sns.countplot(data=filtered_df, x='JobSatisfaction', palette='viridis', hue='JobSatisfaction', legend=False, ax=ax_js)
ax_js.set_title('Distribution of Job Satisfaction Levels')
ax_js.set_xlabel('Job Satisfaction Level')
ax_js.set_ylabel('Number of Employees')
st.pyplot(fig_js)
plt.close(fig_js)
st.markdown("""
**Insight**: Understanding the distribution of job satisfaction helps gauge overall employee morale and potential areas of discontent. Low satisfaction levels can be a significant driver of attrition.
""")

st.header("4. Distribution of Years with Current Manager")
fig_ycm, ax_ycm = plt.subplots(figsize=(10, 6))
sns.countplot(data=filtered_df, x='YearsWithCurrManager', palette='viridis', hue='YearsWithCurrManager', legend=False, ax=ax_ycm)
ax_ycm.set_title('Distribution of Years with Current Manager')
ax_ycm.set_xlabel('Years with Current Manager')
ax_ycm.set_ylabel('Number of Employees')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig_ycm)
plt.close(fig_ycm)
st.markdown("""
**Insight**: This plot illustrates employee tenure with their current manager. Shorter tenures might suggest issues with management styles or career progression paths within teams.
""")

st.header("5. Distribution of OverTime Work")
fig_ot, ax_ot = plt.subplots(figsize=(8, 6))
sns.countplot(data=filtered_df, x='OverTime', palette='viridis', hue='OverTime', legend=False, ax=ax_ot)
ax_ot.set_title('Distribution of OverTime Work')
ax_ot.set_xlabel('OverTime')
ax_ot.set_ylabel('Number of Employees')
st.pyplot(fig_ot)
plt.close(fig_ot)
st.markdown("""
**Insight**: This visualization highlights the proportion of employees engaged in overtime work. High rates of overtime can lead to stress, burnout, and diminished work-life balance, impacting retention.
""")

st.header("6. Age Distribution by Attrition Status")
fig_age_attr, ax_age_attr = plt.subplots(figsize=(8, 6))
sns.violinplot(data=filtered_df, x='Attrition', y='Age', palette='viridis', hue='Attrition', legend=False, ax=ax_age_attr)
ax_age_attr.set_title('Age Distribution by Attrition Status')
ax_age_attr.set_xlabel('Attrition')
ax_age_attr.set_ylabel('Age')
st.pyplot(fig_age_attr)
plt.close(fig_age_attr)
st.markdown("""
**Insight**: This violin plot compares the age distribution of employees who attritted versus those who did not. It can reveal if younger or older employees are more likely to leave the company.
""")

st.header("7. Attrition Rate by Department")
fig_dept_attr, ax_dept_attr = plt.subplots(figsize=(10, 6))
sns.countplot(data=filtered_df, x='Department', hue='Attrition', palette='viridis', ax=ax_dept_attr)
ax_dept_attr.set_title('Attrition Rate by Department')
ax_dept_attr.set_xlabel('Department')
ax_dept_attr.set_ylabel('Number of Employees')
ax_dept_attr.legend(title='Attrition')
st.pyplot(fig_dept_attr)
plt.close(fig_dept_attr)
st.markdown("""
**Insight**: This chart breaks down attrition by department, making it easy to identify which departments face higher turnover challenges, potentially indicating specific issues within those teams.
""")

st.header("8. Monthly Income Distribution by Attrition Status")
fig_inc_attr, ax_inc_attr = plt.subplots(figsize=(10, 6))
sns.violinplot(data=filtered_df, x='Attrition', y='MonthlyIncome', palette='viridis', hue='Attrition', legend=False, ax=ax_inc_attr)
ax_inc_attr.set_title('Monthly Income Distribution by Attrition Status')
ax_inc_attr.set_xlabel('Attrition')
ax_inc_attr.set_ylabel('Monthly Income')
st.pyplot(fig_inc_attr)
plt.close(fig_inc_attr)
st.markdown("""
**Insight**: This plot compares the monthly income distributions of employees who stayed versus those who left. It can highlight whether compensation is a significant factor in employee attrition.
""")

st.header("9. Attrition Rate by OverTime Status")
fig_ot_attr, ax_ot_attr = plt.subplots(figsize=(8, 6))
sns.countplot(data=filtered_df, x='OverTime', hue='Attrition', palette='viridis', ax=ax_ot_attr)
ax_ot_attr.set_title('Attrition Rate by OverTime Status')
ax_ot_attr.set_xlabel('OverTime')
ax_ot_attr.set_ylabel('Number of Employees')
ax_ot_attr.legend(title='Attrition')
st.pyplot(fig_ot_attr)
plt.close(fig_ot_attr)
st.markdown("""
**Insight**: This chart directly compares attrition rates between employees who work overtime and those who don't, often revealing a higher propensity for attrition among overtime workers due to increased stress.
""")

st.header("10. Attrition by Job Satisfaction, Work-Life Balance, and Relationship Satisfaction")
g1 = sns.catplot(data=filtered_df, x='JobSatisfaction', y='Attrition_encoded', hue='WorkLifeBalance', col='RelationshipSatisfaction', kind='point', height=4, aspect=1.2, palette='viridis', errorbar=None)
g1.fig.suptitle('Attrition Rate by Job Satisfaction, Work-Life Balance, and Relationship Satisfaction', y=1.02)
st.pyplot(g1)
plt.close(g1.fig)
st.markdown("""
**Insight**: This multivariate plot reveals complex interactions. For instance, even with high job satisfaction, employees with poor work-life balance or low relationship satisfaction might still exhibit high attrition rates.
""")

st.header("11. Attrition by Years at Company, Age Group, and Job Role")
g2 = sns.catplot(data=filtered_df, x='YearsAtCompany', y='Attrition_encoded', hue='AgeGroup', col='JobRole', kind='point', height=4, aspect=1.2, col_wrap=3, palette='viridis', errorbar=None)
g2.fig.suptitle('Attrition Rate by Years at Company, Age Group, and Job Role', y=1.02)
st.pyplot(g2)
plt.close(g2.fig)
st.markdown("""
**Insight**: This visualization is crucial for understanding how tenure, age, and job role collectively impact attrition. It helps identify specific high-risk segments (e.g., young employees in certain roles leaving early).
""")

st.header("12. Attrition by Distance From Home, Business Travel, and OverTime")
g3 = sns.catplot(data=filtered_df, x='DistanceFromHome', y='Attrition_encoded', hue='BusinessTravel', col='OverTime', kind='point', height=4, aspect=1.2, palette='viridis', errorbar=None)
g3.fig.suptitle('Attrition Rate by Distance From Home, Business Travel, and OverTime', y=1.02)
st.pyplot(g3)
plt.close(g3.fig)
st.markdown("""
**Insight**: This plot highlights how external factors (distance, travel) and work habits (overtime) interact to influence attrition. Employees facing multiple stressors from these categories often show higher attrition.
""")

st.header("13. Attrition by Total Working Years, Job Level, and Monthly Income Bin")
g4 = sns.catplot(data=filtered_df, x='TotalWorkingYears', y='Attrition_encoded', hue='JobLevel', col='MonthlyIncome_bin', kind='point', height=4, aspect=1.2, col_wrap=3, palette='viridis', errorbar=None)
g4.fig.suptitle('Attrition Rate by Total Working Years, Job Level, and Monthly Income Bin', y=1.02)
st.pyplot(g4)
plt.close(g4.fig)
st.markdown("""
**Insight**: This comprehensive view helps understand how career progression (total working years, job level) and compensation (monthly income) together impact attrition. It can pinpoint where compensation or career path concerns might be driving employees away.
""")

# --- Overarching Insights ---
st.header("Overall Business Insights for Stakeholders")
st.markdown("""
1.  **Retention Focus on Vulnerable Groups**: Younger employees, those with lower incomes, and individuals working extensive overtime or frequent business travel exhibit higher attrition risks. Targeted interventions focusing on competitive compensation, work-life balance, and career development are crucial for these segments.
2.  **Departmental and Role-Specific Strategies**: Attrition is not uniform across the organization. Some departments and job roles show significantly higher turnover. A tailored approach, rather than a generic one, is necessary to address the unique challenges within each area.
3.  **Interconnectedness of Employee Well-being**: Factors like job satisfaction, work-life balance, and relationship satisfaction are deeply intertwined with attrition. A holistic approach to employee well-being, fostering a supportive environment and addressing root causes of dissatisfaction, will be key to improving overall retention.
""")