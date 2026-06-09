import React from 'react';
import './RecommendationDashboard.css';

const RecommendationDashboard = ({ recommendations, predictions }) => {
  if (!recommendations) return null;

  return (
    <div className="recommendation-dashboard">
      <div className="rec-section">
        <h3>AI Recommendations</h3>
        <div className="rec-grid">
          <div className="rec-card">
            <h4>Skills to Learn</h4>
            <ul>
              {recommendations.skills?.map((item, i) => <li key={i}>{item}</li>)}
            </ul>
          </div>
          <div className="rec-card">
            <h4>Certifications</h4>
            <ul>
              {recommendations.certifications?.map((item, i) => <li key={i}>{item}</li>)}
            </ul>
          </div>
        </div>
      </div>

      <div className="career-section">
        <h3>Career Prediction</h3>
        <div className="prediction-grid">
          {Object.entries(predictions || {}).map(([role, score], i) => (
            <div key={i} className="prediction-item">
              <div className="role-info">
                <span>{role}</span>
                <span>{score}%</span>
              </div>
              <div className="prediction-bar">
                <div className="bar-fill" style={{ width: `${score}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RecommendationDashboard;
