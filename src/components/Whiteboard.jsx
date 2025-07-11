import React, { useRef, useEffect, useState, useCallback } from 'react'
import { fabric } from 'fabric'
import { 
  Pen, 
  MousePointer, 
  Square, 
  Circle, 
  Type, 
  Trash2, 
  Download,
  RotateCcw,
  Palette,
  Settings
} from 'lucide-react'
import toast from 'react-hot-toast'

const Whiteboard = ({ 
  onDrawingSubmit, 
  width = 800, 
  height = 600, 
  backgroundColor = '#ffffff',
  strokeColor = '#000000',
  strokeWidth = 3,
  ...props 
}) => {
  const canvasRef = useRef(null)
  const fabricCanvasRef = useRef(null)
  const [canvas, setCanvas] = useState(null)
  const [currentTool, setCurrentTool] = useState('pen')
  const [isDrawing, setIsDrawing] = useState(false)
  const [color, setColor] = useState(strokeColor)
  const [brushSize, setBrushSize] = useState(strokeWidth)
  const [bgColor, setBgColor] = useState(backgroundColor)

  // Initialize Fabric.js canvas
  useEffect(() => {
    if (!canvasRef.current) return

    const fabricCanvas = new fabric.Canvas(canvasRef.current, {
      width,
      height,
      backgroundColor: bgColor,
      isDrawingMode: true,
      selection: false
    })

    // Configure drawing brush
    fabricCanvas.freeDrawingBrush.width = brushSize
    fabricCanvas.freeDrawingBrush.color = color

    // Set up event listeners
    fabricCanvas.on('mouse:down', () => setIsDrawing(true))
    fabricCanvas.on('mouse:up', () => setIsDrawing(false))
    fabricCanvas.on('path:created', () => {
      // Auto-save drawing data
      const drawingData = getDrawingData()
      if (props.onDrawingChange) {
        props.onDrawingChange(drawingData)
      }
    })

    setCanvas(fabricCanvas)
    fabricCanvasRef.current = fabricCanvas

    return () => {
      fabricCanvas.dispose()
    }
  }, [width, height])

  // Update brush properties when color or size changes
  useEffect(() => {
    if (!canvas) return

    canvas.freeDrawingBrush.color = color
    canvas.freeDrawingBrush.width = brushSize
  }, [color, brushSize, canvas])

  // Update background color
  useEffect(() => {
    if (!canvas) return
    canvas.setBackgroundColor(bgColor, () => canvas.renderAll())
  }, [bgColor, canvas])

  // Get drawing data for analysis
  const getDrawingData = useCallback(() => {
    if (!canvas) return { objects: [] }

    const objects = canvas.getObjects().map(obj => ({
      type: obj.type,
      left: obj.left,
      top: obj.top,
      width: obj.width,
      height: obj.height,
      stroke: obj.stroke,
      strokeWidth: obj.strokeWidth,
      fill: obj.fill,
      text: obj.text,
      path: obj.path,
      radius: obj.radius,
      rx: obj.rx,
      ry: obj.ry
    }))

    return {
      objects,
      backgroundColor: bgColor,
      width: canvas.width,
      height: canvas.height
    }
  }, [canvas, bgColor])

  // Tool handlers
  const setTool = (tool) => {
    if (!canvas) return

    setCurrentTool(tool)
    canvas.isDrawingMode = tool === 'pen'
    canvas.selection = tool === 'select'

    // Clear selection when switching tools
    canvas.discardActiveObject()
    canvas.renderAll()
  }

  const addShape = (shapeType) => {
    if (!canvas) return

    let shape
    const centerX = canvas.width / 2
    const centerY = canvas.height / 2

    switch (shapeType) {
      case 'rect':
        shape = new fabric.Rect({
          left: centerX - 50,
          top: centerY - 30,
          width: 100,
          height: 60,
          fill: 'transparent',
          stroke: color,
          strokeWidth: brushSize
        })
        break
      case 'circle':
        shape = new fabric.Circle({
          left: centerX - 30,
          top: centerY - 30,
          radius: 30,
          fill: 'transparent',
          stroke: color,
          strokeWidth: brushSize
        })
        break
      case 'line':
        shape = new fabric.Line([centerX - 50, centerY, centerX + 50, centerY], {
          stroke: color,
          strokeWidth: brushSize
        })
        break
      default:
        return
    }

    canvas.add(shape)
    canvas.setActiveObject(shape)
    canvas.renderAll()
  }

  const addText = () => {
    if (!canvas) return

    const text = new fabric.IText('Double click to edit', {
      left: canvas.width / 2,
      top: canvas.height / 2,
      fontSize: 20,
      fill: color,
      fontFamily: 'Inter'
    })

    canvas.add(text)
    canvas.setActiveObject(text)
    canvas.renderAll()
  }

  const clearCanvas = () => {
    if (!canvas) return

    canvas.clear()
    canvas.setBackgroundColor(bgColor, () => canvas.renderAll())
    toast.success('Canvas cleared')
  }

  const undo = () => {
    if (!canvas) return

    const objects = canvas.getObjects()
    if (objects.length > 0) {
      canvas.remove(objects[objects.length - 1])
      canvas.renderAll()
      toast.success('Undone')
    }
  }

  const downloadCanvas = () => {
    if (!canvas) return

    const dataURL = canvas.toDataURL({
      format: 'png',
      quality: 1
    })

    const link = document.createElement('a')
    link.download = `whiteboard-${Date.now()}.png`
    link.href = dataURL
    link.click()
    toast.success('Drawing downloaded')
  }

  const submitDrawing = async () => {
    if (!canvas) return

    const drawingData = getDrawingData()
    
    if (drawingData.objects.length === 0) {
      toast.error('Please draw something first')
      return
    }

    if (onDrawingSubmit) {
      try {
        await onDrawingSubmit(drawingData)
        toast.success('Drawing submitted for analysis')
      } catch (error) {
        toast.error('Failed to submit drawing')
        console.error('Submit error:', error)
      }
    }
  }

  const tools = [
    { id: 'select', icon: MousePointer, label: 'Select' },
    { id: 'pen', icon: Pen, label: 'Draw' },
    { id: 'rect', icon: Square, label: 'Rectangle' },
    { id: 'circle', icon: Circle, label: 'Circle' },
    { id: 'text', icon: Type, label: 'Text' }
  ]

  return (
    <div className="flex flex-col space-y-4">
      {/* Toolbar */}
      <div className="flex items-center justify-between bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="flex items-center space-x-2">
          {tools.map((tool) => (
            <button
              key={tool.id}
              onClick={() => setTool(tool.id)}
              className={`p-2 rounded-lg transition-colors ${
                currentTool === tool.id
                  ? 'bg-primary-100 text-primary-600'
                  : 'hover:bg-gray-100 text-gray-600'
              }`}
              title={tool.label}
            >
              <tool.icon size={20} />
            </button>
          ))}
        </div>

        <div className="flex items-center space-x-4">
          {/* Color picker */}
          <div className="flex items-center space-x-2">
            <Palette size={20} className="text-gray-600" />
            <input
              type="color"
              value={color}
              onChange={(e) => setColor(e.target.value)}
              className="w-8 h-8 rounded border border-gray-300 cursor-pointer"
            />
          </div>

          {/* Brush size */}
          <div className="flex items-center space-x-2">
            <Settings size={20} className="text-gray-600" />
            <input
              type="range"
              min="1"
              max="20"
              value={brushSize}
              onChange={(e) => setBrushSize(parseInt(e.target.value))}
              className="w-20"
            />
            <span className="text-sm text-gray-600 w-6">{brushSize}</span>
          </div>

          {/* Background color */}
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-600">BG:</span>
            <input
              type="color"
              value={bgColor}
              onChange={(e) => setBgColor(e.target.value)}
              className="w-8 h-8 rounded border border-gray-300 cursor-pointer"
            />
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={undo}
            className="p-2 rounded-lg hover:bg-gray-100 text-gray-600"
            title="Undo"
          >
            <RotateCcw size={20} />
          </button>
          <button
            onClick={clearCanvas}
            className="p-2 rounded-lg hover:bg-red-100 text-red-600"
            title="Clear Canvas"
          >
            <Trash2 size={20} />
          </button>
          <button
            onClick={downloadCanvas}
            className="p-2 rounded-lg hover:bg-gray-100 text-gray-600"
            title="Download"
          >
            <Download size={20} />
          </button>
        </div>
      </div>

      {/* Canvas */}
      <div className="relative">
        <canvas
          ref={canvasRef}
          className="border border-gray-300 rounded-lg shadow-sm"
        />
        
        {/* Drawing indicator */}
        {isDrawing && (
          <div className="absolute top-2 right-2 bg-primary-600 text-white px-2 py-1 rounded text-xs">
            Drawing...
          </div>
        )}
      </div>

      {/* Submit button */}
      <div className="flex justify-center">
        <button
          onClick={submitDrawing}
          disabled={!canvas || canvas.getObjects().length === 0}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Submit Drawing for Analysis
        </button>
      </div>
    </div>
  )
}

export default Whiteboard 