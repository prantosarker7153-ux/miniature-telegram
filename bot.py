#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 CINEFLIX ULTIMATE BOT
Premium Video Bot with Full Admin Panel + Enhanced Features
Version: 2.0
Author: CINEFLIX Team
"""

import os
import sys
import logging
from datetime import datetime, timedelta
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ChatJoinRequestHandler
)
from telegram.constants import ParseMode
from telegram.error import BadRequest, TelegramError, Forbidden
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# ===================== CONFIGURATION =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_ID = os.getenv("ADMIN_ID")

# Validate environment variables
if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set!")
    sys.exit(1)

if not MONGO_URI:
    print("❌ ERROR: MONGO_URI environment variable not set!")
    sys.exit(1)

if not ADMIN_ID:
    print("❌ ERROR: ADMIN_ID environment variable not set!")
    sys.exit(1)

try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    print("❌ ERROR: ADMIN_ID must be a number!")
    sys.exit(1)

# ===================== LOGGING SETUP =====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===================== MONGODB SETUP =====================
try:
    logger.info("🔄 Connecting to MongoDB...")
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    mongo_client.server_info()
    db = mongo_client['cineflix_bot']
    
    # Collections
    videos_col = db['videos']
    channels_col = db['channels']
    force_join_col = db['force_join_channels']
    users_col = db['users']
    settings_col = db['settings']
    messages_col = db['messages']
    buttons_col = db['buttons']
    pending_requests_col = db['pending_join_requests']
    
    logger.info("✅ MongoDB Connected Successfully!")
    
except (ConnectionFailure, OperationFailure) as e:
    logger.error(f"❌ MongoDB Connection Failed: {e}")
    sys.exit(1)

# ===================== STATE MANAGEMENT =====================
admin_states = {}
user_video_messages = {}
user_all_messages = {}

# ===================== DEFAULT MESSAGES =====================
DEFAULT_MESSAGES = {
    'welcome': """🎬 **স্বাগতম CINEFLIX এ!**
**Welcome to CINEFLIX!**

━━━━━━━━━━━━━━━━━━━━

Hello **{name}**! 👋

আপনার সব পছন্দের Movies, Series এবং Exclusive Content এক জায়গায়!
All your favorite Movies, Series, and Exclusive Content in one place!

━━━━━━━━━━━━━━━━━━━━

**🚀 কীভাবে ভিডিও দেখবেন?**
**🚀 How to Watch Videos?**

**ধাপ ১:** নিচে "🎮 Open CINEFLIX App" ক্লিক করুন
**Step 1:** Click "🎮 Open CINEFLIX App" below

**ধাপ ২:** পছন্দের ভিডিও সিলেক্ট করুন
**Step 2:** Select your favorite video

**ধাপ ৩:** আমাদের চ্যানেলে জয়েন করুন (প্রথমবার)
**Step 3:** Join our channel (first time only)

**ধাপ ৪:** ভিডিও উপভোগ করুন! 🍿
**Step 4:** Enjoy the video! 🍿

━━━━━━━━━━━━━━━━━━━━

**📢 Important:**
✅ সব কন্টেন্ট আনলক করতে আমাদের চ্যানেল জয়েন করুন
✅ Premium quality HD videos
✅ প্রতিদিন নতুন আপডেট
✅ সম্পূর্ণ ফ্রি!

**🎉 Happy Streaming! 🎉**""",

    'help': """📚 **CINEFLIX Bot - Help Guide**

**🎯 Commands:**
/start - বোট শুরু করুন | Start bot
/help - সাহায্য দেখুন | Show help

**🎬 কীভাবে ভিডিও দেখবেন?**

**Step 1:** /start দিয়ে Mini App খুলুন
**Step 2:** পছন্দের ভিডিও সিলেক্ট করুন
**Step 3:** চ্যানেল জয়েন করুন (যদি বলা হয়)
**Step 4:** ভিডিও উপভোগ করুন! 🍿

**⚠️ সমস্যা?**
- ভিডিও না দেখা গেলে চ্যানেল জয়েন করুন
- লিঙ্ক কাজ না করলে Mini App রিফ্রেশ করুন
- অন্য সমস্যায় Admin কে মেসেজ করুন""",

    'force_join': """🔒 **ভিডিও দেখতে চ্যানেল জয়েন করুন!**
🔒 **Join Channel to Watch Video!**

━━━━━━━━━━━━━━━━━━━━

**📱 কীভাবে দেখবেন?**

