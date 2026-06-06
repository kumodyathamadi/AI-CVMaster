import React, { useState, useRef } from 'react';
import { uploadResume } from '../services/api';
import '../styles/ResumeUpload.css';

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('idle'); // idle | loading | success | error
  const [message, setMessage] = useState('');
  const [isDragActive, setIsDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    validateAndSetFile(selectedFile);
  };

  const validateAndSetFile = (selectedFile) => {
    if (!selectedFile) return;

    // Reset status
    setStatus('idle');
    setMessage('');

    // Validation: Type
    if (selectedFile.type !== 'application/pdf') {
      setStatus('error');
      setMessage('Only PDF files are allowed.');
      setFile(null);
      return;
    }

    // Validation: Size (10MB)
    if (selectedFile.size > 10 * 1024 * 1024) {
      setStatus('error');
      setMessage('File size must be less than 10MB.');
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus('error');
      setMessage('Please select a file first.');
      return;
    }

    setUploading(true);
    setStatus('loading');
    setMessage('');

    try {
      const response = await uploadResume(file, (progressEvent) => {
        // Progress tracking can be added here if needed
      });

      if (response.data.success) {
        setStatus('success');
        setMessage(response.data.message || 'Resume uploaded successfully!');
        setFile(null);
        if (fileInputRef.current) fileInputRef.current.value = '';
      } else {
        throw new Error(response.data.message || 'Upload failed');
      }
    } catch (err) {
      setStatus('error');
      setMessage(err.response?.data?.message || err.message || 'An error occurred during upload.');
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragActive(true);
  };

  const handleDragLeave = () => {
    setIsDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragActive(false);
    const droppedFile = e.dataTransfer.files[0];
    validateAndSetFile(droppedFile);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="upload-container">
      <div
        className={`drop-zone ${isDragActive ? 'active' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current.click()}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf"
          style={{ display: 'none' }}
        />
        <div className="drop-zone-content">
          <div className="upload-icon">📄</div>
          {file ? (
            <div className="file-info">
              <span className="file-name">{file.name}</span>
              <span className="file-size">{formatFileSize(file.size)}</span>
            </div>
          ) : (
            <>
              <p>Drag & drop your PDF resume here</p>
              <span style={{ color: 'var(--text-muted)' }}>or click to browse</span>
            </>
          )}
        </div>
      </div>

      <button
        className="upload-button"
        onClick={handleUpload}
        disabled={uploading || !file}
      >
        {uploading ? (
          <>
            <div className="spinner"></div>
            Uploading...
          </>
        ) : (
          'Analyze Resume'
        )}
      </button>

      {status === 'success' && (
        <div className="status-message success">
          <span>✅</span> {message}
        </div>
      )}

      {status === 'error' && (
        <div className="status-message error">
          <span>❌</span> {message}
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;
