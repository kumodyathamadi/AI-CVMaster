import React, { useState } from 'react';
import ScoreCard from './ScoreCard';
import ProfileCard from './ProfileCard';
import SkillsDashboard from './SkillsDashboard';
import RecommendationDashboard from './RecommendationDashboard';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = ({ data, onReset }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [jdText, setJdText] = useState('');
  const [matchResult, setMatchResult] = useState(null);
  const [isLoadingMatch, setIsLoadingMatch] = useState(false);
  
  if (!data) return null;

  const handleAnalyzeMatch = async () => {
    if (!jdText.trim()) return;
    
    setIsLoadingMatch(true);
    try {
      const response = await axios.post('http://localhost:5000/api/match', {
        resume_text: data.raw_text || "",
        job_description: jdText
      });
      setMatchResult(response.data.data);
    } catch (error) {
      console.error("Match error:", error);
      alert("Failed to analyze match. Please try again.");
    } finally {
      setIsLoadingMatch(false);
    }
  };

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
                  <li>{data.experience?.job_titles?.[0] !== "Not Found" ? '✅' : '❌'} Experience History Detected</li>
                  <li>{data.candidate?.email !== "Not Found" ? '✅' : '❌'} Contact Information Found</li>
                  <li>{data.education?.degree !== "Information Not Available" ? '✅' : '❌'} Education Credentials Found</li>
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
        const titles = data.experience?.job_titles || [];
        const hasTitles = titles.length > 0 && titles[0] !== "Not Found";

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
              {hasTitles ? (
                titles.map((title, i) => (
                  <div key={i} className="timeline-item">
                    <div className="dot"></div>
                    <div className="content">
                      <h4>{title}</h4>
                      <p>{i === 0 ? 'Extracted Position' : 'Previous Position'}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-data">Information Not Available in Resume</div>
              )}
            </div>
            <div className="ai-comment">
              <p>💡 AI Insight: {data.experience?.years > 5 
                ? "Senior-level profile detected based on date analysis." 
                : data.experience?.years > 0 
                  ? "Professional experience detected. Focus on quantitative achievements."
                  : "Entry-level or transition profile detected."}
              </p>
            </div>
          </div>
        );
      case 'match':
        return (
          <div className="tab-content match-view">
            <h2>Job Description Matching</h2>
            <p className="subtitle">Paste a job description below to see your semantic match score.</p>
            <textarea 
              className="jd-input" 
              placeholder="Paste Job Description here..."
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
            ></textarea>
            <button 
              className="match-button" 
              onClick={handleAnalyzeMatch}
              disabled={isLoadingMatch || !jdText.trim()}
            >
              {isLoadingMatch ? 'Analyzing...' : 'Analyze Match'}
            </button>

            {matchResult && (
              <div className="match-results">
                <div className="match-score-radial">
                   <div className="match-score-value">{matchResult.score}%</div>
                   <div className="match-label">Match Probability</div>
                </div>

                <div className="explanation-card">
                  <strong>AI Analysis:</strong> {matchResult.explanation}
                </div>

                <div className="skills-comparison-grid">
                  <div className="skills-list-box">
                    <h5>Matching Skills</h5>
                    <div className="pill-container">
                      {matchResult.matched_skills.map((s, i) => <span key={i} className="pill matched">{s}</span>)}
                      {matchResult.matched_skills.length === 0 && <span>No matching skills found</span>}
                    </div>
                  </div>
                  <div className="skills-list-box">
                    <h5>Missing Skills</h5>
                    <div className="pill-container">
                      {matchResult.missing_skills.map((s, i) => <span key={i} className="pill missing">{s}</span>)}
                      {matchResult.missing_skills.length === 0 && <span>No critical missing skills</span>}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      default:
        return (
          <div className="tab-content overview-view">
            <div className="content-row">
              <ProfileCard 
                candidate={{
                  ...data.candidate,
                  jobTitle: data.experience?.job_titles?.[0] !== "Not Found" ? data.experience?.job_titles?.[0] : "Candidate"
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
          <div className={`nav-item ${activeTab === 'experience' ? 'active' : ''}`} onClick={() => setActiveTab('experience')}>Experience Histroy</div>
          <div className={`nav-item ${activeTab === 'match' ? 'active' : ''}`} onClick={() => setActiveTab('match')}>Job Match</div>
        </div>

        <button className="reset-button" onClick={onReset}>
          Analyze New Resume
        </button>
      </div>

      <div className="dashboard-main">
        <header className="dashboard-header">
          <h1>Resume Intelligence Analysis</h1>
          <p>Analyzing: <strong>{data.candidate?.name !== "Not Found" ? data.candidate?.name : 'Uploaded Document'}</strong></p>
        </header>

        <div className="dashboard-content">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
