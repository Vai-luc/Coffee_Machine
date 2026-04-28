# ⚡ Quick Start Deployment Checklist

## Before You Deploy

- [ ] Read `FIXES_APPLIED.md` to understand what was fixed
- [ ] Read `README_DEPLOYMENT.md` for full documentation
- [ ] Test locally: `python app.py` (should work without DATABASE_URL)
- [ ] Verify all files are synced from GitHub

## Local Testing (5 minutes)

```bash
# 1. Activate environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run app
python app.py

# 4. Open http://localhost:5000
# 5. Test ordering system
# 6. Check data/coffee_machine.json exists
```

Checklist:
- [ ] App starts without errors
- [ ] Homepage loads
- [ ] Menu shows 3 drinks
- [ ] Can select drink and place order
- [ ] Resources display
- [ ] Order history appears
- [ ] Reset button works

## Render Deployment (2 minutes)

### Method 1: Blueprint (Recommended)
```bash
# 1. Commit all changes
git add .
git commit -m "Production-ready: All bugs fixed"
git push origin main

# 2. Go to https://render.com/dashboard
# 3. Click "+ New" → "Blueprint"
# 4. Select your GitHub repo
# 5. Name: coffee-machine
# 6. Click "Create"
# 7. Wait for deployment (3-5 minutes)
```

Checklist:
- [ ] GitHub repo has all latest changes
- [ ] `render.yaml` file exists in repo
- [ ] Render dashboard shows deployment in progress
- [ ] Deployment completes successfully

### Method 2: Manual Web Service

```bash
# In Render Dashboard:
1. New → Web Service
2. Connect GitHub repo
3. Name: coffee-machine
4. Runtime: Python 3
5. Build Command: pip install -r requirements.txt
6. Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 4 app:app
7. Click "Create Web Service"
8. Wait for deployment
```

Checklist:
- [ ] Web Service created
- [ ] Build succeeds
- [ ] Service URL provided
- [ ] Can access service URL

## Verify Deployment

After Render shows "Live":

```bash
# Test the API
curl https://your-app.onrender.com/menu
# Should return menu data

curl https://your-app.onrender.com/session  
# Should return session stats

# Open in browser
https://your-app.onrender.com
# Should show full app with all functions
```

Checklist:
- [ ] API `/menu` returns data
- [ ] API `/session` returns data  
- [ ] Homepage loads
- [ ] Menu displays properly
- [ ] Can place orders
- [ ] Resources show
- [ ] Order history displays

## Troubleshooting

**Issue**: Build fails on Render
- [ ] Check `requirements.txt` has all packages
- [ ] Verify `Dockerfile` uses correct Python version
- [ ] Check Render build logs for errors
- [ ] Try deleting and redeploying

**Issue**: App shows "Internal Server Error"
- [ ] Check Render logs (bottom of dashboard)
- [ ] Verify database is optional (uses JSON fallback)
- [ ] Restart service in Render dashboard
- [ ] Check all environment variables set

**Issue**: Database connection error
- [ ] This is OK - app uses JSON fallback
- [ ] Data will be in `data/coffee_machine.json`
- [ ] If you want PostgreSQL, add database to Render

**Issue**: Ordering doesn't work
- [ ] Check browser console (F12) for errors
- [ ] Verify API returns resources data
- [ ] Check server logs in Render dashboard
- [ ] Try clearing browser cache

## Final Checklist

Before considering deployment complete:

- [ ] App runs locally without DATABASE_URL
- [ ] All files pushed to GitHub
- [ ] Render deployment completed
- [ ] Live URL accessible
- [ ] Homepage loads
- [ ] All menu items visible
- [ ] Can place orders
- [ ] Resources update
- [ ] Order history works
- [ ] Reset button works

## Support Resources

- `README_DEPLOYMENT.md` - Full documentation
- `FIXES_APPLIED.md` - Detailed fix explanations
- `.env.example` - Environment variables guide
- `render.yaml` - Render configuration

---

**You're ready! 🚀**

Good luck with your deployment! All bugs are fixed and the code is production-ready.
