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
        const checks = [
          { label: "Skills Section", desc: "Detection of technical and soft skill blocks", status: data.skills?.technical?.length > 0 },
          { label: "Role History", desc: "Timeline of professional experience and titles", status: data.experience?.job_titles?.[0] !== "Not Found" },
          { label: "Contact Schema", desc: "Email, phone and social link presence", status: data.candidate?.email !== "Not Found" },
          { label: "Academic Records", desc: "Clear education and degree listing", status: data.education?.degree !== "Information Not Available" }
        ];

        return (
          <div className="tab-content ats-view">
            <div className="ats-header-row">
              <h2>ATS Compatibility Analysis</h2>
              <div className="ats-score-badge">
                <span className="score-val">{atsScore}%</span>
                <span className="score-label">System Match</span>
              </div>
            </div>
            
            <div className="ats-main-grid">
              <div className="ats-checks-column">
                <h3 className="section-title">Structural Integrity</h3>
                <div className="checks-container">
                  {checks.map((check, i) => (
                    <div key={i} className={`check-card ${check.status ? 'pass' : 'fail'}`}>
                      <div className="check-icon">{check.status ? '✓' : '✕'}</div>
                      <div className="check-info">
                        <h4>{check.label}</h4>
                        <p>{check.desc}</p>
                      </div>
                      <div className="status-label">{check.status ? 'Detected' : 'Missing'}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="ats-insights-column">
                <div className="optimization-card">
                  <h3>Optimization Strategy</h3>
                  <div className="strategy-content">
                     <div className="strategy-icon">💡</div>
                     <p>
                        {atsScore > 80 
                          ? "Your resume's structure is perfectly aligned with modern ATS parsing algorithms. Most recruiters will be able to search and filter your profile effortlessly."
                          : "To improve scannability, use standard section titles (e.g., 'Work Experience' instead of 'My Journey'). Ensure your most important contact info is in the header, not a footer."}
                     </p>
                  </div>
                </div>

                <div className="ats-tip">
                  <strong>Pro Tip:</strong> Avoid using complex graphics, tables, or text boxes, as they can confuse some older ATS systems.
                </div>
              </div>
            </div>
          </div>
        );
      case 'experience':
        const titles = data.experience?.job_titles || [];
        const hasTitles = titles.length > 0 && titles[0] !== "Not Found";

        return (
          <div className="tab-content experience-view">
            <div className="experience-header-row">
              <h2>Professional Experience Analysis</h2>
              <div className="tenure-badge">
                <span className="tenure-val">{data.experience?.years || 0}</span>
                <span className="tenure-label">Total Years</span>
              </div>
            </div>

            <div className="experience-main-layout">
              <div className="timeline-section">
                <h3 className="section-title">Career Progression</h3>
                <div className="professional-timeline">
                  {hasTitles ? (
                    titles.map((title, i) => (
                      <div key={i} className="timeline-block">
                        <div className="timeline-marker">
                          <div className="marker-core"></div>
                          {i !== titles.length - 1 && <div className="marker-line"></div>}
                        </div>
                        <div className="timeline-content-box">
                          <div className="role-tag">{i === 0 ? 'Current / Latest' : 'Past Role'}</div>
                          <h4>{title}</h4>
                          <p className="role-desc">Extracted from professional history records.</p>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="empty-state-card">
                      <div className="empty-icon">📂</div>
                      <p>Specific job titles were not explicitly identifiable in this document structure.</p>
                    </div>
                  )}
                </div>
              </div>

              <div className="experience-insights-section">
                 <div className="intelligence-card">
                    <h3>Career Intelligence</h3>
                    <div className="intelligence-item">
                      <div className="intel-label">Seniority Level</div>
                      <div className="intel-value">
                        {data.experience?.years > 8 ? "Executive / Expert" : 
                         data.experience?.years > 4 ? "Mid-Senior Level" : 
                         data.experience?.years > 1 ? "Professional" : "Junior / Entry"}
                      </div>
                    </div>
                    <div className="intel-divider"></div>
                    <div className="insight-briefing">
                      <h4>AI Strategic Briefing</h4>
                      <p>
                        {data.experience?.years > 5 
                          ? "Senior-level profile detected. Your extensive tenure suggests high reliability and specialized expertise." 
                          : data.experience?.years > 0 
                            ? "Core professional experience detected. You are in a strong growth phase for specialized roles."
                            : "Entry-level or transition profile detected. Focus on showcasing academic projects and certifications."}
                      </p>
                    </div>
                 </div>
              </div>
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
