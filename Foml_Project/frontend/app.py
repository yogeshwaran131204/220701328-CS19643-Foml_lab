from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

# Initialize app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers="*")

# Load summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", tokenizer="sshleifer/distilbart-cnn-12-6")

# Load BERT model for recommendations
model = SentenceTransformer('all-MiniLM-L6-v2')

# Knowledge base
knowledge_base = [
    # Physics
    "Newton's Laws of Motion", "Thermodynamics", "Quantum Mechanics", "Relativity Theory", "Astrophysics",
    "Cosmology", "Optics", "Electromagnetism", "Nuclear Physics", "Wave-Particle Duality", "Acoustics",
    "Fluid Mechanics", "Quantum Entanglement", "Particle Physics", "Superconductivity", "Thermal Expansion",
    "Kinematics", "Dynamics", "Gravitational Waves", "Photoelectric Effect",

    # Chemistry
    "Atomic Structure", "Periodic Table", "Chemical Bonding", "Organic Chemistry", "Inorganic Chemistry",
    "Acids and Bases", "Chemical Reactions", "Thermochemistry", "Electrochemistry", "Kinetics",
    "Surface Chemistry", "Environmental Chemistry", "Polymers", "Biomolecules", "Nuclear Chemistry",
    "Coordination Compounds", "Isomerism", "pH Scale", "Colloids",

    # Biology
    "Cell Structure", "Photosynthesis", "Respiration in Plants", "Human Digestive System",
    "Human Circulatory System", "Genetics", "DNA Structure", "Evolution", "Ecology", "Biodiversity",
    "Endocrine System", "Nervous System", "Human Reproduction", "Plant Hormones", "Immunity System",
    "Genetic Engineering", "Microbiology", "Biotechnology Applications", "Food Production Technology",

    # Mathematics
    "Algebra", "Linear Equations", "Calculus", "Differential Equations", "Probability Theory",
    "Statistics", "Coordinate Geometry", "Matrix Algebra", "Vector Algebra", "Trigonometry",
    "Set Theory", "Complex Numbers", "Number Theory", "Limits and Continuity", "Permutations and Combinations",
    "Integration Techniques", "Sequences and Series", "Differentiation", "Mathematical Reasoning",

    # Computer Science
    "Data Structures", "Algorithms", "Database Management Systems", "Operating Systems",
    "Computer Networks", "Artificial Intelligence", "Machine Learning", "Neural Networks",
    "Deep Learning", "Natural Language Processing", "Cryptography", "Blockchain Technology",
    "Software Engineering", "Cyber Security", "Cloud Computing", "Internet of Things",
    "Big Data Analytics", "Mobile Computing", "Augmented Reality", "Virtual Reality",

    # History
    "Ancient Egyptian Civilization", "Indus Valley Civilization", "Mesopotamian Civilization",
    "Greek Civilization", "Roman Empire", "Byzantine Empire", "Islamic Golden Age", "Renaissance Era",
    "Industrial Revolution", "American Revolution", "French Revolution", "Russian Revolution",
    "World War I", "World War II", "Cold War", "Civil Rights Movement", "Vietnam War", "Apartheid in South Africa",
    "Fall of the Berlin Wall", "Arab Spring",

    # Geography
    "Plate Tectonics", "Volcanoes", "Earthquakes", "Ocean Currents", "Atmospheric Circulation",
    "Climate Zones", "Desertification", "Tsunamis", "Glaciers", "River Systems",
    "Mountain Formation", "Weathering and Erosion", "Soil Formation", "Natural Resources",
    "Renewable Resources", "Urban Geography", "Demographic Transition", "Agricultural Geography",
    "Geographical Information Systems (GIS)", "Global Positioning System (GPS)",

    # Political Science / Civics
    "Democracy", "Republic", "Constitution", "Separation of Powers", "Judiciary System",
    "Executive Powers", "Legislative Process", "Federalism", "Political Parties", "Elections",
    "Human Rights", "Civil Liberties", "Public Administration", "International Relations",
    "United Nations", "World Trade Organization", "NATO", "European Union", "Brexit", "Globalization",

    # Economics
    "Supply and Demand", "Market Structures", "Monopoly and Oligopoly", "Inflation", "Deflation",
    "Gross Domestic Product (GDP)", "Fiscal Policy", "Monetary Policy", "Banking System",
    "Microeconomics", "Macroeconomics", "International Trade", "Global Financial Crisis",
    "Labor Economics", "Income Inequality", "Public Finance", "Taxation", "Stock Markets",
    "Cryptocurrency", "Economic Development",

    # Environmental Science
    "Climate Change", "Greenhouse Effect", "Global Warming", "Carbon Footprint",
    "Renewable Energy Sources", "Solar Energy", "Wind Energy", "Hydroelectricity",
    "Biodiversity Conservation", "Ozone Layer Depletion", "Water Pollution",
    "Air Pollution", "Deforestation", "Waste Management", "Ecosystem Services",
    "Sustainability", "Carbon Sequestration", "Endangered Species", "Conservation Biology", "Wildlife Protection",

    # Psychology
    "Behavioral Psychology", "Cognitive Psychology", "Developmental Psychology",
    "Clinical Psychology", "Social Psychology", "Abnormal Psychology", "Positive Psychology",
    "Psychological Disorders", "Personality Theories", "Therapy Techniques",
    "Cognitive Behavioral Therapy", "Psychoanalysis", "Freud's Theories", "Humanistic Psychology",
    "Learning Theories", "Memory and Forgetting", "Sensation and Perception", "Motivation Theories",
    "Emotion Theories", "Psychological Testing",

    # Sociology
    "Social Stratification", "Culture and Society", "Socialization", "Gender Roles",
    "Race and Ethnicity", "Urban Sociology", "Rural Sociology", "Family Structures",
    "Religion and Society", "Social Movements", "Deviance and Crime", "Education and Society",
    "Work and Economy", "Globalization Impact", "Social Change", "Social Inequality",
    "Political Sociology", "Medical Sociology", "Demography", "Migration Patterns",

    # Literature
    "Shakespeare's Plays", "Modernist Literature", "Postmodern Literature",
    "Romantic Poetry", "Victorian Novels", "Greek Tragedies", "Epic Poetry",
    "Indian English Literature", "American Literature", "African Literature",
    "Magical Realism", "Realism and Naturalism", "Drama and Theater Studies",
    "Creative Writing", "Literary Criticism", "Poetry Analysis", "Children’s Literature",
    "Women’s Writing", "Contemporary Literature", "Autobiographies and Memoirs",

    # Art and Culture
    "Renaissance Art", "Baroque Art", "Modern Art", "Cubism", "Impressionism",
    "Abstract Art", "Pop Art", "Ancient Greek Sculpture", "Indian Classical Dance",
    "Ballet", "Opera", "Music Theory", "Contemporary Music", "Film Studies",
    "Photography Techniques", "Theater Production", "World Heritage Sites",
    "Cultural Festivals", "Art History", "Sculpture Techniques",

    # General Knowledge / Current Affairs
    "Nobel Prize Winners", "Olympic Games", "Space Exploration",
    "International Organizations", "World Health Organization (WHO)",
    "International Monetary Fund (IMF)", "United Nations Environment Program (UNEP)",
    "World Bank", "G20 Summit", "Climate Summits",
    "Nuclear Non-Proliferation Treaty", "Artificial Islands", "Smart Cities",
    "Digital India", "Clean Energy Initiatives", "5G Technology",
    "Data Privacy Laws", "Cybersecurity Frameworks", "Artificial Intelligence Ethics",
    "Autonomous Vehicles", "Metaverse", "Genetic Modification", "CRISPR Technology",
    "Smart Grids", "Internet of Things Applications", "SpaceX and Private Space Travel",
    "Mars Colonization Projects", "Electric Vehicles", "Drone Technology",
    "Food Security Programs", "Global Pandemic Preparedness", "Medical Breakthroughs",
    "Telemedicine", "Climate Refugees", "Water Crisis Management",
    "Zero Waste Initiatives", "Plastic Pollution Solutions", "Sustainable Fashion",
    "Ethical Hacking", "Renewable Batteries", "Circular Economy", "Global Leadership Challenges",
        "Pulsars", "Quasars", "Neutrino Oscillation", "Dark Flow", "Multiverse Theory",
    "Supernovae", "String Theory", "Astrobiology", "Exoplanet Discoveries", "Event Horizon Telescope",
    "Synthetic Biology", "Gene Therapy", "Human Genome Project", "Stem Cell Research", "Cloning Techniques",
    "CRISPR-Cas9", "Personalized Medicine", "Cancer Immunotherapy", "Epigenetics", "Neuroplasticity",
    "Brain-Computer Interface", "Quantum Cryptography", "Quantum Supremacy", "Quantum Sensors", "Photonic Computing",
    "Smart Dust Technology", "Digital Twins", "Edge Computing", "Fog Computing", "Swarm Robotics",
    "Deep Reinforcement Learning", "Explainable AI", "Federated Learning", "TinyML", "AutoML",
    "World War I Causes", "Renaissance Cultural Movement", "Ottoman Empire Expansion", "Mughal Empire in India", "Colonialism in Africa",
    "American Civil Rights Movement", "Globalization Impacts", "Industrialization Effects", "French Revolution Effects", "Apartheid System",
    "George Orwell", "Aldous Huxley", "J.K. Rowling", "Agatha Christie", "Ernest Hemingway",
    "1984", "Brave New World", "To Kill a Mockingbird", "Pride and Prejudice", "The Great Gatsby",
    "UNICEF", "WHO Health Programs", "International Criminal Court", "World Food Programme", "UNESCO World Heritage",
    "Digital Divide", "Internet Censorship", "E-waste Management", "Smart Agriculture", "Precision Farming",
    "Nobel Prize in Physics", "Nobel Prize in Chemistry", "Nobel Peace Prize Winners", "Youngest Nobel Laureates", "Nobel in Economics",
    "Machine Ethics", "Moral Responsibility in AI", "Privacy and Surveillance", "Algorithmic Bias", "AI Safety Research",
    "Renewable Hydrogen", "Ocean Energy", "Geothermal Energy", "Tidal Energy Projects", "Carbon Capture Technology",
    "Wildlife Corridors", "Coral Reef Conservation", "Wetlands Protection", "Urban Green Spaces", "Ecotourism Benefits",
    "Global Hunger", "Food Security Challenges", "Water Scarcity Solutions", "Desalination Technologies", "Irrigation Innovations",
    "Public Health Policies", "Vaccination Drives", "Pandemic Response Strategies", "Mental Health Awareness", "Occupational Therapy",
    "Social Entrepreneurship", "Microfinance Models", "Financial Literacy", "Cashless Economy", "Cryptocurrency Risks",
    "Data Science Applications", "AI in Healthcare", "Blockchain in Supply Chains", "Digital Banking Trends", "Fintech Innovations",
    "Renewable Battery Technologies", "Solid-State Batteries", "Lithium-Sulfur Batteries", "Graphene Supercapacitors", "Battery Recycling",
    "3D Printing Technology", "Additive Manufacturing", "Biofabrication", "3D Printed Organs", "Custom Prosthetics",
    "Self-Driving Cars", "Ethical Challenges in Automation", "Smart Cities Infrastructure", "Vertical Farming", "Green Architecture",
    "Sustainable Urban Transport", "Metro Rail Systems", "Electric Scooters", "Hyperloop Technology", "Space Tourism",
    "Artemis Mission", "Mars Rover Perseverance", "James Webb Telescope", "Asteroid Mining", "Space Law",
    "Neuroscience Research", "Consciousness Studies", "Dream Analysis", "Emotional Intelligence", "Cognitive Behavioral Therapy",
    "Cultural Anthropology", "Archaeological Discoveries", "Human Migration Patterns", "Population Explosion", "Urban Slums",
    "Mega Cities Challenges", "Gentrification", "Affordable Housing Policies", "Sustainable Development Goals",
    "Income Inequality Trends", "Poverty Alleviation Strategies", "Fair Trade Practices", "Global Trade Agreements",
    "G7 Summits", "BRICS Countries", "OPEC Decisions", "World Economic Forum", "International Labor Organization",
    "Political Ideologies", "Socialism vs Capitalism", "Populism Rise", "Liberal Democracy", "Authoritarianism",
    "Election Processes Worldwide", "Voting Behavior Patterns", "Women in Politics", "Youth Participation in Politics",
    "Global Cybersecurity Threats", "Data Breach Incidents", "Cloud Security Innovations", "GDPR Compliance", "Digital Sovereignty",
    "Ocean Pollution", "Marine Biodiversity Loss", "Plastic Waste Reduction", "Biodegradable Plastics", "Sustainable Fishing Practices",
    "Renewable Packaging", "Zero Carbon Cities", "Circular Economy Models", "Resource Efficiency",
    "Humanitarian Interventions", "War Refugees", "Human Trafficking Issues", "Modern Slavery", "Disaster Risk Reduction",
    "Wildfire Management", "Flood Management Systems", "Early Warning Systems", "Climate Smart Agriculture",
    "Food Waste Solutions", "Bioenergy from Waste", "Composting Systems", "Waste to Energy Plants", "Plastic Alternative Innovations",
    "Remote Sensing Technology", "Satellite Imaging", "Geospatial Data Analysis", "Drone Mapping", "Earth Observation Satellites",
    "Ethical Hacking Careers", "Penetration Testing Methods", "Bug Bounty Programs", "Zero Trust Security Models", "Multi-Factor Authentication",
    "Digital Literacy Programs", "E-learning Innovations", "Virtual Labs", "Online Certification Programs", "Remote Work Trends",
    "Gig Economy Growth", "Freelancing Platforms", "Remote Team Management", "Virtual Reality Meetings", "Digital Nomad Lifestyles",
    "Personal Branding", "Influencer Marketing", "Social Media Analytics", "Online Reputation Management", "Brand Authenticity",
    "Sustainable Fashion", "Eco-Friendly Clothing Brands", "Slow Fashion Movement", "Upcycling Techniques", "Second-Hand Marketplaces",
    "Space Weather Prediction", "Solar Flare Effects", "Geomagnetic Storms", "Astrobiology Missions", "Search for Extraterrestrial Life",
    "Mindfulness Techniques", "Yoga Therapy", "Meditation Research", "Breathwork Practices", "Positive Psychology Applications",
    "Ethics in Journalism", "Freedom of Press", "Media Censorship Cases", "Fake News Identification", "Digital Journalism Trends",
    "Self-Publishing Trends", "Audiobook Market", "E-book Publishing", "Print on Demand Technology", "Crowdfunding for Authors",
    "Biosphere Reserves", "World Natural Heritage Sites", "Global Seed Vault", "Botanical Gardens Role", "Biodiversity Hotspots",
    "Planetary Health", "One Health Approach", "Eco-Health Concepts", "Zoonotic Diseases Awareness", "Biodiversity and Pandemics",
    "Youth Movements", "Climate Activism", "Fridays for Future", "Greta Thunberg Movement", "Grassroots Environmental Campaigns",
    "Paris, France",
    "Rome, Italy",
    "Tokyo, Japan",
    "New York City, USA",
    "London, England",
    "Sydney, Australia",
    "Dubai, UAE",
    "Singapore City, Singapore",
    "Bali, Indonesia",
    "Santorini, Greece",
    "Machu Picchu, Peru",
    "Grand Canyon, USA",
    "Niagara Falls, Canada",
    "Amalfi Coast, Italy",
    "Mount Fuji, Japan",
    "Great Wall of China",
    "Maldives Islands",
    "Iceland Northern Lights",
    "Venice, Italy",
    "Bora Bora, French Polynesia",
    "Petra, Jordan",
    "Great Barrier Reef, Australia",
    "Swiss Alps, Switzerland",
    "Cappadocia, Turkey",
    "Serengeti National Park, Tanzania",
    "Banff National Park, Canada",
    "Yellowstone National Park, USA",
    "New Zealand South Island",
    "Patagonia, Argentina",
    "Angkor Wat, Cambodia",
    "Kyoto, Japan",
    "Edinburgh, Scotland",
    "Cairo, Egypt",
    "Seychelles Islands",
    "Zanzibar, Tanzania",
    "Barcelona, Spain",
    "Madrid, Spain",
    "Prague, Czech Republic",
    "Istanbul, Turkey",
    "Phuket, Thailand",
    "Kruger National Park, South Africa",
    "Athens, Greece",
    "Florence, Italy",
    "Hawaii, USA",
    "Oslo, Norway",
    "Lapland, Finland",
    "Alaska, USA",
    "Dubrovnik, Croatia",
    "Vienna, Austria",
    "Budapest, Hungary",
    "Marrakech, Morocco",
    "Lisbon, Portugal",
    "Reykjavik, Iceland",
    "Vancouver, Canada",
    "Johannesburg, South Africa",
    "Los Angeles, USA",
    "San Francisco, USA",
    "Rio de Janeiro, Brazil",
    "Buenos Aires, Argentina",
    "Victoria Falls, Zimbabwe",
    "Saigon (Ho Chi Minh City), Vietnam",
    "Hoi An, Vietnam",
    "Queenstown, New Zealand",
    "Mauritius Island",
    "Bora Bora Lagoon",
    "Seychelles Praslin Island",
    "Agra, India (Taj Mahal)",
    "Jaipur, India (Pink City)",
    "Kerala, India (Backwaters)",
    "Leh-Ladakh, India",
    "Rovaniemi, Finland",
    "Copenhagen, Denmark",
    "Brussels, Belgium",
    "Bruges, Belgium",
    "Amsterdam, Netherlands",
    "Rotterdam, Netherlands",
    "Abu Dhabi, UAE",
    "Doha, Qatar",
    "Muscat, Oman",
    "Luxor, Egypt",
    "Giza Pyramids, Egypt",
    "Cusco, Peru",
    "Santiago, Chile",
    "Medellín, Colombia",
    "Bogotá, Colombia",
    "Havana, Cuba",
    "Caribbean Cruise Destinations",
    "Galápagos Islands, Ecuador",
    "Easter Island, Chile",
    "Maldives Snorkeling Tours",
    "Caribbean Islands Hopping",
    "Alaskan Cruise Tours",
    "Northern Lights Hunting Trips",
    "Safari Tours in Kenya",
    "Whale Watching in Iceland",
    "Ski Trips to Aspen",
    "Hiking Trails in New Zealand",
    "Adventure Tours in Patagonia",
    "Culinary Tours in Italy",
    "Historical Sites of Rome"
]


# Embed the knowledge base
knowledge_embeddings = model.encode(knowledge_base, convert_to_tensor=True)

# Routes
@app.route('/')
def home():
    return "SmartEdu Backend is Running!"

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    return jsonify({"summary": summary})

@app.route('/recommend', methods=['GET'])
def recommend_topics():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, knowledge_embeddings)[0]
    top_indices = similarities.topk(5).indices.tolist()
    recommendations = [knowledge_base[idx] for idx in top_indices]
    return jsonify({"recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)
