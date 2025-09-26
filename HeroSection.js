import React, { useEffect, useRef } from 'react';
import { TrendingUp, Shield, BarChart3, Users } from 'lucide-react';

const HeroSection = () => {
  const heroRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      },
      { threshold: 0.1 }
    );

    const elements = heroRef.current?.querySelectorAll('.fade-in-up, .slide-in-left, .slide-in-right');
    elements?.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="home" className="hero-section" ref={heroRef}>
      <div className="container">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="heading-1 fade-in-up mb-6">
            Descobre os melhores Signal Providers e Brokers de forma{' '}
            <span style={{color: 'var(--accent-text)'}}>segura e transparente</span>
          </h1>
          
          <p className="body-large fade-in-up mb-8" style={{animationDelay: '0.2s'}}>
            Ranking baseado em estatísticas reais e análises verificadas. 
            Encontra os providers e brokers mais confiáveis do mercado.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12 fade-in-up" style={{animationDelay: '0.4s'}}>
            <button 
              onClick={() => scrollToSection('providers')} 
              className="btn-primary text-lg px-8 py-4"
            >
              <TrendingUp className="w-5 h-5 mr-2" />
              Explorar Providers
            </button>
            <button 
              onClick={() => scrollToSection('brokers')} 
              className="btn-secondary text-lg px-8 py-4"
            >
              <BarChart3 className="w-5 h-5 mr-2" />
              Ver Brokers
            </button>
          </div>

          {/* Trust Indicators */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-2xl mx-auto fade-in-up" style={{animationDelay: '0.6s'}}>
            <div className="text-center hover-float">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <Shield className="w-8 h-8" style={{color: 'var(--accent-text)'}} />
              </div>
              <div className="body-small">
                <div className="font-semibold" style={{color: 'var(--text-primary)'}}>100% Verificado</div>
                <div>Sinais autênticos</div>
              </div>
            </div>

            <div className="text-center hover-float" style={{animationDelay: '0.1s'}}>
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <BarChart3 className="w-8 h-8 text-blue-600" />
              </div>
              <div className="body-small">
                <div className="font-semibold" style={{color: 'var(--text-primary)'}}>Stats Reais</div>
                <div>Dados transparentes</div>
              </div>
            </div>

            <div className="text-center hover-float" style={{animationDelay: '0.2s'}}>
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <Users className="w-8 h-8 text-purple-600" />
              </div>
              <div className="body-small">
                <div className="font-semibold" style={{color: 'var(--text-primary)'}}>+10K Traders</div>
                <div>Comunidade ativa</div>
              </div>
            </div>

            <div className="text-center hover-float" style={{animationDelay: '0.3s'}}>
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <TrendingUp className="w-8 h-8 text-orange-600" />
              </div>
              <div className="body-small">
                <div className="font-semibold" style={{color: 'var(--text-primary)'}}>85% Win Rate</div>
                <div>Média top providers</div>
              </div>
            </div>
          </div>
        </div>

        {/* Floating Dashboard Mockup */}
        <div className="mt-16 max-w-4xl mx-auto fade-in-up hover-pulse" style={{animationDelay: '0.8s'}}>
          <div className="bg-white rounded-2xl shadow-2xl p-8 border border-gray-100">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold mb-2" style={{color: 'var(--accent-text)'}}>250+</div>
                <div className="body-small">Signal Providers</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold mb-2" style={{color: 'var(--accent-text)'}}>50+</div>
                <div className="body-small">Brokers Verificados</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold mb-2" style={{color: 'var(--accent-text)'}}>₹2M+</div>
                <div className="body-small">Volume Mensal</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;