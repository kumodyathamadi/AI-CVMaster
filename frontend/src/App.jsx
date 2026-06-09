import React from 'react';
import Navbar from './components/Navbar';
import ResumeUpload from './components/ResumeUpload';
import Features from './components/Features';
import Dashboard from './components/Dashboard/Dashboard';
import './index.css';

function App() {
  const [analyzedData, setAnalyzedData] = React.useState(null);

  const handleAnalysisComplete = (data) => {
    setAnalyzedData(data);
  };

  return (
    <div className="app-wrapper">
      <Navbar />
      
      <main>
        {!analyzedData ? (
          <>
            <section className="hero-section">
              <div className="hero-content">
                <h1 className="hero-title">
                  Unlock Your <span className="gradient-text">Career Potential</span>
                </h1>
                <p className="hero-subtitle">
                  Upload your resume and get instant AI-driven insights to optimize your profile, 
                  beat the ATS, and land your dream interview.
                </p>
              </div>
              <ResumeUpload onAnalysisComplete={handleAnalysisComplete} />
            </section>
            <Features />
          </>
        ) : (
          <Dashboard data={analyzedData} onReset={() => setAnalyzedData(null)} />
        )}
      </main>

      <footer>
        <div className="footer-container">
          <p>© 2026 CVMaster AI. All rights reserved. Helping professionals grow.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
