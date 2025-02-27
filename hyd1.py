import streamlit as st
import langchain_core
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser


GOOGLE_API_KEY=st.secrets["GOOGLE_API_KEY"]
# Initialize AI Model
chat_model = ChatGoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="gemini-2.0-flash-exp", temperature=1)

# List of Hyderabad Metro Stations with Specialties
stations_info = {
    "Nagole": "Residential area, well-connected to Uppal and IT corridor.",
    "Uppal": "Near Rajiv Gandhi International Cricket Stadium 🏏.",
    "Stadium": "Close to Rajiv Gandhi International Stadium 🏟️.",
    "NGRI": "Near National Geophysical Research Institute 🏛️.",
    "Habsiguda": "Education hub with research institutes 🏫.",
    "Tarnaka": "Shopping centers & eateries 🍽️.",
    "Mettuguda": "Military area & railway colony 🚉.",
    "Secunderabad East": "Major transit hub near Secunderabad Railway Station 🚂.",
    "Parade Ground": "Military parade ground & close to shopping areas 🎖️.",
    "Paradise": "Famous for Paradise Biryani 🍛.",
    "Rasoolpura": "Near Begumpet Airport & army cantonment ✈️.",
    "Prakash Nagar": "Corporate offices & business hubs 🏢.",
    "Begumpet": "Close to Hyderabad’s commercial hub 🏬.",
    "Ameerpet": "Education hub with coaching institutes 📚.",
    "Madhura Nagar": "Residential & peaceful area 🏡.",
    "Yousufguda": "Near Film Nagar, close to Tollywood 🎥.",
    "Jubilee Hills Road No. 5": "Luxury area, near Apollo Hospital 🏥.",
    "Jubilee Hills Check Post": "High-end restaurants & pubs 🍷.",
    "Peddamma Temple": "Famous religious site 🛕.",
    "Madhapur": "Heart of Hyderabad’s IT sector 💻.",
    "Durgam Cheruvu": "Scenic lake with boating 🚣.",
    "Hitech City": "Cyber Towers & IT parks 🌆.",
    "Raidurg": "Close to IKEA & major IT hubs 🛋️.",
    "Miyapur": "Growing residential & commercial hub 🏘️.",
    "JNTU College": "Engineering students’ hub 🎓.",
    "KPHB Colony": "Largest residential colony in Hyderabad 🏠.",
    "Kukatpally": "Major shopping & business center 🛍️.",
    "Balanagar": "Industrial area with manufacturing units 🏭.",
    "Moosapet": "Connectivity hub to major roads 🚗.",
    "Bharat Nagar": "Residential & commercial mix 🏘️.",
    "Erragadda": "Near ESI hospital & mental health institute 🏥.",
    "ESI Hospital": "Major government hospital 🏨.",
    "SR Nagar": "Coaching centers & hostels 🏢.",
    "Punjagutta": "High-end malls & corporate offices 🏙️.",
    "Irrum Manzil": "Close to high-end residential areas 🏡.",
    "Khairatabad": "Near Hussain Sagar Lake & Secretariat 🌊.",
    "Lakdi-ka-Pul": "Near Hyderabad Deccan Railway Station 🚂.",
    "Assembly": "Near Telangana State Assembly 🏛️.",
    "Nampally": "Close to Hyderabad’s old city & markets 🏘️.",
    "Gandhi Bhavan": "Near Gandhi Bhavan Congress HQ 🏢.",
    "Osmania Medical College": "Medical college & hospitals 🏥.",
    "MG Bus Station": "Biggest bus terminal, connects across Telangana 🚌.",
    "Malakpet": "Near Hyderabad Race Club 🏇.",
    "New Market": "Commercial shopping area 🏬.",
    "Musarambagh": "Residential area with local markets 🏘️.",
    "Dilsukhnagar": "Shopping & entertainment hub 🎬.",
    "Chaitanyapuri": "Education centers & PG accommodations 🎓.",
    "Victoria Memorial": "Close to LB Nagar’s residential area 🏠.",
    "LB Nagar": "Major transit hub & real estate hotspot 🏙️.",
    "JBS Parade Ground": "Military area & major bus terminal 🚍.",
    "Secunderabad West": "Near Secunderabad Railway Station 🚉.",
    "Gandhi Hospital": "Large government hospital 🏥.",
    "Musheerabad": "Near RTC X Roads & Chikkadpally 📍.",
    "RTC X Roads": "Cultural & entertainment hub 🎭.",
    "Chikkadpally": "Residential area with movie theaters 🎬.",
    "Narayanaguda": "Coaching centers & restaurants 🍜.",
    "Sultan Bazar": "Old Hyderabad shopping market 🛒."
}

# Define the chat template
chat_template = ChatPromptTemplate(
    messages=[
        ("system",  
         "You are an expert assistant for Hyderabad Metro Rail 🚆, providing optimal metro routes, estimated fares 💰, travel time ⏳, interchange stations 🔄, and key specialties of each station 📍."
         "Hyderabad Metro has three lines: **Blue (Nagole ↔ Raidurg) 🔵, Red (Miyapur ↔ LB Nagar) 🔴, and Green (JBS Parade Ground ↔ MGBS) 🟢**."
         "Calculate fares based on the number of stations traveled (₹10 to ₹60) and adjust the total fare based on the number of passengers. Mention interchange points if applicable."
         "List all stations 📍, highlight entry/exit points 🚉, and provide nearby landmarks and station specialties."
         "If a location is outside the metro network, politely inform users."),
        ("human", "Find the best travel options from {source} to {destination} for {passengers} passenger(s)."),
    ]  
)

parser = StrOutputParser()
chain = chat_template | chat_model | parser

# Streamlit UI
st.title("🚆 AI-Powered Hyderabad Metro Travel Planner 🇮🇳")  

source = st.selectbox("📍 Select Source Location:", list(stations_info.keys()), index=3)  
destination = st.selectbox("📍 Select Destination:", list(stations_info.keys()), index=6)  
passengers = st.number_input("👥 Number of Passengers:", min_value=1, max_value=10, value=1)  

if st.button("🚉 Get Travel Options"):
    if source and destination:
        response = chain.invoke({"source": source, "destination": destination, "passengers": passengers})
        st.success("✅ Here are your travel options:")
        st.write(response)
        
        # Show Station Specialties
        st.subheader("ℹ️ Station Information:")
        st.write(f"🔹 **{source}**: {stations_info[source]}")
        st.write(f"🔹 **{destination}**: {stations_info[destination]}")
    else:
        st.error("⚠️ Please select both source and destination.")
