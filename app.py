import streamlit as st
import streamlit.components.v1 as components

# Initialize session state
if "mic_on" not in st.session_state:
    st.session_state.mic_on = False

# Page configuration
st.set_page_config(page_title="Netflix Voice Search", layout="centered")

# CSS Styles
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: #FFFFFF;
        }
        .title {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: #E50914;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .subtitle {
            font-size: 20px;
            text-align: center;
            color: #B3B3B3;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 40px 0;
        }
        .mic-container {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            min-height: 64px;
        }
        .sound-waves {
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .wave {
            width: 4px;
            background-color: #FFFFFF;
            margin: 0 3px;
            border-radius: 2px;
            transition: background-color 0.3s ease;
        }
        .sound-waves.active .wave {
            background-color: #E50914;
            animation-timing-function: ease-in-out;
            animation-iteration-count: infinite;
            animation-direction: alternate;
        }
        .wave1 {
            height: 20px;
        }
        .wave2 {
            height: 30px;
        }
        .wave3 {
            height: 25px;
        }
        .wave4 {
            height: 35px;
        }
        .wave5 {
            height: 22px;
        }
        .sound-waves.active .wave1 {
            animation-name: wave-animation;
            animation-duration: 0.8s;
        }
        .sound-waves.active .wave2 {
            animation-name: wave-animation;
            animation-duration: 0.7s;
            animation-delay: 0.1s;
        }
        .sound-waves.active .wave3 {
            animation-name: wave-animation;
            animation-duration: 0.9s;
            animation-delay: 0.2s;
        }
        .sound-waves.active .wave4 {
            animation-name: wave-animation;
            animation-duration: 0.6s;
            animation-delay: 0.3s;
        }
        .sound-waves.active .wave5 {
            animation-name: wave-animation;
            animation-duration: 0.8s;
            animation-delay: 0.4s;
        }
        @keyframes wave-animation {
            0% { transform: scaleY(0.3); }
            100% { transform: scaleY(1); }
        }
        .prompt-text {
            text-align: center;
            font-size: 18px;
            color: #B3B3B3;
        }
    </style>
""", unsafe_allow_html=True)

# Title and subtitle
st.markdown('<div class="title">Netflix Voice Search</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find the perfect movie or show with your voice</div>', unsafe_allow_html=True)

# Sound waves HTML
active_class = "active" if st.session_state.mic_on else ""
waves_html = f"""
<div class="center">
    <div class="mic-container" onclick="window.parent.postMessage('mic_toggle', '*')">
        <div class="sound-waves {active_class}">
            <div class="wave wave1"></div>
            <div class="wave wave2"></div>
            <div class="wave wave3"></div>
            <div class="wave wave4"></div>
            <div class="wave wave5"></div>
        </div>
    </div>
</div>

<style>
    .center {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 40px 0;
    }}
    .mic-container {{
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        min-height: 64px;
    }}
    .sound-waves {{
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }}
    .wave {{
        width: 4px;
        background-color: #FFFFFF;
        margin: 0 3px;
        border-radius: 2px;
        transition: background-color 0.3s ease;
    }}
    .sound-waves.active .wave {{
        background-color: #E50914;
        animation-timing-function: ease-in-out;
        animation-iteration-count: infinite;
        animation-direction: alternate;
    }}
    .wave1 {{
        height: 20px;
    }}
    .wave2 {{
        height: 30px;
    }}
    .wave3 {{
        height: 25px;
    }}
    .wave4 {{
        height: 35px;
    }}
    .wave5 {{
        height: 22px;
    }}
    .sound-waves.active .wave1 {{
        animation-name: wave-animation;
        animation-duration: 0.8s;
    }}
    .sound-waves.active .wave2 {{
        animation-name: wave-animation;
        animation-duration: 0.7s;
        animation-delay: 0.1s;
    }}
    .sound-waves.active .wave3 {{
        animation-name: wave-animation;
        animation-duration: 0.9s;
        animation-delay: 0.2s;
    }}
    .sound-waves.active .wave4 {{
        animation-name: wave-animation;
        animation-duration: 0.6s;
        animation-delay: 0.3s;
    }}
    .sound-waves.active .wave5 {{
        animation-name: wave-animation;
        animation-duration: 0.8s;
        animation-delay: 0.4s;
    }}
    @keyframes wave-animation {{
        0% {{ transform: scaleY(0.3); }}
        100% {{ transform: scaleY(1); }}
    }}
</style>
"""

# Render the sound waves
components.html(waves_html, height=120)

# Prompt text
if st.session_state.mic_on:
    st.markdown('<div class="prompt-text">🎙️ Listening... Speak now!</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="prompt-text">Let me know what kind of content you want to watch. I am listening...</div>', unsafe_allow_html=True)
# Handle mic toggle via query parameters
if "mic" in st.query_params:
    st.session_state.mic_on = not st.session_state.mic_on
    del st.query_params["mic"]
    st.rerun()

# JavaScript to handle clicks
st.markdown("""
<script>
    window.addEventListener("message", (event) => {
        if (event.data === "mic_toggle") {
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set("mic", "toggle");
            window.location.href = currentUrl.toString();
        }
    });
</script>
""", unsafe_allow_html=True)
