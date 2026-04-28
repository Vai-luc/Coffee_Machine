# Daily Brew ☕ - Coffee Machine Ordering System

A beautiful, full-stack coffee ordering application with real-time order tracking, resource management, and live price calculations.

## Features

✨ **Interactive Menu** - Browse 3 specialty coffee drinks with descriptions  
📏 **Size Options** - Choose from Tall, Grande, or Venti sizes  
💰 **Live Pricing** - Real-time price calculations with size multipliers  
🛒 **Order Management** - Place orders with quantity and payment  
📊 **Resource Tracking** - Monitor water, milk, and coffee supplies  
📜 **Order History** - View recent orders and session stats  
🎨 **Beautiful UI** - Responsive design with smooth animations  

## Tech Stack

- **Backend**: Flask (Python 3.11)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: PostgreSQL (production) / JSON file (fallback)
- **Deployment**: Docker, Render

## Local Development

### Prerequisites

- Python 3.11+
- PostgreSQL (optional - uses JSON file fallback)

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Coffee_Machine-main
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

   The application will start at `http://localhost:5000`

## Production Deployment on Render

### Using render.yaml (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **Connect to Render**
   - Go to https://render.com
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and deploy

3. **Environment Setup**
   - Render will create the PostgreSQL database automatically
   - Set `DATABASE_URL` environment variable in Render dashboard (it's set automatically via `render.yaml`)

### Manual Deployment

1. **Create a new Web Service on Render**
   - Repository: Connect your GitHub repo
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 4 app:app`
   - Runtime: Python 3

2. **Create PostgreSQL Database**
   - Add PostgreSQL database service in Render
   - Copy the connection string to `DATABASE_URL` env var

3. **Deploy**
   - Click "Deploy"
   - Monitor logs in Render dashboard

## API Endpoints

### GET `/`
- Returns the main HTML page

### GET `/menu`
- Returns available drinks and sizes
- **Response**: `{ menu: [...], sizes: [...] }`

### POST `/order`
- Place a new coffee order
- **Body**: `{ drink, size, quantity, amount }`
- **Response**: `{ status, drink, size, quantity, total, change, resources, recent_orders }`

### GET `/session`
- Get session statistics
- **Response**: `{ status, orders, total_spent, resources, recent_orders }`

### POST `/reset`
- Reset machine state and clear all orders
- **Response**: `{ status, message }`

## File Structure

```
Coffee_Machine-main/
├── app.py                 # Flask application entry point
├── main.py               # CLI interface
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── render.yaml           # Render deployment configuration
├── controllers/
│   └── order_controller.py
├── services/
│   ├── coffee_maker.py
│   ├── money_machine.py
│   ├── menu.py
│   └── persistence.py    # Database abstraction layer
├── static/
│   ├── css/styles.css
│   └── js/
│       ├── app.js
│       └── animation.js
├── templates/
│   └── index.html
├── data/                 # Local data storage (JSON fallback)
└── tests/               # Unit tests
```

## Troubleshooting

### Issue: "No functions showing on website"
**Solution**: 
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console for errors (F12)
- Verify backend is running and returning data
- Check `/menu` endpoint: `curl http://localhost:5000/menu`

### Issue: "DATABASE_URL not set"
**Solution**:
- The app uses JSON file fallback automatically
- For production Render deployment, database URL is set via `render.yaml`
- Manually set `DATABASE_URL` in Render environment variables if needed

### Issue: "Orders not saving"
**Solution**:
- Check that PostgreSQL is running (if using DB)
- Verify `data/` directory exists (for JSON fallback)
- Check application logs for SQL errors

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions

## License

MIT License - Feel free to use this project for learning and development.

## Support

Having issues? 
1. Check the troubleshooting section above
2. Review application logs
3. Verify all environment variables are set correctly
4. Check that the database connection is working
