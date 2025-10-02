# Instagram Analytics Dashboard

A comprehensive Python GUI application for analysing Instagram account performance using the Meta Graph API.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

### 📊 Analytics Dashboard
- **Account Overview**: Follower count, engagement rate, posting frequency
- **Post Analysis**: Performance metrics for individual posts
- **Engagement Tracking**: Likes, comments, shares, and saves analysis
- **Posting Patterns**: Optimal posting times and frequency analysis
- **Visual Charts**: Interactive charts and graphs for data visualization

### 🔧 Technical Features
- **Meta Graph API Integration**: Real Instagram data via official API
- **Demo Mode**: Test the application with realistic demo data
- **Data Export**: Export reports and charts in multiple formats
- **Real-time Updates**: Fetch latest data from Instagram
- **Secure Configuration**: Environment-based credential management

### 📈 Insights & Metrics
- Engagement rate calculation and benchmarking
- Top performing posts identification
- Hashtag performance analysis
- Audience demographic insights
- Growth trend analysis
- Content optimization recommendations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Meta Developer Account (for real data)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd instagram-analytics
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Try Demo Mode**
   - Click "Load Demo Data" to explore the app with sample data
   - No API setup required for demo mode

## 🔑 API Setup (Optional)

To use real Instagram data, you'll need to set up Meta Graph API access:

### Step 1: Create Meta Developer Account
1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a developer account or log in
3. Create a new app

### Step 2: Configure Instagram Basic Display
1. Add "Instagram Basic Display" product to your app
2. Configure OAuth redirect URIs
3. Add test users (your Instagram account)

### Step 3: Get Access Token
1. Generate a User Access Token
2. Exchange for Long-Lived Token (optional)
3. Get your Instagram Business Account ID

### Step 4: Configure Application
1. Create a `.env` file in the project root:
   ```env
   META_ACCESS_TOKEN=your_access_token_here
   META_APP_ID=your_app_id_here
   META_APP_SECRET=your_app_secret_here
   INSTAGRAM_ACCOUNT_ID=your_instagram_business_account_id
   ```

2. Or use the "Setup API Credentials" button in the app

## 📱 Usage Guide

### Getting Started
1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Choose Your Mode**
   - **Demo Mode**: Click "Load Demo Data" for immediate exploration
   - **Live Mode**: Configure API credentials for real data

### Using Demo Mode
1. Click "Load Demo Data" button
2. Explore different tabs:
   - **Account Overview**: See account statistics and metrics
   - **Posts Analysis**: View individual post performance
   - **Charts**: Interactive data visualizations
   - **Insights**: Detailed analytics and recommendations

### Using Live Mode
1. Click "Setup API Credentials" and enter your Meta API details
2. Click "Test Connection" to verify setup
3. Use data fetching buttons:
   - "Fetch Account Data": Get profile information
   - "Fetch Recent Posts": Get latest posts data
   - "Fetch Insights": Get account insights
   - "Analyze All Data": Perform comprehensive analysis

### Analyzing Your Data
1. **Account Overview Tab**
   - View follower growth and engagement metrics
   - See posting frequency and optimal timing
   - Review top-performing content

2. **Posts Analysis Tab**
   - Browse all recent posts with performance metrics
   - Identify high and low-performing content
   - Analyze posting patterns

3. **Charts Tab**
   - Visualize engagement trends
   - See posting pattern distributions
   - Compare performance across different metrics

4. **Insights Tab**
   - Get detailed analytics breakdown
   - View recommendations for improvement
   - See audience demographics (if available)

### Exporting Data
1. **Export Report**: Save detailed analytics as text file
2. **Save Charts**: Export visualizations as PNG images
3. **Data Export**: Save raw data in CSV/JSON format

## 🛠️ Project Structure

```
instagram-analytics/
│
├── main.py                 # Main GUI application
├── instagram_api.py        # Meta Graph API client
├── data_analyzer.py        # Data processing and analysis
├── demo_data.py           # Demo data generator
├── config.py              # Configuration management
├── utils.py               # Utility functions
├── test_app.py            # Unit tests
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
├── README.md             # This file
└── .env                  # Environment variables (create this)
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_app.py
```

The tests cover:
- Demo data generation
- Data analysis functions
- Metrics calculations
- API integration (mocked)
- Utility functions

## 📊 Metrics Explained

### Engagement Rate
```
Engagement Rate = (Likes + Comments) / Followers × 100
```
**Benchmarks**:
- 1-3%: Good for large accounts (100K+ followers)
- 3-6%: Excellent for large accounts
- 6-10%: Good for medium accounts (10K-100K)
- 10%+: Excellent for smaller accounts (<10K)

### Reach Rate
```
Reach Rate = Unique Accounts Reached / Followers × 100
```

### Growth Rate
```
Growth Rate = (Current - Previous) / Previous × 100
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `META_ACCESS_TOKEN` | Meta Graph API access token | Yes* |
| `META_APP_ID` | Meta app ID | Yes* |
| `META_APP_SECRET` | Meta app secret | Yes* |
| `INSTAGRAM_ACCOUNT_ID` | Instagram Business Account ID | Yes* |

*Required only for live data mode

### Application Settings

Modify `config.py` to customize:
- API endpoints and versions
- GUI appearance and colors
- Data refresh intervals
- Chart styling options

## 🚨 Troubleshooting

### Common Issues

**"API Connection Failed"**
- Verify your access token is valid and not expired
- Check that your Instagram account is a Business account
- Ensure all required permissions are granted

**"No Data Available"**
- Make sure you've fetched data using the fetch buttons
- Try using demo mode to verify the app works
- Check if your Instagram account has recent posts

**"Import Errors"**
- Install all required packages: `pip install -r requirements.txt`
- Check Python version (3.8+ required)
- Verify virtual environment activation

**"Charts Not Displaying"**
- Ensure matplotlib backend is compatible with your system
- Try running: `pip install --upgrade matplotlib`
- Check if data has been loaded/analyzed

### Debug Mode

Enable detailed logging by setting:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `python test_app.py`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a Pull Request

### Development Setup

```bash
# Clone your fork
git clone <your-fork-url>
cd instagram-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Meta for providing the Graph API
- tkinter for GUI framework
- matplotlib for data visualization
- All contributors and testers

## 📞 Support

- Create an [Issue](https://github.com/username/instagram-analytics/issues) for bug reports
- Start a [Discussion](https://github.com/username/instagram-analytics/discussions) for questions
- Check existing issues before creating new ones

## 🚀 Future Enhancements

- [ ] Competitor analysis features
- [ ] Advanced scheduling recommendations
- [ ] Story analytics integration
- [ ] Automated report generation
- [ ] Multiple account management
- [ ] Historical data tracking
- [ ] Machine learning insights
- [ ] Mobile app version

---

**Made with ❤️ for Instagram content creators and social media managers**
