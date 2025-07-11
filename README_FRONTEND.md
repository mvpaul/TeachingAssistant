# 🎨 Smart Whiteboard Frontend

A modern React + Tailwind + Vite frontend for the AI-powered Smart Whiteboard tutoring system. This provides a sleek, responsive interface for drawing, AI tutoring, and problem-solving.

## 🚀 Features

### Core Components
- **Whiteboard**: Interactive drawing canvas using Fabric.js
- **ChatBox**: Real-time AI tutoring conversation
- **Sidebar**: Subject/topic selection and session management
- **ProblemSelector**: Browse and launch structured problems
- **FileUploader**: Upload course materials and PDFs

### AI Integration
- **Misconception Detection**: Real-time analysis of drawings and responses
- **Socratic Questioning**: Contextual follow-up questions
- **Session Tracking**: Progress monitoring and analytics
- **Visual Scaffolding**: Suggestions for improving drawings

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Feedback**: Instant AI analysis and suggestions
- **Session Management**: Save, export, and resume sessions
- **Problem Library**: Curated problems with difficulty levels

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Fabric.js** - Canvas drawing library
- **React Router** - Client-side routing
- **Lucide React** - Beautiful icons
- **React Hot Toast** - Toast notifications
- **React Markdown** - Markdown rendering

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd TeachingAssistant
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Open in browser**:
   Navigate to `http://localhost:3000`

## 🏗️ Project Structure

```
src/
├── components/           # React components
│   ├── Whiteboard.jsx   # Drawing canvas
│   ├── ChatBox.jsx      # AI conversation
│   ├── Sidebar.jsx      # Settings & progress
│   ├── FileUploader.jsx # File upload
│   ├── ProblemSelector.jsx # Problem library
│   └── AIEngine.js      # AI integration
├── pages/               # Page components
│   ├── index.jsx        # Homepage
│   └── problem/
│       └── [id].jsx     # Problem viewer
├── utils/               # Utility functions
│   ├── misconceptionDetector.js
│   ├── socraticFlowEngine.js
│   └── sessionTracker.js
├── App.jsx              # Main app component
├── main.jsx             # Entry point
└── index.css            # Global styles
```

## 🎯 Usage

### Getting Started

1. **Launch the app** and you'll see the main whiteboard interface
2. **Select a subject** (Statics, Dynamics, etc.) from the sidebar
3. **Choose a topic** (Free Body Diagrams, Force Analysis, etc.)
4. **Start drawing** on the canvas using the toolbar tools
5. **Submit your drawing** for AI analysis
6. **Chat with the AI tutor** to get feedback and guidance

### Drawing Tools

- **Pen**: Freehand drawing
- **Select**: Move and edit objects
- **Rectangle**: Draw rectangles
- **Circle**: Draw circles
- **Text**: Add text labels
- **Color Picker**: Change stroke color
- **Brush Size**: Adjust stroke width
- **Background**: Change canvas background

### Problem Solving

1. **Browse problems** in the Problem Library
2. **Filter by difficulty** (Beginner, Intermediate, Advanced)
3. **Select a problem** to start
4. **Follow instructions** and use hints
5. **Draw your solution** on the whiteboard
6. **Get AI feedback** in real-time

### File Upload

1. **Upload course materials** (PDFs, images)
2. **Drag and drop** or click to select files
3. **Supported formats**: PDF, PNG, JPG, JPEG
4. **File size limit**: 10MB per file

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_ENDPOINT=http://localhost:8000/api
VITE_AI_MODEL=gpt-4o
VITE_MAX_TOKENS=1000
VITE_TEMPERATURE=0.7
```

### Customization

#### Styling
- Modify `tailwind.config.js` for theme customization
- Update `src/index.css` for global styles
- Component-specific styles are in each component file

#### AI Integration
- Configure AI endpoints in `src/components/AIEngine.js`
- Add new misconception patterns in `src/utils/misconceptionDetector.js`
- Extend question templates in `src/utils/socraticFlowEngine.js`

#### Problem Library
- Add new problems in `src/pages/problem/[id].jsx`
- Extend subjects and topics in `src/components/ProblemSelector.jsx`

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

### Deploy to Netlify

1. **Build the project**:
   ```bash
   npm run build
   ```

2. **Deploy the `dist` folder** to Netlify

## 🔌 API Integration

The frontend is designed to work with the Python backend. Key integration points:

### Drawing Analysis
```javascript
const analysis = await aiEngine.analyzeDrawing(drawingData, {
  subject: 'statics',
  topic: 'free_body_diagrams'
})
```

### Response Processing
```javascript
const response = await aiEngine.processResponse(message, {
  subject: 'statics',
  topic: 'free_body_diagrams'
})
```

### Session Management
```javascript
sessionTracker.createSession(sessionId, {
  subject: 'statics',
  topic: 'free_body_diagrams'
})
```

## 🧪 Testing

### Run Tests
```bash
npm test
```

### Run Linter
```bash
npm run lint
```

### Format Code
```bash
npm run format
```

## 📱 Responsive Design

The interface is fully responsive and works on:

- **Desktop**: Full-featured experience with sidebar
- **Tablet**: Optimized layout with collapsible sidebar
- **Mobile**: Touch-friendly interface with simplified controls

## 🎨 Design System

### Colors
- **Primary**: Blue (#3B82F6) - Main actions and highlights
- **Secondary**: Gray (#64748B) - Text and borders
- **Accent**: Green (#22C55E) - Success and progress
- **Error**: Red (#EF4444) - Errors and warnings

### Typography
- **Font Family**: Inter (sans-serif)
- **Code Font**: JetBrains Mono (monospace)
- **Weights**: 300, 400, 500, 600, 700

### Components
- **Buttons**: Primary, secondary, and danger variants
- **Cards**: Consistent padding and shadows
- **Inputs**: Focus states and validation
- **Modals**: Overlay and backdrop blur

## 🔮 Future Enhancements

### Planned Features
- **Real-time Collaboration**: Multi-user whiteboard sessions
- **Advanced AI Models**: GPT-4o and Claude integration
- **Handwriting Recognition**: Math OCR and LaTeX conversion
- **Video Recording**: Session playback and analysis
- **Mobile App**: Native iOS and Android apps

### Technical Improvements
- **Performance**: Virtual scrolling for large chat histories
- **Offline Support**: Service worker for offline functionality
- **Accessibility**: WCAG 2.1 AA compliance
- **Internationalization**: Multi-language support

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests** for new functionality
5. **Update documentation**
6. **Submit a pull request**

### Development Guidelines

- **Code Style**: Use Prettier and ESLint
- **Components**: Functional components with hooks
- **State Management**: Local state with React hooks
- **Styling**: Tailwind CSS utility classes
- **Testing**: Jest and React Testing Library

## 📄 License

This project is part of the TeachingAssistant system. See the main README for licensing information.

## 🆘 Support

For issues and questions:

1. **Check the documentation** in this README
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Contact the development team**

---

**Ready to start building?** Run `npm run dev` and begin creating amazing AI-powered tutoring experiences! 🚀 