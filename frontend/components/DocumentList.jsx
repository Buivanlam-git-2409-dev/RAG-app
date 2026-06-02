import React from 'react'

export default function DocumentList({ documents }) {
  if (documents.length === 0) {
    return (
      <div>
        <h2 className="font-display text-lg font-medium text-text-primary mb-4">
          Documents
        </h2>
        <p className="font-body text-text-muted text-sm italic">
          No documents uploaded yet
        </p>
      </div>
    )
  }

  return (
    <div>
      <h2 className="font-display text-lg font-medium text-text-primary mb-4">
        Documents
      </h2>
      <ul className="space-y-2">
        {documents.map((doc, index) => (
          <li
            key={doc.id || index}
            className="group flex items-center gap-3 p-3 rounded-lg bg-void-light border border-void-border hover:border-text-muted transition-all duration-200"
          >
            <div className="w-8 h-8 rounded bg-void-border flex items-center justify-center flex-shrink-0">
              <svg className="w-4 h-4 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-body text-text-primary text-sm truncate">
                {doc.name || doc.filename || `Document ${index + 1}`}
              </p>
              <p className="font-mono text-xs text-text-muted">
                {doc.chunk_count || 0} chunks
              </p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
