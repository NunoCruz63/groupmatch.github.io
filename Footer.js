import React from 'react';
import { Mail, Phone, MapPin, Facebook, Twitter, Instagram, Linkedin } from 'lucide-react';

const Footer = () => {
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <footer className="bg-gray-900 text-white py-16">
      <div className="container">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          {/* Brand */}
          <div>
            <div className="font-bold text-2xl mb-4" style={{color: 'var(--accent-primary)'}}>
              TradingHub
            </div>
            <p className="body-small text-gray-300 mb-6">
              A plataforma líder para descobrir os melhores signal providers e brokers de trading com transparência total.
            </p>
            <div className="flex gap-4">
              <div className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer">
                <Facebook className="w-5 h-5" />
              </div>
              <div className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer">
                <Twitter className="w-5 h-5" />
              </div>
              <div className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer">
                <Instagram className="w-5 h-5" />
              </div>
              <div className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer">
                <Linkedin className="w-5 h-5" />
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="heading-3 text-lg mb-6">Links Rápidos</h3>
            <div className="space-y-3">
              <button onClick={() => scrollToSection('home')} className="block text-gray-300 hover:text-white transition-colors text-left">
                Home
              </button>
              <button onClick={() => scrollToSection('providers')} className="block text-gray-300 hover:text-white transition-colors text-left">
                Signal Providers
              </button>
              <button onClick={() => scrollToSection('brokers')} className="block text-gray-300 hover:text-white transition-colors text-left">
                Brokers
              </button>
              <button onClick={() => scrollToSection('how-it-works')} className="block text-gray-300 hover:text-white transition-colors text-left">
                Como Funciona
              </button>
            </div>
          </div>

          {/* Services */}
          <div>
            <h3 className="heading-3 text-lg mb-6">Serviços</h3>
            <div className="space-y-3">
              <div className="text-gray-300">Verificação de Providers</div>
              <div className="text-gray-300">Análise de Brokers</div>
              <div className="text-gray-300">Estatísticas em Tempo Real</div>
              <div className="text-gray-300">Suporte 24/7</div>
              <div className="text-gray-300">Consultoria Premium</div>
            </div>
          </div>

          {/* Contact */}
          <div id="contact">
            <h3 className="heading-3 text-lg mb-6">Contactos</h3>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <Mail className="w-5 h-5 text-gray-400 mt-1 flex-shrink-0" />
                <div>
                  <div className="text-white">suporte@tradinghub.com</div>
                  <div className="text-gray-400 text-sm">Suporte geral</div>
                </div>
              </div>
              
              <div className="flex items-start gap-3">
                <Phone className="w-5 h-5 text-gray-400 mt-1 flex-shrink-0" />
                <div>
                  <div className="text-white">+351 21 123 4567</div>
                  <div className="text-gray-400 text-sm">Segunda a Sexta, 9h-18h</div>
                </div>
              </div>
              
              <div className="flex items-start gap-3">
                <MapPin className="w-5 h-5 text-gray-400 mt-1 flex-shrink-0" />
                <div>
                  <div className="text-white">Lisboa, Portugal</div>
                  <div className="text-gray-400 text-sm">Sede principal</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-gray-400 text-sm">
              © 2024 TradingHub. Todos os direitos reservados.
            </div>
            
            <div className="flex gap-6 text-sm">
              <button className="text-gray-400 hover:text-white transition-colors">
                Política de Privacidade
              </button>
              <button className="text-gray-400 hover:text-white transition-colors">
                Termos de Serviço
              </button>
              <button className="text-gray-400 hover:text-white transition-colors">
                Aviso Legal
              </button>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;