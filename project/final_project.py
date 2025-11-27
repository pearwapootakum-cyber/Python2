import streamlit as st
import random
import time
import requests
import pandas as pd


WEATHER_API_KEY = "477850cd419666f030893bd839f114b7"
TMDB_API_KEY    = "a5b492f57ce7c0e6d1c40031f3b648a3"
FOOD_API_KEY    = "eba58fe8c87d4e8e8f029582ecacf0b5"
PLACES_API_KEY  = "A9rNakCgh04JyLvKLIy5uuCNGrFrYLa4"

st.set_page_config(page_title="Thailand Smart Trip", page_icon="🇹🇭", layout="wide")


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

ALL_PROVINCES = sorted([
    "Bangkok", "Krabi", "Kanchanaburi", "Kalasin", "Kamphaeng Phet", "Khon Kaen", "Chanthaburi", "Chachoengsao", "Chonburi", "Chainat", "Chaiyaphum", "Chumphon", "Chiang Rai", "Chiang Mai", "Trang", "Trat", "Tak", "Nakhon Nayok", "Nakhon Pathom", "Nakhon Phanom", "Nakhon Ratchasima", "Nakhon Si Thammarat", "Nakhon Sawan", "Nonthaburi", "Narathiwat", "Nan", "Bueng Kan", "Buriram", "Pathum Thani", "Prachuap Khiri Khan", "Prachinburi", "Pattani", "Phra Nakhon Si Ayutthaya", "Phayao", "Phang Nga", "Phatthalung", "Phichit", "Phitsanulok", "Phetchaburi", "Phetchabun", "Phrae", "Phuket", "Maha Sarakham", "Mukdahan", "Mae Hong Son", "Yala", "Yasothon", "Roi Et", "Ranong", "Rayong", "Ratchaburi", "Lopburi", "Lampang", "Lamphun", "Loei", "Sisaket", "Sakon Nakhon", "Songkhla", "Satun", "Samut Prakan", "Samut Songkhram", "Samut Sakhon", "Sa Kaeo", "Saraburi", "Sing Buri", "Sukhothai", "Suphan Buri", "Surat Thani", "Surin", "Nong Khai", "Nong Bua Lamphu", "Ang Thong", "Amnat Charoen", "Udon Thani", "Uttaradit", "Uthai Thani", "Ubon Ratchathani"
])


class APIService:
    def __init__(self):
        self.lat = 13.7563
        self.lon = 100.5018

    def get_weather(self, city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},TH&appid={WEATHER_API_KEY}&units=metric"
            res = requests.get(url, timeout=3).json()
            if res.get('weather'):
                self.lat = res['coord']['lat']
                self.lon = res['coord']['lon']
                return {
                    "temp": res['main']['temp'], 
                    "icon": res['weather'][0]['icon'], 
                    "desc": res['weather'][0]['description']
                }
        except: return None

    def get_real_places(self):
        places = []
        try:
            url = f"https://api.opentripmap.com/0.1/en/places/radius?radius=10000&lon={self.lon}&lat={self.lat}&kinds=tourist_facilities&rate=3&format=json&apikey={PLACES_API_KEY}"
            res = requests.get(url, timeout=3).json()
            for item in res[:5]:
                name = item.get('name', 'Unknown Place')
                if name:
                    price = random.choice([0, 0, 20, 50, 100])
                    # OpenTripMap gives coords in the 'point' object
                    lat = item.get('point', {}).get('lat', self.lat)
                    lon = item.get('point', {}).get('lon', self.lon)
                    places.append({"name": name, "price": price, "lat": lat, "lon": lon})
        except: pass
        return places

    def get_food(self):
        foods = []
        try:
            url = f"https://api.spoonacular.com/recipes/random?apiKey={FOOD_API_KEY}&number=3"
            res = requests.get(url, timeout=3).json()
            for item in res['recipes']:
                price = int((item.get('pricePerServing', 100) / 100) * 25) 
                if price < 40: price = 40
                foods.append({"title": item['title'], "image": item.get('image'), "price": price})
        except: pass
        
        if not foods:
            foods = [
                {"title": "Pad Thai", "image": "https://loremflickr.com/400/300/padthai", "price": 50},
                {"title": "Khao Man Gai", "image": "https://loremflickr.com/400/300/chicken,rice", "price": 45},
                {"title": "Mango Sticky Rice", "image": "https://loremflickr.com/400/300/mango,rice", "price": 60}
            ]
        return foods

    def get_movies(self):
        movies = []
        try:
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
            res = requests.get(url, timeout=3).json()
            for item in res['results'][:3]:
                img = f"https://image.tmdb.org/t/p/w200{item['poster_path']}"
                movies.append({"title": item['title'], "image": img, "rating": item['vote_average']})
        except: pass
        return movies

