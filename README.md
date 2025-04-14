# Chennai Rental Price Predictor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)
![ML](https://img.shields.io/badge/ML-Scikit--learn-orange)

</div>


### The project contain flask framework so cannot directly host in github😔 



## Student Information
```
Name            : Athul S
Register Number : RA2311047010117
Course         : BTech AI
Department     : CINTEL
College        : SRM KTR
collage email  : as2227@srm.st.edu.in
personal email : imathul270@gmail.com
gith

```

## Project Overview

The Chennai Rental Price Predictor is an advanced web application that combines machine learning with real-time web scraping to help users find and analyze rental properties in Chennai. It provides accurate rent predictions and finds similar available properties from major real estate websites.

### 🎯 Key Features

1. **Smart Rent Prediction**
   - Machine learning-based price range prediction
   - Location-aware pricing analysis
   - Annual cost estimation
   - Seasonal market insights

2. **Real-Time Property Search**
   - Live data from 99acres and Magicbricks
   - Property matching algorithm
   - Similarity scoring system
   - Comprehensive property details

3. **Intelligent Analysis**
   - Market trend analysis
   - Seasonal pricing advice
   - Location-based comparisons
   - Price range categorization

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Scikit-learn** - Machine learning
- **Pandas** - Data processing
- **NumPy** - Numerical computations

### Frontend
- **HTML5/CSS3**
- **Bootstrap 5** - Responsive design
- **JavaScript** - Dynamic interactions
- **Font Awesome** - UI icons

### Data Collection
- **Selenium** - Web automation
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP client
- **Concurrent.futures** - Parallel processing

## 📊 Supported Locations

The application covers 16 prime locations in Chennai:

1. Anna Nagar
2. T Nagar
3. Velachery
4. Adyar
5. Nungambakkam
6. Kilpauk
7. Kodambakkam
8. Royapettah
9. Saidapet
10. Medavakkam
11. Pallavaram
12. Chromepet
13. Guindy
14. Egmore
15. Perungudi
16. Sholinganallur

## 💰 Price Range Categories

- **Category 1**: ₹10,000 - ₹15,000
- **Category 2**: ₹15,000 - ₹25,000
- **Category 3**: ₹25,000 - ₹35,000
- **Category 4**: ₹35,000+

## 🚀 Installation Guide

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd rentpredicto
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Chrome WebDriver**
   - Download ChromeDriver from: https://sites.google.com/chromium.org/driver/
   - Add to system PATH

5. **Run the Application**
   ```bash
   python app.py
   ```

## 📁 Project Structure

```
rentpredicto/
├── app.py              # Main Flask application
├── scraper.py          # Web scraping module
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── data/              # Data storage
│   ├── rental_data.json
│   └── rental_cache.json
└── templates/         # Frontend templates
    └── index.html
```

## 🔧 Core Components

### 1. Web Scraper (`scraper.py`)
- Multi-threaded scraping
- Intelligent caching system
- Error handling and retries
- Data validation

### 2. ML Model (`app.py`)
- Logistic Regression classifier
- Feature scaling
- Location encoding
- Price range prediction

### 3. Property Matcher
- Area range: ±500 sq ft
- Bedroom range: ±2 rooms
- Similarity threshold: 0.3
- Smart scoring system

## 📈 Features in Detail

### Data Collection
- Real-time scraping from multiple sources
- 24-hour cache mechanism
- Concurrent page processing
- Robust error handling

### Price Prediction
- Location-based analysis
- Area and bedroom correlation
- Occupancy consideration
- Seasonal adjustments

### User Interface
- Responsive design
- Interactive forms
- Real-time updates
- Visual price comparisons

## 🌟 Usage Examples

1. **Basic Search**
   - Select location: "Anna Nagar"
   - Enter area: 1000 sq ft
   - Bedrooms: 2
   - Occupants: 3

2. **Advanced Analysis**
   - Compare multiple locations
   - Track seasonal trends
   - Analyze price ranges
   - View similar properties

## 🔄 Seasonal Advice

The application provides contextual advice based on:

- **Summer (Jun-Aug)**
  ```
  Peak rental season due to academic year start
  Higher prices expected
  ```

- **Winter (Nov-Jan)**
  ```
  Off-peak season
  Better deals available
  ```

- **Other Months**
  ```
  Regular market rates
  Standard availability
  ```

## 🛡️ Error Handling

1. **Web Scraping**
   - Connection timeout handling
   - Parse error recovery
   - Rate limiting protection
   - Data validation

2. **User Input**
   - Input sanitization
   - Range validation
   - Type checking
   - Error messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Data sources: 99acres.com and Magicbricks.com
- Python community for excellent libraries
- Flask framework developers
- Bootstrap team for UI components

---

<div align="center">
Made with ❤️ by Athul S
</div>

<div align="center">

### Contact Information
📧 Email: [as2227@srmist.edu.in](mailto:as2227@srmist.edu.in) | [imathul270@gmail.com](mailto:imathul270@gmail.com)  
🎓 SRM Institute of Science and Technology, KTR Campus

</div>

<div align="center">
<sub>© 2024 Athul S. All Rights Reserved.</sub>

<sub>This project and all its contents are protected by copyright law. Any unauthorized copying, modification, distribution, or use of this material is strictly prohibited.</sub>

![Visitors](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=Visitors&query=value&url=https://api.countapi.xyz/hit/athul-rentpredicto/readme)
![Last Updated](https://img.shields.io/badge/Last%20Updated-March%202024-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
</div> 
