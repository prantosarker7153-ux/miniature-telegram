# 🚂 Railway Deployment Guide

## ⚠️ Python Version Issue Fix

Railway তে deploy করার সময় যদি এই error দেখেন:
```
ERROR Failed to install core:python@3.11.0: no precompiled python found
```

### Solution 1: Python Version Update করুন

`runtime.txt` file এ version change করুন:

```txt
python-3.11.9
```

অথবা এগুলো try করুন:
- `python-3.11.9` ✅ (Recommended)
- `python-3.10.13` ✅
- `python-3.12.1` ✅

### Solution 2: Railway.json ব্যবহার করুন

আপনার project এ `railway.json` file add করুন:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "startCommand": "python bot.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Solution 3: Nixpacks Configuration

`nixpacks.toml` file তৈরি করুন:

```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "python bot.py"
```

---

## 🎯 Railway Deployment Steps

### Step 1: Railway Account তৈরি করুন

1. [Railway.app](https://railway.app) এ যান
2. GitHub দিয়ে sign up করুন
3. Free plan select করুন

### Step 2: New Project তৈরি করুন

1. Dashboard → "New Project"
2. "Deploy from GitHub repo" select করুন
3. আপনার repository select করুন

অথবা:

1. "Empty Project" তৈরি করুন
2. "Create" → "GitHub Repo" → Connect করুন

### Step 3: Environment Variables যোগ করুন

Railway Dashboard → Variables → Add Variables:

```env
BOT_TOKEN=your_bot_token_here
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
ADMIN_ID=your_telegram_user_id
```

**Important:** প্রতিটি variable আলাদা করে add করুন।

### Step 4: Deploy করুন

1. "Deploy" button ক্লিক করুন
2. Build logs দেখুন
3. Success হলে bot চালু হবে!

### Step 5: Logs Check করুন

Railway Dashboard → Deployments → View Logs

দেখবেন:
```
🚀 Starting CINEFLIX Ultimate Bot...
✅ MongoDB Connected Successfully!
✅ CINEFLIX Ultimate Bot is running!
```

---

## 🐛 Common Railway Errors & Solutions

### Error 1: Python Version Not Found

**Error:**
```
no precompiled python found for core:python@3.11.0
```

**Solution:**
```bash
# runtime.txt file change করুন
echo "python-3.11.9" > runtime.txt

# Commit and push
git add runtime.txt
git commit -m "Fix: Update Python version for Railway"
git push
```

### Error 2: Requirements Install Failed

**Error:**
```
ERROR: Could not find a version that satisfies the requirement
```

**Solution:**
```bash
# requirements.txt verify করুন
cat requirements.txt

# Should contain:
python-telegram-bot==21.9
pymongo==4.10.1
python-dotenv==1.0.1
```

### Error 3: MongoDB Connection Failed

**Error:**
```
MongoDB Connection Failed: ServerSelectionTimeoutError
```

**Solution:**
1. MongoDB Atlas → Network Access
2. "Add IP Address" → "Allow from Anywhere" (0.0.0.0/0)
3. Redeploy on Railway

### Error 4: Bot Token Invalid

**Error:**
```
telegram.error.InvalidToken
```

**Solution:**
1. Railway Variables check করুন
2. `BOT_TOKEN` সঠিক আছে কিনা verify করুন
3. Spaces বা extra characters নেই তো?
4. Redeploy করুন

### Error 5: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'telegram'
```

**Solution:**
```bash
# requirements.txt check করুন
# Correct format:
python-telegram-bot==21.9

# NOT:
telegram==...  # ❌ Wrong
```

---

## 📊 Railway vs Other Platforms

| Feature | Railway | Heroku | VPS |
|---------|---------|--------|-----|
| Free Plan | ✅ $5 credit | ❌ Paid only | ❌ Paid |
| Easy Deploy | ✅ Very Easy | ✅ Easy | ⚠️ Medium |
| Auto Deploy | ✅ Yes | ✅ Yes | ❌ Manual |
| Logs | ✅ Real-time | ✅ Yes | ⚠️ Manual |
| Uptime | ✅ 24/7 | ⚠️ Limited | ✅ 24/7 |
| Support | ✅ Discord | ⚠️ Paid | ⚠️ Self |

**Verdict:** Railway recommended for beginners! ✅

---

## 🔄 Auto Deploy Setup

### Method 1: GitHub Integration (Recommended)

1. Railway → Project → Settings
2. "GitHub" → "Connect Repository"
3. Select branch (usually `main` or `master`)
4. ✅ Auto-deploy enabled!

**এখন যখনই GitHub এ push করবেন, automatically deploy হবে!**

### Method 2: Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Or with curl
curl -fsSL cli.new/railway | sh

# Login
railway login

# Link project
railway link

# Deploy manually
railway up
```

---

## 📈 Monitoring Your Bot

### Railway Dashboard

1. **Metrics:** CPU, Memory, Network usage দেখুন
2. **Logs:** Real-time logs দেখুন
3. **Deployments:** Deployment history দেখুন

### Bot Commands

```bash
# Bot status check
/admin → Statistics

# View logs
Railway Dashboard → Deployments → Logs
```

---

## 💰 Railway Pricing

### Free Plan
- ✅ $5 credit per month
- ✅ ~20 days runtime (24/7)
- ✅ 512MB RAM
- ✅ Perfect for small bots

### Hobby Plan ($5/month)
- ✅ $5 base + usage
- ✅ More credits
- ✅ Better support

### Pro Plan ($20/month)
- ✅ $20 base + usage
- ✅ Priority support
- ✅ Higher limits

**আমাদের bot Free plan এ চলবে!** 🎉

---

## 🔧 Advanced Configuration

### Custom Domain

1. Railway → Project → Settings
2. "Domains" → "Add Custom Domain"
3. Enter your domain
4. Add CNAME record to your DNS

### Scaling

Railway automatically scales, কিন্তু manually control করতে:

1. Settings → "Resources"
2. Adjust Memory/CPU
3. Save changes

### Environment Groups

Multiple environments এর জন্য:

1. Dashboard → "Environment Groups"
2. Add "Development", "Production"
3. Different variables for each

---

## 🆘 Railway Support

### Discord Community
- [Railway Discord](https://discord.gg/railway)
- Very responsive support
- Community help available

### Documentation
- [Railway Docs](https://docs.railway.app)
- Detailed guides
- Examples

### Status Page
- [Railway Status](https://status.railway.app)
- Check for outages

---

## ✅ Final Checklist

Deploy করার আগে:

- [ ] `runtime.txt` এ `python-3.11.9` আছে
- [ ] `requirements.txt` সঠিক আছে
- [ ] `.env.example` copy করে `.env` বানিয়েছি
- [ ] GitHub repository তৈরি করেছি
- [ ] Railway account তৈরি করেছি
- [ ] MongoDB Atlas setup করেছি
- [ ] Bot Token নিয়েছি
- [ ] Admin ID জানি
- [ ] Railway এ Environment Variables add করেছি
- [ ] Deploy button ক্লিক করেছি
- [ ] Logs দেখে verify করেছি

---

## 🎉 Success!

আপনার bot এখন Railway তে successfully deploy হয়েছে!

### Next Steps:

1. ✅ Bot test করুন: `/start` পাঠান
2. ✅ Admin panel check করুন: `/admin`
3. ✅ Force join channels add করুন
4. ✅ Videos add করুন
5. ✅ Users কে share করুন!

---

**Railway তে সমস্যা হলে:**
1. Logs check করুন
2. Environment variables verify করুন
3. Discord community তে help চান
4. আমাদের INSTALLATION_GUIDE.md পড়ুন

**Happy Deploying! 🚀**
