#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 CINEFLIX ULTIMATE BOT
Premium Video Bot with Full Admin Panel + Enhanced Features
"""

import os
import sys
import logging
from datetime import datetime, timedelta
import asyncio  # For smooth UX delays
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ConversationHandler,
    ChatJoinRequestHandler
)
from telegram.constants import ParseMode
from telegram.error import BadRequest, TelegramError
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# ===================== CONFIGURATION =====================
# All sensitive data from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_ID = os.getenv("ADMIN_ID")

# Validate required environment variables
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
    pending_requests_col = db['pending_join_requests']  # NEW: Track join requests
    
    logger.info("✅ MongoDB Connected Successfully!")
    
except (ConnectionFailure, OperationFailure) as e:
    logger.error(f"❌ MongoDB Connection Failed: {e}")
    logger.error("Bot cannot run without database. Please check MONGO_URI.")
    sys.exit(1)

# ===================== CONVERSATION STATES =====================
EDITING_MESSAGE = 1
ADDING_CHANNEL = 2
EDITING_SETTING = 3
BROADCASTING = 4

# Admin state tracking
admin_states = {}

# Track user's last video request messages (to delete duplicates)
user_video_messages = {}  # Format: {user_id: {video_id: [message_ids]}}

# NEW: Track user's ALL messages for cleanup (not just video-specific)
user_all_messages = {}  # Format: {user_id: [message_ids]}

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
📚 **CINEFLIX Bot - সাহায্য গাইড**

**🎯 Commands / কমান্ড:**
/start - বোট শুরু করুন | Start bot
/help - সাহায্য দেখুন | Show help

**🎬 কীভাবে ভিডিও দেখবেন?**
**🎬 How to watch videos?**

**Step 1:** /start দিয়ে Mini App খুলুন
**Step 2:** পছন্দের ভিডিও সিলেক্ট করুন
**Step 3:** চ্যানেল জয়েন করুন (যদি বলা হয়)
**Step 4:** ভিডিও উপভোগ করুন! 🍿

**⚠️ সমস্যা? Having issues?**
- ভিডিও না দেখা গেলে চ্যানেল জয়েন করুন
- লিঙ্ক কাজ না করলে Mini App রিফ্রেশ করুন
- অন্য সমস্যায় Admin কে মেসেজ করুন""",

    'force_join': """🔒 **ভিডিও দেখতে চ্যানেল জয়েন করুন!**
🔒 **Join Channel to Watch Video!**

━━━━━━━━━━━━━━━━━━━━

**📱 কীভাবে দেখবেন? (How to Watch?)**

**ধাপ ১:** নিচের চ্যানেল বাটনে ক্লিক করুন
**Step 1:** Click the channel button(s) below

**ধাপ ২:** পাবলিক চ্যানেলে "Join" অথবা প্রাইভেট চ্যানেলে "Request to Join" ক্লিক করুন
**Step 2:** Click "Join" (public) or "Request to Join" (private)

**ধাপ ৩:** বট এ ফিরে এসে "✅ আমি জয়েন করেছি" বাটন ক্লিক করুন
**Step 3:** Return here and click "✅ I Joined" button

━━━━━━━━━━━━━━━━━━━━

**💡 মনে রাখবেন (Remember):**

✅ **পাবলিক চ্যানেল:** Join করার পর verify button click করুন
✅ **Public Channel:** Click verify after joining

✅ **প্রাইভেট চ্যানেল:** শুধু request পাঠান, approve এর দরকার নেই!
✅ **Private Channel:** Just send request, no need to wait for approval!

🎬 **ভিডিও পেতে verify button অবশ্যই click করুন!**
🎬 **Must click verify button to unlock video!**

━━━━━━━━━━━━━━━━━━━━""",

    'after_video': """🎬 **ভিডিও উপভোগ করুন! Enjoy the Video!**

━━━━━━━━━━━━━━━━━━━━

**🌟 আরও ভিডিও দেখতে চান?**
**🌟 Want to watch more videos?**

নিচের বাটনে ক্লিক করে আমাদের Mini App এ যান এবং হাজারো ভিডিও দেখুন!
Click the button below to access our Mini App with thousands of videos!

**📺 প্রতিদিন নতুন কন্টেন্ট!**
**📺 New content daily!**

━━━━━━━━━━━━━━━━━━━━

**💝 ধন্যবাদ! Thank you!**

Stay connected with us! 🎉
আমাদের সাথে থাকুন! 🎉""",

    'video_not_found': """❌ **দুঃখিত! Video Not Found!**

এই ভিডিওটি আর পাওয়া যাচ্ছে না বা লিঙ্ক ভুল।
This video is no longer available or the link is incorrect.

**কী করবেন? What to do?**

✅ Mini App এ ফিরে অন্য ভিডিও দেখুন
✅ Go back to Mini App and watch other videos

✅ আমাদের চ্যানেলে জয়েন থাকুন — প্রতিদিন নতুন কন্টেন্ট!
✅ Stay joined to our channel — new content daily!""",

    'auto_reply': """👋 **Hello!**

আমি একটি Video Bot! 
I'm a Video Bot!

🎬 Videos দেখতে নিচের button এ ক্লিক করুন:
🎬 Click the button below to watch videos:

👇 Use /start to access the Mini App""",

    # 🔥 ULTIMATE PREMIUM MESSAGES (Auto-update force join)
    'force_join_start': """🔐 **Unlock Your Video**

Hey **{name}**! 👋

**Join {count} channel{plural} to unlock:**

{channels_list}

💡 Tap channels → Send requests → Auto-unlock!""",

    'force_join_progress': """✅ **{joined_name} Joined!**

Great! 🎉 **{remaining} more to go!**

{channels_list}""",

    'force_join_almost': """✅ **{joined_name} Joined!**

Almost there! 💪 **Just 1 more!**

{channels_list}""",

    'force_join_complete': """🎉 **All Channels Joined!**

Perfect! Unlocking your video...""",

    'video_unlocked': """🎬 **{video_title}**

Enjoy! 🍿"""
}

DEFAULT_SETTINGS = {
    'mini_app_url': 'https://cinaflix-streaming.vercel.app/',
    'main_channel_id': -1003872857468,
    'main_channel_username': 'Cinaflixsteem',
    'video_protection': True,
    'bot_name': 'CINEFLIX',
    'auto_reply_enabled': True,
    'message_cleanup_enabled': True,
    'welcome_media_enabled': False,  # NEW: Welcome GIF/Video
    'welcome_media_file_id': None,   # NEW: Telegram file_id
    'welcome_media_type': None,      # NEW: 'photo', 'animation', 'video'
    'folder_link_enabled': False,    # NEW: Enable folder join link
    'folder_link_url': ''            # NEW: Telegram folder link (https://t.me/addlist/xxxxx)
}

# ===================== DATABASE HELPER FUNCTIONS =====================

def get_setting(key, default=None):
    """Get setting from database"""
    try:
        setting = settings_col.find_one({'key': key})
        return setting['value'] if setting else default
    except Exception as e:
        logger.error(f"Error getting setting {key}: {e}")
        return default

def set_setting(key, value):
    """Set setting in database"""
    try:
        settings_col.update_one(
            {'key': key},
            {'$set': {'key': key, 'value': value, 'updated_at': datetime.utcnow()}},
            upsert=True
        )
        return True
    except Exception as e:
        logger.error(f"Error setting {key}: {e}")
        return False

def get_message(key):
    """Get message template from database"""
    try:
        msg = messages_col.find_one({'key': key})
        return msg['text'] if msg else DEFAULT_MESSAGES.get(key, '')
    except Exception as e:
        logger.error(f"Error getting message {key}: {e}")
        return DEFAULT_MESSAGES.get(key, '')

def set_message(key, text):
    """Set message template in database"""
    try:
        messages_col.update_one(
            {'key': key},
            {'$set': {'key': key, 'text': text, 'updated_at': datetime.utcnow()}},
            upsert=True
        )
        return True
    except Exception as e:
        logger.error(f"Error setting message {key}: {e}")
        return False

def initialize_defaults():
    """Initialize default settings and messages if not exists"""
    try:
        # Initialize settings
        for key, value in DEFAULT_SETTINGS.items():
            if not settings_col.find_one({'key': key}):
                set_setting(key, value)
        
        # Initialize messages
        for key, text in DEFAULT_MESSAGES.items():
            if not messages_col.find_one({'key': key}):
                set_message(key, text)
        
        logger.info("✅ Default settings and messages initialized")
    except Exception as e:
        logger.error(f"Error initializing defaults: {e}")

