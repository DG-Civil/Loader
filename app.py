import sys
import os

# Force Python to look locally inside your portable folder first
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "lib", "site-packages")))

import streamlit as st
import streamlit.components.v1 as components
import yt_dlp
import validators
import base64

# 1. Page Icon Configuration (Using clipboard-drunk.ico for the browser tab)
page_icon_path = os.path.join(os.path.dirname(__file__), "clipboard-drunk.ico")

# Set up page configurations
st.set_page_config(
    page_title="ሹቅ ፕሮ ማክስ", 
    page_icon=page_icon_path if os.path.exists(page_icon_path) else "📥", 
    layout="centered"
)

# 2. Support Widget Icon Configuration (Using clipboard.ico for the left side image)
icon_path = os.path.join(os.path.dirname(__file__), "clipboard.ico")
icon_base64 = ""
mime_type = "image/x-icon"

if os.path.exists(icon_path):
    with open(icon_path, "rb") as f:
        icon_bytes = f.read()
        icon_base64 = base64.b64encode(icon_bytes).decode("utf-8")
        
    if icon_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
        mime_type = "image/png"

# Build a larger icon snippet for the left side of the widget
icon_html = f'<img src="data:{mime_type};base64,{icon_base64}" width="250" height="250" style="vertical-align: middle;" />' if icon_base64 else '<span style="font-size: 40px;">📋</span>'

# 3. Side-by-side layout (Beer emoji 🍻 replaced with clipboard-drunk icon or text style)
drunk_icon_path = os.path.join(os.path.dirname(__file__), "clipboard-drunk.ico")
drunk_base64 = ""
drunk_mime = "image/x-icon"
if os.path.exists(drunk_icon_path):
    with open(drunk_icon_path, "rb") as f:
        drunk_bytes = f.read()
        drunk_base64 = base64.b64encode(drunk_bytes).decode("utf-8")
    if drunk_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
        drunk_mime = "image/png"

drunk_img_html = f'<img src="data:{drunk_mime};base64,{drunk_base64}" width="150" height="150" style="vertical-align: middle; margin-right: 6px;" />' if drunk_base64 else ''

# 3D Text Shadow & Mask Style
text_3d_style = "font-size: 36px; font-weight: bold; color: #222222; text-shadow: 5px 5px 3px #ffffff, 5px 5px 2px #29abe0, 12px 12px 10px rgba(0,0,0,0.3); line-height: 1.2;"

kofi_html = f"""
<div style="display: flex; justify-content: center; align-items: center; margin-top: 20px; font-family: sans-serif;">
  <a href="https://ko-fi.com/yourusername" target="_blank" style="
      background-color: transparent;
      color: #333333;
      padding: 15px 25px;
      text-decoration: none;
      font-weight: bold;
      border-radius: 20px;
      border: 3px solid #29abe0;
      display: flex;
      flex-direction: row;
      align-items: center;
      gap: 16px;
  ">
    <!-- Left Side: Large Icon -->
    <div style="display: flex; align-items: center;">
      {icon_html}
    </div>
    
    <!-- Right Side: Three Lines Stacked Top-to-Bottom -->
    <div style="display: flex; flex-direction: column; text-align: left; gap: 4px;">
      <span style="font-size: 100px; line-height: 10; display: flex; align-items: center;">{drunk_img_html}</span>
      <span style="{text_3d_style} display: flex; align-items: center;">ችርስ</span>
      <span style="{text_3d_style}">ኣላፋቻ ሮዚና</span>
      <span style="{text_3d_style}">ሓንቲ ቢራ ንወዲ ሹቅ</span>
    </div>
  </a>
</div>
"""

# App UI Headers
#st.title("ዮቱብ፣ ፈይስብክ፣ ትዊተር ቪድዮ ዳውንሎደር ካብ ሹቅ ፕሮ ማክስ")
# App UI Headers (Centered & Two Lines using custom HTML markdown)
st.markdown(
    """
    <h1 style="text-align: center; font-size: 2.2rem; line-height: 1.3;">
        ዮቱብ፣ ፈይስብክ፣ ትዊተር ቪድዮ <br>
        ዳውንሎደር ካብ ሹቅ ፕሮ ማክስ
    </h1>
    """, 
    unsafe_allow_html=True
)
st.write("እዚ ነቶም ሳንቲም ናይ ዮቱብ ክኣርዩ ዝከውንን ዘይከውንን እንዳ ዘርጉሑ ሕብረተሰብ ዘበላሽዉ ንዘይምትብባዕ ዚተበገሰ ፕሮጀክት እዩ።")
st.write("Supports YouTube, Facebook, and X (Twitter). Downloads run directly in your browser.")

