# 🎬 CINEFLIX Ultimate Bot

একটি Premium Telegram Video Bot যা Full Admin Panel এবং Force Join সহ আসে।
A Premium Telegram Video Bot with Full Admin Panel and Force Join features.

---

## 📋 Features / ফিচার

✅ **Mini App Integration** - Web App দিয়ে ভিডিও ব্রাউজ করুন
✅ **Force Join System** - Public ও Private চ্যানেল সাপোর্ট
✅ **Admin Panel** - সম্পূর্ণ কন্ট্রোল প্যানেল
✅ **Auto Video Upload** - চ্যানেলে পোস্ট করলেই database এ save
✅ **Message Customization** - সব মেসেজ customize করুন
✅ **Broadcast System** - সব ইউজারকে মেসেজ পাঠান
✅ **User Statistics** - বিস্তারিত stats দেখুন
✅ **Button Management** - Custom buttons যোগ করুন
✅ **Auto Cleanup** - Old messages auto delete
✅ **MongoDB Database** - Fast এবং reliable

---

## 🚀 Deploy করার ধাপ (Railway)

### 1️⃣ Prerequisites / প্রয়োজনীয় জিনিস

প্রথমে এগুলো সংগ্রহ করুন:

#### **🤖 Bot Token**
1. Telegram এ যান [@BotFather](https://t.me/BotFather)
2. `/newbot` লিখুন
3. Bot এর নাম দিন
4. Username দিন (অবশ্যই `_bot` দিয়ে শেষ হতে হবে)
5. আপনি একটা Token পাবেন: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

#### **💾 MongoDB URI**
1. যান [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Free account খুলুন
3. "Create a New Cluster" ক্লিক করুন (FREE M0 select করুন)
4. Cluster তৈরি হলে "Connect" ক্লিক করুন
5. "Connect your application" সিলেক্ট করুন
6. Connection string কপি করুন: `mongodb+srv://username:password@cluster.mongodb.net/`
7. `<password>` আপনার password দিয়ে replace করুন

#### **👤 Admin ID**
1. Telegram এ যান [@userinfobot](https://t.me/userinfobot)
2. `/start` দিন
3. আপনার ID দেখাবে (উদাহরণ: `123456789`)

---

### 2️⃣ Railway তে Deploy

#### **Step 1: GitHub Repository তৈরি করুন**

1. [GitHub](https://github.com) এ যান এবং login করুন
2. উপরে ডানদিকে "+" ক্লিক করুন → "New repository"
3. Repository name দিন: `cineflix-bot`
4. "Public" select করুন
5. "Create repository" ক্লিক করুন

#### **Step 2: Code Upload করুন**

এই ZIP file টি download করে extract করুন, তারপর:

**Option A: GitHub Desktop দিয়ে** (সহজ)
1. [GitHub Desktop](https://desktop.github.com/) download করুন
2. আপনার repository clone করুন
3. সব ফাইল repository folder এ copy করুন
4. "Commit to main" ক্লিক করুন
5. "Push origin" ক্লিক করুন

**Option B: Command Line দিয়ে**
```bash
cd cineflix_bot_complete
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cineflix-bot.git
git push -u origin main
```

#### **Step 3: Railway তে Deploy**

1. [Railway](https://railway.app/) এ যান
2. "Login with GitHub" ক্লিক করুন
3. "New Project" ক্লিক করুন
4. "Deploy from GitHub repo" সিলেক্ট করুন
5. আপনার `cineflix-bot` repository সিলেক্ট করুন
6. Deploy শুরু হবে...

#### **Step 4: Environment Variables সেট করুন**

Deploy হওয়ার পর:

1. Project এ ক্লিক করুন
2. "Variables" ট্যাব এ যান
3. এই ৩টি variable যোগ করুন:

```
BOT_TOKEN = আপনার_বট_টোকেন
MONGO_URI = আপনার_মংগোডিবি_uri
ADMIN_ID = আপনার_টেলিগ্রাম_আইডি
```

**উদাহরণ:**
```
BOT_TOKEN = 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
MONGO_URI = mongodb+srv://myuser:mypass123@cluster0.abcde.mongodb.net/
ADMIN_ID = 123456789
```

4. সব variable add করার পর bot automatically redeploy হবে

#### **Step 5: Bot চালু করুন**

1. Railway dashboard এ "Deployments" ট্যাব দেখুন
2. Latest deployment এ ক্লিক করুন
3. "View Logs" ক্লিক করুন
4. এই মেসেজ দেখলে success:
```
✅ MongoDB Connected Successfully!
✅ CINEFLIX Ultimate Bot is running!
```

---

## 🎯 Bot Setup করুন

### 1. Mini App URL সেট করুন

1. Telegram এ bot এ যান
2. `/start` দিন
3. `/admin` দিন
4. "⚙️ Settings" ক্লিক করুন
5. "Mini App URL" ক্লিক করুন
6. আপনার web app URL পাঠান

### 2. Main Channel সেট করুন

1. `/admin` → "⚙️ Settings"
2. "Main Channel ID" ক্লিক করুন
3. আপনার channel এর ID পাঠান (উদাহরণ: `-1001234567890`)

**Channel ID কীভাবে পাবেন:**
- Channel এ [@userinfobot](https://t.me/userinfobot) add করুন
- সে ID দেখাবে

### 3. Force Join Channel যোগ করুন

1. `/admin` → "📢 Force Join"
2. "➕ Add Channel" ক্লিক করুন
3. Channel ID এবং invite link পাঠান:
```
-1001234567890 | https://t.me/+AbCdEfGhIjKlMn
```

---

## 📱 Bot ব্যবহার করুন

### Video Upload করুন

1. আপনার channel এ video post করুন
2. Caption এ video title লিখুন
3. Bot automatically database এ save করবে
4. Mini App এ video দেখা যাবে

### Admin Commands

- `/start` - Bot শুরু করুন
- `/admin` - Admin panel খুলুন
- `/help` - Help দেখুন

### Admin Panel Options

- **📊 Statistics** - User এবং video stats
- **📢 Force Join** - Force join channels manage করুন
- **💬 Messages** - সব messages customize করুন
- **🔘 Buttons** - Custom buttons যোগ করুন
- **⚙️ Settings** - Bot settings
- **📣 Broadcast** - সব users কে message পাঠান

---

## 🔧 Troubleshooting

### Bot শুরু হচ্ছে না?

**Check করুন:**
1. Environment variables সঠিক আছে কিনা
2. MongoDB URI সঠিক এবং password replace করেছেন কিনা
3. Railway logs দেখুন কোন error আছে কিনা

### Force Join কাজ করছে না?

**নিশ্চিত করুন:**
1. Bot কে channel এ admin বানিয়েছেন
2. Channel ID সঠিক (অবশ্যই `-100` দিয়ে শুরু)
3. Private channel হলে invite link দিয়েছেন

### Video দেখা যাচ্ছে না?

**Check করুন:**
1. Video channel এ post হয়েছে কিনা
2. Bot সেই channel এ member আছে কিনা
3. Main Channel ID settings এ সেট করা আছে কিনা

---

## 📞 Support

সমস্যা হলে:
1. প্রথমে Railway logs check করুন
2. Environment variables verify করুন
3. MongoDB connection test করুন

---

## 🎉 সফলভাবে Deploy হয়েছে!

এখন আপনার bot সম্পূর্ণ কাজ করবে। Users video request করলে force join করাবে এবং তারপর video দেবে!

**Happy Streaming! 🍿**

---

## 📄 License

MIT License - Free to use and modify

---

**Made with ❤️ for CINEFLIX**