**ধাপ ১:** নিচের চ্যানেল বাটনে ক্লিক করুন
**ধাপ ২:** "Join" অথবা "Request to Join" ক্লিক করুন
**ধাপ ৩:** বট এ ফিরে এসে "✅ আমি জয়েন করেছি" বাটন ক্লিক করুন

━━━━━━━━━━━━━━━━━━━━

**💡 মনে রাখবেন:**
✅ **পাবলিক চ্যানেল:** Join করার পর verify button click করুন
✅ **প্রাইভেট চ্যানেল:** শুধু request পাঠান, approve এর দরকার নেই!

🎬 **ভিডিও পেতে verify button অবশ্যই click করুন!**

━━━━━━━━━━━━━━━━━━━━""",

    'after_video': """🎬 **ভিডিও উপভোগ করুন!**

**🌟 আরও ভিডিও দেখতে চান?**

নিচের বাটনে ক্লিক করে আমাদের Mini App এ যান!

**📺 প্রতিদিন নতুন কন্টেন্ট!**

**💝 ধন্যবাদ! Thank you!**""",

    'video_not_found': """❌ **দুঃখিত! Video Not Found!**

এই ভিডিওটি আর পাওয়া যাচ্ছে না।

**কী করবেন?**
✅ Mini App এ ফিরে অন্য ভিডিও দেখুন
✅ আমাদের চ্যানেলে জয়েন থাকুন""",

    'auto_reply': """👋 **Hello!**

আমি একটি Video Bot!