def get_fallback_places(city, base_lat, base_lon):
    return [
        {"name": f"{city} City Pillar Shrine", "price": 0, "lat": base_lat + 0.01, "lon": base_lon + 0.01},
        {"name": f"Wat Mahathat {city}", "price": 20, "lat": base_lat - 0.01, "lon": base_lon - 0.01},
        {"name": f"{city} Public Park", "price": 0, "lat": base_lat + 0.02, "lon": base_lon - 0.02},
        {"name": f"{city} Walking Street", "price": 0, "lat": base_lat - 0.02, "lon": base_lon + 0.02}
    ]


with st.sidebar:
    st.header("⚙️ Trip Settings")
    name = st.text_input("Traveler Name", "John Doe")
    city = st.selectbox("Destination", ALL_PROVINCES)
    budget = st.slider("Budget (THB)", 0, 10000, 1500, step=100)
    btn = st.button("Generate Itinerary", type="primary")

st.markdown("<div class='main-header'> Smart Trip Planner</div>", unsafe_allow_html=True)

if btn:
    api = APIService()
    
    with st.spinner(f"Creating route for {city}..."):
        time.sleep(1)
        weather = api.get_weather(city)
        real_places = api.get_real_places()
        places = real_places if real_places else get_fallback_places(city, api.lat, api.lon)
        foods = api.get_food()
        movies = api.get_movies()


    c1, c2, c3 = st.columns(3)
    c1.metric("Destination", city)
    c2.metric("Budget", f"{budget:,} THB")
    if weather: c3.metric("Weather", f"{weather['temp']}°C", weather['desc'].title())

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📅 Timeline & Navigate", "🗺️ Route Map", "📊 Budget"])

    curr = budget
    expenses = {"Food": 0, "Activity": 0, "Transport": 0}
    
  
    map_points = []

    with tab1:
        st.subheader(f"🗓️ Itinerary for {name}")

      
        p1 = places[0]
        map_points.append({"lat": p1['lat'], "lon": p1['lon'], "name": p1['name'], "color": "#FF4B4B"})
        
        with st.container():
            col_img, col_txt = st.columns([1, 3])
            col_img.image(f"https://loremflickr.com/400/300/{city},temple", use_container_width=True)
            with col_txt:
                nav_link = f"https://www.google.com/maps/search/?api=1&query={p1['name']}+{city}"
                st.markdown(f"""
                <div class='card'>
                    <b>09:00 AM - {p1['name']}</b><br>
                    Start your journey here.<br>
                    <a href='{nav_link}' target='_blank' class='nav-btn'>📍 Navigate (Google Maps)</a>
                </div>
                """, unsafe_allow_html=True)
                
                if p1['price'] == 0: st.markdown("<span class='free-badge'>Free Entry</span>", unsafe_allow_html=True)
                else: 
                    st.markdown(f"<span class='price-badge'>Entry: {p1['price']} THB</span>", unsafe_allow_html=True)
                    curr -= p1['price']
                    expenses["Activity"] += p1['price']

      
        f1 = foods[0]
        st.markdown("---")
        with st.container():
            col_img, col_txt = st.columns([1, 3])
            col_img.image(f1['image'], width=150)
            with col_txt:
                st.markdown(f"<div class='card'><b>12:00 PM - Lunch: {f1['title']}</b></div>", unsafe_allow_html=True)
                st.markdown(f"<span class='price-badge'>Cost: {f1['price']} THB</span>", unsafe_allow_html=True)
                curr -= f1['price']
                expenses["Food"] += f1['price']

     
        st.markdown("---")
        p2 = places[1] if len(places) > 1 else places[0]
        map_points.append({"lat": p2['lat'], "lon": p2['lon'], "name": p2['name'], "color": "#FF4B4B"})
        
        with st.container():
            col_img, col_txt = st.columns([1, 3])
            col_img.image(f"https://loremflickr.com/400/300/{city},park", use_container_width=True)
            with col_txt:
                nav_link = f"https://www.google.com/maps/search/?api=1&query={p2['name']}+{city}"
                st.markdown(f"""
                <div class='card'>
                    <b>03:00 PM - Visit: {p2['name']}</b><br>
                    Relaxing afternoon.<br>
                    <a href='{nav_link}' target='_blank' class='nav-btn'>📍 Navigate (Google Maps)</a>
                </div>
                """, unsafe_allow_html=True)
                
                if p2['price'] == 0: st.markdown("<span class='free-badge'>Free Entry</span>", unsafe_allow_html=True)
                else:
                     st.markdown(f"<span class='price-badge'>Entry: {p2['price']} THB</span>", unsafe_allow_html=True)
                     curr -= p2['price']
                     expenses["Activity"] += p2['price']

       
        f2 = foods[1] if len(foods) > 1 else foods[0]
        st.markdown("---")
        with st.container():
            col_img, col_txt = st.columns([1, 3])
            col_img.image(f2['image'], width=150)
            with col_txt:
                st.markdown(f"<div class='card'><b>06:00 PM - Dinner: {f2['title']}</b></div>", unsafe_allow_html=True)
                st.markdown(f"<span class='price-badge'>Cost: {f2['price']} THB</span>", unsafe_allow_html=True)
                curr -= f2['price']
                expenses["Food"] += f2['price']

    with tab2:
        st.subheader(f"🗺️ Route Map in {city}")
        if map_points:
            
            df_map = pd.DataFrame(map_points)
            st.map(df_map, zoom=12)
            st.info("💡 Red dots indicate the tourist spots.")
        else:
            st.warning("Map data unavailable.")

    with tab3:
        st.subheader("💰 Financial Summary")
        c1, c2 = st.columns(2)
        with c1:
            if curr >= 0:
                st.success(f"✅ Remaining: {curr:,} THB")
            else:
                st.error(f"❌ Over Budget: {abs(curr):,} THB")
        with c2:
            st.bar_chart(pd.DataFrame.from_dict(expenses, orient='index', columns=['Amount']))

