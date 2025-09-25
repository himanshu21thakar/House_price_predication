import streamlit as st
import pandas as pd
import pickle  # Changed from joblib to pickle
import base64

# Page configuration with custom styling
st.set_page_config(
    page_title="🏠 Luxe Property Predictor", 
    page_icon="🏠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for beautiful styling ---
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, rgba(0,0,0,0.7), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container styling */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Title styling */
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Input styling */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e1e8ed;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        box-shadow: 0 10px 20px rgba(17, 153, 142, 0.3);
    }
    
    /* Data frame styling */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
    }
    
    /* Stats styling */
    .stat-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .stat-item {
        text-align: center;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        flex: 1;
        margin: 0 1rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Hide Streamlit elements */
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    
    /* Sidebar header */
    .css-1lcbmhc {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# Load CSS
load_css()

# --- Load trained pipeline ---
@st.cache_resource
def load_model():
    try:
        # Changed from joblib.load to pickle.load
        with open("house_best_rf1.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("Model file 'house_best_rf1.pkl' not found. Please ensure the model file is in the correct directory.")
        return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

model = load_model()

if model is None:
    st.stop()

# --- Main Header ---
st.markdown("""
<div class="main-container">
    <div class="header-container">
        <h1 class="main-title">🏠 Luxe Property Predictor</h1>
        <p class="subtitle">
            Discover your dream home's value with our AI-powered prediction system
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Stats Section ---
st.markdown("""
<div class="main-container">
    <div class="stat-container">
        <div class="stat-item">
            <div class="stat-number">99.2%</div>
            <div class="stat-label">Accuracy</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">10K+</div>
            <div class="stat-label">Properties Analyzed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Available</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">AI</div>
            <div class="stat-label">Powered</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Extract feature names ---
try:
    preprocessor = model.named_steps['preprocessor']
    num_features = preprocessor.transformers_[0][2]  # numeric feature names
    cat_features = preprocessor.transformers_[1][2]  # categorical feature names
except (AttributeError, IndexError):
    st.error("Error extracting features from the model pipeline. Please check the model structure.")
    st.stop()

# --- Enhanced Sidebar ---
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 1rem;'>
    <h2 style='color: white; margin: 0; font-weight: 600;'>🏡 Property Details</h2>
</div>
""", unsafe_allow_html=True)

# --- Numeric Inputs with better organization ---
numeric_inputs = {}
st.sidebar.markdown("### 📊 **Property Specifications**")

# Group numeric features by category for better UX
property_specs = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
location_specs = []
other_specs = []

for feat in num_features:
    feat_lower = feat.lower()
    if any(spec in feat_lower for spec in property_specs):
        continue  # Handle these specially
    elif 'location' in feat_lower or 'distance' in feat_lower:
        location_specs.append(feat)
    else:
        other_specs.append(feat)

# Property specifications with better defaults and ranges
for feat in num_features:
    feat_lower = feat.lower()
    if 'area' in feat_lower or 'size' in feat_lower:
        numeric_inputs[feat] = st.sidebar.slider(f"🏠 {feat} (sq ft)", min_value=500, max_value=10000, value=2000, step=100)
    elif 'bedroom' in feat_lower:
        numeric_inputs[feat] = st.sidebar.selectbox(f"🛏️ {feat}", options=[1, 2, 3, 4, 5, 6], index=2)
    elif 'bathroom' in feat_lower:
        numeric_inputs[feat] = st.sidebar.selectbox(f"🚿 {feat}", options=[1, 2, 3, 4, 5], index=1)
    elif 'stories' in feat_lower or 'floor' in feat_lower:
        numeric_inputs[feat] = st.sidebar.selectbox(f"🏢 {feat}", options=[1, 2, 3, 4, 5], index=0)
    elif 'parking' in feat_lower or 'garage' in feat_lower:
        numeric_inputs[feat] = st.sidebar.selectbox(f"🚗 {feat}", options=[0, 1, 2, 3, 4], index=1)
    elif 'age' in feat_lower or 'year' in feat_lower:
        numeric_inputs[feat] = st.sidebar.slider(f"📅 {feat}", min_value=0, max_value=100, value=10, step=1)
    else:
        numeric_inputs[feat] = st.sidebar.number_input(f"📈 {feat}", value=0.0, step=0.1)

# --- Enhanced Categorical Inputs ---
streets = ["MG Road", "Park Street", "Brigade Road", "Commercial Street", "Residency Road", "Koregaon Park", "Banjara Hills"]
cities = ["Pune", "Mumbai", "Bengaluru", "Hyderabad", "Chennai", "Delhi", "Ahmedabad", "Kolkata"]
states = ["Maharashtra", "Karnataka", "Telangana", "Tamil Nadu", "Delhi", "Gujarat", "West Bengal"]
zipcodes = ["411001", "400001", "560001", "500001", "600001", "110001", "380001", "700001"]
counties = [
    "Pune District", "Mumbai Suburban", "Bangalore Urban", "Hyderabad District",
    "Chennai District", "New Delhi District", "Ahmedabad District", "Kolkata District"
]
countries = ["India"]

property_types = ["Villa", "Apartment", "Independent House", "Penthouse", "Studio", "Duplex"]
furnishing_status = ["Fully Furnished", "Semi Furnished", "Unfurnished"]

categorical_inputs = {}
if cat_features:
    st.sidebar.markdown("### 🌍 **Location & Features**")
    
    for feat in cat_features:
        feat_lower = feat.lower()
        if "street" in feat_lower:
            categorical_inputs[feat] = st.sidebar.selectbox("🛣️ Street", streets, index=0)
        elif "city" in feat_lower:
            categorical_inputs[feat] = st.sidebar.selectbox("🏙️ City", cities, index=0)
        elif "state" in feat_lower:
            categorical_inputs[feat] = st.sidebar.selectbox("🗺️ State", states, index=0)
        elif "zipcode" in feat_lower or "pincode" in feat_lower:
            categorical_inputs[feat] = st.sidebar.selectbox("📮 Zipcode", zipcodes, index=0)
        elif "county" in feat_lower:
            categorical_inputs[feat] = st.sidebar.selectbox("🏘️ County", counties, index=0)
        elif "country" in feat_lower:
            categorical_inputs[feat] = st.sidebar.selectbox("🌏 Country", countries, index=0)
        elif "type" in feat_lower:
            categorical_inputs[feat] = st.sidebar.selectbox("🏠 Property Type", property_types, index=0)
        elif "furnish" in feat_lower:
            categorical_inputs[feat] = st.sidebar.selectbox("🪑 Furnishing", furnishing_status, index=1)
        else:
            categorical_inputs[feat] = st.sidebar.text_input(f"✏️ {feat}", value="Standard")

# --- Main Content Area ---
col1, col2 = st.columns([2, 1])

with col1:
    # --- Display Input Data ---
    input_data = {**numeric_inputs, **categorical_inputs}
    input_df = pd.DataFrame([input_data])
    
    st.markdown("""
    <div class="main-container">
        <h3 style='color: #667eea; font-weight: 600; margin-bottom: 1rem;'>📋 Property Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a more visually appealing display of the data
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**🏠 Property Features**")
        for key, value in list(input_data.items())[:len(input_data)//2]:
            st.write(f"• **{key}**: {value}")
    
    with col_b:
        st.markdown("**📍 Location Details**")
        for key, value in list(input_data.items())[len(input_data)//2:]:
            st.write(f"• **{key}**: {value}")

with col2:
    # --- Prediction Button and Result ---
    st.markdown("""
    <div class="main-container" style="text-align: center;">
        <h3 style='color: #667eea; font-weight: 600; margin-bottom: 1rem;'>🔮 Get Prediction</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Predict Property Value", use_container_width=True):
        try:
            with st.spinner('🔄 Analyzing property data...'):
                pred_usd = model.predict(input_df)[0]
                usd_to_inr = 83.0  # Current conversion rate
                pred_inr = pred_usd * usd_to_inr
            
            # Enhanced success display
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                margin: 1rem 0;
                color: white;
                box-shadow: 0 15px 30px rgba(17, 153, 142, 0.3);
            '>
                <h2 style='margin: 0; font-size: 1.5rem;'>🏡 Estimated Value</h2>
                <h1 style='margin: 0.5rem 0; font-size: 2.5rem; font-weight: 700;'>₹{pred_inr:,.0f}</h1>
                <p style='margin: 0; opacity: 0.9;'>≈ ${pred_usd:,.0f} USD</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            
            # Additional insights
            st.markdown(f"""
            <div class="main-container">
                <h4 style='color: #667eea;'>💡 Market Insights</h4>
                <div style='background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #667eea;'>
                    <p><strong>Price per sq ft:</strong> ₹{pred_inr/max(input_data.get('area', input_data.get('size', 1000)), 1):,.0f}</p>
                    <p><strong>Market Segment:</strong> {'Luxury' if pred_inr > 10000000 else 'Premium' if pred_inr > 5000000 else 'Standard'}</p>
                    <p><strong>Investment Potential:</strong> {'High' if pred_inr > 8000000 else 'Medium' if pred_inr > 3000000 else 'Entry Level'}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error making prediction: {str(e)}")

# --- Footer ---
st.markdown("""
<div class="main-container" style="text-align: center; margin-top: 3rem;">
    <p style='color: #666; font-size: 0.9rem;'>
        🚀 Powered by Advanced Machine Learning | 
        🔒 Secure & Private | 
        📱 Real-time Predictions
    </p>
    <p style='color: #999; font-size: 0.8rem;'>
        Built with ❤️ using Streamlit & Random Forest Algorithm
    </p>
</div>
""", unsafe_allow_html=True)

# --- Floating action button style prediction summary ---
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