# Using a form so both hitting Enter and clicking the Search button work smoothly
with st.form(key="download_form"):
    user_url = st.text_input(
        "ሊንክ ካብ ዮቱብ፣ ፈይስብክ፣ ትዊተር ኣብዚ ግበር:", 
        placeholder="https://youtube.com... or https://x.com/... or https://facebook.com..."
    )
    
    # Submit button for the form (acts as our search button)
    submit_button = st.form_submit_button(label="🔍 ቪድዮ ድለ (Search / Prepare)")

# Extraction Function
def get_video_stream_url(video_url):
    ydl_opts = {
        'format': 'best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            stream_url = info.get('url')
            
            if not stream_url and 'formats' in info:
                combined_formats = [
                    f for f in info['formats'] 
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url')
                ]
                if combined_formats:
                    combined_formats.sort(key=lambda x: x.get('height') or 0, reverse=True)
                    stream_url = combined_formats[0]['url']

            return {
                "title": info.get('title') or info.get('description', 'video')[:30],
                "download_url": stream_url,
                "thumbnail": info.get('thumbnail')
            }
    except Exception as e:
        st.error(f"Error fetching video data: {str(e)}")
        return None

# Trigger search when the form button is clicked and text is entered
if submit_button:
    if not user_url:
        st.warning("በጃኻ ሊንክ ኣእቱ (Please enter a URL first).")
    elif not validators.url(user_url):
        st.error("በጃኻ ቅኑዕ ሊንክ ኣእቱ (Please enter a valid URL).")
    else:
        with st.spinner("ቪድዮ ብቐጥታ ይዳሎ ኣሎ..."):
            video_data = get_video_stream_url(user_url)
        
        if video_data and video_data.get('download_url'):
            st.markdown(
                f"""
                <div style="font-family: sans-serif; margin-bottom: 10px;">
                    <span style="font-size: 22px; font-weight: bold; color: #28a745;">ወዲ ሹቅ፥ ወዮ ቪድዮ ተዳልያ ኣላ</span><br>
                    <span style="font-size: 15px; color: #333; font-weight: bold;">{video_data['title']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # SIDE-BY-SIDE LAYOUT: Thumbnail on left, Download component on right
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if video_data['thumbnail']:
                    st.image(video_data['thumbnail'], use_container_width=True)
            
            with col2:
                safe_title = "".join(c for c in video_data['title'] if c.isalnum() or c in (' ', '_', '-')).strip()
                if not safe_title:
                    safe_title = "video_download"

                custom_download_html = f"""
                    <div style="display: flex; flex-direction: column; align-items: stretch; font-family: sans-serif;">
                        <a href="{video_data['download_url']}" 
                            download="{safe_title}.mp4" 
                            target="_blank"
                            rel="noopener noreferrer"
                            style="
                                background-color: #FF4B4B;
                                color: white;
                                padding: 14px 20px;
                                text-decoration: none;
                                font-size: 16px;
                                font-weight: bold;
                                border-radius: 8px;
                                text-align: center;
                                box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
                                display: block;
                            ">
                            🚀 ዳውንሎደር ክትገብር ኣብዚ ጠውቕ 
                        </a>
                        <p style="font-size: 12px; color: #555; margin-top: 8px; text-align: center; line-height: 1.3;">
                          📱 <b>Mobile Tip:</b> If it opens in a new tab, hold/tap browser menu and select <b>"Download"</b>.
                        </p>
                    </div>
                """
                components.html(custom_download_html, height=140)
        else:
            st.error("እዛ ቪድዮ ክትረክብ ኣይከኣለን። ብህዝባዊ መንገዲ (Public) ምዃኑ የረጋግጹ።")

# Render Support Widget
components.html(kofi_html, height=350)