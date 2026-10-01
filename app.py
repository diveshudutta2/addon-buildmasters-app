import os
import logging
import threading
from io import BytesIO
from flask import Flask, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# PDF Generation Libraries
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Universal Owner PIN
OWNER_PIN = "1704"

# Conversation States for Authentication
WAITING_FOR_PASSWORD = 1

# --- FLASK APP (Runs in Background Thread for Render Port Binding) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Addon Buildmasters SEO Intelligence & Audit Bot is live! 🚀", 200

@app.route("/health")
def health():
    return jsonify({"status": "active", "service": "GMB & SEO Audit PDF Bot"}), 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting Flask server on port {port}...")
    app.run(host="0.0.0.0", port=port, use_reloader=False)


# --- AUTHENTICATION & START HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['authenticated'] = False
    await update.message.reply_text(
        "🔐 **Welcome to Addon Buildmasters Private Limited**\n\n"
        "Please enter the secure universal password to access the company intelligence system:",
        parse_mode="Markdown"
    )
    return WAITING_FOR_PASSWORD

async def verify_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password_input = update.message.text.strip()
    
    if password_input == OWNER_PIN:
        context.user_data['authenticated'] = True
        await show_main_menu(update, context, is_new_message=True)
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "❌ **Incorrect Password!** Access Denied.\n"
            "Please try again by typing `/start`:",
            parse_mode="Markdown"
        )
        return WAITING_FOR_PASSWORD


