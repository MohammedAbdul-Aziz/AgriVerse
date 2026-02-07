import requests
import time
import pandas as pd
import numpy as np
# --- 1. SIMULATED "AGRIVERSE" DATABASE ---
# (All your dictionaries like yield_factors, farmer_purchases_db, etc. go here)
# ... (I'm omitting them for brevity, but YOU must copy them here) ...
yield_factors = {
    "ADILABAD": {
        'Arhar/Tur': 0.6338016797793798, 
        'Bajra': 0.6775081607965021, 
        'Banana': 35.31948027866677, 
        'Cashewnut': 0.34993123498568823, 
        'Castor seed': 0.5294299396105792, 
        'Coriander': 0.6816462459005687, 
        'Cotton(lint)': 1.968766339663747, 
        'Cowpea(Lobia)': 0.9792704180959897, 
        'Dry chillies': 2.589558914378318, 
        'Garlic': 2.2939452603471295, 
        'Ginger': 7.133333333333333, 
        'Gram': 1.1889818059277788, 
        'Groundnut': 1.3522696140570951, 
        'Horse-gram': 0.3595373385317904, 
        'Jowar': 1.0698201762294264, 
        'Linseed': 0.2372927187806985, 
        'Maize': 3.7981353241131868, 
        'Masoor': 0.2907719507892771, 
        'Mesta': 8.722943722943723, 
        'Moong(Green Gram)': 0.4782024437322385, 
        'Onion': 22.570587196002244, 
        'Other Kharif pulses': 0.22869234398930655, 
        'Other Rabi pulses': 0.2296695956961218, 
        'Potato': 9.319444444444445, 
        'Ragi': 1.0227300389483933, 
        'Rapeseed &Mustard': 0.5670853611282137, 
        'Rice': 2.590915325275653, 
        'Safflower': 0.5738260336679647, 
        'Sesamum': 0.2708516861065035, 
        'Small millets': 0.8221208291203237, 
        'Soyabean': 1.2835542614111557, 
        'Sugarcane': 81.76698446215028, 
        'Sunflower': 0.888627821261034, 
        'Sweet potato': 10.118019943019943, 
        'Tobacco': 2.6497892175286397, 
        'Turmeric': 4.995396030701519, 
        'Urad': 0.6625460068021918, 
        'Wheat': 1.1242929821984666
    },
    "ANANTAPUR": {
        'Arecanut': 2.389589373841, 
        'Arhar/Tur': 0.22324255108263674, 
        'Bajra': 0.9102617840065902, 
        'Banana': 55.80965644491786, 
        'Black pepper': 1.0, 
        'Cashewnut': 0.49824561403508766, 
        'Castor seed': 0.4768288321399556, 
        'Coconut': 8651.115193856727, 
        'Coriander': 0.36439218645453036, 
        'Cotton(lint)': 1.2583668861488637, 
        'Cowpea(Lobia)': 0.527530125297591, 
        'Dry chillies': 2.591709940508802, 
        'Gram': 0.6661506419653622, 
        'Groundnut': 0.9789026547137489, 
        'Horse-gram': 0.39303043899706575, 
        'Jowar': 0.8682800450714069, 
        'Linseed': 0.3372464503042596, 
        'Maize': 4.60015855523168, 
        'Masoor': 0.13453037918026578, 
        'Mesta': 7.934722222222223, 
        'Moong(Green Gram)': 0.4951495767850978, 
        'Oilseeds total': 1.084726156115939, 
        'Onion': 25.945763888102736, 
        'Other Kharif pulses': 0.3172839496352427, 
        'Other Rabi pulses': 0.7952941176470588, 
        'Potato': 11.640706547535816, 
        'Ragi': 1.8551053232984045, 
        'Rice': 2.661254454744091, 
        'Safflower': 0.400767064050455, 
        'Sesamum': 0.3611111111111111, 
        'Small millets': 0.6239308634035156, 
        'Soyabean': 1.023433872490797, 
        'Sugarcane': 90.52512501582167, 
        'Sunflower': 0.5365192191500556, 
        'Sweet potato': 10.744846106246877, 
        'Tobacco': 1.4774560447792533, 
        'Turmeric': 8.81422380772987, 
        'Urad': 0.7204102359218785, 
        'Wheat': 0.6782770385836127, 
        'other oilseeds': 3.5871784025773534
    },
    "KHAMMAM": {
        'Rice': 3.5, 
        'Maize': 2.8,
        'Cotton': 1.6, 
        'Chilli': 3.2,
        'Turmeric': 5.5,
        'Groundnut': 1.1,
        'Sugarcane': 85.0,
        'Jowar': 1.2
    },
    "MEDAK": {
        'Rice': 2.9, 
        'Maize': 2.5,
        'Jowar': 1.1,
        'Turmeric': 4.8,
        'Red Gram': 0.7, 
        'Soyabean': 1.05,
        'Cotton': 1.4,
        'Bajra': 0.95
    }
}
farmer_purchases_db = {
    "101": {"seeds": "Premium", "fertilizer": "Standard"},
    "102": {"seeds": "Local", "fertilizer": "Standard"},
    "103": {"seeds": "Certified", "fertilizer": "Premium"},
}
farmer_history_db = {
    "101": {"rating": 5, "training_completed": True},
    "102": {"rating": 3, "training_completed": False},
    "103": {"rating": 4, "training_completed": True},
}
pest_alert_db = {
    "ADILABAD": {"alert_level": "Low", "report_date": "2025-11-01"},
    "KHAMMAM":  {"alert_level": "High", "report_date": "2025-11-03"},
    "MEDAK":    {"alert_level": "Medium", "report_date": "2025-11-02"},
}
MLR_INTERCEPT = 0.536
MLR_WEIGHTS = {
    'Weather': 0.8250,
    'Irrigation': 0.7000,
    'IPQual': 0.3500,
    'Management': 0.2500,
    'Pestcon': 0.6500
}


