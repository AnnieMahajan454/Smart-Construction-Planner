import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from scipy.stats import zscore
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    memory = ConversationBufferMemory()
    llm = ChatOpenAI(model="gpt-4", temperature=0.5, openai_api_key=openai_api_key)
    conversation = ConversationChain(llm=llm, memory=memory)
    ai_enabled = True
else:
    st.warning("⚠️ OPENAI_API_KEY not found. AI explanations disabled.")
    ai_enabled = False
    conversation = None

city_base_rates = {
    'New York': 3500,
    'San Francisco': 3400,
    'Los Angeles': 3000,
    'Chicago': 2600,
    'Miami': 2500,
    'Dallas': 2400,
    'Houston': 2300,
    'Atlanta': 2200
}

@st.cache_data
def load_data():
    df = pd.read_csv("realistic_construction_estimates.csv")
    df['Project_Type'] = df['Project_Type'].astype(str)
    df['Location'] = df['Location'].astype(str)
    return df

df_original = load_data()

st.title("💰 Cost Estimator")

st.header("📊 Data Overview")
if st.checkbox("Show Raw Data"):
    st.dataframe(df_original.head(10))

if df_original.isnull().sum().sum() == 0:
    st.success("No missing values detected!")
else:
    st.error("Missing values found! Filling with median values.")
    df_original = df_original.fillna(df_original.median(numeric_only=True))

numeric_cols = df_original.select_dtypes(include=['float64', 'int64']).columns
z_scores = zscore(df_original[numeric_cols])
outliers = (abs(z_scores) > 3).any(axis=1)
if outliers.sum() == 0:
    st.success("No major outliers detected!")
else:
    st.warning(f"{outliers.sum()} outlier records detected. They are retained for analysis.")

st.subheader("Processed Data")
st.dataframe(df_original.head(10))

df = df_original.copy()
label_encoders = {}
for col in ['Project_Type', 'Location']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df.drop(columns=['Total_Estimate'])
y = df['Total_Estimate']
model = RandomForestRegressor(random_state=42)
model.fit(X, y)

def prepare_features(project_type, location, total_area, floors, basements):
    base_rate = city_base_rates.get(location, 2500)
    base_cost = total_area * base_rate
    material_cost = base_cost * 0.6 * (1 + 0.05 * (floors - 1) + 0.10 * basements)
    labor_cost = base_cost * 0.3 * (1 + 0.05 * (floors - 1) + 0.10 * basements)
    return pd.DataFrame({
        'Material_Cost': [material_cost],
        'Labor_Cost': [labor_cost],
        'Project_Type': [label_encoders['Project_Type'].transform([project_type])[0]],
        'Total_Area': [total_area],
        'Number_of_Floors': [floors],
        'Number_of_Basements': [basements],
        'Location': [label_encoders['Location'].transform([location])[0]]
    })

st.header("Estimator")
col1, col2 = st.columns(2)
with col1:
    project_type = st.selectbox("Project Type", ['Residential', 'Commercial', 'Industrial', 'Institutional'])
    location = st.selectbox("Location", list(city_base_rates.keys()))
    total_area = st.number_input("Total Area (m²)", min_value=50.0, format="%.2f")
with col2:
    number_of_floors = st.number_input("Number of Floors", min_value=1, max_value=20, step=1)
    number_of_basements = st.number_input("Number of Basements", min_value=0, max_value=5, step=1)

if st.button("Estimate Cost", type="primary"):
    input_data = prepare_features(project_type, location, total_area, number_of_floors, number_of_basements)
    predicted_cost = model.predict(input_data)[0]
    st.success(f"Predicted Total Construction Cost: ${predicted_cost:,.0f}")
    st.session_state['base_project'] = {
        'project_type': project_type,
        'location': location,
        'total_area': total_area,
        'number_of_floors': number_of_floors,
        'number_of_basements': number_of_basements,
        'predicted_cost': predicted_cost
    }

st.header("🔄 What-If Simulator")
what_if_change = st.text_input("Describe a project change (e.g., 'Increase area by 20%', 'Add 2 floors'):")

if st.button("Simulate"):
    if 'base_project' not in st.session_state:
        st.warning("Please estimate a base project first.")
    elif not what_if_change.strip():
        st.warning("Please describe a change.")
    else:
        base = st.session_state['base_project']
        updated_area = base['total_area']
        updated_floors = base['number_of_floors']
        updated_basements = base['number_of_basements']
        change = what_if_change.lower()
        if 'increase area' in change:
            percent = int(''.join(filter(str.isdigit, change)))
            updated_area *= (1 + percent / 100)
        if 'decrease area' in change:
            percent = int(''.join(filter(str.isdigit, change)))
            updated_area *= (1 - percent / 100)
        if 'add' in change and 'floor' in change:
            num = int(''.join(filter(str.isdigit, change)))
            updated_floors += num
        if 'add' in change and 'basement' in change:
            num = int(''.join(filter(str.isdigit, change)))
            updated_basements += num
        input_data = prepare_features(base['project_type'], base['location'], updated_area, updated_floors, updated_basements)
        new_predicted_cost = model.predict(input_data)[0]
        st.success(f"Updated Estimated Cost: ${new_predicted_cost:,.0f}")
        if ai_enabled:
            prompt = f"Base area {base['total_area']} m², floors {base['number_of_floors']}, basements {base['number_of_basements']}, cost ${base['predicted_cost']:,.0f}. Change: {what_if_change}. After: area {updated_area:.2f}, floors {updated_floors}, basements {updated_basements}, cost ${new_predicted_cost:,.0f}. Explain briefly why cost changed and give advice."
            response = conversation.run(prompt)
            st.markdown(f"**Explanation:**\n\n{response}")
        else:
            delta = new_predicted_cost - base['predicted_cost']
            pct = (delta / base['predicted_cost']) * 100
            st.info(f"Cost change: ${delta:,.0f} ({pct:+.1f}%). Enable AI for narrative explanation.")
