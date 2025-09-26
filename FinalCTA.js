import React, { useEffect, useRef } from 'react';
import { TrendingUp, ArrowRight, Users, Shield, Award } from 'lucide-react';

const FinalCTA = () => {
  const sectionRef = useRef(null);

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

    const elements = sectionRef.current?.querySelectorAll('.fade-in-up, .slide-in-left, .slide-in-right, .scale-in');
    elements?.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const features = [
    {
      icon: <Shield className="w-6 h-6" />,
      text: "250+ Providers Verificados"
    },
    {
      icon: <Users className="w-6 h-6" />,
      text: "Comunidade de +10K Traders"
    },
    {
      icon: <Award className="w-6 h-6" />,
      text: "87% Taxa de Sucesso Média"
    }
  ];

  return (
    <section id="final-cta" className="py-20 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white relative overflow-hidden" ref={sectionRef}>
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 25% 25%, rgba(255,255,255,0.1) 0%, transparent 50%),
                           radial-gradient(circle at 75% 75%, rgba(255,255,255,0.1) 0%, transparent 50%)`
        }}></div>
      </div>

      <div className="container relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          {/* Main Heading */}
          <div className="fade-in-up mb-8">
            <h2 className="heading-1 text-white mb-6">
              Começa a Seguir os Melhores Providers{' '}
              <span className="bg-gradient-to-r from-green-400 to-green-600 bg-clip-text text-transparent">
                Agora
              </span>
            </h2>
            <p className="body-large text-gray-300 max-w-2xl mx-auto">
              Junta-te a milhares de traders que já estão a lucrar com os nossos signal providers e brokers verificados. 
              O teu sucesso começa hoje.
            </p>
          </div>

          {/* Features List */}
          <div className="fade-in-up flex flex-col sm:flex-row items-center justify-center gap-6 mb-12" style={{animationDelay: '0.3s'}}>
            {features.map((feature, index) => (
              <div key={index} className="flex items-center gap-2 text-green-400">
                {feature.icon}
                <span className="text-sm font-medium">{feature.text}</span>
              </div>
            ))}
          </div>

          {/* CTA Buttons */}
          <div className="fade-in-up flex flex-col sm:flex-row gap-4 justify-center mb-16" style={{animationDelay: '0.5s'}}>
            <button
              onClick={() => scrollToSection('providers')}
              className="btn-primary text-lg px-8 py-4 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-400 hover:to-green-500 transform hover:scale-105 shadow-2xl"
            >
              <TrendingUp className="w-6 h-6 mr-2" />
              Explorar Signal Providers
              <ArrowRight className="w-5 h-5 ml-2" />
            </button>
            
            <button
              onClick={() => scrollToSection('brokers')}
              className="btn-secondary text-lg px-8 py-4 bg-transparent border-2 border-white text-white hover:bg-white hover:text-gray-900 transform hover:scale-105"
            >
              Ver Brokers Recomendados
            </button>
          </div>

          {/* Trust Indicators */}
          <div className="fade-in-up grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto" style={{animationDelay: '0.7s'}}>
            <div className="text-center hover-float">
              <div className="text-4xl font-bold text-green-400 mb-2">100%</div>
              <div className="text-sm text-gray-300">Providers Verificados</div>
            </div>
            
            <div className="text-center hover-float" style={{animationDelay: '0.1s'}}>
              <div className="text-4xl font-bold text-green-400 mb-2">24/7</div>
              <div className="text-sm text-gray-300">Suporte Disponível</div>
            </div>
            
            <div className="text-center hover-float" style={{animationDelay: '0.2s'}}>
              <div className="text-4xl font-bold text-green-400 mb-2">0%</div>
              <div className="text-sm text-gray-300">Taxas Escondidas</div>
            </div>
          </div>

          {/* Urgency Message */}
          <div className="fade-in-up mt-12 p-6 bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-2xl border border-orange-500/30" style={{animationDelay: '0.9s'}}>
            <div className="flex items-center justify-center gap-2 mb-2">
              <div className="w-2 h-2 bg-orange-400 rounded-full animate-pulse"></div>
              <span className="text-orange-400 font-medium text-sm">OFERTA LIMITADA</span>
            </div>
            <p className="text-gray-300 text-sm">
              Primeiros 100 utilizadores obtêm acesso premium às análises exclusivas dos nossos experts
            </p>
          </div>

          {/* Social Proof */}
          <div className="fade-in-up mt-8 text-center" style={{animationDelay: '1.1s'}}>
            <p className="text-xs text-gray-400 mb-4">Confiado por traders em mais de 50 países</p>
            
            <div className="flex justify-center items-center space-x-8 opacity-60">
              <div className="flex -space-x-2">
                {[...Array(5)].map((_, i) => (
                  <div
                    key={i}
                    className="w-8 h-8 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full border-2 border-white flex items-center justify-center text-white text-xs font-bold"
                  >
                    {String.fromCharCode(65 + i)}
                  </div>
                ))}
              </div>
              <span className="text-sm text-gray-400">+10,247 traders ativos</span>
            </div>
          </div>
        </div>

        {/* Decorative Elements */}
        <div className="absolute top-10 left-10 w-20 h-20 bg-green-500/10 rounded-full blur-xl"></div>
        <div className="absolute bottom-10 right-10 w-32 h-32 bg-blue-500/10 rounded-full blur-xl"></div>
        <div className="absolute top-1/2 left-1/4 w-16 h-16 bg-purple-500/10 rounded-full blur-xl"></div>
      </div>
    </section>
  );
};

export default FinalCTA;