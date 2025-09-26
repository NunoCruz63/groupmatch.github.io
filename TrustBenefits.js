import React, { useEffect, useRef } from 'react';
import { Shield, CheckCircle, CreditCard, Headphones, Users, TrendingUp, Award, Lock } from 'lucide-react';

const TrustBenefits = () => {
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

  const benefits = [
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Sinais Verificados",
      description: "Todos os signal providers passam por verificação rigorosa com auditoria de performance",
      color: "green",
      highlight: "100% Verificados"
    },
    {
      icon: <CheckCircle className="w-8 h-8" />,
      title: "Subscrição Segura",
      description: "Links afiliados oficiais com proteção SSL e pagamentos seguros garantidos",
      color: "blue",
      highlight: "SSL Protegido"
    },
    {
      icon: <CreditCard className="w-8 h-8" />,
      title: "Pagamentos via Afiliado",
      description: "Sem taxas adicionais, pagamentos processados diretamente pelos providers oficiais",
      color: "purple",
      highlight: "0% Taxas Extra"
    },
    {
      icon: <Headphones className="w-8 h-8" />,
      title: "Suporte 24/7",
      description: "Equipa de suporte especializada disponível para ajudar em qualquer questão",
      color: "orange",
      highlight: "Sempre Online"
    }
  ];

  const statistics = [
    {
      icon: <Users className="w-6 h-6" />,
      value: "10,000+",
      label: "Traders Ativos",
      color: "blue"
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      value: "87%",
      label: "Taxa de Sucesso Média",
      color: "green"
    },
    {
      icon: <Award className="w-6 h-6" />,
      value: "250+",
      label: "Providers Verificados",
      color: "purple"
    },
    {
      icon: <Lock className="w-6 h-6" />,
      value: "100%",
      label: "Dados Seguros",
      color: "orange"
    }
  ];

  const getColors = (color) => {
    switch (color) {
      case 'green':
        return {
          bg: 'bg-green-100',
          text: 'text-green-600',
          border: 'border-green-200'
        };
      case 'blue':
        return {
          bg: 'bg-blue-100',
          text: 'text-blue-600',
          border: 'border-blue-200'
        };
      case 'purple':
        return {
          bg: 'bg-purple-100',
          text: 'text-purple-600',
          border: 'border-purple-200'
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
    <section id="benefits" className="py-16 bg-white" ref={sectionRef}>
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="heading-2 fade-in-up mb-4">
            Porque Confiar na <span style={{color: 'var(--accent-text)'}}>TradingHub</span>
          </h2>
          <p className="body-large fade-in-up max-w-2xl mx-auto" style={{animationDelay: '0.2s'}}>
            A tua segurança e sucesso são as nossas prioridades. Oferecemos transparência total e proteção completa.
          </p>
        </div>

        {/* Main Benefits Grid */}
        <div className="trading-grid mb-16">
          {benefits.map((benefit, index) => {
            const colors = getColors(benefit.color);
            return (
              <div
                key={index}
                className={`product-card scale-in group`}
                style={{animationDelay: `${0.3 + index * 0.1}s`}}
              >
                {/* Highlight Badge */}
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${colors.bg} ${colors.text} mb-4`}>
                  {benefit.highlight}
                </div>

                {/* Icon */}
                <div className={`w-16 h-16 ${colors.bg} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <div className={colors.text}>
                    {benefit.icon}
                  </div>
                </div>

                {/* Content */}
                <h3 className="heading-3 mb-4">{benefit.title}</h3>
                <p className="body-medium text-gray-600">{benefit.description}</p>

                {/* Decorative Element */}
                <div className={`mt-6 h-1 ${colors.bg} rounded-full w-full group-hover:w-1/2 transition-all duration-300`}></div>
              </div>
            );
          })}
        </div>

        {/* Statistics Section */}
        <div className="fade-in-up" style={{animationDelay: '0.7s'}}>
          <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-3xl p-8">
            <div className="text-center mb-8">
              <h3 className="heading-3 mb-2">Números que Falam por Si</h3>
              <p className="body-medium text-gray-600">
                Estatísticas reais da nossa plataforma em tempo real
              </p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {statistics.map((stat, index) => {
                const colors = getColors(stat.color);
                return (
                  <div
                    key={index}
                    className={`text-center hover-float`}
                    style={{animationDelay: `${index * 0.1}s`}}
                  >
                    <div className={`w-12 h-12 ${colors.bg} rounded-full flex items-center justify-center mx-auto mb-3`}>
                      <div className={colors.text}>
                        {stat.icon}
                      </div>
                    </div>
                    <div className="text-2xl font-bold mb-1" style={{color: 'var(--text-primary)'}}>
                      {stat.value}
                    </div>
                    <div className="body-small text-gray-600">{stat.label}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Trust Seals */}
        <div className="mt-16 text-center fade-in-up" style={{animationDelay: '0.9s'}}>
          <p className="body-small text-gray-500 mb-6">Certificados e Parceiros de Confiança</p>
          
          <div className="flex justify-center items-center flex-wrap gap-8 opacity-60">
            {/* Mock trust seals */}
            <div className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-full">
              <Shield className="w-4 h-4 text-green-600" />
              <span className="text-sm font-medium">SSL Verified</span>
            </div>
            
            <div className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-full">
              <CheckCircle className="w-4 h-4 text-blue-600" />
              <span className="text-sm font-medium">KYC Compliant</span>
            </div>
            
            <div className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-full">
              <Award className="w-4 h-4 text-purple-600" />
              <span className="text-sm font-medium">ISO Certified</span>
            </div>
            
            <div className="flex items-center gap-2 px-4 py-2 bg-gray-100 rounded-full">
              <Lock className="w-4 h-4 text-orange-600" />
              <span className="text-sm font-medium">GDPR Protected</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TrustBenefits;