def save_video(channel_id, message_id, channel_name="Main", media_type="video"):
    """Save video/photo/animation to database"""
    try:
        video_data = {
            'channel_id': channel_id,
            'message_id': message_id,
            'channel_name': channel_name,
            'media_type': media_type,  # NEW: 'video', 'photo', 'animation', 'document'
            'saved_at': datetime.utcnow(),
            'views': 0
        }
        videos_col.update_one(
            {'channel_id': channel_id, 'message_id': message_id},
            {'$set': video_data},
            upsert=True
        )
        logger.info(f"✅ {media_type.title()} saved: {channel_name} - {message_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving {media_type}: {e}")
        return False

def get_video(message_id):
    """Get video from database"""
    try:
        return videos_col.find_one({'message_id': int(message_id)})
    except Exception as e:
        logger.error(f"Error getting video: {e}")
        return None

def increment_video_view(message_id):
    """Increment video view count"""
    try:
        videos_col.update_one(
            {'message_id': int(message_id)},
            {'$inc': {'views': 1}}
        )
    except Exception as e:
        logger.error(f"Error incrementing view: {e}")

def add_force_join_channel(channel_id, username, invite_link=None):
    """Add force join channel with optional invite link for private channels"""
    try:
        channel_data = {
            'channel_id': channel_id,
            'username': username.replace('@', ''),
            'invite_link': invite_link,  # NEW: Support private channel invite links
            'added_at': datetime.utcnow(),
            'is_active': True
        }
        force_join_col.update_one(
            {'channel_id': channel_id},
            {'$set': channel_data},
            upsert=True
        )
        
        link_info = f" (invite: {invite_link})" if invite_link else ""
        logger.info(f"✅ Force join channel added: @{username}{link_info}")
        return True
    except Exception as e:
        logger.error(f"Error adding force join channel: {e}")
        return False

def remove_force_join_channel(channel_id):
    """Remove force join channel"""
    try:
        result = force_join_col.delete_one({'channel_id': channel_id})
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Error removing force join channel: {e}")
        return False

def get_force_join_channels():
    """Get all active force join channels"""
    try:
        return list(force_join_col.find({'is_active': True}))
    except Exception as e:
        logger.error(f"Error getting force join channels: {e}")
        return []