🎬 Videos দেখতে /start ব্যবহার করুন"""
}

# ===================== DATABASE FUNCTIONS =====================
def initialize_defaults():
    """Initialize default messages and settings"""
    for key, value in DEFAULT_MESSAGES.items():
        if not messages_col.find_one({'key': key}):
            messages_col.insert_one({'key': key, 'text': value})
    
    default_settings = {
        'mini_app_url': 'https://your-mini-app-url.com',
        'main_channel_id': None,
        'main_channel_username': None,
        'video_protection': True,
        'auto_delete_enabled': True,
        'auto_delete_delay': 300
    }
    
    for key, value in default_settings.items():
        if not settings_col.find_one({'key': key}):
            settings_col.insert_one({'key': key, 'value': value})

def get_message(key):
    """Get message from database"""
    msg = messages_col.find_one({'key': key})
    return msg['text'] if msg else DEFAULT_MESSAGES.get(key, '')

def set_message(key, text):
    """Update message in database"""
    try:
        messages_col.update_one(
            {'key': key},
            {'$set': {'text': text}},
            upsert=True
        )
        return True
    except Exception as e:
        logger.error(f"Failed to set message: {e}")
        return False

def get_setting(key):
    """Get setting from database"""
    setting = settings_col.find_one({'key': key})
    return setting['value'] if setting else None

def set_setting(key, value):
    """Update setting in database"""
    try:
        settings_col.update_one(
            {'key': key},
            {'$set': {'value': value}},
            upsert=True
        )
        return True
    except Exception as e:
        logger.error(f"Failed to set setting: {e}")
        return False

def get_buttons(location):
    """Get buttons for a location"""
    buttons = list(buttons_col.find({'location': location}).sort('order', 1))
    return buttons

def add_button(location, text, url, btn_type, order=0):
    """Add button to database"""
    try:
        buttons_col.insert_one({
            'location': location,
            'text': text,
            'url': url,
            'type': btn_type,
            'order': order
        })
        return True
    except Exception as e:
        logger.error(f"Failed to add button: {e}")
        return False

def delete_button(button_id):
    """Delete button from database"""
    try:
        from bson.objectid import ObjectId
        buttons_col.delete_one({'_id': ObjectId(button_id)})
        return True
    except Exception as e:
        logger.error(f"Failed to delete button: {e}")
        return False

def add_user(user_id, username, first_name):
    """Add or update user in database"""
    try:
        users_col.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'username': username,
                    'first_name': first_name,
                    'last_seen': datetime.now()
                },
                '$setOnInsert': {
                    'joined_at': datetime.now()
                }
            },
            upsert=True
        )
        return True
    except Exception as e:
        logger.error(f"Failed to add user: {e}")
        return False

def get_all_users():
    """Get all user IDs"""
    try:
        users = users_col.find({}, {'user_id': 1})
        return [user['user_id'] for user in users]
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        return []

def get_stats():
    """Get bot statistics"""
    try:
        total_users = users_col.count_documents({})
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        active_today = users_col.count_documents({'last_seen': {'$gte': today}})
        total_videos = videos_col.count_documents({})
        
        top_video = videos_col.find_one(sort=[('views', -1)])
        top_views = top_video['views'] if top_video else 0
        
        force_join_count = force_join_col.count_documents({})
        
        return {
            'users': total_users,
            'active_today': active_today,
            'videos': total_videos,
            'top_views': top_views,
            'force_join': force_join_count
        }
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        return {'users': 0, 'active_today': 0, 'videos': 0, 'top_views': 0, 'force_join': 0}

def get_video(video_id):
    """Get video from database"""
    return videos_col.find_one({'video_id': video_id})

def increment_video_views(video_id):
    """Increment video view count"""
    try:
        videos_col.update_one(
            {'video_id': video_id},
            {'$inc': {'views': 1}}
        )
        return True
    except Exception as e:
        logger.error(f"Failed to increment views: {e}")
        return False

def get_force_join_channels():
    """Get all force join channels"""
    return list(force_join_col.find({'enabled': True}))

def add_force_join_channel(channel_id, channel_name=None, channel_link=None):
    """Add force join channel"""
    try:
        force_join_col.insert_one({
            'channel_id': channel_id,
            'channel_name': channel_name,
            'channel_link': channel_link,
            'enabled': True,
            'added_at': datetime.now()
        })
        return True
    except Exception as e:
        logger.error(f"Failed to add force join channel: {e}")
        return False

def delete_force_join_channel(channel_id):
    """Delete force join channel"""
    try:
        force_join_col.delete_one({'channel_id': channel_id})
        return True
    except Exception as e:
        logger.error(f"Failed to delete force join channel: {e}")
        return False

def add_pending_request(user_id, channel_id):
    """Track that user sent join request"""
    try:
        pending_requests_col.update_one(
            {'user_id': user_id, 'channel_id': channel_id},
            {
                '$set': {
                    'requested_at': datetime.now(),
                    'status': 'pending'
                }
            },
            upsert=True
        )
        return True
    except Exception as e:
        logger.error(f"Failed to add pending request: {e}")
        return False

def approve_pending_request(user_id, channel_id):
    """Mark join request as approved"""
    try:
        pending_requests_col.update_one(
            {'user_id': user_id, 'channel_id': channel_id},
            {'$set': {'status': 'approved', 'approved_at': datetime.now()}}
        )
        return True
    except Exception as e:
        logger.error(f"Failed to approve request: {e}")
        return False

def is_request_pending_or_approved(user_id, channel_id):
    """Check if user has pending or approved request"""
    request = pending_requests_col.find_one({
        'user_id': user_id,
        'channel_id': channel_id,
        'status': {'$in': ['pending', 'approved']}
    })
    return request is not None

# ===================== HELPER FUNCTIONS =====================
async def is_user_member(bot, user_id, channel_id):
    """Check if user is member of channel"""
    try:
        member = await bot.get_chat_member(channel_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except (BadRequest, Forbidden, TelegramError) as e:
        logger.error(f"Error checking membership for user {user_id} in channel {channel_id}: {e}")
        return False

async def check_all_channels(bot, user_id):
    """Check if user is member of all force join channels"""
    channels = get_force_join_channels()
    not_joined = []
    
    for channel in channels:
        channel_id = channel['channel_id']
        
        # Check if user is actual member
        is_member = await is_user_member(bot, user_id, channel_id)
        
        if not is_member:
            # Check if user has pending/approved request (for private channels)
            has_request = is_request_pending_or_approved(user_id, channel_id)
            if not has_request:
                not_joined.append(channel)
    
    return not_joined

def build_force_join_keyboard(channels):
    """Build keyboard for force join channels"""
    keyboard = []
    
    for channel in channels:
        channel_name = channel.get('channel_name', 'Join Channel')
        channel_link = channel.get('channel_link')
        
        if channel_link:
            keyboard.append([InlineKeyboardButton(f"📢 {channel_name}", url=channel_link)])
        else:
            keyboard.append([InlineKeyboardButton(f"📢 {channel_name}", url=f"https://t.me/{channel['channel_id']}")])
    
    keyboard.append([InlineKeyboardButton("✅ আমি জয়েন করেছি | I Joined", callback_data="verify_join")])
    
    return InlineKeyboardMarkup(keyboard)

def build_welcome_keyboard():
    """Build keyboard for welcome message"""
    mini_app_url = get_setting('mini_app_url') or 'https://your-mini-app-url.com'
    
    keyboard = []
    buttons = get_buttons('welcome')
    
    if not buttons:
        keyboard.append([InlineKeyboardButton(
            "🎮 Open CINEFLIX App",
            web_app=WebAppInfo(url=mini_app_url)
        )])
    else:
        for btn in buttons:
            if btn['type'] == 'web_app':
                keyboard.append([InlineKeyboardButton(btn['text'], web_app=WebAppInfo(url=btn['url']))])
            else:
                keyboard.append([InlineKeyboardButton(btn['text'], url=btn['url'])])
    
    return InlineKeyboardMarkup(keyboard)

def build_after_video_keyboard():
    """Build keyboard for after video message"""
    mini_app_url = get_setting('mini_app_url') or 'https://your-mini-app-url.com'
    
    keyboard = []
    buttons = get_buttons('after_video')
    
    if not buttons:
        keyboard.append([InlineKeyboardButton(
            "🎬 আরও ভিডিও দেখুন | Watch More Videos",
            web_app=WebAppInfo(url=mini_app_url)
        )])
    else:
        for btn in buttons:
            if btn['type'] == 'web_app':
                keyboard.append([InlineKeyboardButton(btn['text'], web_app=WebAppInfo(url=btn['url']))])
            else:
                keyboard.append([InlineKeyboardButton(btn['text'], url=btn['url'])])
    
    return InlineKeyboardMarkup(keyboard)

def admin_main_keyboard():
    """Build admin main keyboard"""
    keyboard = [
        [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats")],
        [InlineKeyboardButton("📺 Force Join Channels", callback_data="admin_channels")],
        [InlineKeyboardButton("✏️ Edit Messages", callback_data="admin_messages")],
        [InlineKeyboardButton("🔘 Manage Buttons", callback_data="admin_buttons")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="admin_settings")],
        [InlineKeyboardButton("📢 Broadcast Message", callback_data="admin_broadcast")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===================== COMMAND HANDLERS =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    # Add user to database
    add_user(user.id, user.username, user.first_name)
    
    # Check for video_id in deep link
    if context.args and context.args[0].startswith('v_'):
        video_id = context.args[0][2:]
        await handle_video_request(update, context, video_id)
        return
    
    # Send welcome message
    welcome_text = get_message('welcome').format(name=user.first_name)
    
    try:
        await update.message.reply_text(
            welcome_text,
            reply_markup=build_welcome_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Error sending welcome message: {e}")
        await update.message.reply_text("👋 Welcome! Use the buttons below to get started.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        get_message('help'),
        parse_mode=ParseMode.MARKDOWN
    )

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    stats = get_stats()
    text = f"""🔧 **CINEFLIX ADMIN PANEL**

