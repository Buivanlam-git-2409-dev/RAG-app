import React from 'react'
import { useState, useCallback } from 'react'

export default function FileUpload({ onUpload }) {
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null)

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
  }, [])

  const handleDragIn = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }, [])

  const handleDragOut = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFile(files[0])
    }
  }, [])

  const handleFileSelect = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFile = async (file) => {
    const validTypes = ['application/pdf', 'text/plain']
    if (!validTypes.includes(file.type)) {
      setUploadStatus({ type: 'error', message: 'Only PDF and TXT files are supported' })
      setTimeout(() => setUploadStatus(null), 3000)
      return
    }

    setIsUploading(true)
    setUploadStatus(null)

    const result = await onUpload(file)

    setIsUploading(false)
    if (result.success) {
      setUploadStatus({ type: 'success', message: 'Document uploaded successfully' })
      setTimeout(() => setUploadStatus(null), 3000)
    } else {
      setUploadStatus({ type: 'error', message: result.error || 'Upload failed' })
    }
  }

  return (
    <div className="mb-8">
      <h2 className="font-display text-lg font-medium text-text-primary mb-4">
        Upload Document
      </h2>

      <div
        onDragEnter={handleDragIn}
        onDragLeave={handleDragOut}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300
          ${isDragging
            ? 'border-accent bg-accent/5'
            : 'border-void-border hover:border-text-muted'
          }
          ${isUploading ? 'pointer-events-none opacity-60' : 'cursor-pointer'}
        `}
      >
        <input
          type="file"
          accept=".pdf,.txt"
          onChange={handleFileSelect}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          disabled={isUploading}
        />

        <div className="space-y-3">
          <div className="w-12 h-12 mx-auto rounded-full bg-void-border flex items-center justify-center">
            <svg className="w-6 h-6 text-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>

          <div>
            <p className="font-body text-text-primary text-lg">
              {isUploading ? 'Uploading...' : 'Drop file here'}
            </p>
            <p className="font-mono text-xs text-text-muted mt-1">
              PDF, TXT
            </p>
          </div>
        </div>
      </div>

      {uploadStatus && (
        <div
          className={`
            mt-3 p-3 rounded-lg text-sm font-mono
            ${uploadStatus.type === 'success'
              ? 'bg-accent/10 text-accent'
              : 'bg-red-500/10 text-red-400'
            }
            animate-fade-in
          `}
        >
          {uploadStatus.message}
        </div>
      )}
    </div>
  )
}