else:
    
    st.image("https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?q=80&w=2039&auto=format&fit=crop", 
             caption="Discover the Amazing Thailand", 
             use_container_width=True)

    st.markdown("## 👋 Welcome to your AI Travel Companion!")
    st.write("Plan your perfect trip to any of Thailand's 77 provinces in seconds. We combine real-time data to give you the best experience.")

    st.divider()

    st.subheader(" What we offer")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info(" **Weather**")
        st.caption("Real-time forecast check")
    
    with col2:
        st.success(" **Food**")
        st.caption("Local menu recommendations")
    
    with col3:
        st.warning(" **Cinema**")
        st.caption("Movie showtimes & ratings")
    
    with col4:
        st.error(" **Navigation**")
        st.caption("Google Maps integration")

   
    st.divider()
    st.subheader(" How to start?")
    
    step1, step2, step3 = st.columns(3)
    with step1:
        st.markdown("#### 1️⃣ Set Profile")
        st.write("Enter your name on the sidebar.")
    with step2:
        st.markdown("#### 2️⃣ Choose City")
        st.write("Select one of 77 provinces.")
    with step3:
        st.markdown("#### 3️⃣ Set Budget")
        st.write("Adjust your budget slider.")

    st.markdown("---")
    st.info("👈 **Ready? Go to the Sidebar on the left to start planning!**")