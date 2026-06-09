import React from 'react';
import './SkillsDashboard.css';

const SkillsDashboard = ({ skills }) => {
  if (!skills) return null;

  return (
    <div className="skills-dashboard">
      <div className="skill-section">
        <h3>Technical Skills</h3>
        <div className="skill-tags">
          {skills.technical?.map((skill, index) => (
            <span key={index} className="skill-badge tech">{skill}</span>
          ))}
        </div>
      </div>
      
      <div className="skill-section">
        <h3>Soft Skills</h3>
        <div className="skill-tags">
          {skills.soft?.map((skill, index) => (
            <span key={index} className="skill-badge soft">{skill}</span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SkillsDashboard;
