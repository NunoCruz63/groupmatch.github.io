import React, { useState, useEffect, useRef } from 'react';
import { Filter, Search, Star, TrendingUp, Shield, ExternalLink, Users } from 'lucide-react';
import { mockProviders } from '../mock/mockData';

const SignalProviders = () => {
  const [providers, setProviders] = useState(mockProviders);
  const [filteredProviders, setFilteredProviders] = useState(mockProviders);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    signalType: 'all',
    riskLevel: 'all',
    priceRange: 'all'
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
    let filtered = providers;

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(provider =>
        provider.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        provider.signalTypes.some(type => type.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Signal type filter
    if (filters.signalType !== 'all') {
      filtered = filtered.filter(provider =>
        provider.signalTypes.includes(filters.signalType)
      );
    }

    // Risk level filter
    if (filters.riskLevel !== 'all') {
      filtered = filtered.filter(provider =>
        provider.riskLevel.toLowerCase() === filters.riskLevel
      );
    }

    // Price range filter
    if (filters.priceRange !== 'all') {
      const [min, max] = filters.priceRange.split('-').map(Number);
      filtered = filtered.filter(provider => {
        if (max) {
          return provider.subscriptionPrice >= min && provider.subscriptionPrice <= max;
        }
        return provider.subscriptionPrice >= min;
      });
    }

    setFilteredProviders(filtered);
  }, [searchTerm, filters, providers]);

  const getRiskColor = (riskLevel) => {
    switch (riskLevel.toLowerCase()) {
      case 'baixo': return 'text-green-600 bg-green-100';
      case 'médio': return 'text-yellow-600 bg-yellow-100';
      case 'alto': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const handleSubscribe = (provider) => {
    // Mock subscription - will be implemented with backend
    window.open(provider.affiliateUrl, '_blank');
  };

  return (
    <section id="providers" className="py-16 bg-gray-50" ref={sectionRef}>
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="heading-2 fade-in-up mb-4">
            Signal Providers <span style={{color: 'var(--accent-text)'}}>Verificados</span>
          </h2>
          <p className="body-large fade-in-up" style={{animationDelay: '0.2s'}}>
            Descobre os melhores signal providers com estatísticas reais e transparentes
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
                placeholder="Pesquisar providers..."
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
            <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Tipo de Sinal</label>
                  <select
                    value={filters.signalType}
                    onChange={(e) => setFilters({...filters, signalType: e.target.value})}
                    className="w-full p-2 border border-gray-200 rounded-lg text-sm"
                  >
                    <option value="all">Todos</option>
                    <option value="Forex">Forex</option>
                    <option value="Crypto">Crypto</option>
                    <option value="CFDs">CFDs</option>
                    <option value="Commodities">Commodities</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Nível de Risco</label>
                  <select
                    value={filters.riskLevel}
                    onChange={(e) => setFilters({...filters, riskLevel: e.target.value})}
                    className="w-full p-2 border border-gray-200 rounded-lg text-sm"
                  >
                    <option value="all">Todos</option>
                    <option value="baixo">Baixo</option>
                    <option value="médio">Médio</option>
                    <option value="alto">Alto</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Preço (USD)</label>
                  <select
                    value={filters.priceRange}
                    onChange={(e) => setFilters({...filters, priceRange: e.target.value})}
                    className="w-full p-2 border border-gray-200 rounded-lg text-sm"
                  >
                    <option value="all">Todos</option>
                    <option value="0-100">$0 - $100</option>
                    <option value="100-150">$100 - $150</option>
                    <option value="150-9999">$150+</option>
                  </select>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Providers Grid */}
        <div className="trading-grid">
          {filteredProviders.map((provider, index) => (
            <div
              key={provider.id}
              className={`product-card scale-in`}
              style={{animationDelay: `${0.1 * index}s`}}
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="heading-3 text-lg">{provider.name}</h3>
                    {provider.verified && (
                      <Shield className="w-5 h-5" style={{color: 'var(--accent-text)'}} />
                    )}
                  </div>
                  <div className="flex items-center gap-2 mb-2">
                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                    <span className="text-sm font-medium">{provider.rating}</span>
                    <span className="text-xs text-gray-500">({provider.followers} seguidores)</span>
                  </div>
                </div>
                <div className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(provider.riskLevel)}`}>
                  {provider.riskLevel}
                </div>
              </div>

              <p className="body-small mb-4">{provider.description}</p>

              <div className="space-y-3 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-sm">Win Rate:</span>
                  <div className="flex items-center gap-2">
                    <span className="font-bold" style={{color: 'var(--accent-text)'}}>{provider.winRate}%</span>
                    <TrendingUp className="w-4 h-4" style={{color: 'var(--accent-text)'}} />
                  </div>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm">Trades (último mês):</span>
                  <span className="font-medium">{provider.tradesLastMonth}</span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm">Profit médio/mês:</span>
                  <span className="font-medium" style={{color: 'var(--accent-text)'}}>
                    {provider.avgPipsProfitMonthly} pips
                  </span>
                </div>
              </div>

              <div className="flex flex-wrap gap-1 mb-4">
                {provider.signalTypes.map((type, idx) => (
                  <span key={idx} className="px-2 py-1 bg-gray-100 text-xs rounded-full">
                    {type}
                  </span>
                ))}
              </div>

              <div className="border-t pt-4">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <div className="text-2xl font-bold" style={{color: 'var(--text-primary)'}}>
                      ${provider.subscriptionPrice}
                    </div>
                    <div className="text-sm text-gray-500">por mês</div>
                  </div>
                  <Users className="w-6 h-6 text-gray-400" />
                </div>

                <div className="flex gap-2">
                  <button className="btn-secondary text-sm px-4 py-2 flex-1">
                    Ver Detalhes
                  </button>
                  <button
                    onClick={() => handleSubscribe(provider)}
                    className="btn-primary text-sm px-4 py-2 flex-1 flex items-center justify-center gap-1"
                  >
                    Subscrever
                    <ExternalLink className="w-3 h-3" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredProviders.length === 0 && (
          <div className="text-center py-12">
            <p className="body-medium text-gray-500">
              Nenhum provider encontrado com os filtros selecionados.
            </p>
          </div>
        )}
      </div>
    </section>
  );
};

export default SignalProviders;