# --- 2. FACTOR-CALCULATING FUNCTIONS ---

API_KEY = "ddad84c82bd8442ba0f74d5614dd201a"
API_URL = "https://www.weatherbit.io/"
def get_weather_factor(location, api_key):
    params = {
        'location': location,
        'country': 'IN',
        'appid':API_KEY , 
        'units': 'metric',
        'days': 14  
    }
    try:
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        daily_temps = []
        for day in data.get('daily', []): 
            temp = day.get('temp_avg') 
            if temp is not None:
                daily_temps.append(temp)
        
        if not daily_temps:
            print("--- API WARNING: No temperature data found in response structure. ---")
            return 0.9  # Default safe factor
        avg_temp = np.mean(daily_temps)  
        OPTIMAL_TEMP_MIN = 25 
        OPTIMAL_TEMP_MAX = 35        
        if OPTIMAL_TEMP_MIN <= avg_temp <= OPTIMAL_TEMP_MAX:
            Weather = 1.0  # Optimal conditions
        elif avg_temp > OPTIMAL_TEMP_MAX:
            # High temperature stress: Factor reduces by 0.05 for every 1°C over optimal
            stress_level = (avg_temp - OPTIMAL_TEMP_MAX) * 0.05
            Weather = max(0.70, 1.0 - stress_level) # Factor floor at 0.70
        else:
            # Low temperature stress (too cold)
            Weather = 0.85 
        print(f"--- API SUCCESS: 30-day Avg Temp: {avg_temp:.2f}°C ---")
        return Weather
        
    except requests.exceptions.RequestException as e:
        print(f"--- API ERROR: API call failed or timed out: {e} ---")
        return 0.90
    except Exception as e:
        print(f"--- UNEXPECTED ERROR during processing: {e} ---")
        return 0.90

# --- MODIFIED: This function now takes a parameter ---
def get_irrigation_factor(irrigation_type):
    print("-> Querying Irrigation Status...")
    if irrigation_type.upper() == 'I':
        return 1.0  # Fully irrigated
    elif irrigation_type.upper() == 'R':
        return 0.95 # Rainfed / Partial
    else:
        return 0.5 # Default if unknown

def get_ipqual_factor(farmer_id):
    # ... (Your full ipqual function) ...
    print(f"-> Checking Marketplace data for {farmer_id}...")
    if farmer_id in farmer_purchases_db:
        seed_type = farmer_purchases_db[farmer_id].get("seeds")
        if seed_type == "Premium": return 1.05
        elif seed_type == "Certified": return 1.0
        elif seed_type == "Local": return 0.9
    return 0.7

