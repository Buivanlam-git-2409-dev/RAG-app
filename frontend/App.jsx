import React, { useState, useRef, useEffect } from 'react'
import FileUpload from './components/FileUpload'
import ChatArea from './components/ChatArea'
import DocumentList from './components/DocumentList'

function App() {
  const [messages, setMessages] = useState([])
  const [documents, setDocuments] = useState([])
  const [isTyping, setIsTyping] = useState(false)
  const chatEndRef = useRef(null)

  useEffect(() => {
    fetchDocuments()
  }, [])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const fetchDocuments = async () => {
    try {
      const response = await fetch('/api/documents')
      if (response.ok) { 
        const data = await response.json()
        setDocuments(data.documents || [])
      }
    } catch (error) {
      console.error('Failed to fetch documents:', error)
    }
  }

  const handleSendMessage = async (content) => {
    if (!content.trim()) return

    const userMessage = { role: 'user', content }
    setMessages(prev => [...prev, userMessage])
    setIsTyping(true)

    try {
      const response = await fetch('/api/query-document', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: content })
      })

      if (response.ok) {
        const data = await response.json()
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.answer,
          sources: data.sources || []
        }])
      } else {
        throw new Error('Failed to get response')
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request.',
        sources: []
      }])
    } finally {
      setIsTyping(false)
    }
  }

  const handleFileUpload = async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/upload-document', {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        await fetchDocuments()
        return { success: true }
      }
      return { success: false, error: 'Upload failed' }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  return (
    <div className="min-h-screen bg-void relative overflow-hidden">
      <div className="noise-overlay" />

      <div className="relative z-10 flex flex-col h-screen">
        <header className="glass border-b border-void-border px-6 py-4">
          <div className="max-w-6xl mx-auto flex items-center justify-between">
            <h1 className="font-display text-2xl font-semibold text-text-primary tracking-tight">
              RAG Chat
            </h1>
            <span className="font-mono text-xs text-text-muted">
              {documents.length} document{documents.length !== 1 ? 's' : ''}
            </span>
          </div>
        </header>

        <main className="flex-1 flex overflow-hidden">
          <aside className="w-80 border-r border-void-border glass overflow-y-auto">
            <div className="p-6">
              <FileUpload onUpload={handleFileUpload} />
              <DocumentList documents={documents} />
            </div>
          </aside>

          <section className="flex-1 flex flex-col">
            <ChatArea
              messages={messages}
              isTyping={isTyping}
              onSendMessage={handleSendMessage}
              chatEndRef={chatEndRef}
            />
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
