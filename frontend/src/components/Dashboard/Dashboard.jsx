import React from 'react';
import ScoreCard from './ScoreCard';
import ProfileCard from './ProfileCard';
import SkillsDashboard from './SkillsDashboard';
import RecommendationDashboard from './RecommendationDashboard';
import './Dashboard.css';

const Dashboard = ({ data, onReset }) => {
  const [activeTab, setActiveTab] = React.useState('overview');
  
  if (!data) return null;

  const renderContent = () => {
    switch (activeTab) {
      case 'ats':
        const atsScore = data.ats_score || 0;
        return (
          <div className="tab-content ats-view">
            <h2>ATS Compatibility Analysis</h2>
            <div className="ats-grid">
              <div className="ats-item">
                <label>Overall ATS Score</label>
                <div className={`ats-status ${atsScore > 70 ? 'success' : 'warning'}`}>
                  {atsScore}%
                </div>
              </div>
              <div className="ats-item">
                <label>Structural Check</label>
                <ul className="check-list">
                  <li>{data.skills?.technical?.length > 0 ? '✅' : '❌'} Skills Section Detected</li>
                  <li>{data.experience?.job_titles?.length > 0 ? '✅' : '❌'} Experience History Detected</li>
                  <li>{data.candidate?.email ? '✅' : '❌'} Contact Information Found</li>
                  <li>{data.education?.degree ? '✅' : '❌'} Education Credentials Found</li>
                </ul>
              </div>
              <div className="ats-item">
                <label>Optimization Tip</label>
                <p>
                  {atsScore > 80 
                    ? "Excellent structure. Your resume is highly readable by modern standard ATS systems."
                    : "Consider adding more standard section headers and ensuring your contact info is at the very top."}
                </p>
              </div>
            </div>
          </div>
        );
      case 'experience':
        return (
          <div className="tab-content experience-view">
            <h2>Experience Analysis</h2>
            <div className="experience-meta">
              <div className="meta-box">
                <label>Years of Experience</label>
                <span>{data.experience?.years || 0} Years</span>
              </div>
            </div>
            <div className="timeline">
              {data.experience?.job_titles?.length > 0 ? (
                data.experience.job_titles.map((title, i) => (
                  <div key={i} className="timeline-item">
                    <div className="dot"></div>
                    <div className="content">
                      <h4>{title}</h4>
                      <p>{i === 0 ? 'Latest Position' : 'Previous Role'}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-data">No specific job titles detected in the resume text.</div>
              )}
            </div>
            <div className="ai-comment">
              <p>💡 AI Insight: {data.experience?.years > 5 
                ? "Senior-level profile detected. Your extensive experience is a major strength." 
                : "Promising profile. Focus on highlighting specific projects to compensate for shorter tenure."}
              </p>
            </div>
          </div>
        );
      case 'match':
        return (
          <div className="tab-content match-view">
            <h2>Job Description Matching</h2>
            <p className="subtitle">Paste a job description below to see your semantic match score.</p>
            <textarea className="jd-input" placeholder="Paste Job Description here..."></textarea>
            <button className="match-button">Analyze Match</button>
            <div className="match-result-placeholder">
              <p>Based on your profile, you are a <strong>{Math.max(...Object.values(data.career_prediction || { 'Default': 0 }))}%</strong> match for current market standards in your primary role.</p>
            </div>
          </div>
        );
      default:
        return (
          <div className="tab-content overview-view">
            <div className="content-row">
              <ProfileCard 
                candidate={{
                  ...data.candidate,
                  jobTitle: data.experience?.job_titles?.[0]
                }} 
              />
              <SkillsDashboard skills={data.skills} />
            </div>
            
            <div className="content-row full">
              <RecommendationDashboard 
                recommendations={data.recommendations} 
                predictions={data.career_prediction} 
              />
            </div>
          </div>
        );
    }
  };

  return (
    <div className="dashboard-root">
      <div className="dashboard-sidebar">
        <ScoreCard 
          score={data.resume_score} 
          status={data.status_badge} 
          atsScore={data.ats_score} 
        />
        
        <div className="sidebar-nav">
          <div className={`nav-item ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>Overview</div>
          <div className={`nav-item ${activeTab === 'ats' ? 'active' : ''}`} onClick={() => setActiveTab('ats')}>ATS Details</div>
          <div className={`nav-item ${activeTab === 'experience' ? 'active' : ''}`} onClick={() => setActiveTab('experience')}>Experience</div>
          <div className={`nav-item ${activeTab === 'match' ? 'active' : ''}`} onClick={() => setActiveTab('match')}>Job Match</div>
        </div>

        <button className="reset-button" onClick={onReset}>
          Analyze New Resume
        </button>
      </div>

      <div className="dashboard-main">
        <header className="dashboard-header">
          <h1>Resume Intelligence Analysis</h1>
          <p>Analyzing: <strong>{data.candidate?.name || 'Uploaded Document'}</strong></p>
        </header>

        <div className="dashboard-content">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