📊 **Statistics:**
👥 Total Users: {stats['users']}
🔥 Active Today: {stats['active_today']}
📹 Videos: {stats['videos']}
👁️ Top Views: {stats['top_views']}
🔒 Force Join: {stats['force_join']}

Select an option below:"""
    
    await update.message.reply_text(
        text,
        reply_markup=admin_main_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

# ===================== VIDEO HANDLER =====================
async def handle_video_request(update: Update, context: ContextTypes.DEFAULT_TYPE, video_id: str):
    """Handle video request from Mini App"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Get video from database
    video = get_video(video_id)
    
    if not video:
        await update.message.reply_text(
            get_message('video_not_found'),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check force join channels
    not_joined = await check_all_channels(context.bot, user_id)
    
    if not_joined:
        force_join_text = get_message('force_join')
        keyboard = build_force_join_keyboard(not_joined)
        
        # Store video_id in user context
        context.user_data['pending_video_id'] = video_id
        
        try:
            await update.message.reply_text(
                force_join_text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            logger.error(f"Error sending force join message: {e}")
            await update.message.reply_text("Please join our channels to watch this video.")
        return
    
    # Send video
    await send_video_to_user(update, context, video)

async def send_video_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE, video: dict):
    """Send video to user"""
    user_id = update.effective_user.id
    video_id = video['video_id']
    
    # Increment view count
    increment_video_views(video_id)
    
    # Send video file
    try:
        file_id = video.get('file_id')
        caption = video.get('caption', '')
        
        if file_id:
            sent_message = await context.bot.send_video(
                chat_id=user_id,
                video=file_id,
                caption=caption,
                parse_mode=ParseMode.MARKDOWN,
                protect_content=get_setting('video_protection')
            )
            
            # Track message for cleanup
            if user_id not in user_video_messages:
                user_video_messages[user_id] = {}
            if video_id not in user_video_messages[user_id]:
                user_video_messages[user_id][video_id] = []
            user_video_messages[user_id][video_id].append(sent_message.message_id)
            
            # Send after video message
            after_text = get_message('after_video')
            await context.bot.send_message(
                chat_id=user_id,
                text=after_text,
                reply_markup=build_after_video_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
            
            logger.info(f"✅ Video {video_id} sent to user {user_id}")
        else:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Video file not available. Please contact admin."
            )
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Failed to send video. Please try again later."
        )

