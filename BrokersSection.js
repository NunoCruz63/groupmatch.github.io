import React, { useState, useEffect, useRef } from 'react';
import { Filter, Search, Star, ExternalLink, Shield, Clock, Globe, Award } from 'lucide-react';
import { mockBrokers } from '../mock/mockData';

const BrokersSection = () => {
  const [brokers, setBrokers] = useState(mockBrokers);
  const [filteredBrokers, setFilteredBrokers] = useState(mockBrokers);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    instrumentType: 'all',
    minDeposit: 'all',
    regulation: 'all'
  });
  const [showFilters, setShowFilters] = useState(false);
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

  useEffect(() => {
    let filtered = brokers;

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(broker =>
        broker.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        broker.instruments.some(instrument => 
          instrument.toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }

    // Instrument type filter
    if (filters.instrumentType !== 'all') {
      filtered = filtered.filter(broker =>
        broker.instruments.includes(filters.instrumentType)
      );
    }

    // Min deposit filter
    if (filters.minDeposit !== 'all') {
      const maxDeposit = parseInt(filters.minDeposit);
      filtered = filtered.filter(broker => broker.minDeposit <= maxDeposit);
    }

    // Regulation filter
    if (filters.regulation !== 'all') {
      filtered = filtered.filter(broker =>
        broker.regulation.includes(filters.regulation)
      );
    }

    setFilteredBrokers(filtered);
  }, [searchTerm, filters, brokers]);

  const handleOpenAccount = (broker) => {
    // Mock account opening - will be implemented with backend
    window.open(broker.affiliateUrl, '_blank');
  };

  return (
    <section id="brokers" className="py-16 bg-white" ref={sectionRef}>
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="heading-2 fade-in-up mb-4">
            Brokers <span style={{color: 'var(--accent-text)'}}>Recomendados</span>
          </h2>
          <p className="body-large fade-in-up" style={{animationDelay: '0.2s'}}>
            Brokers verificados com as melhores condições de trading
          </p>
        </div>

        {/* Search and Filters */}
        <div className="mb-8 fade-in-up" style={{animationDelay: '0.4s'}}>
          <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
            {/* Search Bar */}
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Pesquisar brokers..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-3 border border-gray-200 rounded-full w-full text-sm focus:outline-none focus:border-gray-400"
              />
            </div>

            {/* Filter Toggle */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="btn-secondary flex items-center gap-2"
            >
              <Filter className="w-4 h-4" />
              Filtros
            </button>
          </div>

          {/* Filter Panel */}
          {showFilters && (
            <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Tipo de Ativo</label>
                  <select
                    value={filters.instrumentType}
                    onChange={(e) => setFilters({...filters, instrumentType: e.target.value})}
                    className="w-full p-2 border border-gray-200 rounded-lg text-sm"
                  >
                    <option value="all">Todos</option>
                    <option value="Forex">Forex</option>
                    <option value="Crypto">Crypto</option>
                    <option value="CFDs">CFDs</option>
                    <option value="Stocks">Stocks</option>
                    <option value="Commodities">Commodities</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Depósito Mínimo</label>
                  <select
                    value={filters.minDeposit}
                    onChange={(e) => setFilters({...filters, minDeposit: e.target.value})}
                    className="w-full p-2 border border-gray-200 rounded-lg text-sm"
                  >
                    <option value="all">Todos</option>
                    <option value="100">Até $100</option>
                    <option value="250">Até $250</option>
                    <option value="500">Até $500</option>
                    <option value="1000">Até $1000</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Regulação</label>
                  <select
                    value={filters.regulation}
                    onChange={(e) => setFilters({...filters, regulation: e.target.value})}
                    className="w-full p-2 border border-gray-200 rounded-lg text-sm"
                  >
                    <option value="all">Todas</option>
                    <option value="FCA">FCA (Reino Unido)</option>
                    <option value="CySEC">CySEC (Chipre)</option>
                    <option value="ASIC">ASIC (Austrália)</option>
                  </select>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Brokers Grid */}
        <div className="trading-grid">
          {filteredBrokers.map((broker, index) => (
            <div
              key={broker.id}
              className={`product-card scale-in`}
              style={{animationDelay: `${0.1 * index}s`}}
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="heading-3 text-lg">{broker.name}</h3>
                    {broker.verified && (
                      <Shield className="w-5 h-5" style={{color: 'var(--accent-text)'}} />
                    )}
                  </div>
                  <div className="flex items-center gap-2 mb-2">
                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                    <span className="text-sm font-medium">{broker.rating}</span>
                  </div>
                </div>
                <div className="flex gap-1">
                  {broker.regulation.map((reg, idx) => (
                    <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                      {reg}
                    </span>
                  ))}
                </div>
              </div>

              {/* Bonus/Promotion Highlight */}
              {broker.bonus && (
                <div className="bg-gradient-to-r from-orange-100 to-yellow-100 border-l-4 border-orange-400 p-3 mb-4 rounded-r">
                  <div className="flex items-center gap-2">
                    <Award className="w-4 h-4 text-orange-600" />
                    <span className="text-sm font-medium text-orange-800">{broker.bonus}</span>
                  </div>
                </div>
              )}

              <div className="space-y-3 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-sm">Spreads desde:</span>
                  <span className="font-bold" style={{color: 'var(--accent-text)'}}>{broker.spreadsFrom} pips</span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm">Alavancagem máx:</span>
                  <span className="font-medium">{broker.maxLeverage}</span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm">Depósito mínimo:</span>
                  <span className="font-medium">${broker.minDeposit}</span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    Retiradas:
                  </span>
                  <span className="font-medium">{broker.withdrawalTime}</span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm flex items-center gap-1">
                    <Globe className="w-3 h-3" />
                    Suporte:
                  </span>
                  <span className="font-medium">{broker.customerSupport}</span>
                </div>
              </div>

              {/* Account Types */}
              <div className="mb-4">
                <div className="text-sm font-medium mb-2">Tipos de Conta:</div>
                <div className="flex flex-wrap gap-1">
                  {broker.accountTypes.map((type, idx) => (
                    <span key={idx} className="px-2 py-1 bg-gray-100 text-xs rounded-full">
                      {type}
                    </span>
                  ))}
                </div>
              </div>

              {/* Trading Instruments */}
              <div className="mb-4">
                <div className="text-sm font-medium mb-2">Instrumentos:</div>
                <div className="flex flex-wrap gap-1">
                  {broker.instruments.map((instrument, idx) => (
                    <span key={idx} className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-full">
                      {instrument}
                    </span>
                  ))}
                </div>
              </div>

              {/* Platforms */}
              <div className="mb-6">
                <div className="text-sm font-medium mb-2">Plataformas:</div>
                <div className="flex flex-wrap gap-1">
                  {broker.platformsSupported.map((platform, idx) => (
                    <span key={idx} className="px-2 py-1 bg-green-50 text-green-700 text-xs rounded-full">
                      {platform}
                    </span>
                  ))}
                </div>
              </div>

              <div className="border-t pt-4">
                <div className="flex gap-2">
                  <button className="btn-secondary text-sm px-4 py-2 flex-1">
                    Ver Detalhes
                  </button>
                  <button
                    onClick={() => handleOpenAccount(broker)}
                    className="btn-primary text-sm px-4 py-2 flex-1 flex items-center justify-center gap-1"
                  >
                    Abrir Conta
                    <ExternalLink className="w-3 h-3" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredBrokers.length === 0 && (
          <div className="text-center py-12">
            <p className="body-medium text-gray-500">
              Nenhum broker encontrado com os filtros selecionados.
            </p>
          </div>
        )}
      </div>
    </section>
  );
};

export default BrokersSection;