def get_management_factor(farmer_id):
    # ... (Your full management function) ...
    print(f"-> Checking Farmer History for {farmer_id}...")
    if farmer_id in farmer_history_db:
        history = farmer_history_db[farmer_id]
        if history["rating"] >= 4 and history["training_completed"]: return 1.05
        elif history["rating"] >= 3: return 1.0
        else: return 0.9
    return 0.75

def get_pestcon_factor(location):
    # ... (Your full pestcon function) ...
    print(f"-> Checking Pest Alerts for {location}...")
    if location in pest_alert_db:
        alert_level = pest_alert_db.get(location, {}).get("alert_level")
        if alert_level == "High": return 0.7
        elif alert_level == "Medium": return 0.85
        elif alert_level == "Low": return 0.98
    return 1.0

# --- 3. THE MAIN LOGIC FUNCTION ---
# This REPLACES your main() function
# It takes data *in* and returns a dictionary *out*

#  df = pd.read_csv("India Agriculture Crop Production.csv")
#  yield_predictor = df[['District', 'Crop', 'Production']]
#  yield_predictor_new = df.pivot_table(index='District', columns='Crop', values='Production')
#  yield_factors = yield_predictor_new.to_dict('index')

#Adding weights using multiple linear regression:

from sklearn.linear_model import LinearRegression
data = {
    'Actual_Yield': [11.43, 2.99, 1.54, 2.33, 1.05, 2.24, 2.15, 1.64, 2.37, 1.77], 
    'Baseline_Factor': [12.95, 3.39, 1.75, 2.65, 1.19, 2.49, 2.38, 1.82, 2.64, 1.97], 
    'Weather': [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9], 
    'Irrigation': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    'IPQual': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    'Management': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    'Pestcon': [0.98, 0.98, 0.98, 0.98, 0.98, 1, 1, 1, 1, 1]
}

weig = pd.DataFrame(data)

features = ['Weather', 'Irrigation', 'IPQual', 'Management', 'Pestcon']
x = weig[features]
y = weig['Actual_Yield']

model = LinearRegression()
model.fit(x, y)

def calculate_yield(data):
    try:
        
        farmer_id = data['farmer_id'].upper()
        location = data['location'].upper()
        area = float(data['area'])
        crop = data['crop']
        irrigation_type = data['irrigation_type'] # e.g., "I" or "R"

        YOUR_API_KEY = "ddad84c82bd8442ba0f74d5614dd201a"

        
        factor = yield_factors.get(location, {}).get(crop)
        if not factor:
            return {"error": f"No yield data for {crop} in {location}."}
        
        BaselineYield = area * factor

        
        
        weather = get_weather_factor(location, YOUR_API_KEY)
        irrigation = get_irrigation_factor(irrigation_type)
        ipqual = get_ipqual_factor(farmer_id)
        management = get_management_factor(farmer_id)
        pestcon = get_pestcon_factor(location)
        
        
        AdjustedYield = MLR_INTERCEPT
    
        
        AdjustedYield += MLR_WEIGHTS['Weather'] * weather
        AdjustedYield += MLR_WEIGHTS['Irrigation'] * irrigation
        AdjustedYield += MLR_WEIGHTS['IPQual'] * ipqual
        AdjustedYield += MLR_WEIGHTS['Management'] * management
        AdjustedYield += MLR_WEIGHTS['Pestcon'] * pestcon
        
        AdjustedYield = AdjustedYield + (BaselineYield * weather * irrigation * ipqual * management * pestcon)
        
        x = AdjustedYield * 0.15
        z = AdjustedYield - x
        y = AdjustedYield + x
        
        
        return {
            "success": True,
            "baseline_yield": f"{BaselineYield:.2f}",
            "adjusted_yield": f"{AdjustedYield:.2f}",
            "yield_range_min": f"{z:.2f}",
            "yield_range_max": f"{y:.2f}",
            "factors": {
                "weather": weather,
                "irrigation": irrigation,
                "ipqual": ipqual,
                "management": management,
                "pestcon": pestcon
            }
        }

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}