def save_user(user_id, username, first_name):
    """Save user to database"""
    try:
        user_data = {
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'last_active': datetime.utcnow()
        }
        users_col.update_one(
            {'user_id': user_id},
            {'$set': user_data, '$setOnInsert': {'first_seen': datetime.utcnow()}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Error saving user: {e}")

def get_stats():
    """Get bot statistics"""
    try:
        # Basic stats
        total_users = users_col.count_documents({})
        total_videos = videos_col.count_documents({})
        total_force_join = force_join_col.count_documents({'is_active': True})
        
        # Active users (last 24 hours)
        yesterday = datetime.utcnow() - timedelta(days=1)
        active_today = users_col.count_documents({
            'last_active': {'$gte': yesterday}
        })
        
        # Most viewed video
        top_video = videos_col.find_one(sort=[('views', -1)])
        top_views = top_video['views'] if top_video else 0
        
        return {
            'users': total_users,
            'videos': total_videos,
            'force_join': total_force_join,
            'active_today': active_today,
            'top_views': top_views
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {
            'users': 0,
            'videos': 0,
            'force_join': 0,
            'active_today': 0,
            'top_views': 0
        }

def get_all_users():
    """Get all user IDs for broadcasting"""
    try:
        users = users_col.find({}, {'user_id': 1})
        return [user['user_id'] for user in users]
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return []

def get_buttons(location):
    """Get buttons for a specific location (welcome or after_video)"""
    try:
        buttons = list(buttons_col.find({'location': location, 'is_active': True}).sort('order', 1))
        return buttons
    except Exception as e:
        logger.error(f"Error getting buttons for {location}: {e}")
        return []

def add_button(location, text, url, button_type='url', order=0):
    """Add a custom button"""
    try:
        button_data = {
            'location': location,  # 'welcome' or 'after_video'
            'text': text,
            'url': url,
            'type': button_type,  # 'url' or 'web_app'
            'order': order,
            'is_active': True,
            'created_at': datetime.utcnow()
        }
        result = buttons_col.insert_one(button_data)
        logger.info(f"✅ Button added: {text} at {location}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error adding button: {e}")
        return None

def remove_button(button_id):
    """Remove a button"""
    try:
        from bson.objectid import ObjectId
        result = buttons_col.delete_one({'_id': ObjectId(button_id)})
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Error removing button: {e}")
        return False

# ===================== PENDING JOIN REQUEST HELPERS =====================
def mark_join_request_sent(user_id, channel_id):
    """Mark that user has sent a join request to a channel"""
    try:
        pending_requests_col.update_one(
            {'user_id': user_id, 'channel_id': channel_id},
            {
                '$set': {
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'requested_at': datetime.now(),  # Fixed: was request_sent_at
                    'status': 'pending'
                }
            },
            upsert=True
        )
        logger.info(f"✅ Marked join request: user {user_id} -> channel {channel_id}")
        return True
    except Exception as e:
        logger.error(f"Error marking join request: {e}")
        return False

def has_pending_join_request(user_id, channel_id):
    """Check if user has a pending join request to a channel"""
    try:
        request = pending_requests_col.find_one({
            'user_id': user_id,
            'channel_id': channel_id,
            'status': 'pending'
        })
        return request is not None
    except Exception as e:
        logger.error(f"Error checking pending request: {e}")
        return False

# 🔥 ULTIMATE PREMIUM HELPERS
def format_channels_list(channels, index_start=1):
    """Format channels as numbered list"""
    lines = []
    for i, channel in enumerate(channels, index_start):
        name = channel.get('name', 'Channel')
        lines.append(f"{i}. 🔒 **{name}**")
    return "\n".join(lines)

async def get_user_pending_channels(user_id):
    """Get list of channels user has already sent requests to (within 24h)"""
    try:
        cutoff = datetime.now() - timedelta(hours=24)
        requests = list(pending_requests_col.find({
            'user_id': user_id,
            'requested_at': {'$gte': cutoff}
        }))
        return [req['channel_id'] for req in requests]
    except Exception as e:
        logger.error(f"Error getting pending channels: {e}")
        return []

async def get_not_joined_channels(user_id):
    """Get channels user hasn't joined yet"""
    all_channels = get_force_join_channels()
    pending_channel_ids = await get_user_pending_channels(user_id)
    
    # Filter out already joined
    not_joined = [ch for ch in all_channels if ch['channel_id'] not in pending_channel_ids]
    return not_joined

def create_channel_buttons(channels):
    """Create inline keyboard buttons for channels"""
    buttons = []
    for channel in channels:
        name = channel.get('name', 'Channel')
        # Use invite_link OR username
        invite_link = channel.get('invite_link')
        username = channel.get('username', '')
        
        if invite_link:
            url = invite_link
        elif username:
            url = f"https://t.me/{username}"
        else:
            continue  # Skip if no way to join
        
        buttons.append([InlineKeyboardButton(f"🔒 {name}", url=url)])
    
    return InlineKeyboardMarkup(buttons) if buttons else None

# ===================== EXISTING HELPERS CONTINUE =====================

def clear_join_request(user_id, channel_id):
    """Clear join request after user is approved"""
    try:
        pending_requests_col.update_one(
            {'user_id': user_id, 'channel_id': channel_id},
            {'$set': {'status': 'approved'}}
        )
        return True
    except Exception as e:
        logger.error(f"Error clearing join request: {e}")
        return False

def remove_button_old(button_id):
    """Remove a button"""
    try:
        from bson.objectid import ObjectId
        result = buttons_col.delete_one({'_id': ObjectId(button_id)})
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Error removing button: {e}")
        return False

def update_button(button_id, text=None, url=None):
    """Update button text or URL"""
    try:
        from bson.objectid import ObjectId
        update_data = {}
        if text:
            update_data['text'] = text
        if url:
            update_data['url'] = url
        
        if update_data:
            result = buttons_col.update_one(
                {'_id': ObjectId(button_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        return False
    except Exception as e:
        logger.error(f"Error updating button: {e}")
        return False

# ===================== ADVANCED AUTO CLEANUP SYSTEM =====================
async def cleanup_user_messages(context: ContextTypes.DEFAULT_TYPE, user_id: int, chat_id: int, keep_last: int = 0):
    """
    🔥 ADVANCED: Clean up all previous bot messages for ultra-clean chat
    keep_last: Number of recent messages to keep (0 = delete all)
    """
    cleanup_enabled = get_setting('message_cleanup_enabled', True)
    
    if not cleanup_enabled:
        return
    
    if user_id in user_all_messages:
        messages_to_delete = user_all_messages[user_id]
        
        # If keep_last > 0, only delete older messages
        if keep_last > 0 and len(messages_to_delete) > keep_last:
            messages_to_delete = messages_to_delete[:-keep_last]
        
        deleted_count = 0
        for msg_id in messages_to_delete:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
                deleted_count += 1
            except Exception as e:
                logger.debug(f"Could not delete message {msg_id}: {e}")
        
        if deleted_count > 0:
            logger.info(f"🧹 Cleaned up {deleted_count} messages for user {user_id}")
        
        # Keep only last N messages if specified
        if keep_last > 0:
            user_all_messages[user_id] = user_all_messages[user_id][-keep_last:]
        else:
            user_all_messages[user_id] = []

async def track_message(user_id: int, message_id: int):
    """Track a message for future cleanup"""
    if user_id not in user_all_messages:
        user_all_messages[user_id] = []
    user_all_messages[user_id].append(message_id)
    
    # Auto-limit: Keep max 50 messages tracked (prevent memory bloat)
    if len(user_all_messages[user_id]) > 50:
        user_all_messages[user_id] = user_all_messages[user_id][-50:]

# ===================== ADMIN PANEL KEYBOARDS =====================

def admin_main_keyboard():
    """Main admin panel keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("📺 Channel Manager", callback_data="admin_channels"),
            InlineKeyboardButton("📝 Edit Messages", callback_data="admin_messages")
        ],
        [
            InlineKeyboardButton("🔘 Button Manager", callback_data="admin_buttons"),
            InlineKeyboardButton("⚙️ Settings", callback_data="admin_settings")
        ],
        [
            InlineKeyboardButton("📊 Statistics", callback_data="admin_stats"),
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
        ],
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="admin_refresh"),
            InlineKeyboardButton("❌ Close", callback_data="admin_close")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def channel_manager_keyboard():
    """Channel manager keyboard"""
    channels = get_force_join_channels()
    keyboard = []
    
    for ch in channels:
        # Add 🔒 icon for private channels (those with invite link)
        channel_icon = "🔒" if ch.get('invite_link') else "📢"
        keyboard.append([
            InlineKeyboardButton(
                f"{channel_icon} @{ch['username']}", 
                callback_data=f"view_channel_{ch['channel_id']}"
            ),
            InlineKeyboardButton(
                "❌ Remove", 
                callback_data=f"remove_channel_{ch['channel_id']}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("➕ Add New Channel", callback_data="add_channel")])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="admin_main")])
    
    return InlineKeyboardMarkup(keyboard)

def message_editor_keyboard():
    """Message editor keyboard"""
    keyboard = [
        [InlineKeyboardButton("✏️ Welcome Message", callback_data="edit_msg_welcome")],
        [InlineKeyboardButton("✏️ Help Message", callback_data="edit_msg_help")],
        [InlineKeyboardButton("✏️ Force Join Message", callback_data="edit_msg_force_join")],
        [InlineKeyboardButton("✏️ After Video Message", callback_data="edit_msg_after_video")],
        [InlineKeyboardButton("✏️ Video Not Found Message", callback_data="edit_msg_video_not_found")],
        [InlineKeyboardButton("✏️ Auto Reply Message", callback_data="edit_msg_auto_reply")],
        [InlineKeyboardButton("🔙 Back", callback_data="admin_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def settings_keyboard():
    """Settings keyboard"""
    keyboard = [
        [InlineKeyboardButton("🎮 Mini App URL", callback_data="setting_mini_app")],
        [InlineKeyboardButton("📢 Main Channel", callback_data="setting_main_channel")],
        [InlineKeyboardButton("🔒 Video Protection", callback_data="setting_protection")],
        [InlineKeyboardButton("🤖 Bot Name", callback_data="setting_bot_name")],
        [InlineKeyboardButton("💬 Auto Reply", callback_data="setting_auto_reply")],
        [InlineKeyboardButton("🧹 Message Cleanup", callback_data="setting_cleanup")],
        [InlineKeyboardButton("🎬 Welcome Media", callback_data="setting_welcome_media")],
        [InlineKeyboardButton("📁 Folder Join Link", callback_data="setting_folder_link")],  # NEW
        [InlineKeyboardButton("🔙 Back", callback_data="admin_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def button_manager_keyboard():
    """Button manager keyboard"""
    keyboard = [
        [InlineKeyboardButton("➕ Add Welcome Button", callback_data="add_btn_welcome")],
        [InlineKeyboardButton("➕ Add After Video Button", callback_data="add_btn_after_video")],
        [InlineKeyboardButton("📋 View Welcome Buttons", callback_data="view_btn_welcome")],
        [InlineKeyboardButton("📋 View After Video Buttons", callback_data="view_btn_after_video")],
        [InlineKeyboardButton("🔙 Back", callback_data="admin_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===================== ULTIMATE FORCE JOIN SYSTEM =====================

async def show_force_join(user_id, video_id, user_name, context):
    """Show force join screen or send video if all joined"""
    # Get channels user hasn't joined
    not_joined = await get_not_joined_channels(user_id)
    
    if not not_joined:
        # All channels already joined! Send video directly
        await send_video_direct_by_id(user_id, video_id, context)
        return
    
    # Create message
    count = len(not_joined)
    plural = "s" if count > 1 else ""
    channels_list = format_channels_list(not_joined)
    
    message_text = get_message('force_join_start').format(
        name=user_name,
        count=count,
        plural=plural,
        channels_list=channels_list
    )
    
    # Create buttons
    keyboard = create_channel_buttons(not_joined)
    
    if not keyboard:
        # No way to join channels - just send video
        await send_video_direct_by_id(user_id, video_id, context)
        return
    
    # Send message
    sent_msg = await context.bot.send_message(
        chat_id=user_id,
        text=message_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Save message ID and video ID for auto-update
    context.user_data[f"pending_video_{user_id}"] = video_id
    context.user_data[f"pending_msg_{user_id}"] = sent_msg.message_id
    
    logger.info(f"📋 Showed force join: {count} channels for user {user_id}")

async def update_force_join_progress(user_id, context):
    """Update force join message after user joins a channel"""
    # Get saved data
    video_id = context.user_data.get(f"pending_video_{user_id}")
    message_id = context.user_data.get(f"pending_msg_{user_id}")
    
    if not video_id or not message_id:
        logger.debug(f"No pending video/message for user {user_id}")
        return
    
    # Get remaining channels
    not_joined = await get_not_joined_channels(user_id)
    
    if not not_joined:
        # ALL CHANNELS JOINED! 🎉
        
        # Delete force join message
        try:
            await context.bot.delete_message(chat_id=user_id, message_id=message_id)
        except:
            pass
        
        # Show completion message
        completion_msg = await context.bot.send_message(
            chat_id=user_id,
            text=get_message('force_join_complete'),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Wait a moment
        await asyncio.sleep(0.5)
        
        # Delete completion message
        try:
            await completion_msg.delete()
        except:
            pass
        
        # Clear pending data
        context.user_data.pop(f"pending_video_{user_id}", None)
        context.user_data.pop(f"pending_msg_{user_id}", None)
        
        # Send video!
        await send_video_direct_by_id(user_id, video_id, context)
        
        logger.info(f"✅ All channels joined! Sent video to user {user_id}")
    
    else:
        # Still channels remaining - update message
        count = len(not_joined)
        
        # Get last joined channel name (first one not in not_joined list)
        all_channels = get_force_join_channels()
        last_joined = None
        for ch in all_channels:
            if ch not in not_joined:
                last_joined = ch
                break
        
        joined_name = last_joined.get('name', 'Channel') if last_joined else 'Channel'
        
        # Choose appropriate message
        if count == 1:
            message_key = 'force_join_almost'
        else:
            message_key = 'force_join_progress'
        
        # Format message
        channels_list = format_channels_list(not_joined)
        message_text = get_message(message_key).format(
            joined_name=joined_name,
            remaining=count,
            channels_list=channels_list
        )
        
        # Create buttons
        keyboard = create_channel_buttons(not_joined)
        
        # Update message
        try:
            await context.bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=message_text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            logger.info(f"📊 Updated progress: {count} channels remaining for user {user_id}")
        except:
            # If edit fails, delete and send new
            try:
                await context.bot.delete_message(chat_id=user_id, message_id=message_id)
            except:
                pass
            
            sent_msg = await context.bot.send_message(
                chat_id=user_id,
                text=message_text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Update message ID
            context.user_data[f"pending_msg_{user_id}"] = sent_msg.message_id

async def send_video_direct_by_id(user_id, video_id, context):
    """Send video directly by ID without force join check"""
    # Convert video_id to message_id
    try:
        message_id = int(video_id)
    except ValueError:
        await context.bot.send_message(
            chat_id=user_id,
            text=get_message('video_not_found'),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    video = get_video(message_id)
    
    if not video:
        await context.bot.send_message(
            chat_id=user_id,
            text=get_message('video_not_found'),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Send video using copy_message (same as manual verify flow)
    try:
        protect = get_setting('video_protection', True)
        
        video_msg = await context.bot.copy_message(
            chat_id=user_id,
            from_chat_id=video['channel_id'],
            message_id=message_id,
            protect_content=protect
        )
        
        increment_video_view(message_id)
        
        # After video message with dynamic buttons
        after_buttons = get_buttons('after_video')
        
        if after_buttons:
            # Use custom buttons from database
            keyboard = []
            for btn in after_buttons:
                if btn['type'] == 'web_app':
                    keyboard.append([InlineKeyboardButton(btn['text'], web_app={"url": btn['url']})])
                else:  # url type
                    keyboard.append([InlineKeyboardButton(btn['text'], url=btn['url'])])
        else:
            # Default button
            mini_app_url = get_setting('mini_app_url', DEFAULT_SETTINGS['mini_app_url'])
            keyboard = [[InlineKeyboardButton("🔙 Back to App", web_app={"url": mini_app_url})]]
        
        after_msg = await context.bot.send_message(
            chat_id=user_id,
            text=get_message('after_video'),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"✅ Video {message_id} sent to user {user_id}")
        
    except BadRequest as e:
        if "message to copy not found" in str(e).lower():
            await context.bot.send_message(
                chat_id=user_id,
                text=get_message('video_not_found'),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            logger.error(f"Error sending video: {e}")
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Error sending video. Please try again.",
                parse_mode=ParseMode.MARKDOWN
            )
    except Exception as e:
        logger.error(f"Error in send_video_direct_by_id: {e}")
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Error sending video. Please try again.",
            parse_mode=ParseMode.MARKDOWN
        )

# ===================== CHAT JOIN REQUEST HANDLER =====================
async def handle_chat_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle when user sends join request to private channel
    🔥 UPGRADED: Now triggers auto-update of force join message!
    """
    chat_join_request = update.chat_join_request
    user = chat_join_request.from_user
    chat = chat_join_request.chat
    
    logger.info(f"🔔 JOIN REQUEST: User {user.id} (@{user.username}) → Channel {chat.id}")
    
    # Mark this join request in database
    mark_join_request_sent(user.id, chat.id)
    
    # 🔥 NEW: Auto-update force join message if user has pending video
    await update_force_join_progress(user.id, context)

# ===================== START COMMAND =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with ultra-clean chat experience"""
    user = update.effective_user
    save_user(user.id, user.username, user.first_name)
    
    # 🔥 ADVANCED: Track user's /start command message for deletion
    user_command_msg_id = update.message.message_id
    
    # 🧹 STEP 1: Cleanup ALL old messages (ultra-clean)
    await cleanup_user_messages(context, user.id, update.effective_chat.id)
    
    # Check for video deep link
    if context.args and len(context.args) > 0:
        video_id = context.args[0]
        
        # 🔥 Delete user's command message for clean chat
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=user_command_msg_id
            )
        except:
            pass
        
        await handle_video_request(update, context, video_id)
        return
    
    # Get settings
    mini_app_url = get_setting('mini_app_url', DEFAULT_SETTINGS['mini_app_url'])
    
    # Build keyboard with custom buttons
    keyboard = []
    
    # Get custom welcome buttons from database
    custom_buttons = get_buttons('welcome')
    
    if custom_buttons:
        # Use custom buttons from database
        for btn in custom_buttons:
            if btn['type'] == 'web_app':
                keyboard.append([InlineKeyboardButton(btn['text'], web_app={"url": btn['url']})])
            else:  # url type
                keyboard.append([InlineKeyboardButton(btn['text'], url=btn['url'])])
    else:
        # Default buttons if no custom buttons set
        main_channel = get_setting('main_channel_username', DEFAULT_SETTINGS['main_channel_username'])
        keyboard = [
            [InlineKeyboardButton("🎮 Open CINEFLIX App", web_app={"url": mini_app_url})],
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{main_channel}")],
            [InlineKeyboardButton("❓ Help", callback_data="help")]
        ]
    
    welcome_text = get_message('welcome').format(name=user.first_name)
    
    try:
        # Send welcome media first (if enabled)
        welcome_media_enabled = get_setting('welcome_media_enabled', False)
        
        if welcome_media_enabled:
            media_file_id = get_setting('welcome_media_file_id')
            media_type = get_setting('welcome_media_type')
            
            if media_file_id and media_type:
                try:
                    media_msg = None
                    if media_type == 'photo':
                        media_msg = await update.message.reply_photo(photo=media_file_id)
                    elif media_type == 'animation':
                        media_msg = await update.message.reply_animation(animation=media_file_id)
                    elif media_type == 'video':
                        media_msg = await update.message.reply_video(video=media_file_id)
                    
                    # Track media message
                    if media_msg:
                        await track_message(user.id, media_msg.message_id)
                        logger.info(f"✅ Welcome media sent to user {user.id}")
                except Exception as e:
                    logger.error(f"Error sending welcome media: {e}")
        
        # Send welcome text message with buttons
        sent_msg = await update.message.reply_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Track welcome message
        await track_message(user.id, sent_msg.message_id)
        
        # 🔥 DELETE user's /start command for ultra-clean chat
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=user_command_msg_id
            )
            logger.debug(f"🧹 Deleted user's /start command")
        except Exception as e:
            logger.debug(f"Could not delete user command: {e}")
        
    except Exception as e:
        logger.error(f"Error sending welcome message: {e}")

# ===================== VIDEO REQUEST HANDLER =====================
async def handle_video_request(update: Update, context: ContextTypes.DEFAULT_TYPE, video_id: str):
    """Handle video playback request"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # NEW: Cleanup old messages first (for clean experience)
    await cleanup_user_messages(context, user.id, chat_id)
    
    try:
        message_id = int(video_id)
    except ValueError:
        msg = await update.message.reply_text(
            get_message('video_not_found'),
            parse_mode=ParseMode.MARKDOWN
        )
        # Track message
        if user.id not in user_all_messages:
            user_all_messages[user.id] = []
        await track_message(user.id, msg.message_id)
        return
    
    # Get video from database
    video = get_video(message_id)
    if not video:
        msg = await update.message.reply_text(
            get_message('video_not_found'),
            parse_mode=ParseMode.MARKDOWN
        )
        # Track message
        if user.id not in user_all_messages:
            user_all_messages[user.id] = []
        await track_message(user.id, msg.message_id)
        return
    
    # Check force join channels
    force_channels = get_force_join_channels()
    not_joined = []
    
    for channel in force_channels:
        try:
            # Try to get chat member status
            member = await context.bot.get_chat_member(channel['channel_id'], user.id)
            
            # Log detailed status for debugging
            logger.info(f"🔍 Checking user {user.id} in {channel['username']}: status={member.status}")
            
            # ✅ NEW LOGIC: Check both actual membership AND pending join requests
            is_member_or_admin = member.status in ['member', 'administrator', 'creator']
            has_pending_request = has_pending_join_request(user.id, channel['channel_id'])
            
            if is_member_or_admin:
                logger.info(f"✅ User {user.id} IS MEMBER of {channel['username']}")
                clear_join_request(user.id, channel['channel_id'])
                # Continue to next channel
            elif has_pending_request:
                logger.info(f"✅ User {user.id} has PENDING REQUEST in {channel['username']} - GRANTING ACCESS!")
                # Grant access even though not approved yet!
                # Continue to next channel
            elif member.status in ['left', 'kicked']:
                not_joined.append(channel)
                logger.info(f"❌ User {user.id} NOT in channel {channel['username']}: {member.status}")
            else:
                # Unknown status - be safe and block
                not_joined.append(channel)
                logger.warning(f"⚠️ Unknown status for user {user.id} in {channel['username']}: {member.status}")
                
        except BadRequest as e:
            error_msg = str(e).lower()
            if "chat not found" in error_msg:
                # Bot is not admin in channel or channel ID is wrong
                logger.error(f"⚠️ Bot cannot access channel {channel['username']} (ID: {channel['channel_id']}). Bot must be admin!")
                # Skip this channel - don't block user due to bot config issue
                continue
            elif "user not found" in error_msg:
                # User account issue - rare
                logger.warning(f"User {user.id} not found in Telegram")
                not_joined.append(channel)
            else:
                # Other errors - assume not joined for safety
                logger.error(f"Error checking {channel['username']} for user {user.id}: {e}")
                not_joined.append(channel)
        except Exception as e:
            # Unknown errors - assume not joined
            logger.error(f"Unexpected error checking {channel['username']}: {e}")
            not_joined.append(channel)
    
    if not_joined:
        # User hasn't joined all channels
        keyboard = []
        
        # Check if folder link is enabled
        folder_enabled = get_setting('folder_link_enabled', False)
        folder_url = get_setting('folder_link_url', '')
        
        if folder_enabled and folder_url:
            # ✅ ONE-CLICK JOIN: Show folder link button
            keyboard.append([InlineKeyboardButton(
                "📁 Join All Channels (1-Click)", 
                url=folder_url
            )])
        else:
            # Traditional: Show individual channel buttons
            channel_num = 1
            for ch in not_joined:
                # ✅ NEW: Use invite link if available (for private channels), otherwise username
                if ch.get('invite_link'):
                    # Private channel with invite link
                    button_url = ch['invite_link']
                    # Show numbered name for private channels (helps distinguish multiple private channels)
                    button_text = f"🔒 Join Private Channel {channel_num}"
                    channel_num += 1
                else:
                    # Public channel with username
                    button_url = f"https://t.me/{ch['username']}"
                    button_text = f"📢 Join @{ch['username']}"
                    button_text = f"📢 Join @{ch['username']}"
                
                keyboard.append([InlineKeyboardButton(button_text, url=button_url)])
        
        # ✅ NEW: Manual verify button (optional backup)
        keyboard.append([InlineKeyboardButton(
            "✅ I Joined - Unlock Now", 
            callback_data=f"verify_{video_id}"
        )])
        
        msg = await update.message.reply_text(
            get_message('force_join'),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Track this message for cleanup
        if user.id not in user_all_messages:
            user_all_messages[user.id] = []
        await track_message(user.id, msg.message_id)
        
        logger.info(f"📢 Force join message sent to user {user.id} for video {video_id}")
        
        return
    
    # User joined all channels - send video
    try:
        protect = get_setting('video_protection', True)
        
        video_msg = await context.bot.copy_message(
            chat_id=chat_id,
            from_chat_id=video['channel_id'],
            message_id=message_id,
            protect_content=protect
        )
        
        increment_video_view(message_id)
        
        # After video message with dynamic buttons
        after_buttons = get_buttons('after_video')
        
        if after_buttons:
            # Use custom buttons from database
            keyboard = []
            for btn in after_buttons:
                if btn['type'] == 'web_app':
                    keyboard.append([InlineKeyboardButton(btn['text'], web_app={"url": btn['url']})])
                else:  # url type
                    keyboard.append([InlineKeyboardButton(btn['text'], url=btn['url'])])
        else:
            # Default button
            mini_app_url = get_setting('mini_app_url', DEFAULT_SETTINGS['mini_app_url'])
            keyboard = [[InlineKeyboardButton("🔙 Back to App", web_app={"url": mini_app_url})]]
        
        after_msg = await update.message.reply_text(
            get_message('after_video'),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Track these messages for cleanup
        if user.id not in user_all_messages:
            user_all_messages[user.id] = []
        user_all_messages[user.id].extend([video_msg.message_id, after_msg.message_id])
        
        logger.info(f"✅ Video {message_id} sent to user {user.id}")
        
    except BadRequest as e:
        if "message to copy not found" in str(e).lower():
            msg = await update.message.reply_text(
                get_message('video_not_found'),
                parse_mode=ParseMode.MARKDOWN
            )
            # Track message
            if user.id not in user_all_messages:
                user_all_messages[user.id] = []
            await track_message(user.id, msg.message_id)
        else:
            logger.error(f"Error sending video: {e}")

# ===================== AUTO-CHECK AND UNLOCK =====================
async def auto_check_and_unlock(context: ContextTypes.DEFAULT_TYPE):
    """
    Automatically check if user has joined all channels and unlock video
    This runs every 5 seconds for up to 30 seconds
    """
    job = context.job
    data = job.data
    
    user_id = data['user_id']
    chat_id = data['chat_id']
    video_id = data['video_id']
    force_join_msg_id = data['message_id']
    check_count = data.get('check_count', 0)
    max_checks = data.get('max_checks', 6)
    
    # Increment check count
    data['check_count'] = check_count + 1
    
    logger.info(f"🔍 Auto-check #{check_count + 1}/{max_checks} for user {user_id}, video {video_id}")
    
    # If max checks reached, stop job
    if check_count >= max_checks:
        logger.info(f"⏱️ Max checks reached for user {user_id}. Stopping auto-check.")
        job.schedule_removal()
        return
    
    try:
        # Get video from database
        try:
            message_id = int(video_id)
        except ValueError:
            logger.error(f"Invalid video_id: {video_id}")
            job.schedule_removal()
            return
        
        video = get_video(message_id)
        if not video:
            logger.error(f"Video not found: {video_id}")
            job.schedule_removal()
            return
        
        # Check force join channels
        force_channels = get_force_join_channels()
        not_joined = []
        
        for channel in force_channels:
            try:
                member = await context.bot.get_chat_member(channel['channel_id'], user_id)
                
                # Check if user joined or sent request
                
                # Log detailed status
                logger.debug(f"🔍 Auto-check: user {user_id} in {channel['username']}: status={member.status}")
                
                # Allow if: member, admin, creator, OR restricted (join request sent)
                if member.status in ['member', 'administrator', 'creator', 'restricted']:
                    logger.debug(f"✅ Auto-check: User {user_id} HAS ACCESS to {channel['username']}: status={member.status}")
                    # Continue to next channel
                elif member.status in ['left', 'kicked']:
                    not_joined.append(channel)
                    logger.debug(f"❌ Auto-check: User {user_id} still NOT in {channel['username']}: {member.status}")
                else:
                    # Unknown status - be safe and block
                    not_joined.append(channel)
                    logger.warning(f"⚠️ Auto-check: Unknown status for user {user_id} in {channel['username']}: {member.status}")
                    
            except Exception as e:
                logger.debug(f"Error checking {channel['username']}: {e}")
                not_joined.append(channel)
        
        # If user still hasn't joined all channels
        if not_joined:
            # Create readable channel list (handle private channels properly)
            remaining_names = []
            private_num = 1
            for ch in not_joined:
                if ch.get('invite_link'):
                    # Private channel - show numbered
                    remaining_names.append(f"🔒 Private Channel {private_num}")
                    private_num += 1
                else:
                    # Public channel - show username
                    remaining_names.append(f"@{ch['username']}")
            
            remaining = ", ".join(remaining_names)
            logger.info(f"⏳ User {user_id} still not joined: {remaining}")
            
            # Update message to show remaining channels
            try:
                remaining_list = "\n".join([f"❌ {name}" for name in remaining_names])
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=force_join_msg_id,
                    text=f"{get_message('force_join')}\n\n"
                         f"**📊 Status:**\n"
                         f"Waiting for you to join:\n{remaining_list}\n\n"
                         f"⏱️ Auto-checking... ({check_count + 1}/{max_checks})",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            "✅ Check Again Now", 
                            callback_data=f"verify_{video_id}"
                        )]
                    ]),
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                logger.debug(f"Could not update message: {e}")
            
            return  # Continue checking
        
        # ✅ ALL CHANNELS JOINED! Send video automatically!
        logger.info(f"🎉 User {user_id} joined all channels! Auto-unlocking video {video_id}...")
        
        # Stop the job
        job.schedule_removal()
        
        # Delete force join message
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=force_join_msg_id)
            logger.info(f"🗑️ Deleted force join message")
        except Exception as e:
            logger.debug(f"Could not delete force join message: {e}")
        
        # Clean up old messages
        await cleanup_user_messages(context, user_id, chat_id)
        
        # Send video
        try:
            protect = get_setting('video_protection', True)
            
            video_msg = await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=video['channel_id'],
                message_id=message_id,
                protect_content=protect
            )
            
            increment_video_view(message_id)
            
            # After video message
            after_buttons = get_buttons('after_video')
            
            if after_buttons:
                keyboard = []
                for btn in after_buttons:
                    if btn['type'] == 'web_app':
                        keyboard.append([InlineKeyboardButton(btn['text'], web_app={"url": btn['url']})])
                    else:
                        keyboard.append([InlineKeyboardButton(btn['text'], url=btn['url'])])
            else:
                mini_app_url = get_setting('mini_app_url', DEFAULT_SETTINGS['mini_app_url'])
                keyboard = [[InlineKeyboardButton("🔙 Back to App", web_app={"url": mini_app_url})]]
            
            after_msg = await context.bot.send_message(
                chat_id=chat_id,
                text=get_message('after_video'),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Send success notification
            await context.bot.send_message(
                chat_id=chat_id,
                text="✅ **ভিডিও আনলক হয়েছে! Video Unlocked!**\n\n"
                     "🤖 বট অটোমেটিক ডিটেক্ট করেছে যে আপনি চ্যানেল জয়েন করেছেন!\n"
                     "🤖 Bot automatically detected that you joined the channel!\n\n"
                     "🎉 এখন ভিডিও উপভোগ করুন! Enjoy! 🍿",
                parse_mode=ParseMode.MARKDOWN
            )
            
            logger.info(f"✅ Auto-unlock successful for user {user_id}, video {video_id}")
            
        except Exception as e:
            logger.error(f"Error auto-sending video: {e}")
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Error unlocking video. Please try again using /start",
                parse_mode=ParseMode.MARKDOWN
            )
    
    except Exception as e:
        logger.error(f"Error in auto_check_and_unlock: {e}")
        job.schedule_removal()

# ===================== CALLBACK QUERY HANDLER =====================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    
    # Help button
    if data == "help":
        await query.message.reply_text(
            get_message('help'),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # 🔥 ULTIMATE: Video request with progressive force join
    if data.startswith("verify_"):
        video_id = data.replace("verify_", "")
        user = query.from_user
        
        try:
            message_id = int(video_id)
        except ValueError:
            await query.message.edit_text(
                get_message('video_not_found'),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Check if video exists
        video = get_video(message_id)
        if not video:
            await query.message.edit_text(
                get_message('video_not_found'),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Delete the callback query message
        try:
            await query.message.delete()
        except:
            pass
        
        # Show force join OR send video directly (smart detection!)
        await show_force_join(
            user_id=user.id,
            video_id=str(message_id),
            user_name=user.first_name or "User",
            context=context
        )
        return
    # Admin panel navigation
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
        
        await query.edit_message_text(
            text,
            reply_markup=admin_main_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "admin_channels":
        await query.edit_message_text(
            "📺 **Channel Manager**\n\nManage force join channels:",
            reply_markup=channel_manager_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "admin_messages":
        await query.edit_message_text(
            "📝 **Message Editor**\n\nSelect a message to edit:",
            reply_markup=message_editor_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "admin_buttons":
        await query.edit_message_text(
            "🔘 **Button Manager**\n\n"
            "Add custom buttons to Welcome or After Video messages.\n\n"
            "You can add:\n"
            "• Channel/Group links\n"
            "• Mini App buttons\n"
            "• Any custom URL\n\n"
            "Select an option:",
            reply_markup=button_manager_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "admin_settings":
        # Get current settings
        mini_app = get_setting('mini_app_url', DEFAULT_SETTINGS['mini_app_url'])
        main_channel = get_setting('main_channel_username', DEFAULT_SETTINGS['main_channel_username'])
        protection = get_setting('video_protection', True)
        bot_name = get_setting('bot_name', DEFAULT_SETTINGS['bot_name'])
        auto_reply = get_setting('auto_reply_enabled', True)
        cleanup = get_setting('message_cleanup_enabled', True)
        welcome_media = get_setting('welcome_media_enabled', False)
        folder_enabled = get_setting('folder_link_enabled', False)  # NEW
        folder_url = get_setting('folder_link_url', '')  # NEW
        
        protection_status = "🔒 ON" if protection else "🔓 OFF"
        auto_reply_status = "✅ ON" if auto_reply else "❌ OFF"
        cleanup_status = "✅ ON" if cleanup else "❌ OFF"
        welcome_media_status = "✅ ON" if welcome_media else "❌ OFF"
        folder_status = "✅ ON" if folder_enabled else "❌ OFF"  # NEW
        
        settings_text = f"""⚙️ **Bot Settings**

🎮 **Mini App URL:**
`{mini_app}`

📢 **Main Channel:**
@{main_channel}

🔒 **Video Protection:** {protection_status}
💬 **Auto Reply:** {auto_reply_status}
🧹 **Message Cleanup:** {cleanup_status}
🎬 **Welcome Media:** {welcome_media_status}
📁 **Folder Join Link:** {folder_status}

🤖 **Bot Name:** {bot_name}

Click a button below to edit:"""
        
        await query.edit_message_text(
            settings_text,
            reply_markup=settings_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "admin_stats":
        stats = get_stats()
        
        # Simple short message
        text = f"""📊 Bot Stats

👥 Users: {stats['users']}
📹 Videos: {stats['videos']}
🔒 Channels: {stats['force_join']}

✅ Running"""
        
        await query.answer(text, show_alert=True)
    
    elif data == "admin_broadcast":
        admin_states[user_id] = {'action': 'broadcast'}
        await query.message.reply_text(
            "📢 **Broadcast Message**\n\n"
            "Send the message you want to broadcast to all users.\n\n"
            "✅ You can send:\n"
            "• Text messages\n"
            "• Photos with captions\n"
            "• Videos with captions\n\n"
            "⚠️ This will be sent to ALL users!\n\n"
            "Or /cancel to cancel",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "admin_refresh":
        await query.answer("🔄 Refreshed!")
        # Re-trigger the current callback to refresh
        if data == "admin_main":
            await button_callback(update, context)
    
    elif data == "admin_close":
        await query.message.delete()
        await query.answer("Panel closed")
    
    elif data == "add_channel":
        admin_states[user_id] = {'action': 'add_channel'}
        await query.message.reply_text(
            "➕ **Add New Force Join Channel**\n\n"
            "**📢 Public Channel:**\n"
            "`channel_id username`\n\n"
            "**🔒 Private Channel (Easy):**\n"
            "`channel_id invite_link`\n"
            "_(Bot auto-generates username)_\n\n"
            "**🔒 Private Channel (Custom):**\n"
            "`channel_id username invite_link`\n\n"
            "**Examples:**\n\n"
            "Public:\n"
            "`-1001234567890 MyChannel`\n\n"
            "Private (Easy):\n"
            "`-1001234567890 https://t.me/+xxxxxx`\n\n"
            "Private (Custom):\n"
            "`-1001234567890 MyPrivateChannel https://t.me/+xxxxxx`\n\n"
            "Or /cancel to cancel",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data.startswith("remove_channel_"):
        channel_id = int(data.replace("remove_channel_", ""))
        if remove_force_join_channel(channel_id):
            await query.answer("✅ Channel removed!")
            await button_callback(update, context)  # Refresh list
        else:
            await query.answer("❌ Failed to remove channel", show_alert=True)
    
    elif data.startswith("add_btn_"):
        location = data.replace("add_btn_", "")
        admin_states[user_id] = {'action': 'add_button', 'location': location}
        
        location_name = "Welcome Message" if location == "welcome" else "After Video Message"
        
        await query.message.reply_text(
            f"➕ **Add Button to {location_name}**\n\n"
            f"Send button details in this format:\n"
            f"`Text | URL | Type`\n\n"
            f"**Type** can be:\n"
            f"• `url` - Regular link button\n"
            f"• `webapp` - Mini App button\n\n"
            f"**Examples:**\n"
            f"`📢 Join Channel | https://t.me/MyChannel | url`\n"
            f"`🎮 Open App | https://myapp.com/ | webapp`\n"
            f"`👥 Join Group | https://t.me/+grouplink | url`\n\n"
            f"Or /cancel to cancel",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data.startswith("view_btn_"):
        location = data.replace("view_btn_", "")
        buttons = get_buttons(location)
        
        location_name = "Welcome Message" if location == "welcome" else "After Video Message"
        
        if not buttons:
            await query.answer(f"No custom buttons for {location_name}", show_alert=True)
            return
        
        # Create keyboard with button list
        keyboard = []
        for btn in buttons:
            btn_id = str(btn['_id'])
            btn_type_icon = "🌐" if btn['type'] == 'web_app' else "🔗"
            keyboard.append([
                InlineKeyboardButton(f"{btn_type_icon} {btn['text']}", callback_data=f"dummy"),
                InlineKeyboardButton("🗑️", callback_data=f"remove_btn_{btn_id}")
            ])
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="admin_buttons")])
        
        await query.edit_message_text(
            f"📋 **{location_name} Buttons**\n\n"
            f"Total: {len(buttons)} button(s)\n\n"
            f"Click 🗑️ to remove a button:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data.startswith("remove_btn_"):
        button_id = data.replace("remove_btn_", "")
        if remove_button(button_id):
            await query.answer("✅ Button removed!")
            await button_callback(update, context)
        else:
            await query.answer("❌ Failed to remove button", show_alert=True)
    
    elif data.startswith("edit_msg_"):
        msg_key = data.replace("edit_msg_", "")
        admin_states[user_id] = {'action': 'edit_message', 'key': msg_key}
        
        current_msg = get_message(msg_key)
        await query.message.reply_text(
            f"✏️ **Editing {msg_key.replace('_', ' ').title()}**\n\n"
            f"Current message:\n\n{current_msg}\n\n"
            f"Send the new message text or /cancel to cancel",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data.startswith("setting_"):
        setting_key = data.replace("setting_", "")
        
        # Handle toggles
        if setting_key == "protection":
            current = get_setting('video_protection', True)
            new_val = not current
            set_setting('video_protection', new_val)
            
            status = "🔒 ON" if new_val else "🔓 OFF"
            await query.answer(f"Video Protection: {status}")
            await button_callback(update, context)
            return
        
        elif setting_key == "auto_reply":
            current = get_setting('auto_reply_enabled', True)
            new_val = not current
            set_setting('auto_reply_enabled', new_val)
            
            status = "✅ ON" if new_val else "❌ OFF"
            await query.answer(f"Auto Reply: {status}")
            await button_callback(update, context)
            return
        
        elif setting_key == "cleanup":
            current = get_setting('message_cleanup_enabled', True)
            new_val = not current
            set_setting('message_cleanup_enabled', new_val)
            
            status = "✅ ON" if new_val else "❌ OFF"
            await query.answer(f"Message Cleanup: {status}")
            await button_callback(update, context)
            return
        
        # NEW: Welcome Media management
        elif setting_key == "welcome_media":
            current = get_setting('welcome_media_enabled', False)
            
            if not current:
                # Currently OFF, prompt to upload media
                admin_states[user_id] = {'action': 'upload_welcome_media'}
                await query.message.reply_text(
                    "🎬 **Upload Welcome Media**\n\n"
                    "Send me a photo, GIF, or short video that will be shown when users use /start.\n\n"
                    "📝 **Tips:**\n"
                    "• Keep videos under 5 seconds\n"
                    "• File size under 5 MB recommended\n"
                    "• GIFs work great for animations!\n\n"
                    "Or /cancel to cancel",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                # Currently ON, toggle OFF
                set_setting('welcome_media_enabled', False)
                await query.answer("✅ Welcome Media: OFF")
                await button_callback(update, context)
            return
        
        # NEW: Folder Link management
        elif setting_key == "folder_link":
            current_enabled = get_setting('folder_link_enabled', False)
            current_url = get_setting('folder_link_url', '')
            
            if not current_enabled or not current_url:
                # Ask for folder URL
                admin_states[user_id] = {'action': 'set_folder_link'}
                await query.message.reply_text(
                    "📁 **Setup Folder Join Link**\n\n"
                    "**How to create a folder link:**\n"
                    "1. Go to Telegram Settings > Folders\n"
                    "2. Create a folder with all your private channels\n"
                    "3. Share the folder and copy the link\n\n"
                    "**Example link format:**\n"
                    "`https://t.me/addlist/xxxxxxxxxxxxx`\n\n"
                    "Send me your folder link, or /cancel to cancel",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                # Toggle OFF
                set_setting('folder_link_enabled', False)
                await query.answer("✅ Folder Link: OFF (Individual channels will be shown)")
                await button_callback(update, context)
            return
        
        # For other settings, ask for input
        admin_states[user_id] = {'action': 'edit_setting', 'key': setting_key}
        
        # Map callback data to actual setting keys
        setting_map = {
            'mini_app': 'mini_app_url',
            'main_channel': 'main_channel_username',
            'bot_name': 'bot_name'
        }
        
        actual_key = setting_map.get(setting_key, setting_key)
        current = get_setting(actual_key)
        
        # Provide helpful hints
        hints = {
            'mini_app': "Example: https://yourapp.vercel.app/",
            'main_channel': "Example: YourChannel (without @)",
            'bot_name': "Example: CINEFLIX"
        }
        
        hint_text = f"\n\n💡 {hints.get(setting_key, '')}" if setting_key in hints else ""
        
        await query.message.reply_text(
            f"⚙️ **Editing {actual_key.replace('_', ' ').title()}**\n\n"
            f"Current value: `{current}`{hint_text}\n\n"
            f"Send the new value or /cancel to cancel",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Store the actual key for later use
        admin_states[user_id]['actual_key'] = actual_key

# ===================== CHANNEL POST HANDLER =====================
async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle videos posted in channels"""
    try:
        logger.info(f"📥 Channel post received! Update: {update}")
        
        message = update.channel_post
        
        if not message:
            logger.warning("⚠️ No message in channel_post update")
            return
        
        # NEW: Check for all media types including photos
        has_video = bool(message.video)
        has_document = bool(message.document)
        has_animation = bool(message.animation)
        has_photo = bool(message.photo)  # NEW: Photo support
        
        logger.info(f"📝 Message type - Video: {has_video}, Document: {has_document}, Animation: {has_animation}, Photo: {has_photo}")
        
        # NEW: Accept videos, documents, animations, and photos
        if not (has_video or has_document or has_animation or has_photo):
            logger.info("⏭️ Not a media file, skipping")
            return
        
        channel_id = message.chat.id
        message_id = message.message_id
        channel_name = message.chat.title or "Unknown"
        
        # NEW: Detect media type
        media_type = "video"  # default
        media_icon = "🎬"
        if has_photo:
            media_type = "photo"
            media_icon = "📸"
        elif has_animation:
            media_type = "animation"
            media_icon = "🎞️"
        elif has_document:
            media_type = "document"
            media_icon = "📄"
        
        logger.info(f"{media_icon} Processing {media_type} - Channel: {channel_name} ({channel_id}), Message ID: {message_id}")
        
        # Save to database with media type
        save_video(channel_id, message_id, channel_name, media_type)
        logger.info(f"💾 {media_type.title()} saved to database")
        
        # Get bot username for deep link
        bot_info = await context.bot.get_me()
        bot_username = bot_info.username
        
        # Create admin notification - USE HTML instead of MARKDOWN to avoid parsing errors
        deep_link = f"https://t.me/{bot_username}?start={message_id}"
        
        # Escape HTML special characters in channel name
        import html
        safe_channel_name = html.escape(channel_name)
        
        # Send notification with HTML format (more reliable than Markdown)
        info_text = f"""{media_icon} <b>New {media_type.title()} Uploaded!</b>

📺 Channel: {safe_channel_name}
📋 Message ID: <code>{message_id}</code>
📁 Type: {media_type.upper()}

🌐 Direct Link:
{deep_link}

✅ {media_type.title()} saved to database!
Users can now access this content!

👇 <b>Tap the number below to copy:</b>"""
        
        logger.info(f"📤 Sending notification to admin {ADMIN_ID}")
        
        # First message with info (using HTML parse mode)
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=info_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        
        # Second message with ONLY the copyable shortcode
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"<code>{message_id}</code>",
            parse_mode=ParseMode.HTML
        )
        
        logger.info(f"✅ Successfully notified admin about {media_type} {message_id}")
        
    except Exception as e:
        logger.error(f"❌ Error in channel_post handler: {e}", exc_info=True)

# ===================== ADMIN MESSAGE HANDLER =====================
async def admin_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin text messages for editing"""
    user_id = update.effective_user.id
    
    # Check if this is a broadcast message (admin sending to users)
    if user_id in admin_states and admin_states[user_id].get('action') == 'broadcast':
        await handle_broadcast(update, context)
        return
    
    # Auto-reply for non-admin users
    if user_id != ADMIN_ID:
        auto_reply_enabled = get_setting('auto_reply_enabled', True)
        if auto_reply_enabled:
            mini_app_url = get_setting('mini_app_url', DEFAULT_SETTINGS['mini_app_url'])
            keyboard = [[InlineKeyboardButton("🎮 Open Mini App", web_app={"url": mini_app_url})]]
            
            await update.message.reply_text(
                get_message('auto_reply'),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN
            )
        return
    
    # Admin-specific handlers
    if user_id not in admin_states:
        return
    
    # NEW: Handle welcome media upload (photo/animation/video)
    if admin_states[user_id].get('action') == 'upload_welcome_media':
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            media_type = 'photo'
        elif update.message.animation:
            file_id = update.message.animation.file_id
            media_type = 'animation'
        elif update.message.video:
            file_id = update.message.video.file_id
            media_type = 'video'
        else:
            await update.message.reply_text(
                "❌ Please send a photo, GIF, or video!\n\nOr /cancel to cancel",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Save to settings
        set_setting('welcome_media_file_id', file_id)
        set_setting('welcome_media_type', media_type)
        set_setting('welcome_media_enabled', True)
        
        await update.message.reply_text(
            f"✅ **Welcome {media_type.title()} Saved!**\n\n"
            f"Users will now see this {media_type} when they use /start.\n\n"
            f"You can toggle it on/off anytime from Settings.",
            parse_mode=ParseMode.MARKDOWN
        )
        
        del admin_states[user_id]
        logger.info(f"✅ Welcome media uploaded: {media_type}")
        return
    
    text = update.message.text
    state = admin_states[user_id]
    
    if text == "/cancel":
        del admin_states[user_id]
        await update.message.reply_text("❌ Cancelled")
        return
    
    # NEW: Handle folder link setup
    if state['action'] == 'set_folder_link':
        text = text.strip()
        
        # Validate folder link format
        if not text.startswith('https://t.me/addlist/'):
            await update.message.reply_text(
                "❌ **Invalid Folder Link!**\n\n"
                "Folder links must start with:\n"
                "`https://t.me/addlist/`\n\n"
                "Please send a valid folder link or /cancel to cancel",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Save folder link settings
        set_setting('folder_link_url', text)
        set_setting('folder_link_enabled', True)
        
        await update.message.reply_text(
            "✅ **Folder Link Saved!**\n\n"
            f"URL: `{text}`\n\n"
            "Users will now see a single '📁 Join All Channels (1-Click)' button instead of individual channel buttons.\n\n"
            "You can toggle it on/off anytime from Settings.",
            parse_mode=ParseMode.MARKDOWN
        )
        
        del admin_states[user_id]
        logger.info(f"✅ Folder link configured: {text}")
        return
    
    if state['action'] == 'add_channel':
        parts = text.split()
        
        # Support multiple formats:
        # Format 1: channel_id username (public)
        # Format 2: channel_id invite_link (private - auto generate username)
        # Format 3: channel_id username invite_link (private with custom username)
        
        if len(parts) < 2:
            await update.message.reply_text(
                "❌ Invalid format!\n\n"
                "**Public Channel:**\n`channel_id username`\n\n"
                "**Private Channel (Option 1):**\n`channel_id invite_link`\n"
                "Bot will auto-generate username\n\n"
                "**Private Channel (Option 2):**\n`channel_id username invite_link`\n\n"
                "Examples:\n"
                "`-1001234567890 MyChannel`\n"
                "`-1001234567890 https://t.me/+xxxxx`\n"
                "`-1001234567890 MyChannel https://t.me/+xxxxx`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            channel_id = int(parts[0])
            
            # Smart detection: Is part[1] a link or username?
            if parts[1].startswith('https://t.me/'):
                # Format 2: channel_id invite_link
                invite_link = parts[1]
                # Auto-generate username from channel_id
                username = f"Channel{abs(channel_id)}"
                logger.info(f"Auto-generated username: {username}")
            elif len(parts) >= 3 and parts[2].startswith('https://t.me/'):
                # Format 3: channel_id username invite_link
                username = parts[1].replace('@', '')
                invite_link = parts[2]
            else:
                # Format 1: channel_id username (public)
                username = parts[1].replace('@', '')
                invite_link = None
            
            # Validate invite link format if provided
            if invite_link and not (invite_link.startswith('https://t.me/+') or invite_link.startswith('https://t.me/joinchat/')):
                await update.message.reply_text(
                    "❌ Invalid invite link!\n\n"
                    "Private channel invite link must start with:\n"
                    "`https://t.me/+xxxxx` or `https://t.me/joinchat/xxxxx`",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            if add_force_join_channel(channel_id, username, invite_link):
                channel_type = "🔒 Private" if invite_link else "📢 Public"
                link_info = f"\n**Invite Link:** `{invite_link}`" if invite_link else ""
                await update.message.reply_text(
                    f"✅ **Channel Added!**\n\n"
                    f"**Type:** {channel_type}\n"
                    f"**Username:** @{username}\n"
                    f"**ID:** `{channel_id}`{link_info}",
                    parse_mode=ParseMode.MARKDOWN
                )
                del admin_states[user_id]
            else:
                await update.message.reply_text("❌ Failed to add channel")
        except ValueError:
            await update.message.reply_text("❌ Channel ID must be a number")
    
    elif state['action'] == 'add_button':
        parts = text.split('|')
        if len(parts) != 3:
            await update.message.reply_text(
                "❌ Invalid format!\n\nUse: `Text | URL | Type`\n\n"
                "Example: `📢 Join Channel | https://t.me/MyChannel | url`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        btn_text = parts[0].strip()
        btn_url = parts[1].strip()
        btn_type = parts[2].strip().lower()
        
        if btn_type not in ['url', 'webapp']:
            await update.message.reply_text(
                "❌ Type must be 'url' or 'webapp'",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        if not btn_url.startswith('http'):
            await update.message.reply_text("❌ URL must start with http:// or https://")
            return
        
        # Convert webapp to web_app
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
    
    elif state['action'] == 'edit_message':
        msg_key = state['key']
        if set_message(msg_key, text):
            await update.message.reply_text("✅ Message updated!")
            del admin_states[user_id]
        else:
            await update.message.reply_text("❌ Failed to update message")
    
    elif state['action'] == 'edit_setting':
        # Get the actual setting key (mapped from callback data)
        setting_key = state.get('actual_key', state['key'])
        
        # Clean up input
        text = text.strip()
        
        # Type conversion and validation
        if setting_key == 'main_channel_id':
            try:
                text = int(text)
            except ValueError:
                await update.message.reply_text("❌ Channel ID must be a number")
                return
        elif setting_key == 'main_channel_username':
            # Remove @ if user added it
            text = text.replace('@', '')
        elif setting_key == 'mini_app_url':
            # Validate URL format
            if not text.startswith('http'):
                await update.message.reply_text("❌ URL must start with http:// or https://")
                return
        elif setting_key == 'video_protection':
            text = text.lower() in ['true', 'yes', '1', 'on']
        
        if set_setting(setting_key, text):
            await update.message.reply_text(
                f"✅ **{setting_key.replace('_', ' ').title()} Updated!**\n\n"
                f"New value: `{text}`",
                parse_mode=ParseMode.MARKDOWN
            )
            del admin_states[user_id]
        else:
            await update.message.reply_text("❌ Failed to update setting")

# ===================== NEW: BROADCAST HANDLER =====================
async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle broadcast message from admin"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        return
    
    # Get all users
    all_users = get_all_users()
    
    if not all_users:
        await update.message.reply_text("❌ No users to broadcast to!")
        del admin_states[user_id]
        return
    
    # Confirm broadcast
    await update.message.reply_text(
        f"📢 **Broadcasting to {len(all_users)} users...**\n\n"
        f"This may take a few moments. Please wait...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    success_count = 0
    fail_count = 0
    
    # Forward the message to all users
    for target_user_id in all_users:
        try:
            # Copy the message to each user
            if update.message.photo:
                # Photo message
                await context.bot.send_photo(
                    chat_id=target_user_id,
                    photo=update.message.photo[-1].file_id,
                    caption=update.message.caption,
                    parse_mode=ParseMode.MARKDOWN if update.message.caption else None
                )
            elif update.message.video:
                # Video message
                await context.bot.send_video(
                    chat_id=target_user_id,
                    video=update.message.video.file_id,
                    caption=update.message.caption,
                    parse_mode=ParseMode.MARKDOWN if update.message.caption else None
                )
            else:
                # Text message
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=update.message.text,
                    parse_mode=ParseMode.MARKDOWN
                )
            
            success_count += 1
            logger.info(f"✅ Broadcast sent to user {target_user_id}")
            
        except Exception as e:
            fail_count += 1
            logger.error(f"❌ Failed to send broadcast to user {target_user_id}: {e}")
    
    # Send summary to admin
    await update.message.reply_text(
        f"✅ **Broadcast Complete!**\n\n"
        f"✅ Sent: {success_count}\n"
        f"❌ Failed: {fail_count}\n"
        f"📊 Total: {len(all_users)}",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Clear admin state
    del admin_states[user_id]
    
    logger.info(f"📢 Broadcast completed: {success_count} success, {fail_count} failed")

# ===================== ADMIN COMMANDS =====================
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin panel"""
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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help"""
    await update.message.reply_text(
        get_message('help'),
        parse_mode=ParseMode.MARKDOWN
    )

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
    
    # ✅ NEW: Chat join request handler - CRITICAL for private channels!
    application.add_handler(ChatJoinRequestHandler(handle_chat_join_request))
    
    # Admin message handlers - text and media
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_message_handler))
    application.add_handler(MessageHandler(
        (filters.PHOTO | filters.ANIMATION | filters.VIDEO) & filters.User(ADMIN_ID),
        admin_message_handler
    ))
    
    # Channel post handler - catches ALL channel posts first
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
    logger.info(f"✨ NEW FEATURES: Photo Support, Welcome Media, Auto Cleanup, Broadcast, Enhanced Stats, Auto-Reply")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
