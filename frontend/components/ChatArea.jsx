import React, { useState, useRef, useEffect } from 'react'

export default function ChatArea({ messages, isTyping, onSendMessage, chatEndRef }) {
  const [input, setInput] = useState('')
  const textareaRef = useRef(null)

  useEffect(() => {
    textareaRef.current?.focus()
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (input.trim()) {
      onSendMessage(input)
      setInput('')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 mx-auto rounded-full bg-void-border flex items-center justify-center">
                <svg className="w-8 h-8 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <p className="font-display text-text-secondary text-lg">
                Ask a question about your documents
              </p>
              <p className="font-body text-text-muted text-sm">
                Upload a document to get started
              </p>
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`
                animate-slide-up
                ${message.role === 'user' ? 'flex justify-end' : 'flex justify-start'}
              `}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div
                className={`
                  max-w-2xl rounded-lg p-5
                  ${message.role === 'user'
                    ? 'bg-accent/10 border border-accent/20'
                    : 'bg-void-light border border-void-border'
                  }
                `}
              >
                <p className="font-body text-text-primary text-balance leading-relaxed">
                  {message.content}
                </p>

                {message.sources && message.sources.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-void-border">
                    <p className="font-mono text-xs text-text-muted mb-2">
                      Sources
                    </p>
                    <div className="space-y-2">
                      {message.sources.map((source, i) => (
                        <div
                          key={i}
                          className="p-3 rounded bg-void border border-void-border text-sm"
                        >
                          <p className="font-body text-text-secondary line-clamp-3">
                            {source.content || source.text}
                          </p>
                          <p className="font-mono text-xs text-text-muted mt-2">
                            {source.document_name || source.filename}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))
        )}

        {isTyping && (
          <div className="flex justify-start animate-fade-in">
            <div className="bg-void-light border border-void-border rounded-lg p-5">
              <div className="flex gap-1">
                <span className="w-2 h-2 rounded-full bg-text-muted animate-pulse-slow" style={{ animationDelay: '0s' }} />
                <span className="w-2 h-2 rounded-full bg-text-muted animate-pulse-slow" style={{ animationDelay: '0.2s' }} />
                <span className="w-2 h-2 rounded-full bg-text-muted animate-pulse-slow" style={{ animationDelay: '0.4s' }} />
              </div>
            </div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      <div className="border-t border-void-border p-6 glass">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
          <div className="relative">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question..."
              rows={1}
              className="w-full bg-void-light border border-void-border rounded-lg px-4 py-3 pr-12 font-body text-text-primary placeholder:text-text-muted resize-none focus:outline-none focus:border-accent/50 transition-colors"
              style={{ minHeight: '48px', maxHeight: '200px' }}
            />
            <button
              type="submit"
              disabled={!input.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-lg text-text-muted hover:text-accent disabled:opacity-30 disabled:hover:text-text-muted transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
