import streamlit as st
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Page configuration
st.set_page_config(
    page_title="Smart Whiteboard - AI Tutoring",
    page_icon="✏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .canvas-container {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 10px;
        background: white;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .ai-message {
        background-color: #f0f8ff;
        border-left: 4px solid #1f77b4;
    }
    .user-message {
        background-color: #f0fff0;
        border-left: 4px solid #2ca02c;
    }
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        height: 3rem;
        font-size: 1.1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'canvas_data' not in st.session_state:
    st.session_state.canvas_data = None

# Import the integration module
try:
    from ui.whiteboard_integration import tutoring_agent, DrawingAnalysis
    INTEGRATION_AVAILABLE = True
except ImportError:
    INTEGRATION_AVAILABLE = False
    print("Warning: Tutoring agent integration not available")

def analyze_drawing(canvas_data):
    """
    Analyze the drawing using the tutoring agent integration.
    
    Args:
        canvas_data: The canvas data from streamlit-drawable-canvas
        
    Returns:
        dict: Analysis results including detected content and suggestions
    """
    if INTEGRATION_AVAILABLE:
        # Use the tutoring agent for analysis
        analysis = tutoring_agent.analyze_drawing(canvas_data, subject, topic)
        
        return {
            "detected_content": f"{analysis.content_type} with {', '.join(analysis.detected_elements)}",
            "confidence": analysis.confidence,
            "suggestions": analysis.suggestions,
            "next_question": analysis.next_question,
            "misconceptions": analysis.misconceptions,
            "visual_scaffolding": analysis.visual_scaffolding
        }
    else:
        # Fallback to placeholder analysis
        return {
            "detected_content": "Free body diagram with forces",
            "confidence": 0.85,
            "suggestions": [
                "I see you've drawn a free body diagram. Let me ask: What forces are acting on this object?",
                "Consider: Are there any forces you might have missed?",
                "Think about: What direction is the net force pointing?"
            ],
            "next_question": "What is the magnitude of the normal force in your diagram?"
        }

def generate_socratic_response(analysis_result):
    """
    Generate Socratic-style questions based on drawing analysis.
    
    Args:
        analysis_result: Results from analyze_drawing()
        
    Returns:
        str: Socratic question or feedback
    """
    if INTEGRATION_AVAILABLE and "misconceptions" in analysis_result:
        # Use the tutoring agent for more sophisticated responses
        if analysis_result["misconceptions"]:
            misconception_text = ", ".join(analysis_result["misconceptions"])
            return f"I notice some potential issues: {misconception_text}. {analysis_result['next_question']}"
        else:
            return f"Excellent work! {analysis_result['next_question']}"
    else:
        # Fallback to simple response
        if analysis_result["confidence"] > 0.8:
            return f"Great! I can see you've drawn {analysis_result['detected_content']}. {analysis_result['next_question']}"
        else:
            return "I'm not quite sure what you've drawn. Could you try drawing it again, or tell me what you're trying to represent?"

def save_canvas_as_image(canvas_data):
    """
    Convert canvas data to PIL Image for processing.
    
    Args:
        canvas_data: Canvas data from streamlit-drawable-canvas
        
    Returns:
        PIL.Image: The canvas as an image
    """
    if canvas_data is not None and canvas_data.json_data is not None:
        # Convert canvas to image
        canvas_image = Image.fromarray(canvas_data.image_data)
        return canvas_image
    return None

def main():
    # Header
    st.markdown('<h1 class="main-header">✏️ Smart Whiteboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Draw equations, diagrams, and sketches for AI-powered tutoring</p>', unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎨 Canvas Controls")
        
        # Tool selection
        tool_mode = st.selectbox(
            "Drawing Tool",
            ["freedraw", "line", "rect", "circle"],
            format_func=lambda x: x.title()
        )
        
        # Stroke settings
        stroke_width = st.slider("Stroke Width", 1, 20, 3)
        stroke_color = st.color_picker("Stroke Color", "#000000")
        
        # Background settings
        bg_color = st.color_picker("Background Color", "#ffffff")
        
        # Canvas size
        canvas_width = st.slider("Canvas Width", 400, 800, 600)
        canvas_height = st.slider("Canvas Height", 300, 600, 400)
        
        st.markdown("---")
        st.markdown("### 📚 Subject Selection")
        subject = st.selectbox(
            "Choose Subject",
            ["Statics", "Dynamics", "Thermodynamics", "Fluid Mechanics"],
            index=0
        )
        
        topic = st.selectbox(
            "Choose Topic",
            ["Free Body Diagrams", "Force Analysis", "Moment Calculations", "Equilibrium"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 🔧 Advanced Options")
        enable_math_recognition = st.checkbox("Enable Math Recognition", value=True)
        enable_diagram_analysis = st.checkbox("Enable Diagram Analysis", value=True)
        
        # Clear canvas button
        if st.button("🗑️ Clear Canvas"):
            st.session_state.canvas_data = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Session Summary")
        
        if INTEGRATION_AVAILABLE:
            summary = tutoring_agent.get_session_summary()
            st.metric("Session Length", summary["session_length"])
            st.metric("Misconceptions Addressed", summary["misconceptions_addressed"])
            st.metric("Questions Asked", summary["questions_asked"])
        else:
            st.info("Session tracking available with full integration")

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
        
        # Canvas component
        canvas_result = st_canvas(
            fill_color=bg_color,
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            width=canvas_width,
            height=canvas_height,
            drawing_mode=tool_mode,
            key="smart_whiteboard_canvas",
            display_toolbar=True,
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        col_button1, col_button2, col_button3 = st.columns([1, 1, 1])
        
        with col_button2:
            if st.button("🚀 Submit Drawing", type="primary"):
                if canvas_result.json_data is not None:
                    # Store canvas data
                    st.session_state.canvas_data = canvas_result
                    
                    # Analyze drawing (placeholder)
                    with st.spinner("🤖 Analyzing your drawing..."):
                        analysis_result = analyze_drawing(canvas_result)
                    
                    # Generate response
                    ai_response = generate_socratic_response(analysis_result)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "type": "ai",
                        "message": ai_response,
                        "analysis": analysis_result
                    })
                    
                    st.success("Analysis complete! Check the chat below.")
                    st.rerun()
                else:
                    st.error("Please draw something on the canvas first!")
    
    with col2:
        st.header("📊 Drawing Info")
        
        if st.session_state.canvas_data is not None:
            # Display canvas statistics
            canvas_data = st.session_state.canvas_data
            
            if canvas_data.json_data is not None:
                st.metric("Objects Drawn", len(canvas_data.json_data["objects"]))
                
                # Show drawing objects
                if canvas_data.json_data["objects"]:
                    st.subheader("Drawing Objects:")
                    for i, obj in enumerate(canvas_data.json_data["objects"][-5:]):  # Show last 5
                        st.write(f"• {obj.get('type', 'Unknown')} (Object {i+1})")
                
                # Save image option
                if st.button("💾 Save as Image"):
                    image = save_canvas_as_image(canvas_data)
                    if image:
                        # Convert to bytes for download
                        buf = BytesIO()
                        image.save(buf, format='PNG')
                        byte_im = buf.getvalue()
                        
                        st.download_button(
                            label="📥 Download PNG",
                            data=byte_im,
                            file_name="whiteboard_drawing.png",
                            mime="image/png"
                        )
        else:
            st.info("Draw something to see analysis options!")
    
    # Chat area
    st.markdown("---")
    st.header("💬 AI Tutoring Chat")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["type"] == "ai":
            st.markdown(f"""
            <div class="chat-message ai-message">
                <strong>🤖 AI Tutor:</strong> {message["message"]}
            </div>
            """, unsafe_allow_html=True)
            
            # Show analysis details in expander
            if "analysis" in message:
                with st.expander("🔍 Analysis Details"):
                    st.json(message["analysis"])
    
    # User input area
    st.markdown("---")
    user_input = st.text_area(
        "💭 Your response to the AI tutor:",
        placeholder="Type your answer or ask a question...",
        height=100
    )
    
    col_input1, col_input2 = st.columns([3, 1])
    
    with col_input1:
        if st.button("📤 Send Response"):
            if user_input.strip():
                # Add user response to chat history
                st.session_state.chat_history.append({
                    "type": "user",
                    "message": user_input
                })
                
                # Generate AI response using tutoring agent
                if INTEGRATION_AVAILABLE and st.session_state.chat_history:
                    # Get the last AI analysis if available
                    last_analysis = None
                    for msg in reversed(st.session_state.chat_history):
                        if msg.get("type") == "ai" and "analysis" in msg:
                            last_analysis = msg["analysis"]
                            break
                    
                    if last_analysis:
                        ai_response = tutoring_agent.process_student_response(user_input, last_analysis)
                        st.session_state.chat_history.append({
                            "type": "ai",
                            "message": ai_response
                        })
                
                st.rerun()
            else:
                st.warning("Please enter a response!")
    
    with col_input2:
        if st.button("🔄 New Session"):
            st.session_state.chat_history = []
            st.session_state.canvas_data = None
            st.rerun()

if __name__ == "__main__":
    main() 