# ===================== CALLBACK HANDLERS =====================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    data = query.data
    
    # Verify join callback
    if data == "verify_join":
        pending_video_id = context.user_data.get('pending_video_id')
        
        if not pending_video_id:
            await query.message.edit_text("❌ No pending video request found. Please try again from Mini App.")
            return
        
        # Check if user joined all channels
        not_joined = await check_all_channels(context.bot, user_id)
        
        if not_joined:
            await query.answer("❌ আপনি এখনও সব চ্যানেলে জয়েন করেননি! | You haven't joined all channels yet!", show_alert=True)
            return
        
        # User joined all channels, send video
        video = get_video(pending_video_id)
        if video:
            await query.message.delete()
            
            # Create a temporary update object for sending video
            await send_video_to_user(update, context, video)
            
            # Clear pending video
            context.user_data.pop('pending_video_id', None)
        else:
            await query.message.edit_text(get_message('video_not_found'), parse_mode=ParseMode.MARKDOWN)
        return
    
    # Admin callbacks (only for admin)
    if user_id != ADMIN_ID:
        await query.answer("❌ You are not authorized!", show_alert=True)
        return
    
    await handle_admin_callback(update, context, data)

async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    """Handle admin panel callbacks"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    # Main menu
    if data == "admin_main":
        stats = get_stats()
        text = f"""🔧 **CINEFLIX ADMIN PANEL**

📊 **Statistics:**
👥 Total Users: {stats['users']}
🔥 Active Today: {stats['active_today']}
📹 Videos: {stats['videos']}
👁️ Top Views: {stats['top_views']}
🔒 Force Join: {stats['force_join']}

Select an option below:"""
        
        await query.message.edit_text(
            text,
            reply_markup=admin_main_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Statistics
    elif data == "admin_stats":
        stats = get_stats()
        text = f"""📊 **Detailed Statistics**

👥 **Users:**
• Total: {stats['users']}
• Active Today: {stats['active_today']}

📹 **Videos:**
• Total: {stats['videos']}
• Top Views: {stats['top_views']}

