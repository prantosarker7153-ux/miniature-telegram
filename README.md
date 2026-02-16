# 🎬 CINEFLIX ULTIMATE BOT

## 📖 বিবরণ | Description

**বাংলা:**
CINEFLIX একটি শক্তিশালী Telegram Video Bot যা আপনার movies, series এবং exclusive content share করার জন্য তৈরি। এতে রয়েছে:

- ✅ Mini App Integration
- ✅ Force Join Channels (Public & Private)
- ✅ Admin Panel with Full Control
- ✅ Auto Video Detection from Channel
- ✅ Broadcast System
- ✅ Video View Counter
- ✅ User Analytics
- ✅ Custom Messages & Buttons

**English:**
CINEFLIX is a powerful Telegram Video Bot designed to share your movies, series, and exclusive content. Features include:

- ✅ Mini App Integration
- ✅ Force Join Channels (Public & Private)
- ✅ Admin Panel with Full Control
- ✅ Auto Video Detection from Channel
- ✅ Broadcast System
- ✅ Video View Counter
- ✅ User Analytics
- ✅ Custom Messages & Buttons

---

## 🚀 সেটআপ | Setup

### 1️⃣ প্রয়োজনীয় জিনিস | Requirements

- Python 3.8 বা তার উপরে (or higher)
- MongoDB Database (Free: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas))
- Telegram Bot Token ([BotFather](https://t.me/BotFather) থেকে)

### 2️⃣ ইনস্টলেশন | Installation

**বাংলা:**

```bash
# 1. Repository Clone করুন
cd cineflix-bot

# 2. Python Packages Install করুন
pip install -r requirements.txt

# 3. Environment Variables Setup করুন
# .env.example কপি করে .env তে নাম পরিবর্তন করুন
cp .env.example .env

# 4. .env ফাইল Edit করুন এবং আপনার তথ্য দিন:
# - BOT_TOKEN: আপনার bot token
# - MONGO_URI: MongoDB connection string
# - ADMIN_ID: আপনার Telegram User ID
```

**English:**

```bash
# 1. Clone the repository
cd cineflix-bot

# 2. Install Python packages
pip install -r requirements.txt

# 3. Setup environment variables
# Copy .env.example to .env
cp .env.example .env

# 4. Edit .env file with your credentials:
# - BOT_TOKEN: Your bot token
# - MONGO_URI: MongoDB connection string
# - ADMIN_ID: Your Telegram User ID
```

### 3️⃣ MongoDB Setup

**বাংলা:**

1. [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) এ যান
2. Free Cluster তৈরি করুন
3. Database User তৈরি করুন
4. Network Access এ `0.0.0.0/0` যোগ করুন
5. Connection String কপি করে `.env` ফাইলে পেস্ট করুন

**English:**

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a Free Cluster
3. Create Database User
4. Add `0.0.0.0/0` to Network Access
5. Copy Connection String and paste in `.env` file

### 4️⃣ Bot Token পাবেন কিভাবে? | How to Get Bot Token?

**বাংলা:**

1. Telegram এ [@BotFather](https://t.me/BotFather) এ যান
2. `/newbot` পাঠান
3. Bot এর নাম এবং username দিন
4. Token কপি করে `.env` ফাইলে পেস্ট করুন

**English:**

1. Go to [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Provide bot name and username
4. Copy token and paste in `.env` file

### 5️⃣ Admin ID পাবেন কিভাবে? | How to Get Admin ID?

**বাংলা:**

1. [@userinfobot](https://t.me/userinfobot) এ যান
2. Bot কে `/start` পাঠান
3. আপনার User ID কপি করুন
4. `.env` ফাইলে `ADMIN_ID` তে পেস্ট করুন

**English:**

1. Go to [@userinfobot](https://t.me/userinfobot)
2. Send `/start` to the bot
3. Copy your User ID
4. Paste in `ADMIN_ID` in `.env` file

---

## ▶️ Bot চালু করুন | Start the Bot

```bash
# Bot চালু করুন | Start bot
python bot.py
```

**সফল হলে দেখবেন (You should see):**
```
🚀 Starting CINEFLIX Ultimate Bot...
✅ MongoDB Connected Successfully!
✅ CINEFLIX Ultimate Bot is running!
👑 Admin: [YOUR_ID]
💾 MongoDB: Connected
🎬 Ready to serve!
```

---

## 🎯 Bot Features কিভাবে ব্যবহার করবেন? | How to Use Bot Features?

### 1️⃣ Admin Panel Access

**বাংলা:**
- Bot এ `/admin` পাঠান
- Admin Panel খুলবে যেখানে সব features দেখতে পাবেন

**English:**
- Send `/admin` to the bot
- Admin Panel will open with all features

### 2️⃣ Force Join Channels Add করুন | Add Force Join Channels

**বাংলা:**

1. Admin Panel → "📺 Force Join Channels"
2. "➕ Add Channel" ক্লিক করুন
3. Channel info পাঠান এই format এ:
   ```
   -1001234567890 | My Channel | https://t.me/mychannel
   ```
   অথবা শুধু Channel ID পাঠান:
   ```
   -1001234567890
   ```

**English:**

1. Admin Panel → "📺 Force Join Channels"
2. Click "➕ Add Channel"
3. Send channel info in this format:
   ```
   -1001234567890 | My Channel | https://t.me/mychannel
   ```
   Or just send Channel ID:
   ```
   -1001234567890
   ```

**📝 Note:** Channel ID পেতে [@username_to_id_bot](https://t.me/username_to_id_bot) ব্যবহার করুন | Use [@username_to_id_bot](https://t.me/username_to_id_bot) to get Channel ID

### 3️⃣ Video Add করুন | Add Videos

**বাংলা:**

**Method 1: Auto (সেরা | Best):**
1. Bot কে আপনার Video Channel এ Admin বানান
2. Admin Panel → Settings → "Main Channel ID" সেট করুন
3. Channel এ video post করুন - automatically add হবে!

**Method 2: Manual:**
1. MongoDB তে `videos` collection খুলুন
2. নতুন document যোগ করুন:
   ```json
   {
     "video_id": "v123",
     "file_id": "BAACAgIAAxkBAAI...",
     "caption": "Movie Name (2024)",
     "views": 0
   }
   ```

**English:**

**Method 1: Auto (Best):**
1. Make bot admin in your Video Channel
2. Admin Panel → Settings → Set "Main Channel ID"
3. Post video in channel - auto-adds!

**Method 2: Manual:**
1. Open `videos` collection in MongoDB
2. Add new document:
   ```json
   {
     "video_id": "v123",
     "file_id": "BAACAgIAAxkBAAI...",
     "caption": "Movie Name (2024)",
     "views": 0
   }
   ```

### 4️⃣ Custom Messages Edit করুন | Edit Custom Messages

**বাংলা:**
1. Admin Panel → "✏️ Edit Messages"
2. যেকোনো message select করুন
3. নতুন message text পাঠান
4. ✅ Updated!

**English:**
1. Admin Panel → "✏️ Edit Messages"
2. Select any message
3. Send new message text
4. ✅ Updated!

### 5️⃣ Custom Buttons Add করুন | Add Custom Buttons

**বাংলা:**
1. Admin Panel → "🔘 Manage Buttons"
2. Location select করুন (Welcome/After Video)
3. "➕ Add Button" ক্লিক করুন
4. Button info পাঠান:
   ```
   📢 Join Channel | https://t.me/mychannel | url
   ```
   অথবা Mini App button এর জন্য:
   ```
   🎮 Open App | https://your-app.com | webapp
   ```

**English:**
1. Admin Panel → "🔘 Manage Buttons"
2. Select location (Welcome/After Video)
3. Click "➕ Add Button"
4. Send button info:
   ```
   📢 Join Channel | https://t.me/mychannel | url
   ```
   Or for Mini App button:
   ```
   🎮 Open App | https://your-app.com | webapp
   ```

### 6️⃣ Broadcast Message পাঠান | Send Broadcast Message

**বাংলা:**
1. Admin Panel → "📢 Broadcast Message"
2. আপনার message পাঠান (text/photo/video)
3. সব users কে automatically পাঠানো হবে!

**English:**
1. Admin Panel → "📢 Broadcast Message"
2. Send your message (text/photo/video)
3. Automatically sent to all users!

### 7️⃣ Statistics দেখুন | View Statistics

**বাংলা:**
- Admin Panel → "📊 Statistics"
- দেখুন:
  - Total Users
  - Active Today
  - Total Videos
  - Top Views
  - Force Join Channels

**English:**
- Admin Panel → "📊 Statistics"
- View:
  - Total Users
  - Active Today
  - Total Videos
  - Top Views
  - Force Join Channels

---

## 🔧 Settings Configuration

### Mini App URL Setup

**বাংলা:**
1. Admin Panel → Settings → "Mini App URL"
2. আপনার Mini App URL দিন
3. এটি Welcome message এর button এ ব্যবহার হবে

**English:**
1. Admin Panel → Settings → "Mini App URL"
2. Enter your Mini App URL
3. This will be used in Welcome message button

### Video Protection

**বাংলা:**
- `True`: Users video forward/save করতে পারবে না
- `False`: Users video forward/save করতে পারবে

**English:**
- `True`: Users can't forward/save videos
- `False`: Users can forward/save videos

---

## 🆘 Common Issues & Solutions

### ❌ Bot Starting না হলে | Bot Not Starting

**Problem:** `BOT_TOKEN environment variable not set!`

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Edit .env file
nano .env

# Add your tokens
BOT_TOKEN=your_token_here
MONGO_URI=your_mongodb_uri
ADMIN_ID=your_user_id
```

### ❌ MongoDB Connection Error

**Problem:** `MongoDB Connection Failed`

**Solution:**
1. Check MongoDB URI is correct
2. Check internet connection
3. Verify MongoDB user credentials
4. Check Network Access settings in MongoDB Atlas

### ❌ Force Join Not Working

**Problem:** Users join করলেও video পায় না

**Solution:**
1. Bot কে Channel এ Admin বানান
2. Bot এর সব permissions দিন
3. Channel ID সঠিক দিয়েছেন কিনা check করুন (-)

### ❌ Video Not Adding Automatically

**Problem:** Channel এ post করলেও add হচ্ছে না

**Solution:**
1. Bot কে Channel এ Admin বানান
2. Settings এ Main Channel ID set করুন
3. Channel ID সঠিক আছে কিনা verify করুন

---

## 📱 Deploy to Server

### Heroku (Free)

**বাংলা:**

```bash
# 1. Heroku CLI Install করুন
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Login করুন
heroku login

# 3. App তৈরি করুন
heroku create your-app-name

# 4. Environment Variables সেট করুন
heroku config:set BOT_TOKEN=your_token
heroku config:set MONGO_URI=your_mongo_uri
heroku config:set ADMIN_ID=your_id

# 5. Deploy করুন
git init
git add .
git commit -m "Deploy CINEFLIX Bot"
git push heroku master
```

### VPS (Ubuntu/Debian)

**বাংলা:**

```bash
# 1. Server এ login করুন
ssh user@your-server-ip

# 2. Python install করুন
sudo apt update
sudo apt install python3 python3-pip

# 3. Files upload করুন
# Use FileZilla or SCP

# 4. Dependencies install করুন
pip3 install -r requirements.txt

# 5. Bot চালু করুন (background)
nohup python3 bot.py &

# 6. Process check করুন
ps aux | grep bot.py
```

### Screen ব্যবহার করুন (Recommended)

```bash
# Screen install
sudo apt install screen

# New screen session তৈরি করুন
screen -S cineflix

# Bot চালু করুন
python3 bot.py

# Detach করুন: Ctrl+A তারপর D

# Re-attach করুন
screen -r cineflix
```

---

## 🛡️ Security Best Practices

**বাংলা:**
1. ✅ `.env` file কখনো GitHub এ upload করবেন না
2. ✅ Strong passwords ব্যবহার করুন
3. ✅ ADMIN_ID সঠিক দিন, নইলে অন্যরা access পাবে
4. ✅ MongoDB Network Access সীমিত রাখুন
5. ✅ Regular backups নিন

**English:**
1. ✅ Never upload `.env` file to GitHub
2. ✅ Use strong passwords
3. ✅ Set correct ADMIN_ID, others can get access
4. ✅ Limit MongoDB Network Access
5. ✅ Take regular backups

---

## 📞 Support & Contact

**বাংলা:**
- সমস্যা হলে Issue open করুন
- প্রশ্ন করতে Telegram এ যোগাযোগ করুন

**English:**
- Open an Issue for problems
- Contact on Telegram for questions

---

## 📄 License

MIT License - Free to use and modify

---

## 🙏 Credits

**Developed by:** CINEFLIX Team
**Version:** 2.0
**Last Updated:** 2024

**বাংলা:**
আপনার bot সফলভাবে চলুক! ❤️

**English:**
May your bot run successfully! ❤️

---

## 🚀 Quick Start Checklist

**বাংলা:**
- [ ] Python 3.8+ installed
- [ ] MongoDB Atlas account তৈরি
- [ ] Bot Token নিয়েছি (@BotFather থেকে)
- [ ] Admin ID জানি (@userinfobot থেকে)
- [ ] `.env` file তৈরি করে সব info দিয়েছি
- [ ] `pip install -r requirements.txt` চালিয়েছি
- [ ] `python bot.py` চালিয়েছি
- [ ] Bot চলছে! 🎉

**English:**
- [ ] Python 3.8+ installed
- [ ] MongoDB Atlas account created
- [ ] Got Bot Token (from @BotFather)
- [ ] Got Admin ID (from @userinfobot)
- [ ] Created `.env` file with all info
- [ ] Ran `pip install -r requirements.txt`
- [ ] Ran `python bot.py`
- [ ] Bot is running! 🎉

---

**🎬 Happy Streaming! 🎬**
