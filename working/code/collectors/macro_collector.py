"""Financial macro data collector using yfinance."""
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import yfinance as yf

logger = logging.getLogger(__name__)


class MacroCollector:
    """Collector for financial macro data: power generation, exports, PMI."""

    # Yahoo Finance tickers for macro indicators
    TICKERS = {
        # US macro indicators
        'us_pmi': 'SPINITL',  # S&P Global US Manufacturing PMI
        'us_exports': 'XTUPUS',  # US Exports
        'us_industrial_production': 'FRED:INDPRO',  # Industrial Production
        # China macro (via ETF proxies)
        'china_pmi': 'FXI',  # China PMI ETF (iShares)
        'china_exports': 'CHIX',  # China Exports ETF
        # Global/economic
        'copper': 'COPX',  # Copper (industrial metal proxy)
        'oil': 'USO',  # Oil
        'gold': 'GLD',  # Gold
    }

    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.last_fetch: Optional[datetime] = None

    def fetch_power_generation(self, period: str = "1y") -> Dict[str, Any]:
        """Fetch power generation proxy data via industrial ETFs."""
        result = {'source': 'power_generation', 'data': [], 'timestamp': datetime.now().isoformat()}
        
        # Use industrial production as proxy
        tickers = ['INDPRO', 'IGE', 'XLI']  # Industrial, Energy, Infrastructure ETFs
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                if not hist.empty:
                    result['data'].append({
                        'ticker': ticker,
                        'type': 'etf_price',
                        'data_points': len(hist),
                        'latest': float(hist['Close'].iloc[-1]),
                        'latest_date': str(hist.index[-1].date())
                    })
            except Exception as e:
                logger.warning(f"Failed to fetch {ticker}: {e}")
        
        logger.info(f"Fetched power/industrial data: {len(result['data'])} series")
        return result

    def fetch_exports(self, period: str = "1y") -> Dict[str, Any]:
        """Fetch export-related data via country ETFs."""
        result = {'source': 'exports', 'data': [], 'timestamp': datetime.now().isoformat()}
        
        # Export-heavy country ETFs as proxies
        tickers = ['FXI', 'EWH', 'EWJ', 'EWN']  # China, Hong Kong, Japan, Netherlands
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                if not hist.empty:
                    result['data'].append({
                        'ticker': ticker,
                        'type': 'etf_price',
                        'data_points': len(hist),
                        'latest': float(hist['Close'].iloc[-1]),
                        'latest_date': str(hist.index[-1].date())
                    })
            except Exception as e:
                logger.warning(f"Failed to fetch {ticker}: {e}")
        
        logger.info(f"Fetched export data: {len(result['data'])} series")
        return result

    def fetch_pmi(self, period: str = "1y") -> Dict[str, Any]:
        """Fetch PMI data via related ETFs."""
        result = {'source': 'pmi', 'data': [], 'timestamp': datetime.now().isoformat()}
        
        # PMI indicates manufacturing health - use related ETFs
        tickers = ['IWM', 'IWD', 'VB']  # Russell 2000, Value, Small Cap
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                if not hist.empty:
                    result['data'].append({
                        'ticker': ticker,
                        'type': 'etf_price',
                        'data_points': len(hist),
                        'latest': float(hist['Close'].iloc[-1]),
                        'latest_date': str(hist.index[-1].date())
                    })
            except Exception as e:
                logger.warning(f"Failed to fetch {ticker}: {e}")
        
        logger.info(f"Fetched PMI proxy data: {len(result['data'])} series")
        return result

    def fetch_all(self, period: str = "1y") -> Dict[str, Any]:
        """Fetch all macro data."""
        self.data = {
            'power_generation': self.fetch_power_generation(period),
            'exports': self.fetch_exports(period),
            'pmi': self.fetch_pmi(period)
        }
        self.last_fetch = datetime.now()
        return self.data

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of collected data."""
        return {
            'last_fetch': self.last_fetch.isoformat() if self.last_fetch else None,
            'sources': list(self.data.keys()) if self.data else []
        }


if __name__ == "__main__":
    collector = MacroCollector()
    all_data = collector.fetch_all()
    print(f"Collected macro data: {collector.get_summary()}")
    import json
    print(json.dumps(all_data, indent=2))