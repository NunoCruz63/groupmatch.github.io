import React, { useState, useEffect } from 'react';
import { Search, Menu, X } from 'lucide-react';

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setIsMobileMenuOpen(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    // Mock search functionality - will be implemented with backend
    console.log('Searching for:', searchQuery);
  };

  return (
    <header className={`nav-header ${isScrolled ? 'scrolled' : ''}`}>
      <div className="flex items-center gap-4">
        <div className="font-bold text-xl" style={{color: 'var(--text-primary)'}}>
          TradingHub
        </div>
      </div>

      {/* Desktop Navigation */}
      <nav className="hidden md:flex items-center gap-6">
        <button onClick={() => scrollToSection('home')} className="nav-link">
          Home
        </button>
        <button onClick={() => scrollToSection('providers')} className="nav-link">
          Signal Providers
        </button>
        <button onClick={() => scrollToSection('brokers')} className="nav-link">
          Brokers
        </button>
        <button onClick={() => scrollToSection('about')} className="nav-link">
          Sobre
        </button>
        <button onClick={() => scrollToSection('contact')} className="nav-link">
          Contactos
        </button>
      </nav>

      {/* Search Bar */}
      <div className="hidden lg:flex items-center gap-4">
        <form onSubmit={handleSearch} className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="text"
            placeholder="Pesquisar providers ou brokers..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 pr-4 py-2 border border-gray-200 rounded-full w-64 text-sm focus:outline-none focus:border-gray-400"
          />
        </form>
        
        <button 
          onClick={() => scrollToSection('providers')} 
          className="btn-primary"
        >
          Começar Agora
        </button>
      </div>

      {/* Mobile Menu Button */}
      <button
        className="md:hidden p-2"
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      >
        {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-lg shadow-lg p-4 md:hidden">
          <div className="flex flex-col gap-4">
            <form onSubmit={handleSearch} className="relative mb-4">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Pesquisar..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-200 rounded-full w-full text-sm focus:outline-none focus:border-gray-400"
              />
            </form>
            
            <button onClick={() => scrollToSection('home')} className="nav-link text-left">
              Home
            </button>
            <button onClick={() => scrollToSection('providers')} className="nav-link text-left">
              Signal Providers
            </button>
            <button onClick={() => scrollToSection('brokers')} className="nav-link text-left">
              Brokers
            </button>
            <button onClick={() => scrollToSection('about')} className="nav-link text-left">
              Sobre
            </button>
            <button onClick={() => scrollToSection('contact')} className="nav-link text-left">
              Contactos
            </button>
            
            <button 
              onClick={() => scrollToSection('providers')} 
              className="btn-primary mt-4"
            >
              Começar Agora
            </button>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;