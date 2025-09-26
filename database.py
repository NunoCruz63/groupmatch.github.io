from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os
from models import Provider, Broker, Testimonial
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db: AsyncIOMotorDatabase = None
    
    async def connect(self):
        """Connect to MongoDB"""
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'tradinghub')
        
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[db_name]
        
        logger.info(f"Connected to MongoDB: {db_name}")
        
        # Initialize with seed data if collections are empty
        await self._seed_data()
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    async def _seed_data(self):
        """Seed database with initial mock data"""
        try:
            # Check if collections are empty
            provider_count = await self.db.providers.count_documents({})
            broker_count = await self.db.brokers.count_documents({})
            testimonial_count = await self.db.testimonials.count_documents({})
            
            if provider_count == 0:
                await self._seed_providers()
                logger.info("Seeded providers collection")
            
            if broker_count == 0:
                await self._seed_brokers()
                logger.info("Seeded brokers collection")
                
            if testimonial_count == 0:
                await self._seed_testimonials()
                logger.info("Seeded testimonials collection")
                
        except Exception as e:
            logger.error(f"Error seeding data: {str(e)}")
    
    async def _seed_providers(self):
        """Seed providers collection"""
        providers = [
            {
                "id": "1",
                "name": "Alpha Signals",
                "winRate": 87,
                "tradesLastMonth": 156,
                "signalTypes": ["Forex", "Crypto"],
                "subscriptionPrice": 99,
                "currency": "USD",
                "rating": 4.8,
                "followers": 2340,
                "description": "Estratégias conservadoras com foco em capital preservation",
                "riskLevel": "Baixo",
                "avgPipsProfitMonthly": 450,
                "verified": True,
                "affiliateUrl": "https://alphasignals.com/subscribe",
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            },
            {
                "id": "2",
                "name": "CryptoWave Pro",
                "winRate": 92,
                "tradesLastMonth": 89,
                "signalTypes": ["Crypto", "DeFi"],
                "subscriptionPrice": 149,
                "currency": "USD",
                "rating": 4.9,
                "followers": 1890,
                "description": "Especialistas em movimentos cripto de alta volatilidade",
                "riskLevel": "Alto",
                "avgPipsProfitMonthly": 680,
                "verified": True,
                "affiliateUrl": "https://cryptowavepro.com/join",
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            },
            {
                "id": "3",
                "name": "ForexProX Elite",
                "winRate": 84,
                "tradesLastMonth": 203,
                "signalTypes": ["Forex", "CFDs"],
                "subscriptionPrice": 79,
                "currency": "USD",
                "rating": 4.7,
                "followers": 3120,
                "description": "High-frequency trading com análise técnica avançada",
                "riskLevel": "Médio",
                "avgPipsProfitMonthly": 380,
                "verified": True,
                "affiliateUrl": "https://forexprox.com/premium",
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            },
            {
                "id": "4",
                "name": "GoldMaster Signals",
                "winRate": 89,
                "tradesLastMonth": 67,
                "signalTypes": ["Commodities", "Forex"],
                "subscriptionPrice": 119,
                "currency": "USD",
                "rating": 4.6,
                "followers": 1450,
                "description": "Especialistas em metais preciosos e commodities",
                "riskLevel": "Baixo",
                "avgPipsProfitMonthly": 520,
                "verified": True,
                "affiliateUrl": "https://goldmaster.com/subscribe",
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            },
            {
                "id": "5",
                "name": "Scalping Masters",
                "winRate": 78,
                "tradesLastMonth": 421,
                "signalTypes": ["Forex", "Indices"],
                "subscriptionPrice": 199,
                "currency": "USD",
                "rating": 4.4,
                "followers": 2890,
                "description": "Scalping de alta frequência para traders experientes",
                "riskLevel": "Alto",
                "avgPipsProfitMonthly": 750,
                "verified": True,
                "affiliateUrl": "https://scalpingmasters.com/vip",
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            },
            {
                "id": "6",
                "name": "Swing Profits",
                "winRate": 91,
                "tradesLastMonth": 34,
                "signalTypes": ["Forex", "Stocks"],
                "subscriptionPrice": 89,
                "currency": "USD",
                "rating": 4.8,
                "followers": 1670,
                "description": "Swing trading com holds de 2-5 dias",
                "riskLevel": "Médio",
                "avgPipsProfitMonthly": 320,
                "verified": True,
                "affiliateUrl": "https://swingprofits.com/access",
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            }
        ]
        
        await self.db.providers.insert_many(providers)
    
    async def _seed_brokers(self):
        """Seed brokers collection"""
        brokers = [
            {
                "id": "1",
                "name": "TradeMax Pro",
                "accountTypes": ["Standard", "Premium", "VIP"],
                "minDeposit": 100,
                "maxLeverage": "1:500",
                "spreadsFrom": 0.1,
                "currency": "USD",
                "bonus": "100% Deposit Bonus até $5000",
                "rating": 4.7,
                "regulation": ["CySEC", "FCA"],
                "instruments": ["Forex", "Crypto", "CFDs", "Commodities"],
                "platformsSupported": ["MT4", "MT5", "WebTrader"],
                "withdrawalTime": "24h",
                "customerSupport": "24/7",
                "verified": True,
                "affiliateUrl": "https://trademaxpro.com/register",
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            },
            {
                "id": "2",
                "name": "BlueFX Global",
                "accountTypes": ["Basic", "Advanced", "Professional"],
                "minDeposit": 250,
                "maxLeverage": "1:400",
                "spreadsFrom": 0.2,
                "currency": "USD",
                "bonus": "50% Welcome Bonus",
                "rating": 4.5,
                "regulation": ["ASIC", "CySEC"],
                "instruments": ["Forex", "Indices", "Commodities"],
                "platformsSupported": ["MT4", "cTrader"],
                "withdrawalTime": "1-3 days",
                "customerSupport": "24/5",
                "verified": True,
                "affiliateUrl": "https://bluefxglobal.com/signup",
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            },
            {
                "id": "3",
                "name": "PrimeMarkets",
                "accountTypes": ["Starter", "Professional", "Institutional"],
                "minDeposit": 500,
                "maxLeverage": "1:200",
                "spreadsFrom": 0.0,
                "currency": "USD",
                "bonus": "Zero Spreads Promo",
                "rating": 4.8,
                "regulation": ["FCA", "ASIC", "CySEC"],
                "instruments": ["Forex", "Crypto", "Stocks", "ETFs"],
                "platformsSupported": ["MT5", "TradingView", "WebPlatform"],
                "withdrawalTime": "Same day",
                "customerSupport": "24/7",
                "verified": True,
                "affiliateUrl": "https://primemarkets.com/open-account",
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            },
            {
                "id": "4",
                "name": "CryptoEdge Exchange",
                "accountTypes": ["Basic", "Premium"],
                "minDeposit": 50,
                "maxLeverage": "1:100",
                "spreadsFrom": 0.05,
                "currency": "USD",
                "bonus": "0% Trading Fees por 30 dias",
                "rating": 4.4,
                "regulation": ["Estonia FIU"],
                "instruments": ["Crypto", "DeFi", "NFTs"],
                "platformsSupported": ["Web App", "Mobile App"],
                "withdrawalTime": "Instant",
                "customerSupport": "24/7",
                "verified": True,
                "affiliateUrl": "https://cryptoedge.com/register",
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            },
            {
                "id": "5",
                "name": "EliteTrade Solutions",
                "accountTypes": ["Standard", "Gold", "Platinum"],
                "minDeposit": 1000,
                "maxLeverage": "1:300",
                "spreadsFrom": 0.3,
                "currency": "USD",
                "bonus": "VIP Account Manager",
                "rating": 4.6,
                "regulation": ["FCA", "CySEC"],
                "instruments": ["Forex", "Commodities", "Indices"],
                "platformsSupported": ["MT4", "MT5", "ProTrader"],
                "withdrawalTime": "24-48h",
                "customerSupport": "24/7",
                "verified": True,
                "affiliateUrl": "https://elitetrade.com/account",
                "createdAt": datetime.now(timezone.utc),
                "updatedAt": datetime.now(timezone.utc)
            }
        ]
        
        await self.db.brokers.insert_many(brokers)
    
    async def _seed_testimonials(self):
        """Seed testimonials collection"""
        testimonials = [
            {
                "id": "1",
                "name": "João Silva",
                "role": "Trader Profissional",
                "avatar": "JS",
                "rating": 5,
                "text": "Uso a plataforma há 8 meses e consegui aumentar o meu capital em 340%. Os signal providers são realmente verificados e confiáveis.",
                "location": "Lisboa, Portugal",
                "approved": True,
                "createdAt": datetime.now(timezone.utc)
            },
            {
                "id": "2",
                "name": "Maria Santos",
                "role": "Day Trader",
                "avatar": "MS",
                "rating": 5,
                "text": "A transparência das estatísticas é impressionante. Finalmente encontrei providers que realmente entregam o que prometem.",
                "location": "Porto, Portugal",
                "approved": True,
                "createdAt": datetime.now(timezone.utc)
            },
            {
                "id": "3",
                "name": "Carlos Pereira",
                "role": "Investidor Swing",
                "avatar": "CP",
                "rating": 4,
                "text": "Plataforma intuitiva e brokers com excelentes condições. O suporte é sempre prestativo e rápido nas respostas.",
                "location": "Coimbra, Portugal",
                "approved": True,
                "createdAt": datetime.now(timezone.utc)
            }
        ]
        
        await self.db.testimonials.insert_many(testimonials)

# Global database instance
database = Database()