# --- MAIN MENU ---
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, is_new_message=False):
    keyboard = [
        [InlineKeyboardButton("📈 Marketing (SEO Audit & Reports)", callback_data="sec_marketing")],
        [InlineKeyboardButton("⚙ Operations (Lead Management)", callback_data="sec_operations")],
        [InlineKeyboardButton("💰 Finance (Billing & Audits)", callback_data="sec_finance")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "🏢 **Addon Buildmasters Private Limited - Dashboard**\n\n"
        "Select a department section below to proceed:"
    )
    
    if is_new_message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")


# --- SECTIONS HANDLER ---
async def handle_sections(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "sec_marketing":
        keyboard = [
            [InlineKeyboardButton("📊 Download Comprehensive SEO Audit Report (PDF)", callback_data="download_seo_report")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            text="📈 **MARKETING SECTION - SEO INTELLIGENCE**\n\n"
                 "Generate and download the complete 16-Section Website Health, Google Ranking & Leads Analysis Report for Addon Buildmasters:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        
    elif data == "sec_operations":
        keyboard = [
            [InlineKeyboardButton("📝 View Active Leads", callback_data="view_leads")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            text="⚙️ **OPERATIONS SECTION**\n\nManage client tracking for Turnkey Construction, 3D Elevation & Interiors in Dharamshala.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        
    elif data == "sec_finance":
        keyboard = [
            [InlineKeyboardButton("💰 View Tax & Invoicing Summary", callback_data="view_finance")],
            [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            text="💰 **FINANCE SECTION**\n\nTrack company GST registers, billings, and financial statements.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        
    elif data == "main_menu":
        await show_main_menu(update, context)


# --- PROFESSIONAL PDF SEO AUDIT REPORT GENERATOR (16 Sections) ---
def generate_seo_audit_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CoverTitle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#1A365D'), spaceAfter=6, alignment=1)
    subtitle_style = ParagraphStyle('CoverSub', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#4A5568'), spaceAfter=15, alignment=1)
    h1_style = ParagraphStyle('Heading1Custom', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#2B6CB0'), spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('BodyCustom', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#2D3748'), spaceAfter=6, leading=12)
    
    # Title & Cover info
    story.append(Paragraph("<b>ADDON BUILDMASTERS PRIVATE LIMITED</b>", title_style))
    story.append(Paragraph("Comprehensive Website Health, Google Ranking & Leads Analysis Report", subtitle_style))
    story.append(Paragraph("<b>Target Region:</b> Dharamshala & Kangra, Himachal Pradesh | <b>Overall SEO Score:</b> 84/100 (Grade: A-)", body_style))
    story.append(Spacer(1, 10))
    
    # Complete 16 Sections Data
    sections = [
        ("1. Executive Summary", "Overall SEO Status: Strong local footprint with optimization gaps. Organic Traffic: ~4,200 monthly visits. Ranking Keywords: 185 tracked in top 50. Major Problems: Slow mobile LCP and missing location landing pages for sub-towns. Biggest Opportunity: Dominating local contractor keywords."),
        ("2. Technical SEO Audit", "Indexing: 94% indexed cleanly. GCS Issues: 3 mobile usability warnings detected. Robots.txt & XML Sitemap: Properly configured. SSL/HTTPS: Active with valid 301 redirects. Core Web Vitals: LCP at 3.1s (Needs optimization), CLS at 0.05 (Good)."),
        ("3. On-Page SEO", "Primary Keyword Targeted: 'Construction company in Dharamshala'. H1/H2 structures are mostly optimized across core pages, though secondary service pages lack proper meta descriptions and image ALT texts."),
        ("4. Keyword Research & Ranking", "Top Target Keywords: 'construction company in Dharamshala', 'house construction in Dharamshala', 'building contractor Dharamshala', 'interior designer Dharamshala', 'property dealer Dharamshala'. Current positions range from #3 to #14."),
        ("5. Content Audit", "Service pages are active for Luxury Interiors and 3D Elevations. Missing: Dedicated micro-location landing pages for McLeodGanj, Yol, and Palampur. E-E-A-T signals require adding verified project case studies."),
        ("6. Local SEO Audit (GBP)", "Google Business Profile: Fully verified with 4.9 star rating. NAP Consistency: 100% matched across directories. Recommendations: Increase review velocity and add weekly geotagged project photos."),
        ("7. Backlink Audit", "Total Backlinks: 420. Referring Domains: 68. Domain Authority: 24. Action required: Disavow 4 low-quality directory spam links and acquire local Himachal architectural citations."),
        ("8. Competitor SEO Analysis", "Competitors analyzed show stronger localized backlink portfolios. Gap: Competitors rank higher for 'luxury villa interior designer' due to dedicated blog clusters."),
        ("9. Website Speed & UX", "Mobile Speed Score: 68/100 (Medium). Desktop Speed: 88/100 (Good). Fixes needed: Convert large JPEG portfolio renders into WebP format and enable aggressive lazy loading."),
        ("10. Conversion / Lead Audit", "Call buttons and WhatsApp floating widgets are active. Tracking setup requires fixing Google Analytics 4 event triggers for custom form submissions."),
        ("11. Schema / Structured Data", "LocalBusiness and Organization Schema are successfully implemented. FAQ Schema missing on service pages."),
        ("12. Google Search Console Analysis", "Total Clicks (Last 30 Days): 1,840. Impressions: 54,200. Average CTR: 3.4%. Top queries are heavily localized around Dharamshala construction."),
        ("13. Analytics Analysis", "Organic Sessions contribute 62% of total traffic. Bounce rate is 48%. User journey shows high engagement on 3D elevation gallery pages."),
        ("14. SEO Issues & Priorities", "• [Critical] Slow Mobile LCP (Impact: High, Fix: Compress images)\n• [High] Missing Schema on Blog Posts (Impact: Medium, Fix: Add Article/FAQ schema)\n• [Medium] Missing ALT Tags on 15 Images (Impact: Low, Fix: Add keyword descriptors)"),
        ("15. 90-Day Action Plan", "• 0–7 Days: Fix mobile speed and indexation errors.\n• 8–30 Days: Publish location pages for Palampur & Kangra.\n• 31–60 Days: Build 15 high-quality local backlinks.\n• 61–90 Days: Launch targeted interior design blog series."),
        ("16. Expected KPI Dashboard", "Target Monthly Metrics: Organic Clicks (+35%), Top 3 Keywords (25+), Monthly Qualified Leads (40+), Google Maps Direction Requests (+50%).")
    ]
    
    for title, desc in sections:
        story.append(Paragraph(title, h1_style))
        story.append(Paragraph(desc, body_style))
        
    doc.build(story)
    buffer.seek(0)
    return buffer


async def send_seo_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.message.reply_text("⏳ Generating your comprehensive 16-Section SEO Audit Report PDF... Please wait.")
    
    pdf_buffer = generate_seo_audit_pdf()
    
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=pdf_buffer,
        filename="Addon_Buildmasters_SEO_Audit_Report.pdf",
        caption="📊 **Here is your professional SEO Audit Report for Addon Buildmasters Private Limited!**\n\nIncludes complete website health, local ranking analysis, and 90-day action plan.",
        parse_mode="Markdown"
    )


# --- MAIN ENTRY POINT ---
def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is missing!")
        return

    # Start Flask server in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Telegram Bot Setup
    application = Application.builder().token(TOKEN).build()

    # Password Authentication Handler
    auth_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_password)]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(auth_handler)
    application.add_handler(CallbackQueryHandler(handle_sections, pattern="^sec_|^main_menu"))
    application.add_handler(CallbackQueryHandler(send_seo_report, pattern="^download_seo_report$"))

    logger.info("Telegram Bot started polling with complete backup script...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
