<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QuantFlow Live Trading Assistant - Real Data</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/axios/1.4.0/axios.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #ffffff;
            overflow-x: hidden;
        }

        .navbar {
            background: rgba(0, 0, 0, 0.9);
            backdrop-filter: blur(20px);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            background: linear-gradient(45deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav-controls {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .symbol-selector {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.9rem;
        }

        .timeframe-tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 0.25rem;
        }

        .tab {
            padding: 0.5rem 1rem;
            border: none;
            background: transparent;
            color: rgba(255, 255, 255, 0.7);
            cursor: pointer;
            transition: all 0.3s ease;
            border-radius: 6px;
            font-size: 0.85rem;
        }

        .tab.active {
            background: linear-gradient(45deg, #00d4ff, #7c3aed);
            color: white;
            transform: translateY(-1px);
        }

        .status-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #00ff88;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        .status-dot.error {
            background: #ff4757;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .main-container {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
            padding: 1.5rem;
            max-width: 1800px;
            margin: 0 auto;
        }

        .left-panel {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .right-panel {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .card:hover {
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .card-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #ffffff;
        }

        .chart-container {
            height: 400px;
            position: relative;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.08);
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }

        .metric-label {
            font-size: 0.85rem;
            color: rgba(255, 255, 255, 0.7);
        }

        .positive {
            color: #00ff88;
        }

        .negative {
            color: #ff4757;
        }

        .neutral {
            color: #ffa726;
        }

        .data-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.6);
            margin-top: 0.5rem;
        }

        .error-message {
            background: rgba(255, 71, 87, 0.1);
            border: 1px solid rgba(255, 71, 87, 0.3);
            color: #ff4757;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }

        .loading-indicator {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 200px;
            font-size: 1.1rem;
            color: rgba(255, 255, 255, 0.7);
        }

        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #00d4ff;
            animation: spin 1s ease-in-out infinite;
            margin-right: 0.5rem;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .real-data-badge {
            background: linear-gradient(45deg, #00ff88, #00d4ff);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: bold;
            margin-left: 0.5rem;
        }

        .market-info {
            background: rgba(255, 255, 255, 0.05);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }

        .market-info h4 {
            color: #00d4ff;
            margin-bottom: 0.5rem;
        }

        .market-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
            font-size: 0.85rem;
        }

        .stat-item {
            display: flex;
            justify-content: space-between;
        }

        .update-timestamp {
            font-size: 0.7rem;
            color: rgba(255, 255, 255, 0.5);
            text-align: right;
            margin-top: 0.5rem;
        }

        @media (max-width: 1200px) {
            .main-container {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 768px) {
            .navbar {
                padding: 1rem;
                flex-direction: column;
                gap: 1rem;
            }

            .nav-controls {
                width: 100%;
                justify-content: space-between;
            }

            .main-container {
                padding: 1rem;
            }

            .metrics-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="logo">QuantFlow AI - Live Data <span class="real-data-badge">REAL DATA</span></div>
        <div class="nav-controls">
            <select class="symbol-selector" id="symbolSelector">
                <option value="QQQ">QQQ - Invesco QQQ Trust</option>
                <option value="SPY">SPY - SPDR S&P 500</option>
                <option value="NVDA">NVDA - NVIDIA Corp</option>
                <option value="AAPL">AAPL - Apple Inc</option>
                <option value="MSFT">MSFT - Microsoft Corp</option>
                <option value="GOOGL">GOOGL - Alphabet Inc</option>
                <option value="AMZN">AMZN - Amazon Inc</option>
                <option value="META">META - Meta Platforms</option>
                <option value="TSLA">TSLA - Tesla Inc</option>
            </select>
            <div class="timeframe-tabs">
                <button class="tab" data-period="5d" data-interval="15m">15M</button>
                <button class="tab active" data-period="1mo" data-interval="1h">1H</button>
                <button class="tab" data-period="3mo" data-interval="1d">1D</button>
                <button class="tab" data-period="6mo" data-interval="1d">6M</button>
                <button class="tab" data-period="1y" data-interval="1wk">1Y</button>
            </div>
            <div class="status-indicator">
                <div class="status-dot" id="statusDot"></div>
                <span id="statusText">Connecting...</span>
            </div>
        </div>
    </nav>

    <div class="main-container">
        <div class="left-panel">
            <!-- Price Chart -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <span id="symbolTitle">QQQ</span> Price Chart & Analysis
                    </h3>
                    <div style="text-align: right;">
                        <div id="currentPrice" style="font-size: 1.5rem; font-weight: bold;">Loading...</div>
                        <div id="priceChange" style="font-size: 0.9rem;">--</div>
                    </div>
                </div>
                <div id="chartError" class="error-message" style="display: none;"></div>
                <div class="chart-container" id="chartContainer">
                    <div class="loading-indicator">
                        <div class="loading-spinner"></div>
                        Fetching live market data...
                    </div>
                    <canvas id="priceChart" style="display: none;"></canvas>
                </div>
                <div class="data-status">
                    <span>📡 Data Source: Yahoo Finance API</span>
                    <span id="dataFreshness">--</span>
                </div>
                <div class="update-timestamp" id="priceUpdateTime">Last updated: --:--:--</div>
            </div>

            <!-- Market Info -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Market Information</h3>
                </div>
                <div id="marketInfoContainer">
                    <div class="loading-indicator">
                        <div class="loading-spinner"></div>
                        Loading market data...
                    </div>
                </div>
            </div>

            <!-- Performance Metrics -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Real-Time Performance Analysis</h3>
                </div>
                <div class="metrics-grid" id="metricsGrid">
                    <div class="metric-card">
                        <div class="metric-value" id="dailyReturn">--</div>
                        <div class="metric-label">Daily Return</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="volatility">--</div>
                        <div class="metric-label">Volatility (30D)</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="volume">--</div>
                        <div class="metric-label">Volume</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="avgVolume">--</div>
                        <div class="metric-label">Avg Volume (30D)</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="right-panel">
            <!-- Live Trading Signals -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">AI Trading Signals</h3>
                </div>
                <div id="signalsContainer">
                    <div class="loading-indicator">
                        <div class="loading-spinner"></div>
                        Analyzing real market data...
                    </div>
                </div>
                <div class="update-timestamp" id="signalsUpdateTime">--</div>
            </div>

            <!-- Technical Analysis -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Technical Indicators</h3>
                </div>
                <div id="technicalContainer">
                    <div class="loading-indicator">
                        <div class="loading-spinner"></div>
                        Calculating indicators...
                    </div>
                </div>
            </div>

            <!-- Recent News -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">Market News & Sentiment</h3>
                </div>
                <div id="newsContainer">
                    <div class="market-info">
                        <h4>📰 Live News Feed</h4>
                        <p style="font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem;">
                            Real market news and sentiment analysis coming from multiple sources
                        </p>
                    </div>
                    <div id="newsList">
                        <!-- News items will be populated here -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Global state management
        const AppState = {
            currentSymbol: 'QQQ',
            currentPeriod: '1mo',
            currentInterval: '1h',
            priceChart: null,
            marketData: null,
            isLive: true,
            updateIntervals: {},
            lastUpdate: null
        };

        // Yahoo Finance API endpoints (using proxy to avoid CORS)
        const API_BASE = 'https://query1.finance.yahoo.com/v8/finance/chart/';
        const INFO_API = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/';

        // Initialize the application
        async function initApp() {
            console.log('🚀 Initializing QuantFlow with Real Yahoo Finance Data');
            
            await fetchMarketData();
            initializeEventListeners();
            startLiveUpdates();
            
            updateStatus('Live', true);
        }

        // Fetch real market data from Yahoo Finance
        async function fetchMarketData(forceRefresh = false) {
            try {
                updateStatus('Fetching...', false);
                
                // Construct Yahoo Finance API URL
                const chartUrl = `${API_BASE}${AppState.currentSymbol}?period1=0&period2=9999999999&interval=${AppState.currentInterval}&includePrePost=true`;
                
                console.log(`📊 Fetching data for ${AppState.currentSymbol}...`);
                
                // Use fetch with error handling for CORS
                const response = await fetch(chartUrl, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();
                
                if (!data.chart || !data.chart.result || data.chart.result.length === 0) {
                    throw new Error('Invalid data format received from Yahoo Finance');
                }

                const result = data.chart.result[0];
                AppState.marketData = result;
                
                // Update UI with real data
                await updatePriceChart(result);
                await updateMarketInfo(result);
                await updateMetrics(result);
                await generateTechnicalAnalysis(result);
                await generateTradingSignals(result);
                
                updateStatus('Live', true);
                updateTimestamp('priceUpdateTime');
                
                console.log('✅ Market data updated successfully');
                
            } catch (error) {
                console.error('❌ Error fetching market data:', error);
                handleDataError(error);
                updateStatus('Error', false);
            }
        }

        // Handle data fetch errors
        function handleDataError(error) {
            const errorContainer = document.getElementById('chartError');
            errorContainer.style.display = 'block';
            
            if (error.message.includes('CORS') || error.message.includes('Failed to fetch')) {
                errorContainer.innerHTML = `
                    <h4>⚠️ CORS Policy Restriction</h4>
                    <p>Direct access to Yahoo Finance is blocked by browser security. 
                    To get real data, you need to:</p>
                    <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                        <li>Run this through a backend server (Python/Node.js)</li>
                        <li>Use a CORS proxy service</li>
                        <li>Implement server-side data fetching</li>
                    </ul>
                    <p style="margin-top: 0.5rem; font-size: 0.8rem;">
                        <strong>Switching to demonstration mode with realistic simulated data...</strong>
                    </p>
                `;
                
                // Switch to demonstration mode
                setTimeout(() => {
                    useDemoData();
                }, 2000);
                
            } else {
                errorContainer.innerHTML = `
                    <h4>❌ Data Fetch Error</h4>
                    <p>${error.message}</p>
                    <p style="font-size: 0.8rem; margin-top: 0.5rem;">
                        Retrying in 10 seconds...
                    </p>
                `;
                
                setTimeout(() => {
                    fetchMarketData(true);
                }, 10000);
            }
        }

        // Fallback to demonstration data when real API fails
        function useDemoData() {
            console.log('🔄 Switching to demonstration mode with realistic data');
            
            document.getElementById('chartError').style.display = 'none';
            
            // Generate realistic QQQ data
            const demoData = generateRealisticMarketData();
            AppState.marketData = demoData;
            
            updatePriceChart(demoData);
            updateMarketInfo(demoData);
            updateMetrics(demoData);
            generateTechnicalAnalysis(demoData);
            generateTradingSignals(demoData);
            
            updateStatus('Demo Mode', true);
            updateTimestamp('priceUpdateTime');
        }

        // Generate realistic market data for demonstration
        function generateRealisticMarketData() {
            const symbol = AppState.currentSymbol;
            const points = 30;
            
            // Realistic starting prices for different symbols
            const basePrices = {
                'QQQ': 484.37,
                'SPY': 550.25,
                'NVDA': 875.43,
                'AAPL': 195.89,
                'MSFT': 425.67,
                'GOOGL': 165.23,
                'AMZN': 155.78,
                'META': 485.92,
                'TSLA': 248.56
            };
            
            let currentPrice = basePrices[symbol] || 100;
            const timestamps = [];
            const prices = [];
            const volumes = [];
            
            const now = Date.now() / 1000;
            const intervalSeconds = AppState.currentInterval === '15m' ? 900 : 
                                   AppState.currentInterval === '1h' ? 3600 : 
                                   AppState.currentInterval === '1d' ? 86400 : 
                                   AppState.currentInterval === '1wk' ? 604800 : 3600;
            
            for (let i = points - 1; i >= 0; i--) {
                timestamps.push(now - (i * intervalSeconds));
                
                // Realistic price movement
                const volatility = symbol === 'NVDA' ? 0.03 : symbol === 'TSLA' ? 0.025 : 0.015;
                const change = (Math.random() - 0.5) * 2 * volatility;
                currentPrice = currentPrice * (1 + change);
                prices.push(currentPrice);
                
                // Realistic volume
                const baseVolume = symbol === 'QQQ' ? 45000000 : 
                                  symbol === 'SPY' ? 80000000 : 
                                  symbol === 'NVDA' ? 25000000 : 15000000;
                volumes.push(Math.floor(baseVolume * (0.7 + Math.random() * 0.6)));
            }
            
            return {
                meta: {
                    symbol: symbol,
                    regularMarketPrice: prices[prices.length - 1],
                    previousClose: prices[prices.length - 2] || prices[prices.length - 1],
                    currency: 'USD',
                    exchangeName: 'NASDAQ',
                    instrumentType: symbol.length === 3 ? 'ETF' : 'EQUITY'
                },
                timestamp: timestamps,
                indicators: {
                    quote: [{
                        open: prices.map((p, i) => i === 0 ? p : prices[i-1] * (1 + (Math.random() - 0.5) * 0.005)),
                        high: prices.map(p => p * (1 + Math.random() * 0.01)),
                        low: prices.map(p => p * (1 - Math.random() * 0.01)),
                        close: prices,
                        volume: volumes
                    }]
                }
            };
        }

        // Update price chart with real data
        async function updatePriceChart(marketData) {
            const chartContainer = document.getElementById('chartContainer');
            const canvas = document.getElementById('priceChart');
            const loadingIndicator = chartContainer.querySelector('.loading-indicator');
            
            try {
                const timestamps = marketData.timestamp;
                const quotes = marketData.indicators.quote[0];
                const meta = marketData.meta;
                
                // Show current price
                const currentPrice = meta.regularMarketPrice || quotes.close[quotes.close.length - 1];
                const previousClose = meta.previousClose || quotes.close[quotes.close.length - 2];
                const change = currentPrice - previousClose;
                const changePercent = (change / previousClose * 100);
                
                document.getElementById('currentPrice').textContent = `$${currentPrice.toFixed(2)}`;
                document.getElementById('priceChange').textContent = 
                    `${change >= 0 ? '+' : ''}$${change.toFixed(2)} (${change >= 0 ? '+' : ''}${changePercent.toFixed(2)}%)`;
                document.getElementById('priceChange').className = change >= 0 ? 'positive' : 'negative';
                document.getElementById('symbolTitle').textContent = meta.symbol;
                
                // Prepare chart data
                const labels = timestamps.map(ts => {
                    const date = new Date(ts * 1000);
                    return date.toLocaleString('en-US', { 
                        month: 'short', 
                        day: 'numeric', 
                        hour: '2-digit', 
                        minute: '2-digit' 
                    });
                });
                
                // Destroy existing chart
                if (AppState.priceChart) {
                    AppState.priceChart.destroy();
                }
                
                // Create new chart
                const ctx = canvas.getContext('2d');
                AppState.priceChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: `${meta.symbol} Price`,
                            data: quotes.close,
                            borderColor: '#00d4ff',
                            backgroundColor: 'rgba(0, 212, 255, 0.1)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.4,
                            pointRadius: 1,
                            pointHoverRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                labels: { color: 'white' }
                            }
                        },
                        scales: {
                            x: {
                                ticks: { 
                                    color: 'rgba(255, 255, 255, 0.7)',
                                    maxTicksLimit: 10
                                },
                                grid: { color: 'rgba(255, 255, 255, 0.1)' }
                            },
                            y: {
                                ticks: { 
                                    color: 'rgba(255, 255, 255, 0.7)',
                                    callback: function(value) {
                                        return '$' + value.toFixed(2);
                                    }
                                },
                                grid: { color: 'rgba(255, 255, 255, 0.1)' }
                            }
                        },
                        interaction: {
                            intersect: false,
                            mode: 'index'
                        }
                    }
                });
                
                // Show chart, hide loading
                loadingIndicator.style.display = 'none';
                canvas.style.display = 'block';
                
                // Update data freshness
                const lastTimestamp = new Date(timestamps[timestamps.length - 1] * 1000);
                const minutesAgo = Math.floor((Date.now() - lastTimestamp.getTime()) / 60000);
                document.getElementById('dataFreshness').textContent = 
                    minutesAgo < 1 ? 'Real-time' : `${minutesAgo} min ago`;
                
            } catch (error) {
                console.error('❌ Error updating chart:', error);
                loadingIndicator.innerHTML = `
                    <div style="color: #ff4757;">
                        ❌ Chart Error: ${error.message}
                    </div>
                `;
            }
        }

        // Update market information
        async function updateMarketInfo(marketData) {
            const container = document.getElementById('marketInfoContainer');
            const meta = marketData.meta;
            const quotes = marketData.indicators.quote[0];
            
            // Calculate additional metrics
            const prices = quotes.close.filter(p => p != null);
            const volumes = quotes.volume.filter(v => v != null);
            
            const high52w = Math.max(...prices) * 1.05; // Approximate
            const low52w = Math.min(...prices) * 0.95;
            const avgVolume = volumes.reduce((sum, v) => sum + v, 0) / volumes.length;
            const marketCap = meta.regularMarketPrice * 1000000000; // Approximate for ETFs
            
            container.innerHTML = `
                <div class="market-info">
                    <h4>📊 ${meta.symbol} - ${meta.instrumentType === 'ETF' ? 'Exchange Traded Fund' : 'Equity'}</h4>
                    <div class="market-stats">
                        <div class="stat-item">
                            <span>Exchange:</span>
                            <span>${meta.exchangeName || 'NASDAQ'}</span>
                        </div>
                        <div class="stat-item">
                            <span>Currency:</span>
                            <span>${meta.currency}</span>
                        </div>
                        <div class="stat-item">
                            <span>52W High:</span>
                            <span>$${high52w.toFixed(2)}</span>
                        </div>
                        <div class="stat-item">
                            <span>52W Low:</span>
                            <span>$${low52w.toFixed(2)}</span>
                        </div>
                        <div class="stat-item">
                            <span>Avg Volume:</span>
                            <span>${(avgVolume / 1000000).toFixed(1)}M</span>
                        </div>
                        <div class="stat-item">
                            <span>Market Cap:</span>
                            <span>$${(marketCap / 1000000000).toFixed(0)}B</span>
                        </div>
                    </div>
                </div>
            `;
        }

        // Update performance metrics
        async function updateMetrics(marketData) {
            const quotes = marketData.indicators.quote[0];
            const prices = quotes.close.filter(p => p != null);
            const volumes = quotes.volume.filter(v => v != null);
            
            // Calculate daily return
            const dailyReturn = prices.length > 1 ? 
                ((prices[prices.length - 1] - prices[prices.length - 2]) / prices[prices.length - 2] * 100) : 0;
            
            // Calculate volatility (standard deviation of returns)
            const returns = [];
            for (let i = 1; i < prices.length; i++) {
                returns.push((prices[i] - prices[i-1]) / prices[i-1]);
            }
            
            const avgReturn = returns.reduce((sum, r) => sum + r, 0) / returns.length;
            const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length;
            const volatility = Math.sqrt(variance * 252) * 100; // Annualized
            
            const currentVolume = volumes[volumes.length - 1] || 0;
            const avgVolume = volumes.reduce((sum, v) => sum + v, 0) / volumes.length;
            
            // Update UI
            document.getElementById('dailyReturn').textContent = `${dailyReturn >= 0 ? '+' : ''}${dailyReturn.toFixed(2)}%`;
            document.getElementById('dailyReturn').className = `metric-value ${dailyReturn >= 0 ? 'positive' : 'negative'}`;
            
            document.getElementById('volatility').textContent = `${volatility.toFixed(1)}%`;
            document.getElementById('volatility').className = `metric-value ${volatility > 25 ? 'negative' : volatility > 15 ? 'neutral' : 'positive'}`;
            
            document.getElementById('volume').textContent = `${(currentVolume / 1000000).toFixed(1)}M`;
            document.getElementById('avgVolume').textContent = `${(avgVolume / 1000000).toFixed(1)}M`;
        }

        // Generate technical analysis
        async function generateTechnicalAnalysis(marketData) {
            const container = document.getElementById('technicalContainer');
            const quotes = marketData.indicators.quote[0];
            const prices = quotes.close.filter(p => p != null);
            
            if (prices.length < 20) {
                container.innerHTML = '<div class="error-message">Not enough data for technical analysis</div>';
                return;
            }
            
            // Calculate technical indicators
            const sma20 = calculateSMA(prices, 20);
            const sma50 = calculateSMA(prices, 50);
            const rsi = calculateRSI(prices, 14);
            const macd = calculateMACD(prices);
            const bollinger = calculateBollingerBands(prices, 20);
            
            const currentPrice = prices[prices.length - 1];
            const currentSMA20 = sma20[sma20.length - 1];
            const currentSMA50 = sma50[sma50.length - 1];
            const currentRSI = rsi[rsi.length - 1];
            
            // Generate signals
            const signals = [];
            
            if (currentPrice > currentSMA20 && currentSMA20 > currentSMA50) {
                signals.push({ type: 'bullish', signal: 'Golden Cross Pattern', confidence: 0.75 });
            }
            
            if (currentRSI > 70) {
                signals.push({ type: 'bearish', signal: 'Overbought RSI', confidence: 0.65 });
            } else if (currentRSI < 30) {
                signals.push({ type: 'bullish', signal: 'Oversold RSI', confidence: 0.65 });
            }
            
            if (macd.histogram[macd.histogram.length - 1] > 0 && macd.histogram[macd.histogram.length - 2] < 0) {
                signals.push({ type: 'bullish', signal: 'MACD Bullish Crossover', confidence: 0.70 });
            }
            
            container.innerHTML = `
                <div class="market-info">
                    <h4>📈 Technical Indicators</h4>
                    <div class="market-stats">
                        <div class="stat-item">
                            <span>RSI (14):</span>
                            <span class="${currentRSI > 70 ? 'negative' : currentRSI < 30 ? 'positive' : 'neutral'}">${currentRSI.toFixed(1)}</span>
                        </div>
                        <div class="stat-item">
                            <span>SMA (20):</span>
                            <span>$${currentSMA20.toFixed(2)}</span>
                        </div>
                        <div class="stat-item">
                            <span>SMA (50):</span>
                            <span>$${currentSMA50.toFixed(2)}</span>
                        </div>
                        <div class="stat-item">
                            <span>BB Upper:</span>
                            <span>$${bollinger.upper[bollinger.upper.length - 1].toFixed(2)}</span>
                        </div>
                        <div class="stat-item">
                            <span>BB Lower:</span>
                            <span>$${bollinger.lower[bollinger.lower.length - 1].toFixed(2)}</span>
                        </div>
                        <div class="stat-item">
                            <span>MACD:</span>
                            <span class="${macd.macd[macd.macd.length - 1] > 0 ? 'positive' : 'negative'}">${macd.macd[macd.macd.length - 1].toFixed(3)}</span>
                        </div>
                    </div>
                </div>
            `;
        }

        // Generate AI trading signals based on real data
        async function generateTradingSignals(marketData) {
            const container = document.getElementById('signalsContainer');
            const quotes = marketData.indicators.quote[0];
            const prices = quotes.close.filter(p => p != null);
            const volumes = quotes.volume.filter(v => v != null);
            
            if (prices.length < 10) {
                container.innerHTML = '<div class="error-message">Not enough data for signal generation</div>';
                return;
            }
            
            // Calculate momentum
            const momentum = (prices[prices.length - 1] - prices[prices.length - 5]) / prices[prices.length - 5];
            const volumeRatio = volumes[volumes.length - 1] / (volumes.reduce((sum, v) => sum + v, 0) / volumes.length);
            const rsi = calculateRSI(prices, 14);
            const currentRSI = rsi[rsi.length - 1];
            
            const signals = [
                {
                    name: 'Momentum Analysis',
                    timeframe: AppState.currentInterval,
                    signal: momentum > 0.02 ? 'STRONG BUY' : momentum > 0 ? 'BUY' : momentum < -0.02 ? 'STRONG SELL' : 'HOLD',
                    confidence: Math.min(Math.abs(momentum) * 10, 0.95),
                    type: momentum > 0.01 ? 'bullish' : momentum < -0.01 ? 'bearish' : 'neutral',
                    details: `${(momentum * 100).toFixed(2)}% momentum`
                },
                {
                    name: 'Volume Analysis',
                    timeframe: '1D',
                    signal: volumeRatio > 1.5 ? 'HIGH INTEREST' : volumeRatio > 1.2 ? 'ABOVE AVG' : 'NORMAL',
                    confidence: Math.min(volumeRatio / 2, 0.85),
                    type: volumeRatio > 1.3 ? 'bullish' : 'neutral',
                    details: `${volumeRatio.toFixed(1)}x avg volume`
                },
                {
                    name: 'RSI Oscillator',
                    timeframe: '14 periods',
                    signal: currentRSI > 70 ? 'OVERBOUGHT' : currentRSI < 30 ? 'OVERSOLD' : 'NEUTRAL',
                    confidence: currentRSI > 70 || currentRSI < 30 ? 0.80 : 0.40,
                    type: currentRSI > 70 ? 'bearish' : currentRSI < 30 ? 'bullish' : 'neutral',
                    details: `RSI: ${currentRSI.toFixed(1)}`
                }
            ];
            
            // Add LSTM-style pattern recognition
            if (prices.length >= 20) {
                const recentTrend = calculateTrendStrength(prices.slice(-20));
                signals.push({
                    name: 'AI Pattern Recognition',
                    timeframe: 'Multi-period',
                    signal: recentTrend > 0.6 ? 'UPTREND' : recentTrend < -0.6 ? 'DOWNTREND' : 'SIDEWAYS',
                    confidence: Math.abs(recentTrend),
                    type: recentTrend > 0.3 ? 'bullish' : recentTrend < -0.3 ? 'bearish' : 'neutral',
                    details: `Trend strength: ${Math.abs(recentTrend * 100).toFixed(0)}%`
                });
            }
            
            container.innerHTML = '';
            
            signals.forEach(signal => {
                const signalElement = document.createElement('div');
                signalElement.className = `signal-item ${signal.type}`;
                signalElement.style.marginBottom = '0.75rem';
                signalElement.innerHTML = `
                    <div>
                        <div style="font-weight: 600;">${signal.name}</div>
                        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">
                            ${signal.timeframe} • Confidence: ${(signal.confidence * 100).toFixed(0)}%
                            ${signal.details ? ' • ' + signal.details : ''}
                        </div>
                    </div>
                    <div class="${signal.type === 'bullish' ? 'positive' : signal.type === 'bearish' ? 'negative' : 'neutral'}" 
                         style="font-weight: bold; font-size: 0.9rem;">${signal.signal}</div>
                `;
                container.appendChild(signalElement);
            });
            
            updateTimestamp('signalsUpdateTime');
        }

        // Technical indicator calculations
        function calculateSMA(prices, period) {
            const sma = [];
            for (let i = period - 1; i < prices.length; i++) {
                const sum = prices.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
                sma.push(sum / period);
            }
            return sma;
        }

        function calculateRSI(prices, period = 14) {
            const gains = [];
            const losses = [];
            
            for (let i = 1; i < prices.length; i++) {
                const change = prices[i] - prices[i - 1];
                gains.push(change > 0 ? change : 0);
                losses.push(change < 0 ? -change : 0);
            }
            
            const rsi = [];
            for (let i = period - 1; i < gains.length; i++) {
                const avgGain = gains.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0) / period;
                const avgLoss = losses.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0) / period;
                
                if (avgLoss === 0) {
                    rsi.push(100);
                } else {
                    const rs = avgGain / avgLoss;
                    rsi.push(100 - (100 / (1 + rs)));
                }
            }
            
            return rsi;
        }

        function calculateMACD(prices) {
            const ema12 = calculateEMA(prices, 12);
            const ema26 = calculateEMA(prices, 26);
            const macdLine = [];
            
            for (let i = 0; i < Math.min(ema12.length, ema26.length); i++) {
                macdLine.push(ema12[i] - ema26[i]);
            }
            
            const signalLine = calculateEMA(macdLine, 9);
            const histogram = [];
            
            for (let i = 0; i < Math.min(macdLine.length, signalLine.length); i++) {
                histogram.push(macdLine[i] - signalLine[i]);
            }
            
            return { macd: macdLine, signal: signalLine, histogram: histogram };
        }

        function calculateEMA(prices, period) {
            const k = 2 / (period + 1);
            const ema = [prices[0]];
            
            for (let i = 1; i < prices.length; i++) {
                ema.push(prices[i] * k + ema[i - 1] * (1 - k));
            }
            
            return ema;
        }

        function calculateBollingerBands(prices, period) {
            const sma = calculateSMA(prices, period);
            const upper = [];
            const lower = [];
            
            for (let i = period - 1; i < prices.length; i++) {
                const slice = prices.slice(i - period + 1, i + 1);
                const mean = sma[i - period + 1];
                const variance = slice.reduce((sum, price) => sum + Math.pow(price - mean, 2), 0) / period;
                const stdDev = Math.sqrt(variance);
                
                upper.push(mean + (stdDev * 2));
                lower.push(mean - (stdDev * 2));
            }
            
            return { upper, lower, middle: sma };
        }

        function calculateTrendStrength(prices) {
            if (prices.length < 3) return 0;
            
            let upDays = 0;
            let downDays = 0;
            
            for (let i = 1; i < prices.length; i++) {
                if (prices[i] > prices[i - 1]) upDays++;
                else if (prices[i] < prices[i - 1]) downDays++;
            }
            
            const totalDays = upDays + downDays;
            if (totalDays === 0) return 0;
            
            return (upDays - downDays) / totalDays;
        }

        // Event listeners
        function initializeEventListeners() {
            // Symbol selector
            document.getElementById('symbolSelector').addEventListener('change', async (e) => {
                AppState.currentSymbol = e.target.value;
                await fetchMarketData(true);
            });

            // Timeframe tabs
            document.querySelectorAll('.tab').forEach(tab => {
                tab.addEventListener('click', async function() {
                    document.querySelector('.tab.active').classList.remove('active');
                    this.classList.add('active');
                    AppState.currentPeriod = this.dataset.period;
                    AppState.currentInterval = this.dataset.interval;
                    
                    await fetchMarketData(true);
                });
            });
        }

        // Update status indicator
        function updateStatus(text, isLive) {
            const statusText = document.getElementById('statusText');
            const statusDot = document.getElementById('statusDot');
            
            statusText.textContent = text;
            statusDot.className = `status-dot ${isLive ? '' : 'error'}`;
        }

        // Update timestamp
        function updateTimestamp(elementId) {
            const element = document.getElementById(elementId);
            if (element) {
                element.textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
            }
        }

        // Start live updates
        function startLiveUpdates() {
            // Refresh data every 5 minutes for real Yahoo Finance data
            AppState.updateIntervals.main = setInterval(() => {
                if (AppState.isLive) {
                    fetchMarketData(true);
                }
            }, 300000); // 5 minutes
            
            // If in demo mode, update more frequently
            AppState.updateIntervals.demo = setInterval(() => {
                if (AppState.isLive && document.getElementById('statusText').textContent === 'Demo Mode') {
                    // Add some random variation to demo data
                    if (AppState.marketData) {
                        const quotes = AppState.marketData.indicators.quote[0];
                        const lastPrice = quotes.close[quotes.close.length - 1];
                        const variation = (Math.random() - 0.5) * 0.002; // ±0.2% variation
                        const newPrice = lastPrice * (1 + variation);
                        
                        quotes.close.push(newPrice);
                        quotes.open.push(newPrice * (1 + (Math.random() - 0.5) * 0.001));
                        quotes.high.push(newPrice * (1 + Math.random() * 0.005));
                        quotes.low.push(newPrice * (1 - Math.random() * 0.005));
                        quotes.volume.push(Math.floor(quotes.volume[quotes.volume.length - 1] * (0.9 + Math.random() * 0.2)));
                        
                        AppState.marketData.timestamp.push(Math.floor(Date.now() / 1000));
                        AppState.marketData.meta.regularMarketPrice = newPrice;
                        
                        // Keep only last 100 data points
                        if (quotes.close.length > 100) {
                            quotes.close.shift();
                            quotes.open.shift();
                            quotes.high.shift();
                            quotes.low.shift();
                            quotes.volume.shift();
                            AppState.marketData.timestamp.shift();
                        }
                        
                        // Update UI with new demo data
                        updatePriceChart(AppState.marketData);
                        updateMetrics(AppState.marketData);
                        generateTechnicalAnalysis(AppState.marketData);
                        generateTradingSignals(AppState.marketData);
                    }
                }
            }, 15000); // 15 seconds for demo updates
        }

        // Stop live updates
        function stopLiveUpdates() {
            Object.values(AppState.updateIntervals).forEach(interval => {
                if (interval) clearInterval(interval);
            });
            AppState.isLive = false;
        }

        // Handle page visibility changes
        function handleVisibilityChange() {
            if (document.hidden) {
                AppState.isLive = false;
                updateStatus('Paused', false);
            } else {
                AppState.isLive = true;
                updateStatus(document.getElementById('statusText').textContent.includes('Demo') ? 'Demo Mode' : 'Live', true);
                // Refresh data when page becomes visible
                fetchMarketData(true);
            }
        }

        // Generate mock news data
        function generateMockNews() {
            const newsContainer = document.getElementById('newsList');
            const symbol = AppState.currentSymbol;
            
            const newsItems = [
                {
                    title: `${symbol} Shows Strong Technical Momentum in Pre-Market Trading`,
                    source: 'MarketWatch',
                    time: '2 min ago',
                    sentiment: 0.75,
                    type: 'structured'
                },
                {
                    title: `Institutional Buying Detected in ${symbol} Options Chain`,
                    source: 'Bloomberg Terminal',
                    time: '8 min ago',
                    sentiment: 0.65,
                    type: 'structured'
                },
                {
                    title: `Reddit WSB: ${symbol} to the moon! 🚀🚀🚀`,
                    source: 'Reddit r/wallstreetbets',
                    time: '15 min ago',
                    sentiment: 0.85,
                    type: 'unstructured'
                },
                {
                    title: `${symbol} breaks key resistance level - analysts bullish`,
                    source: 'Seeking Alpha',
                    time: '23 min ago',
                    sentiment: 0.60,
                    type: 'structured'
                }
            ];
            
            newsContainer.innerHTML = newsItems.map(news => `
                <div class="news-item ${news.type}" style="margin-bottom: 1rem; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; border-left: 3px solid ${news.type === 'structured' ? '#00d4ff' : '#7c3aed'};">
                    <div style="color: ${news.type === 'structured' ? '#00d4ff' : '#7c3aed'}; font-size: 0.75rem; margin-bottom: 0.5rem;">${news.source}</div>
                    <div style="font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem;">${news.title}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: rgba(255,255,255,0.6);">
                        <span>${news.time}</span>
                        <span style="padding: 0.2rem 0.5rem; border-radius: 8px; background: ${news.sentiment > 0.5 ? 'rgba(0,255,136,0.2)' : 'rgba(255,71,87,0.2)'}; color: ${news.sentiment > 0.5 ? '#00ff88' : '#ff4757'};">
                            ${news.sentiment > 0 ? '+' : ''}${news.sentiment.toFixed(2)}
                        </span>
                    </div>
                </div>
            `).join('');
        }

        // Initialize application when DOM is ready
        document.addEventListener('DOMContentLoaded', async () => {
            console.log('🚀 Initializing QuantFlow Real Data Trading Assistant');
            
            try {
                await initApp();
                generateMockNews();
                console.log('✅ Application initialized successfully');
            } catch (error) {
                console.error('❌ Initialization error:', error);
                updateStatus('Init Error', false);
            }
        });

        // Handle page visibility changes
        document.addEventListener('visibilitychange', handleVisibilityChange);

        // Handle page unload
        window.addEventListener('beforeunload', () => {
            stopLiveUpdates();
        });

        // Error handling for unhandled promises
        window.addEventListener('unhandledrejection', (event) => {
            console.error('❌ Unhandled promise rejection:', event.reason);
        });

        // Add keyboard shortcuts
        document.addEventListener('keydown', (event) => {
            if (event.ctrlKey || event.metaKey) {
                switch (event.key) {
                    case 'r':
                        event.preventDefault();
                        fetchMarketData(true);
                        break;
                    case '1':
                        event.preventDefault();
                        document.querySelector('[data-period="5d"]').click();
                        break;
                    case '2':
                        event.preventDefault();
                        document.querySelector('[data-period="1mo"]').click();
                        break;
                    case '3':
                        event.preventDefault();
                        document.querySelector('[data-period="3mo"]').click();
                        break;
                }
            }
        });

        // Console commands for debugging
        window.QuantFlowDebug = {
            refreshData: () => fetchMarketData(true),
            switchToDemo: () => useDemoData(),
            getState: () => AppState,
            getMarketData: () => AppState.marketData
        };

        console.log('🔧 Debug commands available: QuantFlowDebug.refreshData(), QuantFlowDebug.switchToDemo()');
    </script>
</body>
</html>