🔒 **Force Join:**
• Channels: {stats['force_join']}"""
        
        keyboard = [[InlineKeyboardButton("« Back", callback_data="admin_main")]]
        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Force Join Channels Management
    elif data == "admin_channels":
        channels = get_force_join_channels()
        
        text = "📺 **Force Join Channels**\n\n"
        keyboard = []
        
        if channels:
            for channel in channels:
                channel_id = channel['channel_id']
                channel_name = channel.get('channel_name', 'Unknown')
                text += f"• {channel_name} (`{channel_id}`)\n"
                keyboard.append([
                    InlineKeyboardButton(f"❌ {channel_name}", callback_data=f"del_channel_{channel_id}")
                ])
        else:
            text += "No force join channels added yet."
        
        keyboard.append([InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")])
        keyboard.append([InlineKeyboardButton("« Back", callback_data="admin_main")])
        
        await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Add channel
    elif data == "add_channel":
        admin_states[user_id] = {'action': 'add_channel'}
        await query.message.edit_text(
            "📝 **Add Force Join Channel**\n\n"
            "Send channel info in this format:\n"
            "`Channel ID | Channel Name | Channel Link`\n\n"
            "Example:\n"
            "`-1001234567890 | My Channel | https://t.me/mychannel`\n\n"
            "Or just send Channel ID for auto-detection.",
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Delete channel
    elif data.startswith("del_channel_"):
        channel_id = int(data.replace("del_channel_", ""))
        if delete_force_join_channel(channel_id):
            await query.answer("✅ Channel deleted!", show_alert=True)
            # Refresh channels list
            await handle_admin_callback(update, context, "admin_channels")
        else:
            await query.answer("❌ Failed to delete channel", show_alert=True)
    
    # Messages Management
    elif data == "admin_messages":
        text = "✏️ **Edit Messages**\n\nSelect message to edit:"
        keyboard = [
            [InlineKeyboardButton("👋 Welcome Message", callback_data="edit_msg_welcome")],
            [InlineKeyboardButton("📚 Help Message", callback_data="edit_msg_help")],
            [InlineKeyboardButton("🔒 Force Join Message", callback_data="edit_msg_force_join")],
            [InlineKeyboardButton("🎬 After Video Message", callback_data="edit_msg_after_video")],
            [InlineKeyboardButton("❌ Video Not Found", callback_data="edit_msg_video_not_found")],
            [InlineKeyboardButton("« Back", callback_data="admin_main")]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    
    # Edit message
    elif data.startswith("edit_msg_"):
        msg_key = data.replace("edit_msg_", "")
        admin_states[user_id] = {'action': 'edit_message', 'key': msg_key}
        
        current_text = get_message(msg_key)
        await query.message.edit_text(
            f"📝 **Edit {msg_key.replace('_', ' ').title()}**\n\n"
            f"Current message:\n\n{current_text}\n\n"
            f"Send new message text:",
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Buttons Management
    elif data == "admin_buttons":
        text = "🔘 **Manage Buttons**\n\nSelect location:"
        keyboard = [
            [InlineKeyboardButton("👋 Welcome Buttons", callback_data="buttons_welcome")],
            [InlineKeyboardButton("🎬 After Video Buttons", callback_data="buttons_after_video")],
            [InlineKeyboardButton("« Back", callback_data="admin_main")]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    
    # View/manage buttons for location
    elif data.startswith("buttons_"):
        location = data.replace("buttons_", "")
        buttons = get_buttons(location)
        
        location_name = "Welcome Message" if location == "welcome" else "After Video Message"
        text = f"🔘 **{location_name} Buttons**\n\n"
        
        keyboard = []
        if buttons:
            for btn in buttons:
                btn_id = str(btn['_id'])
                text += f"• {btn['text']} ({btn['type']})\n"
                keyboard.append([
                    InlineKeyboardButton(f"❌ {btn['text']}", callback_data=f"del_btn_{btn_id}")
                ])
        else:
            text += "No buttons added yet."
        
        keyboard.append([InlineKeyboardButton("➕ Add Button", callback_data=f"add_btn_{location}")])
        keyboard.append([InlineKeyboardButton("« Back", callback_data="admin_buttons")])
        
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    
    # Add button
    elif data.startswith("add_btn_"):
        location = data.replace("add_btn_", "")
        admin_states[user_id] = {'action': 'add_button', 'location': location}
        
        await query.message.edit_text(
            f"📝 **Add Button**\n\n"
            f"Send button info in this format:\n"
            f"`Text | URL | Type`\n\n"
            f"Example:\n"
            f"`📢 Join Channel | https://t.me/mychannel | url`\n"
            f"`🎮 Open App | https://app.com | webapp`\n\n"
            f"Types: `url` or `webapp`",
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Delete button
    elif data.startswith("del_btn_"):
        btn_id = data.replace("del_btn_", "")
        if delete_button(btn_id):
            await query.answer("✅ Button deleted!", show_alert=True)
            # Go back to buttons menu
            await handle_admin_callback(update, context, "admin_buttons")
        else:
            await query.answer("❌ Failed to delete button", show_alert=True)
    
    # Settings
    elif data == "admin_settings":
        text = "⚙️ **Settings**\n\nSelect setting to edit:"
        keyboard = [
            [InlineKeyboardButton("🌐 Mini App URL", callback_data="set_mini_app_url")],
            [InlineKeyboardButton("📢 Main Channel ID", callback_data="set_main_channel_id")],
            [InlineKeyboardButton("🔒 Video Protection", callback_data="set_video_protection")],
            [InlineKeyboardButton("🗑️ Auto Delete", callback_data="set_auto_delete")],
            [InlineKeyboardButton("« Back", callback_data="admin_main")]
        ]
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    
    # Edit setting
    elif data.startswith("set_"):
        setting_key = data.replace("set_", "")
        admin_states[user_id] = {'action': 'edit_setting', 'key': setting_key}
        
        current_value = get_setting(setting_key)
        await query.message.edit_text(
            f"📝 **Edit {setting_key.replace('_', ' ').title()}**\n\n"
            f"Current value: `{current_value}`\n\n"
            f"Send new value:",
            parse_mode=ParseMode.MARKDOWN
        )
    
    # Broadcast
    elif data == "admin_broadcast":
        admin_states[user_id] = {'action': 'broadcast'}
        await query.message.edit_text(
            "📢 **Broadcast Message**\n\n"
            "Send the message you want to broadcast to all users.\n"
            "You can send text, photo, or video.\n\n"
            "⚠️ This will be sent to ALL users!"
        )

# ===================== ADMIN MESSAGE HANDLER =====================
async def admin_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin text/media messages"""
    user_id = update.effective_user.id
    
    # Check if user is in admin state
    if user_id not in admin_states:
        # Auto-reply for non-admin messages
        if user_id != ADMIN_ID:
            await update.message.reply_text(
                get_message('auto_reply'),
                parse_mode=ParseMode.MARKDOWN
            )
        return
    
    state = admin_states[user_id]
    action = state['action']
    
    # Handle broadcast
    if action == 'broadcast':
        await handle_broadcast(update, context)
        return
    
    # Handle text-based actions
    if not update.message.text:
        await update.message.reply_text("❌ Please send text message for this action")
        return
    
    text = update.message.text.strip()
    
    # Add channel
    if action == 'add_channel':
        parts = text.split('|')
        
        if len(parts) == 3:
            try:
                channel_id = int(parts[0].strip())
                channel_name = parts[1].strip()
                channel_link = parts[2].strip()
            except ValueError:
                await update.message.reply_text("❌ Invalid format! Channel ID must be a number.")
                return
        elif len(parts) == 1:
            try:
                channel_id = int(parts[0].strip())
                channel_name = f"Channel {channel_id}"
                channel_link = None
            except ValueError:
                await update.message.reply_text("❌ Channel ID must be a number")
                return
        else:
            await update.message.reply_text(
                "❌ Invalid format!\n\n"
                "Send: `Channel ID | Channel Name | Channel Link`\n"
                "Or just: `Channel ID`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if add_force_join_channel(channel_id, channel_name, channel_link):
            await update.message.reply_text(
                f"✅ **Channel Added!**\n\n"
                f"**Name:** {channel_name}\n"
                f"**ID:** `{channel_id}`",
                parse_mode=ParseMode.MARKDOWN
            )
            del admin_states[user_id]
        else:
            await update.message.reply_text("❌ Failed to add channel")
    
    # Add button
    elif action == 'add_button':
        parts = text.split('|')
        if len(parts) != 3:
            await update.message.reply_text(
                "❌ Invalid format!\n\n"
                "Use: `Text | URL | Type`\n\n"
                "Example: `📢 Join Channel | https://t.me/MyChannel | url`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        btn_text = parts[0].strip()
        btn_url = parts[1].strip()
        btn_type = parts[2].strip().lower()
        
        if btn_type not in ['url', 'webapp']:
            await update.message.reply_text("❌ Type must be 'url' or 'webapp'")
            return
        
        if not btn_url.startswith('http'):
            await update.message.reply_text("❌ URL must start with http:// or https://")
            return
        
        if btn_type == 'webapp':
            btn_type = 'web_app'
        
        location = state['location']
        existing_count = len(get_buttons(location))
        
        if add_button(location, btn_text, btn_url, btn_type, order=existing_count):
            location_name = "Welcome Message" if location == "welcome" else "After Video Message"
            await update.message.reply_text(
                f"✅ **Button Added to {location_name}!**\n\n"
                f"Text: {btn_text}\n"
                f"URL: {btn_url}\n"
                f"Type: {btn_type}",
                parse_mode=ParseMode.MARKDOWN
            )
            del admin_states[user_id]
        else:
            await update.message.reply_text("❌ Failed to add button")
    
    # Edit message
    elif action == 'edit_message':
        msg_key = state['key']
        if set_message(msg_key, text):
            await update.message.reply_text("✅ Message updated!")
            del admin_states[user_id]
        else:
            await update.message.reply_text("❌ Failed to update message")
    
    # Edit setting
    elif action == 'edit_setting':
        setting_key = state['key']
        
        # Type conversion
        if setting_key in ['main_channel_id']:
            try:
                text = int(text)
            except ValueError:
                await update.message.reply_text("❌ Must be a number")
                return
        elif setting_key == 'video_protection':
            text = text.lower() in ['true', 'yes', '1', 'on']
        elif setting_key == 'auto_delete_enabled':
            text = text.lower() in ['true', 'yes', '1', 'on']
        elif setting_key == 'auto_delete_delay':
            try:
                text = int(text)
            except ValueError:
                await update.message.reply_text("❌ Delay must be a number (seconds)")
                return
        
        if set_setting(setting_key, text):
            await update.message.reply_text(
                f"✅ **{setting_key.replace('_', ' ').title()} Updated!**\n\n"
                f"New value: `{text}`",
                parse_mode=ParseMode.MARKDOWN
            )
            del admin_states[user_id]
        else:
            await update.message.reply_text("❌ Failed to update setting")

# ===================== BROADCAST HANDLER =====================
async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle broadcast to all users"""
    user_id = update.effective_user.id
    
    all_users = get_all_users()
    
    if not all_users:
        await update.message.reply_text("❌ No users to broadcast to!")
        del admin_states[user_id]
        return
    
    await update.message.reply_text(
        f"📢 **Broadcasting to {len(all_users)} users...**\n\n"
        f"Please wait...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    success_count = 0
    fail_count = 0
    
    for target_user_id in all_users:
        try:
            if update.message.photo:
                await context.bot.send_photo(
                    chat_id=target_user_id,
                    photo=update.message.photo[-1].file_id,
                    caption=update.message.caption,
                    parse_mode=ParseMode.MARKDOWN if update.message.caption else None
                )
            elif update.message.video:
                await context.bot.send_video(
                    chat_id=target_user_id,
                    video=update.message.video.file_id,
                    caption=update.message.caption,
                    parse_mode=ParseMode.MARKDOWN if update.message.caption else None
                )
            else:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=update.message.text,
                    parse_mode=ParseMode.MARKDOWN
                )
            
            success_count += 1
            
        except Exception as e:
            fail_count += 1
            logger.error(f"Failed to send broadcast to user {target_user_id}: {e}")
    
    await update.message.reply_text(
        f"✅ **Broadcast Complete!**\n\n"
        f"✅ Sent: {success_count}\n"
        f"❌ Failed: {fail_count}\n"
        f"📊 Total: {len(all_users)}",
        parse_mode=ParseMode.MARKDOWN
    )
    
    del admin_states[user_id]

# ===================== CHANNEL POST HANDLER =====================
async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle channel posts to auto-add videos"""
    if not update.channel_post:
        return
    
    channel_id = update.channel_post.chat.id
    
    # Check if this is the main channel
    main_channel_id = get_setting('main_channel_id')
    
    if not main_channel_id or channel_id != main_channel_id:
        return
    
    # Check if post has video
    if not update.channel_post.video:
        return
    
    video = update.channel_post.video
    file_id = video.file_id
    caption = update.channel_post.caption or ''
    
    # Generate video_id from message_id
    video_id = f"v{update.channel_post.message_id}"
    
    # Save to database
    try:
        videos_col.update_one(
            {'video_id': video_id},
            {
                '$set': {
                    'file_id': file_id,
                    'caption': caption,
                    'channel_id': channel_id,
                    'message_id': update.channel_post.message_id,
                    'added_at': datetime.now()
                },
                '$setOnInsert': {
                    'views': 0
                }
            },
            upsert=True
        )
        logger.info(f"✅ Auto-added video: {video_id}")
    except Exception as e:
        logger.error(f"Failed to auto-add video: {e}")

# ===================== JOIN REQUEST HANDLER =====================
async def handle_chat_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle join requests to private channels"""
    if not update.chat_join_request:
        return
    
    user_id = update.chat_join_request.from_user.id
    channel_id = update.chat_join_request.chat.id
    
    # Track the request
    add_pending_request(user_id, channel_id)
    
    logger.info(f"✅ Join request tracked: User {user_id} -> Channel {channel_id}")

# ===================== ERROR HANDLER =====================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

# ===================== MAIN FUNCTION =====================
def main():
    """Start the bot"""
    logger.info("🚀 Starting CINEFLIX Ultimate Bot...")
    
    # Initialize defaults
    initialize_defaults()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(ChatJoinRequestHandler(handle_chat_join_request))
    
    # Admin message handlers
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        admin_message_handler
    ))
    application.add_handler(MessageHandler(
        (filters.PHOTO | filters.VIDEO) & filters.User(ADMIN_ID),
        admin_message_handler
    ))
    
    # Channel post handler
    application.add_handler(MessageHandler(
        filters.ChatType.CHANNEL,
        channel_post
    ))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    logger.info("✅ CINEFLIX Ultimate Bot is running!")
    logger.info(f"👑 Admin: {ADMIN_ID}")
    logger.info(f"💾 MongoDB: Connected")
    logger.info(f"🎬 Ready to serve!")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
