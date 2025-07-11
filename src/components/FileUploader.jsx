import React, { useState, useRef } from 'react'
import { Upload, FileText, X, CheckCircle, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'

const FileUploader = ({ onFileUpload, acceptedTypes = ['.pdf', '.png', '.jpg', '.jpeg'], className = '' }) => {
  const [isDragOver, setIsDragOver] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [isUploading, setIsUploading] = useState(false)
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragOver(false)
    
    const files = Array.from(e.dataTransfer.files)
    handleFiles(files)
  }

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files)
    handleFiles(files)
  }

  const handleFiles = async (files) => {
    const validFiles = files.filter(file => {
      const isValidType = acceptedTypes.some(type => 
        file.name.toLowerCase().endsWith(type.replace('.', ''))
      )
      
      if (!isValidType) {
        toast.error(`${file.name} is not a supported file type`)
        return false
      }
      
      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        toast.error(`${file.name} is too large (max 10MB)`)
        return false
      }
      
      return true
    })

    if (validFiles.length === 0) return

    setIsUploading(true)

    try {
      const processedFiles = await Promise.all(
        validFiles.map(async (file) => {
          const fileData = await processFile(file)
          return {
            id: Date.now() + Math.random(),
            name: file.name,
            size: file.size,
            type: file.type,
            data: fileData,
            status: 'uploaded'
          }
        })
      )

      setUploadedFiles(prev => [...prev, ...processedFiles])
      
      // Call parent callback
      if (onFileUpload) {
        await onFileUpload(processedFiles)
      }

      toast.success(`${validFiles.length} file(s) uploaded successfully`)
    } catch (error) {
      console.error('File upload error:', error)
      toast.error('Failed to upload files')
    } finally {
      setIsUploading(false)
    }
  }

  const processFile = async (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      
      reader.onload = (e) => {
        resolve({
          content: e.target.result,
          base64: e.target.result.split(',')[1]
        })
      }
      
      reader.onerror = () => reject(new Error('Failed to read file'))
      
      if (file.type.startsWith('image/')) {
        reader.readAsDataURL(file)
      } else {
        reader.readAsArrayBuffer(file)
      }
    })
  }

  const removeFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId))
    toast.success('File removed')
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop()?.toLowerCase()
    
    switch (extension) {
      case 'pdf':
        return <FileText size={20} className="text-red-500" />
      case 'png':
      case 'jpg':
      case 'jpeg':
        return <FileText size={20} className="text-blue-500" />
      default:
        return <FileText size={20} className="text-gray-500" />
    }
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
          isDragOver
            ? 'border-primary-400 bg-primary-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <Upload size={48} className="mx-auto mb-4 text-gray-400" />
        
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Upload Course Materials
        </h3>
        
        <p className="text-sm text-gray-600 mb-4">
          Drag and drop files here, or click to select files
        </p>
        
        <div className="text-xs text-gray-500 mb-4">
          Supported formats: {acceptedTypes.join(', ')} (max 10MB each)
        </div>
        
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={isUploading}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isUploading ? 'Uploading...' : 'Choose Files'}
        </button>
        
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={acceptedTypes.join(',')}
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>

      {/* Uploaded Files */}
      {uploadedFiles.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-medium text-gray-700">Uploaded Files</h4>
          
          <div className="space-y-2">
            {uploadedFiles.map((file) => (
              <div
                key={file.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  {getFileIcon(file.name)}
                  <div>
                    <div className="text-sm font-medium text-gray-900">
                      {file.name}
                    </div>
                    <div className="text-xs text-gray-500">
                      {formatFileSize(file.size)}
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  {file.status === 'uploaded' && (
                    <CheckCircle size={16} className="text-green-500" />
                  )}
                  
                  <button
                    onClick={() => removeFile(file.id)}
                    className="p-1 rounded hover:bg-red-100 text-red-600"
                    title="Remove file"
                  >
                    <X size={16} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Upload Progress */}
      {isUploading && (
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
          <span>Processing files...</span>
        </div>
      )}
    </div>
  )
}

export default FileUploader 