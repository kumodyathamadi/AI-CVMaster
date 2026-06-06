import React from 'react';
import './Features.css';

const featureList = [
  {
    icon: '🎯',
    title: 'ATS Scoring',
    description: 'Get an instant score on how well your resume matches Applicant Tracking Systems.'
  },
  {
    icon: '🔍',
    title: 'Keyword Optimization',
    description: 'Identify missing keywords that are crucial for your specific job role.'
  },
  {
    icon: '✨',
    title: 'Formatting Check',
    description: 'Ensure your resume layout is professional and easy for AI to read.'
  }
];

const Features = () => {
  return (
    <section id="features" className="features-section">
      <div className="section-header">
        <h2 className="section-title">Why Use Our AI Analyzer?</h2>
        <p className="section-subtitle">We use advanced NLP to give you the same insights recruiters have.</p>
      </div>
      <div className="features-grid">
        {featureList.map((feature, index) => (
          <div key={index} className="feature-card">
            <div className="feature-icon">{feature.icon}</div>
            <h3 className="feature-title">{feature.title}</h3>
            <p className="feature-description">{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Features;
