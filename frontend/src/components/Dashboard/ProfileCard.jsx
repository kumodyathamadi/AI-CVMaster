import React from 'react';
import './ProfileCard.css';

const ProfileCard = ({ candidate }) => {
  if (!candidate) return null;

  return (
    <div className="profile-card">
      <div className="profile-header">
        <div className="avatar">
          {candidate.name ? candidate.name.charAt(0) : 'U'}
        </div>
        <div className="candidate-info">
          <h2>{candidate.name || 'John Doe'}</h2>
          <p>{candidate.jobTitle || 'Professional Profile'}</p>
        </div>
      </div>
      
      <div className="contact-links">
        <div className="contact-item">
          <span className="icon">📧</span>
          <span>{candidate.email && candidate.email !== "Not Found" ? candidate.email : 'N/A'}</span>
        </div>
        <div className="contact-item">
          <span className="icon">📱</span>
          <span>{candidate.phone && candidate.phone !== "Not Found" ? candidate.phone : 'N/A'}</span>
        </div>
      </div>

      <div className="social-links">
        {candidate.links?.linkedin && candidate.links.linkedin !== "Not Found" && (
          <a href={candidate.links.linkedin} target="_blank" rel="noopener noreferrer" className="social-tag linkedin">LinkedIn</a>
        )}
        {candidate.links?.github && candidate.links.github !== "Not Found" && (
          <a href={candidate.links.github} target="_blank" rel="noopener noreferrer" className="social-tag github">GitHub</a>
        )}
      </div>
    </div>
  );
};

export default ProfileCard;
