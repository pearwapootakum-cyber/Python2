import streamlit as st
import random
import time
import requests
import pandas as pd
from abc import ABC, abstractmethod
from functools import wraps


WEATHER_API_KEY = "477850cd419666f030893bd839f114b7"
TMDB_API_KEY    = "a5b492f57ce7c0e6d1c40031f3b648a3"
FOOD_API_KEY    = "eba58fe8c87d4e8e8f029582ecacf0b5"
PLACES_API_KEY  = "A9rNakCgh04JyLvKLIy5uuCNGrFrYLa4"


st.set_page_config(page_title="Thailand Smart Trip", page_icon="⛟", layout="wide")


st.markdown("""
<style>
    .main-header { font-size: 32px; font-weight: bold; color: #1E3A8A; }
    .card { background-color: #FFFFFF; color: #000000; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px; border-left: 5px solid #1E3A8A; }
    .price-badge { background-color: #DCFCE7; color: #166534; padding: 2px 8px; border-radius: 12px; font-size: 0.9em; font-weight: bold; }
    .free-badge { background-color: #FEF9C3; color: #854D0E; padding: 2px 8px; border-radius: 12px; font-size: 0.9em; font-weight: bold; }
    .nav-btn { text-decoration: none; display: inline-block; padding: 5px 15px; background-color: #4285F4; color: white !important; border-radius: 20px; font-size: 0.8em; margin-top: 5px; }
    .nav-btn:hover { background-color: #357AE8; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_provinces_from_api():
    try:
        url = "https://raw.githubusercontent.com/pythailand/thai-data/master/thai_provinces.json"
        response = requests.get(url, timeout=5).json()
        provinces = [item['name_en'] for item in response]
        return sorted(provinces)
    except Exception:
        return ["Bangkok", "Chiang Mai", "Phuket", "Khon Kaen", "Chonburi"]

PROVINCE_LIST = get_provinces_from_api()

def safe_api_call(default_value = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return default_value
        return wrapper
    return decorator

class TravelServiceInterface(ABC):
    @abstractmethod
    def fetch_weather(self, city_name):
        pass
    @abstractmethod
    def fetch_food_recommendations(self):
        pass

class TripAPIService(TravelServiceInterface):
    def __init__(self):
        self.current_lat = 13.7563
        self.current_lon = 100.5018

    @safe_api_call(default_value=None)
    def fetch_weather(self, city_name):
        api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name},TH&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(api_url, timeout=3).json()
        
        if response.get('weather'):
            self.current_lat = response['coord']['lat']
            self.current_lon = response['coord']['lon']
            return {
                "temperature": response['main']['temp'], 
                "icon_code": response['weather'][0]['icon'], 
                "description": response['weather'][0]['description']
            }
        return None

    def place_generator(self):
        try:
            api_url = f"https://api.opentripmap.com/0.1/en/places/radius?radius=10000&lon={self.current_lon}&lat={self.current_lat}&kinds=tourist_facilities&rate=3&format=json&apikey={PLACES_API_KEY}"
            response = requests.get(api_url, timeout=3).json()
            
            for place_data in response[:5]: 
                place_name = place_data.get('name', 'Unknown Place')
                if place_name:
                    entry_fee = random.choice([0, 0, 20, 50, 100])
                    latitude = place_data.get('point', {}).get('lat', self.current_lat)
                    longitude = place_data.get('point', {}).get('lon', self.current_lon)
                    yield {"name": place_name, "price": entry_fee, "lat": latitude, "lon": longitude}
        except Exception:
            return []

    @safe_api_call(default_value=[])
    def fetch_food_recommendations(self):
        food_list = []
        api_url = f"https://api.spoonacular.com/recipes/random?apiKey={FOOD_API_KEY}&number=3"
        response = requests.get(api_url, timeout=3).json()
        
        for recipe in response['recipes']:
            cost = int((recipe.get('pricePerServing', 100) / 100) * 25) 
            if cost < 40: cost = 40
            food_list.append({"title": recipe['title'], "image": recipe.get('image'), "price": cost})
        
        if not food_list:
            food_list = [
                {"title": "Pad Thai", "image": "https://loremflickr.com/400/300/padthai", "price": 50},
                {"title": "Khao Man Gai", "image": "https://loremflickr.com/400/300/chicken,rice", "price": 45},
                {"title": "Mango Sticky Rice", "image": "https://loremflickr.com/400/300/mango,rice", "price": 60}
            ]
        return food_list

def create_fallback_places(city_name, lat, lon):
    return [
        {"name": f"{city_name} City Pillar Shrine", "price": 0, "lat": lat + 0.01, "lon": lon + 0.01},
        {"name": f"Wat Mahathat {city_name}", "price": 20, "lat": lat - 0.01, "lon": lon - 0.01},
        {"name": f"{city_name} Public Park", "price": 0, "lat": lat + 0.02, "lon": lon - 0.02},
        {"name": f"{city_name} Walking Street", "price": 0, "lat": lat - 0.02, "lon": lon + 0.02}
    ]

with st.sidebar:
    st.header("⚙️ Trip Settings")
    traveler_name = st.text_input("Traveler Name", "John Doe")
    selected_city = st.selectbox("Destination", PROVINCE_LIST) # ใช้ List ที่ดึงจาก API
    initial_budget = st.slider("Budget (THB)", 0, 10000, 1500, step=100)
    generate_button = st.button("Generate Itinerary", type="primary")

st.markdown("<div class='main-header'> Smart Trip Planner</div>", unsafe_allow_html=True)

if generate_button:
    trip_service = TripAPIService()
    
    with st.spinner(f"Creating route for {selected_city}..."):
        time.sleep(1)
        
        weather_data = trip_service.fetch_weather(selected_city)
        
        places_gen = trip_service.place_generator()
        found_places = list(places_gen) 
        
        final_places = found_places if found_places else create_fallback_places(selected_city, trip_service.current_lat, trip_service.current_lon)
        food_menu = trip_service.fetch_food_recommendations()

    col_dest, col_budget, col_weather = st.columns(3)
    col_dest.metric("Destination", selected_city)
    col_budget.metric("Budget", f"{initial_budget:,} THB")
    
    if weather_data: 
        col_weather.metric("Weather", f"{weather_data['temperature']}°C", weather_data['description'].title())

    st.markdown("---")
    tab_itinerary, tab_map, tab_finance = st.tabs(["📅 Timeline & Navigate", "Route Map", "Budget"])

    remaining_budget = initial_budget
    expense_summary = {"Food": 0, "Activity": 0, "Transport": 0}
    map_markers = []

    with tab_itinerary:
        st.subheader(f"Itinerary for {traveler_name}")
        
        if final_places:
            morning_activity = final_places[0]
            map_markers.append({"lat": morning_activity['lat'], "lon": morning_activity['lon'], "name": morning_activity['name'], "color": "#FF4B4B"})
            
            with st.container():
                col_image, col_text = st.columns([1, 3])
                col_image.image(f"https://loremflickr.com/400/300/{selected_city},temple", use_container_width=True)
                with col_text:
                    google_maps_link = f"https://www.google.com/maps/search/?api=1&query={morning_activity['name']}+{selected_city}"
                    st.markdown(f"""
                    <div class='card'>
                        <b>09:00 AM - {morning_activity['name']}</b><br>
                        Start your journey here.<br>
                        <a href='{google_maps_link}' target='_blank' class='nav-btn'>📍 Navigate (Google Maps)</a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if morning_activity['price'] == 0: 
                        st.markdown("<span class='free-badge'>Free Entry</span>", unsafe_allow_html=True)
                    else: 
                        st.markdown(f"<span class='price-badge'>Entry: {morning_activity['price']} THB</span>", unsafe_allow_html=True)
                        remaining_budget -= morning_activity['price']
                        expense_summary["Activity"] += morning_activity['price']

        st.markdown("---")
        
        if food_menu:
            lunch_meal = food_menu[0]
            with st.container():
                col_image, col_text = st.columns([1, 3])
                col_image.image(lunch_meal['image'], width=150)
                with col_text:
                    st.markdown(f"<div class='card'><b>12:00 PM - Lunch: {lunch_meal['title']}</b></div>", unsafe_allow_html=True)
                    st.markdown(f"<span class='price-badge'>Cost: {lunch_meal['price']} THB</span>", unsafe_allow_html=True)
                    remaining_budget -= lunch_meal['price']
                    expense_summary["Food"] += lunch_meal['price']

        st.markdown("---")
        
        if len(final_places) > 1:
            afternoon_activity = final_places[1]
            map_markers.append({"lat": afternoon_activity['lat'], "lon": afternoon_activity['lon'], "name": afternoon_activity['name'], "color": "#FF4B4B"})
            
            with st.container():
                col_image, col_text = st.columns([1, 3])
                col_image.image(f"https://loremflickr.com/400/300/{selected_city},park", use_container_width=True)
                with col_text:
                    google_maps_link = f"https://www.google.com/maps/search/?api=1&query={afternoon_activity['name']}+{selected_city}"
                    st.markdown(f"""
                    <div class='card'>
                        <b>03:00 PM - Visit: {afternoon_activity['name']}</b><br>
                        Relaxing afternoon.<br>
                        <a href='{google_maps_link}' target='_blank' class='nav-btn'>📍 Navigate (Google Maps)</a>
                    </div>
                    """, unsafe_allow_html=True)

                    if afternoon_activity['price'] == 0: 
                        st.markdown("<span class='free-badge'>Free Entry</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='price-badge'>Entry: {afternoon_activity['price']} THB</span>", unsafe_allow_html=True)
                        remaining_budget -= afternoon_activity['price']
                        expense_summary["Activity"] += afternoon_activity['price']

        st.markdown("---")
        
        if len(food_menu) > 1:
            dinner_meal = food_menu[1]
            with st.container():
                col_image, col_text = st.columns([1, 3])
                col_image.image(dinner_meal['image'], width=150)
                with col_text:
                    st.markdown(f"<div class='card'><b>06:00 PM - Dinner: {dinner_meal['title']}</b></div>", unsafe_allow_html=True)
                    st.markdown(f"<span class='price-badge'>Cost: {dinner_meal['price']} THB</span>", unsafe_allow_html=True)
                    remaining_budget -= dinner_meal['price']
                    expense_summary["Food"] += dinner_meal['price']

    with tab_map:
        st.subheader(f"🗺️ Route Map in {selected_city}")
        if map_markers:
            map_df = pd.DataFrame(map_markers)
            st.map(map_df, zoom=12)
            st.info("💡 Red dots indicate the tourist spots.")
        else:
            st.warning("Map data unavailable.")

    with tab_finance:
        st.subheader("💰 Financial Summary")
        col_status, col_chart = st.columns(2)
        with col_status:
            if remaining_budget >= 0:
                st.success(f" Remaining: {remaining_budget:,} THB")
            else:
                st.error(f"Over Budget: {abs(remaining_budget):,} THB")
        with col_chart:
            st.bar_chart(pd.DataFrame.from_dict(expense_summary, orient='index', columns=['Amount']))

else:
    st.image("https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?q=80&w=2039&auto=format&fit=crop", 
             caption="Discover the Amazing Thailand", 
             use_container_width=True)
    st.markdown("👋 Welcome to your AI Travel Companion!")
    st.write("Plan your perfect trip to any of Thailand's 77 provinces in seconds.")
    
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info(" **Weather**")
        st.caption("Real-time forecast")
    with col2:
        st.success(" **Food**")
        st.caption("Local menu ideas")
    with col3:
        st.warning(" **Attractions**")
        st.caption("Top rated places")
    with col4:
        st.error(" **Navigation**")
        st.caption("Google Maps Link")

    st.divider()
    st.info("👈 **Ready? Go to the Sidebar on the left to start planning!**")