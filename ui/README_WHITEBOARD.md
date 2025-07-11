# ✏️ Smart Whiteboard UI

A modern, AI-powered drawing interface for STEM education built with Streamlit and integrated with the tutoring agent architecture.

## 🚀 Features

### Drawing Interface
- **Interactive Canvas**: Draw equations, diagrams, and free body sketches
- **Multiple Tools**: Freehand drawing, lines, rectangles, circles
- **Customizable**: Stroke width, colors, canvas size
- **Real-time Preview**: See your drawing as you create it

### AI Integration
- **Drawing Analysis**: Automatic detection of content type and complexity
- **Misconception Detection**: Identifies common errors in STEM drawings
- **Socratic Questioning**: Generates contextual follow-up questions
- **Visual Scaffolding**: Suggests improvements and next steps

### Chat Interface
- **Conversational AI**: Natural dialogue with the tutoring agent
- **Context Awareness**: Remembers previous interactions
- **Session Tracking**: Monitors progress and misconceptions addressed

## 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Whiteboard**:
   ```bash
   python3 run_whiteboard.py
   ```

3. **Access the Interface**:
   Open your browser to `http://localhost:8501`

## 📖 Usage

### Basic Drawing
1. **Select a Tool**: Choose from freehand, line, rectangle, or circle
2. **Adjust Settings**: Set stroke width and colors in the sidebar
3. **Draw**: Use your mouse or stylus to create on the canvas
4. **Submit**: Click "Submit Drawing" to analyze your work

### AI Tutoring
1. **Get Analysis**: The AI will analyze your drawing and provide feedback
2. **Respond**: Answer the AI's questions in the chat area
3. **Iterate**: Use the feedback to improve your drawing
4. **Track Progress**: Monitor your session in the sidebar

### Advanced Features
- **Subject Selection**: Choose from Statics, Dynamics, Thermodynamics, etc.
- **Topic Focus**: Select specific topics like Free Body Diagrams
- **Session Management**: Start new sessions or continue previous ones
- **Export**: Save your drawings as PNG images

## 🔧 Architecture

### Core Components
```
ui/
├── smart_whiteboard.py      # Main Streamlit interface
├── whiteboard_integration.py # Tutoring agent integration
└── README_WHITEBOARD.md     # This file
```

### Integration Points
- **Canvas Data**: Drawing information passed to analysis modules
- **Tutoring Agent**: Full integration with misconception detection and Socratic questioning
- **Session State**: Persistent conversation and progress tracking
- **Visual Feedback**: Real-time suggestions and scaffolding

## 🎯 Use Cases

### STEM Education
- **Physics**: Free body diagrams, force analysis
- **Engineering**: Circuit diagrams, structural analysis
- **Mathematics**: Equation solving, geometric proofs
- **Chemistry**: Molecular structures, reaction mechanisms

### Adaptive Learning
- **Misconception Detection**: Identifies common student errors
- **Personalized Feedback**: Tailored responses based on drawing analysis
- **Progressive Scaffolding**: Gradual complexity increase
- **Concept Reinforcement**: Multiple representations of the same concept

## 🔮 Future Enhancements

### Handwriting Recognition
- **Math OCR**: Integration with Mathpix or LaTeX-OCR
- **Symbol Recognition**: Automatic detection of mathematical symbols
- **Equation Parsing**: Convert handwritten equations to LaTeX

### Advanced AI
- **GPT-4o Integration**: Enhanced natural language understanding
- **Claude Integration**: Alternative AI reasoning capabilities
- **Multi-modal Analysis**: Combined text and visual understanding

### Enhanced Features
- **Collaborative Drawing**: Multi-user whiteboard sessions
- **Template Library**: Pre-built diagrams and equations
- **Export Options**: PDF, LaTeX, or interactive formats
- **Mobile Support**: Touch-optimized interface

## 🐛 Troubleshooting

### Common Issues
1. **Canvas Not Loading**: Check if `streamlit-drawable-canvas` is installed
2. **Integration Errors**: Ensure all core modules are available
3. **Performance Issues**: Reduce canvas size for better performance
4. **Browser Compatibility**: Use modern browsers (Chrome, Firefox, Safari)

### Debug Mode
Run with debug information:
```bash
streamlit run ui/smart_whiteboard.py --logger.level debug
```

## 📝 Development

### Adding New Features
1. **Canvas Tools**: Extend the drawing capabilities
2. **Analysis Modules**: Add new content recognition
3. **Subject Modules**: Create domain-specific tutoring
4. **UI Components**: Enhance the user interface

### Testing
```bash
# Run the whiteboard in test mode
python3 -m pytest tests/test_whiteboard.py

# Manual testing
python3 run_whiteboard.py
```

## 🤝 Contributing

1. **Fork the Repository**
2. **Create a Feature Branch**
3. **Make Your Changes**
4. **Test Thoroughly**
5. **Submit a Pull Request**

## 📄 License

This project is part of the TeachingAssistant system. See the main README for licensing information.

---

**Ready to start drawing?** Run `python3 run_whiteboard.py` and begin your AI-powered learning journey! 🚀 