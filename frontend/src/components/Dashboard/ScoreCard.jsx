import React from 'react';
import './ScoreCard.css';

const ScoreCard = ({ score, status, atsScore }) => {
  const getScoreColor = (s) => {
    if (s >= 90) return '#22c55e'; // Excellent
    if (s >= 75) return '#6366f1'; // Good
    if (s >= 50) return '#f59e0b'; // Average
    return '#ef4444'; // Needs Improvement
  };

  const percentage = score || 0;
  const strokeDasharray = `${percentage}, 100`;

  return (
    <div className="score-card">
      <div className="overall-score">
        <div className="circular-progress">
          <svg viewBox="0 0 36 36" className="circular-chart">
            <path className="circle-bg"
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <path className="circle"
              strokeDasharray={strokeDasharray}
              stroke={getScoreColor(percentage)}
              d="M18 2.0845
                a 15.9155 15.9155 0 0 1 0 31.831
                a 15.9155 15.9155 0 0 1 0 -31.831"
            />
            <text x="18" y="20.35" className="percentage" fill={getScoreColor(percentage)}>{percentage}</text>
          </svg>
        </div>
        <div className="score-details">
          <h3>Resume Score</h3>
          <span className="status-badge" style={{ backgroundColor: getScoreColor(percentage) }}>
            {status}
          </span>
        </div>
      </div>
      
      <div className="ats-mini-score">
        <label>ATS Compatibility</label>
        <div className="progress-bar-container">
          <div className="progress-bar" style={{ width: `${atsScore}%`, backgroundColor: getScoreColor(atsScore) }}></div>
        </div>
        <span>{atsScore}%</span>
      </div>
    </div>
  );
};

export default ScoreCard;
