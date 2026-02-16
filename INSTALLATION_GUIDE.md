# 🎬 CINEFLIX BOT - সম্পূর্ণ ইনস্টলেশন গাইড

## 📋 বিষয়সূচী

1. [প্রয়োজনীয় জিনিস](#প্রয়োজনীয়-জিনিস)
2. [MongoDB Setup](#mongodb-setup)
3. [Bot Token Setup](#bot-token-setup)
4. [Bot Installation](#bot-installation)
5. [Bot Configuration](#bot-configuration)
6. [Bot চালু করা](#bot-চালু-করা)
7. [Force Join Setup](#force-join-setup)
8. [Video Add করা](#video-add-করা)
9. [Server Deploy](#server-deploy)
10. [Troubleshooting](#troubleshooting)

---

## 🛠️ প্রয়োজনীয় জিনিস

### 1. Python 3.8 বা তার উপরে

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version  # Check version
```

**Windows:**
- [Python.org](https://www.python.org/downloads/) থেকে download করুন
- Installation এর সময় "Add Python to PATH" check করুন

**MacOS:**
```bash
brew install python3
```

### 2. Git (Optional)

```bash
# Ubuntu/Debian
sudo apt install git

# Windows: Download from git-scm.com
# MacOS
brew install git
```

### 3. Text Editor

- **Notepad++** (Windows)
- **nano/vim** (Linux)
- **VS Code** (All platforms) - Recommended

---

## 🗄️ MongoDB Setup

MongoDB হলো database যেখানে সব data সংরক্ষিত থাকবে।

### Step 1: MongoDB Atlas Account তৈরি করুন

1. [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) এ যান
2. "Try Free" বাটনে ক্লিক করুন
3. Google/Email দিয়ে Sign up করুন
4. Login করুন

### Step 2: Cluster তৈরি করুন

1. "Create a Cluster" ক্লিক করুন
2. **FREE** plan select করুন (M0 Sandbox)
3. Cloud Provider: **AWS** select করুন
4. Region: **Singapore** বা কাছের region select করুন
5. Cluster Name: `CINEFLIX` (অথবা যেকোনো নাম)
6. "Create Cluster" ক্লিক করুন
7. 2-3 মিনিট wait করুন

### Step 3: Database User তৈরি করুন

1. Left sidebar এ "Database Access" ক্লিক করুন
2. "Add New Database User" ক্লিক করুন
3. **Username:** `cineflix_admin` (অথবা যেকোনো)
4. **Password:** Strong password দিন এবং কোথাও save করুন
5. **Database User Privileges:** "Read and write to any database"
6. "Add User" ক্লিক করুন

### Step 4: Network Access Setup

1. Left sidebar এ "Network Access" ক্লিক করুন
2. "Add IP Address" ক্লিক করুন
3. "Allow Access from Anywhere" select করুন
4. IP Address: `0.0.0.0/0` automatically add হবে
5. "Confirm" ক্লিক করুন

### Step 5: Connection String নিন

1. Left sidebar এ "Database" ক্লিক করুন
2. Cluster এর "Connect" বাটনে ক্লিক করুন
3. "Connect your application" select করুন
4. **Driver:** Python, **Version:** 3.12 or later
5. Connection string কপি করুন:
   ```
   mongodb+srv://cineflix_admin:<password>@cluster0.xxxxx.mongodb.net/
   ```
6. `<password>` এর জায়গায় আপনার actual password দিন
7. এটি `.env` file এ ব্যবহার করবেন

**উদাহরণ:**
```
mongodb+srv://cineflix_admin:MyPassword123@cluster0.xxxxx.mongodb.net/
```

---

## 🤖 Bot Token Setup

### Step 1: BotFather এ যান

1. Telegram এ [@BotFather](https://t.me/BotFather) খুলুন
2. `/start` পাঠান

### Step 2: New Bot তৈরি করুন

1. `/newbot` পাঠান
2. **Bot Name দিন:** `CINEFLIX Bot` (Display name)
3. **Bot Username দিন:** `your_cineflix_bot` (Must end with 'bot')
   - উদাহরণ: `mycineflix_bot`, `cineflix_video_bot`
   - এটি unique হতে হবে

### Step 3: Bot Token কপি করুন

BotFather একটি message পাঠাবে:
```
Done! Congratulations on your new bot...
Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
```

এই **token টি কপি করে** safe জায়গায় save করুন।

### Step 4: Bot Settings (Optional)

```
/setdescription - Bot এর description
/setabouttext - About text
/setuserpic - Profile picture
/setcommands - Commands list
```

**Commands list example:**
```
start - Start the bot
help - Show help
admin - Admin panel (admin only)
```

---

## 💾 Bot Installation

### Method 1: Direct Download

1. এই folder টি আপনার computer এ extract করুন
2. Terminal/Command Prompt খুলুন
3. Bot folder এ যান:
   ```bash
   cd path/to/cineflix-bot
   ```

### Method 2: Git Clone (If available)

```bash
# Clone repository
git clone <repository-url>
cd cineflix-bot
```

---

## ⚙️ Bot Configuration

### Step 1: .env File তৈরি করুন

```bash
# Linux/Mac
cp .env.example .env

# Windows (Command Prompt)
copy .env.example .env
```

### Step 2: .env File Edit করুন

**Linux/Mac:**
```bash
nano .env
```

**Windows:**
- Notepad++ দিয়ে `.env` file খুলুন

### Step 3: আপনার Credentials দিন

```env
# Telegram Bot Configuration
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789

# MongoDB Configuration
MONGO_URI=mongodb+srv://cineflix_admin:MyPassword123@cluster0.xxxxx.mongodb.net/

# Admin Configuration
ADMIN_ID=1234567890
```

**BOT_TOKEN:** BotFather থেকে পাওয়া token

**MONGO_URI:** MongoDB Atlas থেকে পাওয়া connection string

**ADMIN_ID:** আপনার Telegram User ID

### Admin ID কিভাবে পাবেন?

1. [@userinfobot](https://t.me/userinfobot) এ যান
2. `/start` পাঠান
3. আপনার User ID কপি করুন (Example: `1234567890`)

---

## 🚀 Bot চালু করা

### Dependencies Install করুন

```bash
pip3 install -r requirements.txt
```

অথবা Windows এ:
```bash
pip install -r requirements.txt
```

### Bot Start করুন

**Method 1: Direct Command**
```bash
python3 bot.py
```

অথবা Windows এ:
```bash
python bot.py
```

**Method 2: Using START.sh (Linux/Mac)**
```bash
./START.sh
```

**Method 3: Using Screen (For server - Recommended)**
```bash
# Screen install করুন (if not installed)
sudo apt install screen

# New screen session তৈরি করুন
screen -S cineflix

# Bot চালু করুন
python3 bot.py

# Detach করুন: Ctrl+A then D
# Re-attach করুন: screen -r cineflix
```

### ✅ সফল হলে দেখবেন

```
🚀 Starting CINEFLIX Ultimate Bot...
🔄 Connecting to MongoDB...
✅ MongoDB Connected Successfully!
✅ CINEFLIX Ultimate Bot is running!
👑 Admin: 1234567890
💾 MongoDB: Connected
🎬 Ready to serve!
```

---

## 🔒 Force Join Setup

### Step 1: Channel তৈরি করুন

1. Telegram এ নতুন Channel তৈরি করুন
2. Channel type:
   - **Public:** Anyone can join
   - **Private:** Request required

### Step 2: Bot কে Admin বানান

1. আপনার Channel এ যান
2. Channel Info → Administrators
3. "Add Administrator" ক্লিক করুন
4. আপনার bot search করুন এবং add করুন
5. **সব permissions দিন**

### Step 3: Channel ID নিন

**Method 1: Forward Message (Easy)**
1. Channel এ যেকোনো post forward করুন [@userinfobot](https://t.me/userinfobot) এ
2. Channel ID দেখাবে (Example: `-1001234567890`)

**Method 2: Using Bot**
1. Channel username থেকে ID নিতে [@username_to_id_bot](https://t.me/username_to_id_bot) ব্যবহার করুন

**Method 3: Manual**
1. Channel এ যেকোনো message এর link copy করুন
2. Link format: `https://t.me/c/1234567890/1`
3. Number টি নিয়ে `-100` add করুন: `-1001234567890`

### Step 4: Bot এ Force Join Channel Add করুন

1. Bot এ যান
2. `/admin` পাঠান
3. "📺 Force Join Channels" ক্লিক করুন
4. "➕ Add Channel" ক্লিক করুন
5. Channel info পাঠান:
   ```
   -1001234567890 | My Channel | https://t.me/mychannel
   ```
   অথবা শুধু:
   ```
   -1001234567890
   ```

### ✅ Test করুন

1. নতুন account দিয়ে bot `/start` করুন
2. Video request করুন
3. Force join message দেখাবে
4. Channel join করুন
5. "✅ আমি জয়েন করেছি" ক্লিক করুন
6. Video পাবেন!

---

## 📹 Video Add করা

### Method 1: Auto Add (Best)

এটি সবচেয়ে সহজ এবং recommended method।

**Step 1: Video Channel Setup**

1. একটি separate Channel তৈরি করুন শুধু videos এর জন্য
2. Bot কে এই Channel এ Admin বানান (সব permissions দিয়ে)

**Step 2: Bot Settings**

1. Bot এ `/admin` পাঠান
2. Settings ক্লিক করুন
3. "Main Channel ID" select করুন
4. আপনার Video Channel এর ID পাঠান (Example: `-1001234567890`)

**Step 3: Video Post করুন**

1. Video Channel এ video post করুন
2. Caption দিন (Optional)
3. Bot automatically video detect করবে এবং database এ add করবে!

**Step 4: Video Link তৈরি করুন**

Video post করার পর bot log এ দেখবেন:
```
✅ Auto-added video: v123
```

এখন Mini App এ এই link ব্যবহার করুন:
```
https://t.me/your_bot?start=v_123
```

Format: `https://t.me/BOT_USERNAME?start=v_MESSAGE_ID`

### Method 2: Manual Add

MongoDB database এ manually video add করতে:

**Step 1: MongoDB এ Login**

1. [MongoDB Atlas](https://cloud.mongodb.com) এ যান
2. Cluster → "Browse Collections" ক্লিক করুন
3. Database: `cineflix_bot`
4. Collection: `videos`

**Step 2: Video File ID নিন**

1. আপনার bot এ video send করুন
2. Bot log check করুন অথবা MongoDB database `channels` collection দেখুন
3. `file_id` কপি করুন

**Step 3: Document Insert করুন**

"Insert Document" ক্লিক করুন এবং এই format এ data দিন:

```json
{
  "video_id": "v101",
  "file_id": "BAACAgIAAxkBAAIBY2Z...",
  "caption": "Movie Name (2024) - HD Quality",
  "views": 0,
  "added_at": {"$date": "2024-01-01T00:00:00.000Z"}
}
```

**Fields:**
- `video_id`: Unique ID (যেকোনো - Example: v101, v102)
- `file_id`: Telegram file ID
- `caption`: Video caption/description
- `views`: 0 (initial)
- `added_at`: Current date

**Step 4: Video Link তৈরি করুন**

```
https://t.me/your_bot?start=v_101
```

---

## 🌐 Server Deploy

### Option 1: VPS (Ubuntu)

**Step 1: VPS কিনুন**
- DigitalOcean ($5/month)
- Linode ($5/month)
- Vultr ($3.5/month)
- Contabo (€4/month)

**Step 2: Server এ Login**
```bash
ssh root@your-server-ip
```

**Step 3: Dependencies Install**
```bash
# System update
sudo apt update && sudo apt upgrade -y

# Python install
sudo apt install python3 python3-pip git -y

# Check version
python3 --version
```

**Step 4: Bot Upload**

**Method A: Using Git**
```bash
# Clone repository
git clone <your-repo-url>
cd cineflix-bot
```

**Method B: Using SCP (From local)**
```bash
# From your computer
scp -r cineflix-bot/ root@your-server-ip:/root/
```

**Method C: Using FileZilla**
- FileZilla download করুন
- Server connect করুন (SFTP)
- Files drag & drop করুন

**Step 5: Configuration**
```bash
# .env file তৈরি করুন
nano .env

# আপনার credentials paste করুন
# Ctrl+X, Y, Enter to save
```

**Step 6: Dependencies Install**
```bash
pip3 install -r requirements.txt
```

**Step 7: Bot চালু করুন**

**Temporary (Testing):**
```bash
python3 bot.py
```

**Permanent (Using Screen):**
```bash
# Screen install
sudo apt install screen

# New session
screen -S cineflix

# Bot start
python3 bot.py

# Detach: Ctrl+A then D
# Re-attach: screen -r cineflix

# List sessions: screen -ls
# Kill session: screen -XS cineflix quit
```

**Permanent (Using systemd):**

1. Service file তৈরি করুন:
```bash
sudo nano /etc/systemd/system/cineflix.service
```

2. এই content paste করুন:
```ini
[Unit]
Description=CINEFLIX Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/cineflix-bot
ExecStart=/usr/bin/python3 /root/cineflix-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Service enable এবং start করুন:
```bash
sudo systemctl daemon-reload
sudo systemctl enable cineflix
sudo systemctl start cineflix

# Status check
sudo systemctl status cineflix

# Logs দেখুন
sudo journalctl -u cineflix -f
```

**Commands:**
```bash
sudo systemctl start cineflix    # Start
sudo systemctl stop cineflix     # Stop
sudo systemctl restart cineflix  # Restart
sudo systemctl status cineflix   # Status
```

### Option 2: Heroku (Free - With limitations)

**Step 1: Heroku Account তৈরি করুন**
1. [Heroku](https://heroku.com) এ যান
2. Sign up করুন (Free)

**Step 2: Heroku CLI Install**

**Ubuntu/Debian:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

**Windows/Mac:**
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) থেকে download করুন

**Step 3: Login**
```bash
heroku login
```

**Step 4: App তৈরি করুন**
```bash
cd cineflix-bot
heroku create your-app-name
```

**Step 5: Environment Variables সেট করুন**
```bash
heroku config:set BOT_TOKEN=your_token
heroku config:set MONGO_URI=your_mongo_uri
heroku config:set ADMIN_ID=your_id
```

**Step 6: Deploy করুন**
```bash
# Git initialize (if not done)
git init

# Add files
git add .

# Commit
git commit -m "Deploy CINEFLIX Bot"

# Push to Heroku
git push heroku master
```

**Step 7: Dyno চালু করুন**
```bash
heroku ps:scale worker=1
```

**Step 8: Logs দেখুন**
```bash
heroku logs --tail
```

**⚠️ Note:** Heroku free plan এ bot 550 hours/month পর্যন্ত চলবে।

### Option 3: Railway (Easy & Free)

1. [Railway.app](https://railway.app) এ যান
2. GitHub connect করুন
3. Repository select করুন
4. Environment Variables add করুন:
   - `BOT_TOKEN`
   - `MONGO_URI`
   - `ADMIN_ID`
5. Deploy automatically হবে!

### Option 4: PythonAnywhere (Free)

1. [PythonAnywhere](https://www.pythonanywhere.com) এ account তৈরি করুন
2. "Web" tab → "Add a new web app"
3. Files upload করুন
4. Bash console এ dependencies install করুন
5. Always-on task add করুন (Paid feature)

---

## 🐛 Troubleshooting

### Problem 1: Bot শুরু হচ্ছে না

**Error:** `BOT_TOKEN environment variable not set!`

**Solution:**
```bash
# Check .env file
cat .env

# If empty, edit it
nano .env

# Add your credentials
BOT_TOKEN=your_token_here
MONGO_URI=your_mongo_uri
ADMIN_ID=your_id

# Save: Ctrl+X, Y, Enter
```

### Problem 2: MongoDB Connection Failed

**Error:** `MongoDB Connection Failed: ServerSelectionTimeoutError`

**Solutions:**

1. **Check Internet Connection**
```bash
ping google.com
```

2. **Verify MongoDB URI**
- `.env` file এ MONGO_URI check করুন
- Password correct আছে কিনা verify করুন
- `<password>` replace করতে ভুলে যাননি তো?

3. **Check Network Access**
- MongoDB Atlas → Network Access
- `0.0.0.0/0` added আছে কিনা check করুন

4. **Test Connection Manually**
```bash
pip3 install pymongo
python3 -c "from pymongo import MongoClient; client = MongoClient('YOUR_MONGO_URI'); print(client.server_info())"
```

### Problem 3: Force Join কাজ করছে না

**Solutions:**

1. **Bot Admin আছে কিনা check করুন**
- Channel → Administrators → Bot check করুন

2. **Channel ID সঠিক আছে কিনা**
- Channel ID অবশ্যই `-100` দিয়ে শুরু হবে
- Example: `-1001234567890`

3. **Private Channel এর ক্ষেত্রে**
- User join request পাঠালেই হবে
- Approve এর দরকার নেই

4. **Test করুন**
```bash
# Bot logs দেখুন
# User যখন verify ক্লিক করবে তখন log এ দেখবেন
```

### Problem 4: Video Automatically Add হচ্ছে না

**Solutions:**

1. **Bot Channel এ Admin কিনা**
- Bot কে channel admin বানান
- সব permissions দিন

2. **Main Channel ID সেট করা আছে কিনা**
- `/admin` → Settings → Main Channel ID check করুন

3. **Channel ID Correct কিনা**
- Video channel এর ID সঠিক দিয়েছেন কিনা verify করুন

4. **Bot Logs Check করুন**
```bash
# যখন video post করবেন তখন log এ দেখবেন:
✅ Auto-added video: v123
```

### Problem 5: Permission Denied Error

**Error:** `Permission denied: ./START.sh`

**Solution:**
```bash
chmod +x START.sh
./START.sh
```

### Problem 6: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'telegram'`

**Solution:**
```bash
# Reinstall dependencies
pip3 install -r requirements.txt --upgrade

# Or install manually
pip3 install python-telegram-bot==21.9 pymongo==4.10.1
```

### Problem 7: Bot Responding হচ্ছে না

**Solutions:**

1. **Bot চালু আছে কিনা check করুন**
```bash
ps aux | grep bot.py
```

2. **Logs দেখুন**
```bash
# If using screen
screen -r cineflix

# If using systemd
sudo journalctl -u cineflix -f
```

3. **Restart করুন**
```bash
# Kill process
pkill -f bot.py

# Start again
python3 bot.py
```

### Problem 8: Videos সব users পাচ্ছে না

**Solutions:**

1. **Video File ID Valid কিনা**
- MongoDB তে `file_id` check করুন
- File ID অবশ্যই valid হতে হবে

2. **Video Link Format**
```
Correct: https://t.me/your_bot?start=v_123
Wrong: https://t.me/your_bot?start=123
```

3. **Video Protection**
- Settings → Video Protection check করুন
- True = Protected, False = Not protected

---

## 📝 Final Checklist

Deploy করার আগে এই checklist check করুন:

### Configuration ✅
- [ ] `.env` file তৈরি করেছি
- [ ] `BOT_TOKEN` set করেছি
- [ ] `MONGO_URI` set করেছি
- [ ] `ADMIN_ID` set করেছি
- [ ] MongoDB থেকে connection test করেছি
- [ ] Bot এ `/start` পাঠিয়ে test করেছি

### Force Join ✅
- [ ] Channel তৈরি করেছি
- [ ] Bot কে channel admin বানিয়েছি
- [ ] Channel ID নিয়েছি
- [ ] Bot এ force join channel add করেছি
- [ ] New user দিয়ে test করেছি

### Video Setup ✅
- [ ] Video channel তৈরি করেছি (Optional)
- [ ] Bot কে video channel admin বানিয়েছি
- [ ] Main Channel ID set করেছি
- [ ] Test video post করেছি
- [ ] Video link test করেছি

### Server Deploy ✅
- [ ] Server select করেছি (VPS/Heroku/Railway)
- [ ] Dependencies install করেছি
- [ ] Bot চালু করেছি
- [ ] Bot running আছে কিনা verify করেছি
- [ ] Logs check করেছি

### Monitoring ✅
- [ ] `/admin` command test করেছি
- [ ] Statistics দেখতে পাচ্ছি
- [ ] Broadcast test করেছি
- [ ] Messages edit করতে পারছি
- [ ] Buttons manage করতে পারছি

---

## 🎉 Congratulations!

আপনার CINEFLIX Bot এখন fully functional এবং ready to use! 

### Next Steps:

1. **Mini App তৈরি করুন** - Video listing এর জন্য
2. **Custom Domain** - Professional look এর জন্য
3. **More Channels** - More content এর জন্য
4. **Promote Your Bot** - Users attract করার জন্য

### Support:

- Documentation পড়ুন: `README.md`
- Issues open করুন GitHub এ
- Community join করুন

**🎬 Happy Streaming! 🎬**

---

**Version:** 2.0  
**Last Updated:** 2024  
**Developed by:** CINEFLIX Team
