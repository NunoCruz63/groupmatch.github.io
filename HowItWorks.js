import React, { useEffect, useRef } from 'react';
import { Search, BarChart3, ExternalLink, ArrowRight } from 'lucide-react';

const HowItWorks = () => {
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

  const steps = [
    {
      number: 1,
      title: "Escolhe o Provider ou Broker",
      description: "Navega pela nossa seleção curada de signal providers e brokers verificados",
      icon: <Search className="w-8 h-8" />,
      color: "blue"
    },
    {
      number: 2,
      title: "Visualiza Estatísticas Verificadas",
      description: "Analisa win rates, histórico de trades e performance detalhada em tempo real",
      icon: <BarChart3 className="w-8 h-8" />,
      color: "green"
    },
    {
      number: 3,
      title: "Subscreve via Link Afiliado",
      description: "Acede diretamente às plataformas através dos nossos links seguros e verificados",
      icon: <ExternalLink className="w-8 h-8" />,
      color: "orange"
    }
  ];

  const getStepColors = (color) => {
    switch (color) {
      case 'blue':
        return {
          bg: 'bg-blue-100',
          text: 'text-blue-600',
          border: 'border-blue-200'
        };
      case 'green':
        return {
          bg: 'bg-green-100',
          text: 'text-green-600',
          border: 'border-green-200'
        };
      case 'orange':
        return {
          bg: 'bg-orange-100',
          text: 'text-orange-600',
          border: 'border-orange-200'
        };
      default:
        return {
          bg: 'bg-gray-100',
          text: 'text-gray-600',
          border: 'border-gray-200'
        };
    }
  };

  return (
    <section id="how-it-works" className="py-16 bg-gray-50" ref={sectionRef}>
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="heading-2 fade-in-up mb-4">
            Como <span style={{color: 'var(--accent-text)'}}>Funciona</span>
          </h2>
          <p className="body-large fade-in-up max-w-2xl mx-auto" style={{animationDelay: '0.2s'}}>
            Processo simples e transparente para começares a seguir os melhores traders
          </p>
        </div>

        <div className="max-w-5xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((step, index) => {
              const colors = getStepColors(step.color);
              return (
                <div
                  key={step.number}
                  className={`scale-in relative`}
                  style={{animationDelay: `${0.3 + index * 0.2}s`}}
                >
                  {/* Connection Line (Hidden on Mobile) */}
                  {index < steps.length - 1 && (
                    <div className="hidden md:block absolute top-16 left-full w-8 z-10">
                      <ArrowRight 
                        className="w-6 h-6 text-gray-300 transform translate-x-2" 
                      />
                    </div>
                  )}

                  <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300 h-full">
                    {/* Step Number */}
                    <div className={`w-16 h-16 ${colors.bg} ${colors.border} border-2 rounded-full flex items-center justify-center mb-6 mx-auto`}>
                      <span className={`text-2xl font-bold ${colors.text}`}>
                        {step.number}
                      </span>
                    </div>

                    {/* Icon */}
                    <div className={`w-16 h-16 ${colors.bg} rounded-full flex items-center justify-center mx-auto mb-6 hover-float`}>
                      <div className={colors.text}>
                        {step.icon}
                      </div>
                    </div>

                    {/* Content */}
                    <div className="text-center">
                      <h3 className="heading-3 mb-4">{step.title}</h3>
                      <p className="body-medium text-gray-600">{step.description}</p>
                    </div>

                    {/* Decorative Elements */}
                    <div className="mt-6 flex justify-center space-x-1">
                      {[...Array(3)].map((_, i) => (
                        <div
                          key={i}
                          className={`w-2 h-2 ${colors.bg} rounded-full`}
                          style={{animationDelay: `${i * 0.2}s`}}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Additional Info */}
          <div className="mt-16 text-center fade-in-up" style={{animationDelay: '0.9s'}}>
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 max-w-3xl mx-auto">
              <h3 className="heading-3 mb-4">Processo 100% Seguro</h3>
              <p className="body-medium text-gray-600 mb-6">
                Todos os nossos providers e brokers passam por um rigoroso processo de verificação. 
                As estatísticas são auditadas regularmente para garantir transparência total.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center hover-float">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <span className="text-green-600 font-bold text-lg">✓</span>
                  </div>
                  <div className="body-small">
                    <div className="font-semibold" style={{color: 'var(--text-primary)'}}>Verificação KYC</div>
                    <div>Todos os providers</div>
                  </div>
                </div>

                <div className="text-center hover-float" style={{animationDelay: '0.1s'}}>
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <span className="text-blue-600 font-bold text-lg">✓</span>
                  </div>
                  <div className="body-small">
                    <div className="font-semibold" style={{color: 'var(--text-primary)'}}>Auditoria Mensal</div>
                    <div>Dados em tempo real</div>
                  </div>
                </div>

                <div className="text-center hover-float" style={{animationDelay: '0.2s'}}>
                  <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <span className="text-purple-600 font-bold text-lg">✓</span>
                  </div>
                  <div className="body-small">
                    <div className="font-semibold" style={{color: 'var(--text-primary)'}}>Suporte 24/7</div>
                    <div>Sempre disponível</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;