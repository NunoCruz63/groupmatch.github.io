import React from 'react';
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import SignalProviders from './components/SignalProviders';
import BrokersSection from './components/BrokersSection';
import HowItWorks from './components/HowItWorks';
import TrustBenefits from './components/TrustBenefits';
import TestimonialsSection from './components/TestimonialsSection';
import FinalCTA from './components/FinalCTA';
import Footer from './components/Footer';

const Home = () => {
  return (
    <div className="min-h-screen">
      <Header />
      <HeroSection />
      <SignalProviders />
      <BrokersSection />
      <HowItWorks />
      <TrustBenefits />
      <TestimonialsSection />
      <FinalCTA />
      <Footer />
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
