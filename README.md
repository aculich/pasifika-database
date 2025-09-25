# 🐐 Pasifika Database Project

A comprehensive digital humanities project for cataloging, analyzing, and visualizing Pacific Island films and cultural data using modern web technologies and geospatial visualization tools.

## 📊 Project Overview

This project serves as a digital repository and interactive visualization platform for Pacific Island film data, featuring:

- **104 Films** from Pacific Island nations
- **Interactive Map Visualization** with island polygon overlays
- **Geospatial Data Analysis** using GeoJSON files
- **Cultural Heritage Preservation** through digital archiving
- **Research Tools** for academic and community use

## 🗺️ Data Sources

### Film Database
- **Source**: Curated collection of Pacific Island films
- **Format**: JSON with 104 film records
- **Fields**: Name, release date, country, island, language, status, indigenous leadership, streaming platforms, summaries
- **Coverage**: Hawaii, Samoa, Tonga, Fiji, New Zealand, Australia, and other Pacific nations

### Geospatial Data
- **Island Polygons**: Detailed GeoJSON files for Pacific Island boundaries
- **Cultural Sites**: Sacred places and cultural landmarks
- **Maritime Boundaries**: Exclusive Economic Zones and territorial waters
- **Ocean Currents**: NetCDF data for environmental analysis

## 🛠️ Technology Stack

### Frontend
- **Interactive Maps**: Leaflet.js with OpenStreetMap
- **Visualization**: Custom HTML5/CSS3/JavaScript
- **Responsive Design**: Mobile-friendly interface

### Backend & Data Processing
- **Python**: Data processing and analysis scripts
- **NodeGoat**: Web-based research environment (configured but not deployed)
- **Baserow**: Open-source Airtable alternative (configured)
- **Docker**: Containerized deployment options

### Data Formats
- **JSON**: Film metadata and configuration
- **GeoJSON**: Geospatial data for mapping
- **CSV**: Tabular data exports
- **SQL**: Database schemas and queries

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Modern web browser
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pasifika-database
   ```

2. **Start the visualization server**
   ```bash
   python3 -m http.server 8081
   ```

3. **Open in browser**
   ```
   http://localhost:8081/simple-film-visualizer.html
   ```

### Alternative: Docker Deployment
```bash
docker-compose up --build
```

## 📁 Project Structure

```
pasifika-database/
├── 📊 Data Files
│   ├── nodegoat-film-data.json      # Main film database (104 records)
│   ├── DATA.md                      # FAIR CARE data profile
│   └── SpectStory.md                # Project documentation
│
├── 🗺️ Visualization
│   ├── simple-film-visualizer.html  # Interactive map interface
│   └── pasifika-dashboard.py        # Python dashboard script
│
├── 🔧 Tools & Scripts
│   ├── airtable-explorer.py         # Airtable data exploration
│   ├── airtable-to-baserow.py       # Data migration tools
│   ├── import-pasifika-data.py      # Data import utilities
│   └── setup-nodegoat.py            # NodeGoat setup script
│
├── 🐳 Deployment
│   ├── docker-compose.yml           # Docker configuration
│   ├── Dockerfile                   # Container definition
│   └── apache-config.conf           # Web server config
│
└── 📚 Documentation
    ├── README.md                    # This file
    ├── NODEGOAT-SETUP-COMPLETE.md   # NodeGoat setup guide
    └── PROMPT.md                    # Project prompts
```

## 🎬 Film Database Features

### Interactive Map
- **Geographic Visualization**: Films plotted by island/country location
- **Color-Coded Markers**: 
  - 🔴 Released films
  - 🟠 In Production
  - 🟢 Indigenous Leadership
  - 🔵 Other categories
- **Search & Filter**: Find films by name, country, island, or language
- **Detailed Popups**: Film information with summaries and metadata

### Statistics Dashboard
- **Total Films**: 104 records
- **Countries**: 12 different nations
- **Islands**: 30+ Pacific islands
- **Languages**: 22 different languages

## 🗺️ Geospatial Features

### Island Polygon Overlays
- **Detailed Boundaries**: Accurate island shapes from GeoJSON data
- **Cultural Context**: Sacred sites and traditional territories
- **Environmental Data**: Ocean currents and maritime boundaries
- **Interactive Layers**: Toggle different data types

### Map Capabilities
- **Zoom & Pan**: Navigate across the Pacific
- **Layer Control**: Show/hide different data layers
- **Popup Information**: Detailed data on click
- **Responsive Design**: Works on desktop and mobile

## 🔬 Research Applications

### Academic Use
- **Digital Humanities**: Cultural data analysis
- **Geographic Studies**: Pacific Island research
- **Film Studies**: Indigenous cinema analysis
- **Cultural Preservation**: Heritage documentation

### Community Use
- **Cultural Education**: Learning about Pacific cultures
- **Film Discovery**: Finding relevant content
- **Geographic Context**: Understanding island relationships
- **Data Sharing**: Open access to research data

## 📈 Data Analysis

### FAIR CARE Principles
- **Findable**: Well-documented and searchable
- **Accessible**: Open access with proper attribution
- **Interoperable**: Standard formats (JSON, GeoJSON)
- **Reusable**: Clear licensing and documentation
- **CARE**: Community-driven, Authority to control, Responsibility, Ethics

### 5 Vs of Data Science
- **Volume**: 104 films + 163 GeoJSON files
- **Velocity**: Static dataset with periodic updates
- **Variety**: Multiple formats (JSON, GeoJSON, CSV, SQL)
- **Veracity**: Curated and validated data
- **Value**: Research, education, and cultural preservation

## 🤝 Contributing

### Data Contributions
- Film metadata additions
- Geospatial data improvements
- Cultural context information
- Translation assistance

### Technical Contributions
- Code improvements
- Bug fixes
- Feature additions
- Documentation updates

### Guidelines
- Follow FAIR CARE principles
- Maintain cultural sensitivity
- Provide proper attribution
- Test changes thoroughly

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Pacific Island Communities**: For sharing their stories and culture
- **Filmmakers**: For creating the works documented here
- **Researchers**: For contributing to the database
- **Open Source Community**: For the tools and libraries used

## 📞 Contact

For questions, contributions, or collaboration opportunities, please open an issue or contact the project maintainers.

---

*This project represents a commitment to preserving and sharing Pacific Island cultural heritage through modern digital tools and open access principles.*