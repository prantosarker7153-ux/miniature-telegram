# 🚀 সহজ Deploy গাইড (বাংলায়)

## 🎯 ৫ মিনিটে Deploy করুন!

---

## 📋 যা যা লাগবে

### 1️⃣ Bot Token পান

1. Telegram খুলুন
2. Search করুন: `@BotFather`
3. `/newbot` লিখে পাঠান
4. Bot এর নাম দিন (যেমন: "CINEFLIX Bot")
5. Username দিন (যেমন: "cineflix123_bot")
6. Token save করুন: `1234567890:ABCdefGHI...`

### 2️⃣ MongoDB URI পান

1. যান: https://www.mongodb.com/cloud/atlas/register
2. Email দিয়ে sign up করুন
3. "Create a Free Cluster" ক্লিক করুন
4. Cluster name দিন এবং wait করুন (2-3 মিনিট)
5. "Connect" বাটন ক্লিক করুন
6. "Connect your application" সিলেক্ট করুন
7. URI copy করুন এবং `<password>` নিজের password দিয়ে replace করুন

**উদাহরণ:**
```
mongodb+srv://myuser:MyPassword123@cluster0.abcde.mongodb.net/
```

### 3️⃣ আপনার Telegram ID পান

1. Telegram এ search করুন: `@userinfobot`
2. `/start` দিন
3. আপনার ID copy করুন (যেমন: `123456789`)

---

## 🌐 Railway তে Deploy (সবচেয়ে সহজ)

### Step 1: GitHub এ Repository তৈরি করুন

1. যান: https://github.com
2. Login করুন (নতুন হলে sign up করুন)
3. উপরে ডানে "+" ক্লিক করুন
4. "New repository" ক্লিক করুন
5. Repository name: `cineflix-bot`
6. "Public" select করুন
7. "Create repository" ক্লিক করুন

### Step 2: Code Upload করুন

**সহজ উপায় (Web Interface দিয়ে):**

1. Download করুন এই ZIP file
2. Extract করুন
3. GitHub repository page এ যান
4. "uploading an existing file" link এ ক্লিক করুন
5. সব files drag & drop করুন
6. "Commit changes" ক্লিক করুন

**অথবা GitHub Desktop দিয়ে:**

1. Download: https://desktop.github.com/
2. Repository clone করুন
3. Files copy করুন folder এ
4. "Commit to main" → "Push origin"

### Step 3: Railway তে Deploy করুন

1. যান: https://railway.app/
2. "Start a New Project" ক্লিক করুন
3. "Deploy from GitHub repo" সিলেক্ট করুন
4. "Login with GitHub" করুন
5. আপনার `cineflix-bot` repository সিলেক্ট করুন
6. "Deploy Now" ক্লিক করুন

### Step 4: Environment Variables Add করুন

Deploy হওয়ার সাথে সাথে:

1. Dashboard এ "Variables" ট্যাব ক্লিক করুন
2. "New Variable" ক্লিক করুন
3. এই ৩টি variable add করুন:

**Variable 1:**
```
Variable name: BOT_TOKEN
Value: আপনার_বট_টোকেন
```

**Variable 2:**
```
Variable name: MONGO_URI
Value: আপনার_মংগোডিবি_uri
```

**Variable 3:**
```
Variable name: ADMIN_ID
Value: আপনার_টেলিগ্রাম_আইডি
```

4. "Add" ক্লিক করুন
5. Bot automatically restart হবে

### Step 5: Check করুন Bot চালু হয়েছে কিনা

1. "Deployments" ট্যাবে ক্লিক করুন
2. Latest deployment দেখুন
3. "View Logs" ক্লিক করুন
4. এই lines দেখলে success:

```
✅ MongoDB Connected Successfully!
✅ CINEFLIX Ultimate Bot is running!
```

---

## 🎬 Bot Setup করুন

### 1. Bot এ Admin Command দিন

1. Telegram এ bot এ যান
2. `/start` দিন
3. `/admin` দিন
4. Admin panel দেখা যাবে!

### 2. Channel Setup করুন

**Main Channel ID সেট করুন:**
1. `/admin` কমান্ড দিন
2. "⚙️ Settings" ক্লিক করুন
3. "Main Channel ID" ক্লিক করুন
4. আপনার channel এর ID পাঠান

**Channel ID কীভাবে পাবেন:**
- আপনার channel এ `@userinfobot` কে admin বানান
- Bot channel ID দেখাবে
- ID copy করুন (যেমন: `-1001234567890`)

### 3. Force Join Channel Add করুন

