import React from 'react';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="logo">
          <span className="logo-icon">🚀</span>
          <span className="logo-text">CV<span className="accent">Master</span></span>
        </div>
        <div className="nav-links">
          <a href="#features" className="nav-link">Features</a>
          <a href="#how-it-works" className="nav-link">How it Works</a>
          <a href="#pricing" className="nav-link">Pricing</a>
          <button className="nav-cta">Sign In</button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
