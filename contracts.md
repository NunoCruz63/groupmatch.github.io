# TradingHub - Contratos de Integração Frontend/Backend

## Resumo da Implementação
- **Frontend**: Landing page completa com dados mock
- **Backend**: APIs CRUD + Emergent Auth + MongoDB
- **Integração**: Substituir dados mock por APIs reais

## Dados Mock Atuais

### Signal Providers (`/src/mock/mockData.js`)
```javascript
{
  id, name, winRate, tradesLastMonth, signalTypes[], 
  subscriptionPrice, currency, rating, followers, 
  description, riskLevel, avgPipsProfitMonthly, 
  verified, affiliateUrl
}
```

### Brokers (`/src/mock/mockData.js`)
```javascript
{
  id, name, accountTypes[], minDeposit, maxLeverage,
  spreadsFrom, currency, bonus, rating, regulation[],
  instruments[], platformsSupported[], withdrawalTime,
  customerSupport, verified, affiliateUrl
}
```

### Testimonials
```javascript
{
  id, name, role, avatar, rating, text, location
}
```

## APIs Backend Necessárias

### 1. Signal Providers
- `GET /api/providers` - Listar todos com filtros
- `POST /api/providers` - Criar (admin)
- `PUT /api/providers/:id` - Editar (admin)
- `DELETE /api/providers/:id` - Apagar (admin)
- `GET /api/providers/search?q=` - Pesquisar

### 2. Brokers
- `GET /api/brokers` - Listar todos com filtros
- `POST /api/brokers` - Criar (admin)
- `PUT /api/brokers/:id` - Editar (admin)
- `DELETE /api/brokers/:id` - Apagar (admin)
- `GET /api/brokers/search?q=` - Pesquisar

### 3. Testimonials
- `GET /api/testimonials` - Listar todos
- `POST /api/testimonials` - Criar (admin)
- `PUT /api/testimonials/:id` - Editar (admin)
- `DELETE /api/testimonials/:id` - Apagar (admin)

### 4. Autenticação (Emergent Auth)
- `POST /api/auth/login` - Google login
- `GET /api/auth/me` - User info
- `POST /api/auth/logout` - Logout
- Middleware de proteção para rotas admin

## Modelos MongoDB

### Provider Model
```python
class Provider(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    winRate: int
    tradesLastMonth: int
    signalTypes: List[str]
    subscriptionPrice: int
    currency: str
    rating: float
    followers: int
    description: str
    riskLevel: str
    avgPipsProfitMonthly: int
    verified: bool
    affiliateUrl: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
```

### Broker Model
```python
class Broker(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    accountTypes: List[str]
    minDeposit: int
    maxLeverage: str
    spreadsFrom: float
    currency: str
    bonus: str
    rating: float
    regulation: List[str]
    instruments: List[str]
    platformsSupported: List[str]
    withdrawalTime: str
    customerSupport: str
    verified: bool
    affiliateUrl: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
```

### Testimonial Model
```python
class Testimonial(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    role: str
    avatar: str
    rating: int
    text: str
    location: str
    approved: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)
```

## Filtros e Pesquisa

### Providers Filters
- `signalType`: Forex, Crypto, CFDs, Commodities, Stocks
- `riskLevel`: Baixo, Médio, Alto
- `priceRange`: 0-100, 100-150, 150+
- `search`: Nome + signalTypes

### Brokers Filters  
- `instrumentType`: Forex, Crypto, CFDs, Stocks, Commodities
- `minDeposit`: <=100, <=250, <=500, <=1000
- `regulation`: FCA, CySEC, ASIC
- `search`: Nome + instruments

## Admin Dashboard

### Rotas Frontend
- `/admin` - Login page
- `/admin/dashboard` - Overview stats
- `/admin/providers` - CRUD providers
- `/admin/brokers` - CRUD brokers
- `/admin/testimonials` - CRUD testimonials

### Funcionalidades Admin
- Autenticação via Emergent (Google)
- Criar/editar/apagar providers/brokers
- Visualizar estatísticas básicas
- Aprovar/rejeitar testimonials

## Integração Frontend

### Substituir Mock Data
1. `SignalProviders.js` - usar `useEffect` para fetch `/api/providers`
2. `BrokersSection.js` - usar `useEffect` para fetch `/api/brokers` 
3. `TestimonialsSection.js` - usar `useEffect` para fetch `/api/testimonials`

### API Service
```javascript
// /src/services/api.js
const API_BASE = process.env.REACT_APP_BACKEND_URL + '/api';

export const apiService = {
  providers: {
    getAll: (filters) => fetch(`${API_BASE}/providers?${new URLSearchParams(filters)}`),
    search: (query) => fetch(`${API_BASE}/providers/search?q=${query}`)
  },
  brokers: {
    getAll: (filters) => fetch(`${API_BASE}/brokers?${new URLSearchParams(filters)}`),
    search: (query) => fetch(`${API_BASE}/brokers/search?q=${query}`)
  }
};
```

## Dados Iniciais (Seed)
- Povoar DB com dados mock atuais como dados iniciais
- Script de seed para providers, brokers e testimonials
- Admin user inicial

## Fases de Implementação
1. ✅ Frontend com mock data
2. 🔄 Backend APIs + MongoDB models
3. 🔄 Emergent Auth integração  
4. 🔄 Admin dashboard
5. 🔄 Integração frontend/backend
6. 🔄 Testes e validação