1. `/admin` → "📢 Force Join"
2. "➕ Add Channel" ক্লিক করুন
3. এই format এ পাঠান:
```
-1001234567890 | https://t.me/+InviteLinkHere
```

**Note:** 
- Public channel এ শুধু ID দিলেই হবে
- Private channel এ invite link লাগবে

### 4. Bot কে Channel এ Admin বানান

**Important:**
1. আপনার channel এ যান
2. Administrators → Add Administrator
3. আপনার bot খুঁজুন
4. "Post Messages" permission দিন
5. Save করুন

---

## ✅ Test করুন

### Video Upload Test

1. আপনার channel এ একটা video post করুন
2. Caption দিন
3. Check করুন bot এ `/admin` → "📊 Statistics"
4. Videos count বাড়ছে কিনা দেখুন

### Force Join Test

1. একটা নতুন account দিয়ে bot এ `/start` দিন
2. Mini App খুলুন
3. Video সিলেক্ট করুন
4. Force join message আসবে
5. Channel join করুন
6. Verify করুন
7. Video পাবেন!

---

## 🐛 সমস্যা সমাধান

### Bot Start হচ্ছে না?

**Check List:**
- [ ] BOT_TOKEN সঠিক আছে?
- [ ] MONGO_URI তে password replace করেছেন?
- [ ] ADMIN_ID number আছে (text না)?
- [ ] Railway logs এ কোন error?

**Fix:**
1. Railway dashboard → Variables
2. সব variables double check করুন
3. কোন space বা extra character নেই তো?
4. Save করুন এবং redeploy করুন

### MongoDB Connection Error?

**সমাধান:**
1. MongoDB Atlas দেখুন cluster চালু আছে কিনা
2. Network Access → Add IP Address → Allow from Anywhere (0.0.0.0/0)
3. Database Access → আপনার user এর password verify করুন
4. URI তে password সঠিক আছে কিনা check করুন

### Force Join কাজ করছে না?

**Check করুন:**
1. Bot কে channel এ admin বানিয়েছেন?
2. Channel ID `-100` দিয়ে শুরু হচ্ছে?
3. Private channel এ invite link দিয়েছেন?
4. Bot channel এ message post করতে পারছে?

### Video পাচ্ছে না?

**Checklist:**
1. [ ] Video channel এ post করা আছে?
2. [ ] Bot সেই channel এ member?
3. [ ] Main Channel ID settings এ আছে?
4. [ ] `/admin` → Statistics এ video count দেখা যাচ্ছে?

---

## 📊 Monitor করুন

### Railway Dashboard

**Daily Check করুন:**
- Deployment status (Running হচ্ছে কিনা)
- Logs (কোন error নেই তো)
- Resource usage (limit এর মধ্যে আছে কিনা)

### Bot Stats

**Regular Monitor:**
1. `/admin` → "📊 Statistics"
2. User growth দেখুন
3. Video views track করুন
4. Active users check করুন

---

## 🎉 সফল Deploy!

আপনার bot এখন সম্পূর্ণ চালু!

**এরপর কী করবেন:**
1. ✅ Video upload করা শুরু করুন
2. ✅ Users কে bot share করুন
3. ✅ Force join channels promote করুন
4. ✅ Regular statistics monitor করুন
5. ✅ Content update করুন daily

**Happy Streaming! 🍿🎬**

---

## 💡 Pro Tips

### Better Performance জন্য:

1. **Regular Updates**: প্রতিদিন নতুন content add করুন
2. **Clean Database**: মাঝে মাঝে old/unused videos remove করুন
3. **Monitor Logs**: Weekly logs check করুন issues এর জন্য
4. **Backup**: Important data occasionally backup নিন
5. **User Feedback**: Users দের feedback নিয়ে improve করুন

### Security Tips:

1. ❌ কখনো BOT_TOKEN public করবেন না
2. ❌ MongoDB URI কারো সাথে share করবেন না
3. ✅ Regular password change করুন
4. ✅ Railway access control maintain করুন
5. ✅ Admin access শুধু trusted users কে দিন

---

## 🆘 Help দরকার?

**Resources:**
- Railway Docs: https://docs.railway.app/
- MongoDB Docs: https://docs.mongodb.com/
- Telegram Bot API: https://core.telegram.org/bots/api

**Common Issues:**
- Google করুন error message দিয়ে
- Railway community forum check করুন
- GitHub issues দেখুন similar problems এর জন্য

---

**এই guide follow করলে আপনার bot 100% কাজ করবে!** 🚀

Good luck! 🎊
