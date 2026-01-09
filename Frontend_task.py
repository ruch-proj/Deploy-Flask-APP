from flask import Flask, render_template_string, jsonify
import json
import random
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any

app = Flask(__name__)

# ==================== HTML TEMPLATE ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Axiom Trade - Token Discovery Table</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* CSS Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background: #0a0b0d;
            color: #e2e8f0;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            border-bottom: 1px solid #1e293b;
            margin-bottom: 30px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo h1 {
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .beta-badge {
            background: #10b981;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }

        .nav-links {
            display: flex;
            gap: 24px;
        }

        .nav-link {
            color: #94a3b8;
            text-decoration: none;
            font-weight: 500;
            padding: 8px 12px;
            border-radius: 8px;
            transition: all 0.2s;
            position: relative;
        }

        .nav-link:hover {
            color: #e2e8f0;
            background: #1e293b;
        }

        .nav-link.active {
            color: #3b82f6 !important;
            background: rgba(59, 130, 246, 0.1) !important;
        }

        .nav-link.active::after {
            content: '';
            position: absolute;
            bottom: -21px;
            left: 0;
            width: 100%;
            height: 2px;
            background: #3b82f6;
            border-radius: 2px;
        }

        .header-actions {
            display: flex;
            gap: 12px;
        }

        .btn {
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary {
            background: #3b82f6;
            color: white;
        }

        .btn-secondary {
            background: #1e293b;
            color: #e2e8f0;
        }

        .btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        /* Filters */
        .filters {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 16px;
        }

        .filter-tabs {
            display: flex;
            gap: 8px;
            background: #1e293b;
            padding: 4px;
            border-radius: 12px;
        }

        .filter-tab {
            padding: 8px 16px;
            border-radius: 8px;
            border: none;
            background: transparent;
            color: #94a3b8;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
        }

        .filter-tab.active {
            background: #3b82f6;
            color: white;
        }

        .search-box {
            position: relative;
            flex: 1;
            max-width: 400px;
        }

        .search-input {
            width: 100%;
            padding: 12px 16px 12px 40px;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #e2e8f0;
            font-size: 14px;
        }

        .search-icon {
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: #94a3b8;
        }

        /* Search Results Info */
        .search-info {
            background: #1e293b;
            padding: 12px 20px;
            border-radius: 8px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 4px solid #3b82f6;
        }

        .search-info.hidden {
            display: none;
        }

        .search-result-text {
            font-size: 14px;
            color: #94a3b8;
        }

        .search-result-text strong {
            color: #3b82f6;
        }

        .clear-search {
            background: transparent;
            border: none;
            color: #94a3b8;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 4px 8px;
            border-radius: 4px;
            transition: all 0.2s;
        }

        .clear-search:hover {
            color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
        }

        /* Table */
        .table-container {
            background: #111827;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #1e293b;
            margin-bottom: 30px;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        thead {
            background: #1e293b;
        }

        th {
            padding: 16px 20px;
            text-align: left;
            font-weight: 600;
            color: #94a3b8;
            font-size: 14px;
            border-bottom: 1px solid #334155;
            user-select: none;
            cursor: pointer;
            white-space: nowrap;
        }

        th:hover {
            background: #334155;
        }

        th i {
            margin-left: 8px;
            opacity: 0.5;
        }

        td {
            padding: 18px 20px;
            border-bottom: 1px solid #1e293b;
            white-space: nowrap;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover {
            background: rgba(59, 130, 246, 0.05);
        }

        /* Token Info */
        .token-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .token-icon {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
        }

        .token-name {
            font-weight: 600;
            font-size: 16px;
        }

        .token-symbol {
            color: #94a3b8;
            font-size: 14px;
        }

        /* Badges */
        .badges {
            display: flex;
            gap: 6px;
        }

        .badge {
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }

        .badge-new {
            background: rgba(34, 197, 94, 0.15);
            color: #10b981;
        }

        .badge-final {
            background: rgba(249, 115, 22, 0.15);
            color: #f97316;
        }

        .badge-migrated {
            background: rgba(139, 92, 246, 0.15);
            color: #8b5cf6;
        }

        /* Price Change */
        .price-change {
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 600;
        }

        .price-change.positive {
            color: #10b981;
        }

        .price-change.negative {
            color: #ef4444;
        }

        /* Favorite Button */
        .favorite-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            cursor: pointer;
            font-size: 18px;
            transition: all 0.2s;
            padding: 4px;
        }

        .favorite-btn:hover {
            color: #fbbf24;
            transform: scale(1.1);
        }

        .favorite-btn.active {
            color: #fbbf24;
        }

        /* Price Updates */
        .price-update {
            animation: priceUpdate 0.5s ease;
        }

        @keyframes priceUpdate {
            0% { background: rgba(59, 130, 246, 0.3); }
            100% { background: transparent; }
        }

        /* Loading Skeleton */
        .skeleton {
            background: linear-gradient(90deg, #1e293b 25%, #334155 50%, #1e293b 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
            border-radius: 4px;
            height: 20px;
        }

        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }

        /* Modal */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
        }

        .modal-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        .modal {
            background: #111827;
            border-radius: 16px;
            padding: 30px;
            max-width: 800px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            border: 1px solid #334155;
            transform: translateY(20px);
            transition: transform 0.3s;
        }

        .modal-overlay.active .modal {
            transform: translateY(0);
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }

        .modal-title {
            font-size: 20px;
            font-weight: 700;
        }

        .modal-close {
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 24px;
            cursor: pointer;
            padding: 4px;
        }

        /* Chart Container */
        .chart-container {
            background: #111827;
            border-radius: 16px;
            padding: 24px;
            border: 1px solid #1e293b;
            margin-top: 20px;
            position: relative;
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .chart-title {
            font-size: 18px;
            font-weight: 600;
            color: #e2e8f0;
        }

        .chart-timeframe {
            display: flex;
            gap: 8px;
            background: #1e293b;
            padding: 4px;
            border-radius: 8px;
        }

        .timeframe-btn {
            padding: 6px 12px;
            border-radius: 6px;
            border: none;
            background: transparent;
            color: #94a3b8;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.2s;
        }

        .timeframe-btn.active {
            background: #3b82f6;
            color: white;
        }

        .chart-wrapper {
            position: relative;
            height: 300px;
            width: 100%;
        }

        /* No Results Message - ONLY shown when NO tokens found */
        .no-results {
            text-align: center;
            padding: 40px 20px;
            color: #94a3b8;
            display: none; /* Hidden by default */
        }

        .no-results i {
            font-size: 48px;
            margin-bottom: 16px;
            color: #475569;
        }

        .no-results h3 {
            font-size: 18px;
            margin-bottom: 8px;
            color: #e2e8f0;
        }

        /* Tooltip */
        .tooltip {
            position: relative;
            display: inline-block;
        }

        .tooltip .tooltip-text {
            visibility: hidden;
            background: #1e293b;
            color: #e2e8f0;
            text-align: center;
            padding: 8px 12px;
            border-radius: 6px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            white-space: nowrap;
            font-size: 12px;
            opacity: 0;
            transition: opacity 0.3s;
            border: 1px solid #334155;
        }

        .tooltip:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                gap: 20px;
            }

            .filters {
                flex-direction: column;
                align-items: stretch;
            }

            .search-box {
                max-width: 100%;
            }

            th, td {
                padding: 12px 8px;
                font-size: 13px;
            }

            .token-name {
                font-size: 14px;
            }

            .badge {
                padding: 2px 6px;
                font-size: 10px;
            }

            .chart-wrapper {
                height: 250px;
            }

            .chart-header {
                flex-direction: column;
                gap: 12px;
                align-items: flex-start;
            }

            .chart-timeframe {
                width: 100%;
                justify-content: space-between;
            }

            .nav-link.active::after {
                bottom: -19px;
            }
        }

        @media (max-width: 480px) {
            body {
                padding: 10px;
            }

            .table-container {
                border-radius: 12px;
            }

            th, td {
                padding: 8px 6px;
                font-size: 12px;
            }

            .chart-wrapper {
                height: 200px;
            }

            .nav-links {
                gap: 12px;
            }

            .nav-link {
                padding: 6px 8px;
                font-size: 14px;
            }
        }

        /* Animations */
        .fade-in {
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .pulse {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="logo">
                <h1><i class="fas fa-chart-line"></i> Axiom Trade</h1>
                <span class="beta-badge">Beta</span>
            </div>
            <div class="nav-links">
                <a href="#" class="nav-link active" onclick="setActiveNav('pulse')">Pulse</a>
                <a href="#" class="nav-link" onclick="setActiveNav('trade')">Trade</a>
                <a href="#" class="nav-link" onclick="setActiveNav('portfolio')">Portfolio</a>
                <a href="#" class="nav-link" onclick="setActiveNav('docs')">Docs</a>
            </div>
            <div class="header-actions">
                <button class="btn btn-secondary" onclick="connectWallet()">
                    <i class="fas fa-wallet"></i> Connect Wallet
                </button>
                <button class="btn btn-primary" onclick="showSettings()">
                    <i class="fas fa-cog"></i> Settings
                </button>
            </div>
        </header>

        <!-- Filters -->
        <div class="filters">
            <div class="filter-tabs">
                <button class="filter-tab active" onclick="filterTokens('all')">All Tokens</button>
                <button class="filter-tab" onclick="filterTokens('new')">New Pairs</button>
                <button class="filter-tab" onclick="filterTokens('final')">Final Stretch</button>
                <button class="filter-tab" onclick="filterTokens('migrated')">Migrated</button>
            </div>
            <div class="search-box">
                <i class="fas fa-search search-icon"></i>
                <input type="text" class="search-input" placeholder="Search tokens..." oninput="searchTokens(this.value)">
            </div>
        </div>

        <!-- Search Results Info -->
        <div class="search-info hidden" id="search-info">
            <div class="search-result-text">
                Showing <strong id="search-result-count">0</strong> results for "<strong id="search-query"></strong>"
            </div>
            <button class="clear-search" onclick="clearSearch()">
                <i class="fas fa-times"></i> Clear Search
            </button>
        </div>

        <!-- Table Container - ALWAYS VISIBLE -->
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th onclick="sortTable('name')">
                            Token <i class="fas fa-sort"></i>
                        </th>
                        <th onclick="sortTable('price')">
                            Price <i class="fas fa-sort"></i>
                        </th>
                        <th onclick="sortTable('change')">
                            24h Change <i class="fas fa-sort"></i>
                        </th>
                        <th onclick="sortTable('volume')">
                            24h Volume <i class="fas fa-sort"></i>
                        </th>
                        <th onclick="sortTable('marketCap')">
                            Market Cap <i class="fas fa-sort"></i>
                        </th>
                        <th>Categories</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="token-table-body">
                    <!-- Tokens will be loaded here -->
                </tbody>
            </table>
        </div>

        <!-- No Results Message - ONLY shown when NO tokens found -->
        <div class="no-results" id="no-results">
            <i class="fas fa-search"></i>
            <h3>No tokens found</h3>
            <p>Try adjusting your search or filter to find what you're looking for</p>
        </div>

        <!-- Loading State -->
        <div id="loading-skeleton" style="display: none;">
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Token</th>
                            <th>Price</th>
                            <th>24h Change</th>
                            <th>24h Volume</th>
                            <th>Market Cap</th>
                            <th>Categories</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for i in range(5) %}
                        <tr>
                            <td><div class="skeleton" style="width: 100px; height: 36px;"></div></td>
                            <td><div class="skeleton" style="width: 80px; height: 20px;"></div></td>
                            <td><div class="skeleton" style="width: 70px; height: 20px;"></div></td>
                            <td><div class="skeleton" style="width: 120px; height: 20px;"></div></td>
                            <td><div class="skeleton" style="width: 120px; height: 20px;"></div></td>
                            <td><div class="skeleton" style="width: 100px; height: 20px;"></div></td>
                            <td><div class="skeleton" style="width: 40px; height: 20px;"></div></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Price Chart Section -->
        <div class="chart-container">
            <div class="chart-header">
                <h3 class="chart-title" id="chart-title">
                    <span id="selected-token-name">ETH</span> Price Chart (<span id="selected-timeframe">24H</span>)
                </h3>
                <div class="chart-timeframe">
                    <button class="timeframe-btn active" onclick="changeTimeframe('1h')">1H</button>
                    <button class="timeframe-btn" onclick="changeTimeframe('24h')">24H</button>
                    <button class="timeframe-btn" onclick="changeTimeframe('7d')">7D</button>
                    <button class="timeframe-btn" onclick="changeTimeframe('30d')">30D</button>
                    <button class="timeframe-btn" onclick="changeTimeframe('90d')">90D</button>
                </div>
            </div>
            <div class="chart-wrapper">
                <canvas id="priceChart"></canvas>
            </div>
            <div style="margin-top: 20px; display: flex; justify-content: space-between; color: #94a3b8; font-size: 12px;">
                <div id="chart-info">Showing chart for <strong>ETH</strong> - Click any token to view its chart</div>
                <div id="chart-update-time">Updated: Just now</div>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal-overlay" id="token-modal">
            <div class="modal">
                <div class="modal-header">
                    <h2 class="modal-title" id="modal-token-name"></h2>
                    <button class="modal-close" onclick="closeModal()">×</button>
                </div>
                <div id="modal-content">
                    <!-- Token details will be loaded here -->
                </div>
            </div>
        </div>
    </div>

    <script>
        // JavaScript functionality
        let allTokens = [];
        let filteredTokens = [];
        let currentSort = { column: 'name', direction: 'asc' };
        let currentFilter = 'all';
        let priceChart = null;
        let currentSelectedToken = 'ETH';
        let currentSelectedTokenName = 'Ethereum';
        let currentTimeframe = '24h';
        let currentSearchQuery = '';
        let currentActiveNav = 'pulse';

        // Load tokens on page load
        document.addEventListener('DOMContentLoaded', function() {
            showLoading();
            loadTokens();
            initializeChart();
            setupWebSocket();

            // Hide loading after 1.5 seconds
            setTimeout(() => {
                hideLoading();
            }, 1500);

            // Pre-populate search with "solana" for demo
            setTimeout(() => {
                document.querySelector('.search-input').value = 'solana';
                searchTokens('solana');
            }, 2000);
        });

        // Set active navigation
        function setActiveNav(navItem) {
            event.preventDefault();
            currentActiveNav = navItem;

            // Update active nav styles
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            event.target.classList.add('active');

            // Simulate navigation action
            switch(navItem) {
                case 'pulse':
                    console.log('Navigating to Pulse');
                    break;
                case 'trade':
                    console.log('Navigating to Trade');
                    break;
                case 'portfolio':
                    console.log('Navigating to Portfolio');
                    break;
                case 'docs':
                    console.log('Navigating to Docs');
                    break;
            }
        }

        // Show loading skeleton
        function showLoading() {
            document.getElementById('loading-skeleton').style.display = 'block';
            document.getElementById('token-table-body').innerHTML = '';
        }

        // Hide loading skeleton
        function hideLoading() {
            document.getElementById('loading-skeleton').style.display = 'none';
        }

        // Load tokens from API
        async function loadTokens() {
            try {
                const response = await fetch('/api/tokens');
                allTokens = await response.json();
                filteredTokens = [...allTokens];
                renderTable();
            } catch (error) {
                console.error('Error loading tokens:', error);
                showError('Failed to load tokens. Please refresh the page.');
            }
        }

        // Render table with current tokens
        function renderTable() {
            const tbody = document.getElementById('token-table-body');
            tbody.innerHTML = '';

            // Show/hide no results message - ONLY when NO tokens
            const noResultsDiv = document.getElementById('no-results');
            const searchInfoDiv = document.getElementById('search-info');
            const tableContainer = document.querySelector('.table-container');

            if (filteredTokens.length === 0) {
                // NO TOKENS FOUND - Show message and hide table
                noResultsDiv.style.display = 'block';
                tableContainer.style.display = 'none';
                searchInfoDiv.classList.add('hidden');
            } else {
                // TOKENS FOUND - Show table and hide message
                noResultsDiv.style.display = 'none';
                tableContainer.style.display = 'block';

                // Show search info if searching
                if (currentSearchQuery) {
                    searchInfoDiv.classList.remove('hidden');
                    document.getElementById('search-result-count').textContent = filteredTokens.length;
                    document.getElementById('search-query').textContent = currentSearchQuery;

                    // Auto-select first token in search results for chart
                    if (filteredTokens.length > 0) {
                        const firstToken = filteredTokens[0];
                        if (firstToken.symbol !== currentSelectedToken) {
                            selectTokenForChart(firstToken.symbol, firstToken.name);
                        }
                    }
                } else {
                    searchInfoDiv.classList.add('hidden');
                }

                // Render all found tokens
                filteredTokens.forEach(token => {
                    const row = document.createElement('tr');
                    row.className = 'fade-in';
                    row.onclick = () => selectTokenForChart(token.symbol, token.name);

                    // Format numbers
                    const price = new Intl.NumberFormat('en-US', {
                        style: 'currency',
                        currency: 'USD',
                        minimumFractionDigits: 2
                    }).format(token.price);

                    const change = token.change_24h.toFixed(2) + '%';
                    const volume = '$' + formatNumber(token.volume_24h);
                    const marketCap = '$' + formatNumber(token.market_cap);

                    // Categories badges
                    const categories = token.categories.map(cat => {
                        let badgeClass = '';
                        if (cat === 'New pairs') badgeClass = 'badge-new';
                        if (cat === 'Final Stretch') badgeClass = 'badge-final';
                        if (cat === 'Migrated') badgeClass = 'badge-migrated';

                        return `<span class="badge ${badgeClass}">${cat}</span>`;
                    }).join('');

                    // Favorite button
                    const favoriteIcon = token.is_favorite ? 'fas' : 'far';

                    row.innerHTML = `
                        <td>
                            <div class="token-info">
                                <div class="token-icon">${token.symbol.charAt(0)}</div>
                                <div>
                                    <div class="token-name">${token.name}</div>
                                    <div class="token-symbol">${token.symbol}</div>
                                </div>
                            </div>
                        </td>
                        <td class="price-cell" id="price-${token.id}">
                            <span class="price-value">${price}</span>
                        </td>
                        <td>
                            <div class="price-change ${token.change_24h >= 0 ? 'positive' : 'negative'}">
                                <i class="fas ${token.change_24h >= 0 ? 'fa-arrow-up' : 'fa-arrow-down'}"></i>
                                ${change}
                            </div>
                        </td>
                        <td>${volume}</td>
                        <td>${marketCap}</td>
                        <td>
                            <div class="badges">
                                ${categories}
                            </div>
                        </td>
                        <td>
                            <button class="favorite-btn ${token.is_favorite ? 'active' : ''}" onclick="event.stopPropagation(); toggleFavorite(${token.id})">
                                <i class="${favoriteIcon} fa-star"></i>
                            </button>
                            <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 12px;" onclick="event.stopPropagation(); showTokenDetails(${token.id})">
                                Details
                            </button>
                        </td>
                    `;

                    tbody.appendChild(row);
                });
            }

            // Highlight selected token row
            highlightSelectedToken();
        }

        // Format large numbers
        function formatNumber(num) {
            if (num >= 1e9) {
                return (num / 1e9).toFixed(2) + 'B';
            }
            if (num >= 1e6) {
                return (num / 1e6).toFixed(2) + 'M';
            }
            if (num >= 1e3) {
                return (num / 1e3).toFixed(2) + 'K';
            }
            return num.toFixed(2);
        }

        // Sort table
        function sortTable(column) {
            // Update sort direction
            if (currentSort.column === column) {
                currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
            } else {
                currentSort.column = column;
                currentSort.direction = 'asc';
            }

            // Sort tokens
            filteredTokens.sort((a, b) => {
                let aValue, bValue;

                switch(column) {
                    case 'name':
                        aValue = a.name.toLowerCase();
                        bValue = b.name.toLowerCase();
                        break;
                    case 'price':
                        aValue = a.price;
                        bValue = b.price;
                        break;
                    case 'change':
                        aValue = a.change_24h;
                        bValue = b.change_24h;
                        break;
                    case 'volume':
                        aValue = a.volume_24h;
                        bValue = b.volume_24h;
                        break;
                    case 'marketCap':
                        aValue = a.market_cap;
                        bValue = b.market_cap;
                        break;
                    default:
                        return 0;
                }

                if (currentSort.direction === 'asc') {
                    return aValue > bValue ? 1 : -1;
                } else {
                    return aValue < bValue ? 1 : -1;
                }
            });

            renderTable();
            updateSortIndicators(column);
        }

        // Update sort indicators in table headers
        function updateSortIndicators(column) {
            const headers = document.querySelectorAll('th');
            headers.forEach(header => {
                const icon = header.querySelector('i');
                if (icon) {
                    if (header.textContent.includes(column)) {
                        icon.className = currentSort.direction === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down';
                    } else {
                        icon.className = 'fas fa-sort';
                    }
                }
            });
        }

        // Filter tokens by category
        function filterTokens(category) {
            currentFilter = category;

            // Update active tab
            document.querySelectorAll('.filter-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');

            // Start with all tokens
            let tempFiltered = [...allTokens];

            // Apply category filter
            if (category !== 'all') {
                tempFiltered = tempFiltered.filter(token => {
                    if (category === 'new') return token.categories.includes('New pairs');
                    if (category === 'final') return token.categories.includes('Final Stretch');
                    if (category === 'migrated') return token.categories.includes('Migrated');
                    return true;
                });
            }

            // Apply search filter if exists
            if (currentSearchQuery) {
                tempFiltered = tempFiltered.filter(token => 
                    token.name.toLowerCase().includes(currentSearchQuery) || 
                    token.symbol.toLowerCase().includes(currentSearchQuery)
                );
            }

            filteredTokens = tempFiltered;
            renderTable();
        }

        // Search tokens
        function searchTokens(query) {
            currentSearchQuery = query.trim().toLowerCase();

            // Start with all tokens
            let tempFiltered = [...allTokens];

            // Apply search filter if exists
            if (currentSearchQuery) {
                tempFiltered = tempFiltered.filter(token => 
                    token.name.toLowerCase().includes(currentSearchQuery) || 
                    token.symbol.toLowerCase().includes(currentSearchQuery)
                );
            }

            // Apply category filter
            if (currentFilter !== 'all') {
                tempFiltered = tempFiltered.filter(token => {
                    if (currentFilter === 'new') return token.categories.includes('New pairs');
                    if (currentFilter === 'final') return token.categories.includes('Final Stretch');
                    if (currentFilter === 'migrated') return token.categories.includes('Migrated');
                    return true;
                });
            }

            filteredTokens = tempFiltered;
            renderTable();
        }

        // Clear search
        function clearSearch() {
            document.querySelector('.search-input').value = '';
            currentSearchQuery = '';

            // Start with all tokens
            let tempFiltered = [...allTokens];

            // Apply category filter
            if (currentFilter !== 'all') {
                tempFiltered = tempFiltered.filter(token => {
                    if (currentFilter === 'new') return token.categories.includes('New pairs');
                    if (currentFilter === 'final') return token.categories.includes('Final Stretch');
                    if (currentFilter === 'migrated') return token.categories.includes('Migrated');
                    return true;
                });
            }

            filteredTokens = tempFiltered;
            renderTable();
        }

        // Toggle favorite
        async function toggleFavorite(tokenId) {
            try {
                const response = await fetch(`/api/toggle-favorite/${tokenId}`, {
                    method: 'POST'
                });
                const result = await response.json();

                if (result.success) {
                    // Update local data
                    const token = allTokens.find(t => t.id === tokenId);
                    if (token) {
                        token.is_favorite = result.is_favorite;
                    }

                    // Re-render table
                    renderTable();
                }
            } catch (error) {
                console.error('Error toggling favorite:', error);
            }
        }

        // Select token for chart
        function selectTokenForChart(tokenSymbol, tokenName) {
            currentSelectedToken = tokenSymbol;
            currentSelectedTokenName = tokenName;
            highlightSelectedToken();
            updateChartData();
            updateChartInfo();
        }

        // Highlight selected token row
        function highlightSelectedToken() {
            // Only highlight if table is visible
            const tableContainer = document.querySelector('.table-container');
            if (tableContainer.style.display === 'none') return;

            // Remove previous highlights
            document.querySelectorAll('tr').forEach(row => {
                row.style.background = '';
                row.style.borderLeft = '';
            });

            // Add highlight to selected token
            const rows = document.querySelectorAll('tr');
            rows.forEach(row => {
                const symbolCell = row.querySelector('.token-symbol');
                if (symbolCell && symbolCell.textContent === currentSelectedToken) {
                    row.style.background = 'rgba(59, 130, 246, 0.1)';
                    row.style.borderLeft = '3px solid #3b82f6';
                }
            });
        }

        // Show token details modal
        async function showTokenDetails(tokenId) {
            try {
                const response = await fetch(`/api/token/${tokenId}`);
                const token = await response.json();

                document.getElementById('modal-token-name').textContent = `${token.name} Details`;

                const modalContent = document.getElementById('modal-content');
                modalContent.innerHTML = `
                    <div style="margin-bottom: 20px;">
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                            <div class="token-icon" style="width: 48px; height: 48px; font-size: 18px;">${token.symbol.charAt(0)}</div>
                            <div>
                                <h3 style="font-size: 18px; font-weight: 600;">${token.name} (${token.symbol})</h3>
                                <p style="color: #94a3b8; font-size: 14px;">${token.description}</p>
                            </div>
                        </div>

                        <div style="background: #1e293b; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                            <h4 style="margin-bottom: 12px; color: #3b82f6;">Token Information</h4>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                                <div>
                                    <div style="color: #94a3b8; font-size: 12px;">Current Price</div>
                                    <div style="font-weight: 600; font-size: 18px;">$${token.price.toFixed(2)}</div>
                                </div>
                                <div>
                                    <div style="color: #94a3b8; font-size: 12px;">24h Change</div>
                                    <div class="price-change ${token.change_24h >= 0 ? 'positive' : 'negative'}" style="font-size: 18px;">
                                        ${token.change_24h >= 0 ? '+' : ''}${token.change_24h.toFixed(2)}%
                                    </div>
                                </div>
                                <div>
                                    <div style="color: #94a3b8; font-size: 12px;">Market Cap</div>
                                    <div style="font-weight: 600;">$${formatNumber(token.market_cap)}</div>
                                </div>
                                <div>
                                    <div style="color: #94a3b8; font-size: 12px;">24h Volume</div>
                                    <div style="font-weight: 600;">$${formatNumber(token.volume_24h)}</div>
                                </div>
                            </div>
                        </div>

                        <div style="background: #1e293b; padding: 16px; border-radius: 8px;">
                            <h4 style="margin-bottom: 12px; color: #3b82f6;">Additional Details</h4>
                            <div style="display: grid; gap: 8px;">
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: #94a3b8;">Contract Address</span>
                                    <span style="font-family: monospace; font-size: 12px;">${token.contract_address}</span>
                                </div>
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: #94a3b8;">Launch Date</span>
                                    <span>${token.launch_date}</span>
                                </div>
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: #94a3b8;">Holders</span>
                                    <span>${token.holders.toLocaleString()}</span>
                                </div>
                                <div style="display: flex; justify-content: space-between;">
                                    <span style="color: #94a3b8;">Website</span>
                                    <a href="${token.website}" target="_blank" style="color: #3b82f6;">${token.website}</a>
                                </div>
                            </div>
                        </div>
                    </div>
                `;

                // Show modal
                document.getElementById('token-modal').classList.add('active');
            } catch (error) {
                console.error('Error loading token details:', error);
            }
        }

        // Close modal
        function closeModal() {
            document.getElementById('token-modal').classList.remove('active');
        }

        // Connect wallet
        function connectWallet() {
            alert('Wallet connection would be implemented here in a real application.');
        }

        // Show settings
        function showSettings() {
            alert('Settings modal would open here.');
        }

        // Initialize price chart
        function initializeChart() {
            const ctx = document.getElementById('priceChart').getContext('2d');

            // Generate initial data
            const { labels, data } = generateChartData('24h');

            priceChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Price',
                        data: data,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                        pointBackgroundColor: '#3b82f6',
                        pointHoverBackgroundColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            backgroundColor: '#1e293b',
                            titleColor: '#e2e8f0',
                            bodyColor: '#e2e8f0',
                            borderColor: '#334155',
                            borderWidth: 1,
                            callbacks: {
                                label: function(context) {
                                    return `$${context.parsed.y.toFixed(2)}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.05)',
                                borderColor: 'rgba(255, 255, 255, 0.05)'
                            },
                            ticks: {
                                color: '#94a3b8',
                                maxTicksLimit: 8
                            }
                        },
                        y: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.05)',
                                borderColor: 'rgba(255, 255, 255, 0.05)'
                            },
                            ticks: {
                                color: '#94a3b8',
                                callback: function(value) {
                                    return '$' + value.toFixed(2);
                                }
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });

            updateChartInfo();
        }

        // Generate chart data based on timeframe
        function generateChartData(timeframe) {
            const now = new Date();
            let labels = [];
            let data = [];

            // Get token for chart
            const token = allTokens.find(t => t.symbol === currentSelectedToken) || allTokens[0];
            const basePrice = token ? token.price : 3000;

            // Generate data based on timeframe
            if (timeframe === '1h') {
                // 60 minutes
                for (let i = 60; i >= 0; i--) {
                    const time = new Date(now.getTime() - i * 60000);
                    labels.push(time.getMinutes() + 'm');

                    // Simulate price movement
                    const price = basePrice * (1 + (Math.random() - 0.5) * 0.02);
                    data.push(price);
                }
            } else if (timeframe === '24h') {
                // 24 hours
                for (let i = 24; i >= 0; i--) {
                    const time = new Date(now.getTime() - i * 3600000);
                    labels.push(time.getHours() + 'h');

                    // Simulate price movement with more volatility
                    const price = basePrice * (1 + (Math.random() - 0.5) * 0.05);
                    data.push(price);
                }
            } else if (timeframe === '7d') {
                // 7 days
                for (let i = 7; i >= 0; i--) {
                    const time = new Date(now.getTime() - i * 86400000);
                    labels.push(time.getDate() + 'd');

                    // Simulate price movement
                    const price = basePrice * (1 + (Math.random() - 0.5) * 0.1);
                    data.push(price);
                }
            } else if (timeframe === '30d') {
                // 30 days (weekly points)
                for (let i = 4; i >= 0; i--) {
                    const time = new Date(now.getTime() - i * 7 * 86400000);
                    labels.push('Week ' + (i + 1));

                    // Simulate price movement
                    const price = basePrice * (1 + (Math.random() - 0.5) * 0.15);
                    data.push(price);
                }
            } else if (timeframe === '90d') {
                // 90 days (monthly points)
                for (let i = 3; i >= 0; i--) {
                    labels.push('Month ' + (i + 1));

                    // Simulate price movement
                    const price = basePrice * (1 + (Math.random() - 0.5) * 0.2);
                    data.push(price);
                }
            }

            return { labels, data };
        }

        // Change chart timeframe
        function changeTimeframe(timeframe) {
            currentTimeframe = timeframe;

            // Update active button
            document.querySelectorAll('.timeframe-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');

            // Update title
            document.getElementById('selected-timeframe').textContent = timeframe.toUpperCase();

            updateChartData();
            updateChartInfo();
        }

        // Update chart data
        function updateChartData() {
            const { labels, data } = generateChartData(currentTimeframe);

            if (priceChart) {
                priceChart.data.labels = labels;
                priceChart.data.datasets[0].data = data;

                // Update color based on price movement
                const firstPrice = data[0];
                const lastPrice = data[data.length - 1];
                const isPositive = lastPrice >= firstPrice;

                priceChart.data.datasets[0].borderColor = isPositive ? '#10b981' : '#ef4444';
                priceChart.data.datasets[0].backgroundColor = isPositive ? 
                    'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)';
                priceChart.data.datasets[0].pointBackgroundColor = isPositive ? '#10b981' : '#ef4444';

                priceChart.update();

                // Update timestamp
                const now = new Date();
                document.getElementById('chart-update-time').textContent = 
                    `Updated: ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
            }
        }

        // Update chart info text
        function updateChartInfo() {
            document.getElementById('selected-token-name').textContent = currentSelectedToken;
            document.getElementById('chart-info').innerHTML = 
                `Showing chart for <strong>${currentSelectedToken}</strong> (${currentSelectedTokenName})`;

            // If searching, show search context
            if (currentSearchQuery) {
                const resultCount = filteredTokens.length;
                document.getElementById('chart-info').innerHTML += 
                    ` • ${resultCount} result${resultCount !== 1 ? 's' : ''} for "${currentSearchQuery}"`;
            }
        }

        // Setup WebSocket for real-time updates
        function setupWebSocket() {
            // Update chart every 10 seconds
            setInterval(() => {
                updateChartData();
            }, 10000);

            // Update random prices every 3 seconds
            setInterval(() => {
                updateRandomPrices();
            }, 3000);
        }

        // Update random prices
        function updateRandomPrices() {
            // Select 2-3 random tokens to update
            const tokensToUpdate = [...allTokens]
                .sort(() => Math.random() - 0.5)
                .slice(0, 3);

            tokensToUpdate.forEach(token => {
                // Random small price change (-1% to +1%)
                const change = (Math.random() - 0.5) * 2;
                const newPrice = token.price * (1 + change / 100);

                // Update local data
                token.price = parseFloat(newPrice.toFixed(2));
                token.change_24h += change;

                // Update table if token is visible
                const priceCell = document.getElementById(`price-${token.id}`);
                if (priceCell) {
                    const priceValue = priceCell.querySelector('.price-value');
                    priceValue.textContent = new Intl.NumberFormat('en-US', {
                        style: 'currency',
                        currency: 'USD',
                        minimumFractionDigits: 2
                    }).format(newPrice);

                    // Add animation
                    priceCell.classList.add('price-update');
                    setTimeout(() => {
                        priceCell.classList.remove('price-update');
                    }, 500);
                }
            });

            // Update 24h change display for affected tokens
            renderTable();

            // If selected token is updated, update chart
            if (tokensToUpdate.some(t => t.symbol === currentSelectedToken)) {
                updateChartData();
            }
        }

        // Show error message
        function showError(message) {
            const errorDiv = document.createElement('div');
            errorDiv.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #ef4444;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                z-index: 1000;
                animation: fadeIn 0.3s;
            `;
            errorDiv.textContent = message;
            document.body.appendChild(errorDiv);

            setTimeout(() => {
                errorDiv.remove();
            }, 5000);
        }

        // Close modal on ESC key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });
    </script>
</body>
</html>
'''


# ==================== MOCK DATA GENERATION ====================
def generate_mock_tokens():
    """Generate mock token data"""
    tokens = []
    token_names = [
        ("Ethereum", "ETH"), ("Bitcoin", "BTC"), ("Solana", "SOL"),
        ("Avalanche", "AVAX"), ("BNB", "BNB"), ("Polygon", "MATIC"),
        ("Arbitrum", "ARB"), ("Optimism", "OP"), ("Sui", "SUI"),
        ("Aptos", "APT"), ("Sei", "SEI"), ("Pyth", "PYTH"),
        ("Jupiter", "JUP"), ("dogwifhat", "WIF"), ("Bonk", "BONK")
    ]

    for i, (name, symbol) in enumerate(token_names):
        price = round(random.uniform(0.5, 5000), 2)
        change_24h = round(random.uniform(-15, 30), 2)
        volume_24h = round(random.uniform(1000000, 500000000), 2)
        market_cap = round(random.uniform(50000000, 50000000000), 2)

        # Randomly assign categories
        categories = []
        if random.random() > 0.6:
            categories.append("New pairs")
        if random.random() > 0.7:
            categories.append("Final Stretch")
        if random.random() > 0.5:
            categories.append("Migrated")

        tokens.append({
            "id": i,
            "name": name,
            "symbol": symbol,
            "price": price,
            "change_24h": change_24h,
            "volume_24h": volume_24h,
            "market_cap": market_cap,
            "categories": categories,
            "is_favorite": random.random() > 0.7
        })

    return tokens


# ==================== FLASK ROUTES ====================
tokens_data = generate_mock_tokens()


@app.route('/')
def index():
    """Render the main page"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/tokens')
def get_tokens():
    """Get all tokens"""
    return jsonify(tokens_data)


@app.route('/api/token/<int:token_id>')
def get_token_details(token_id):
    """Get detailed token information"""
    token = next((t for t in tokens_data if t["id"] == token_id), None)
    if token:
        # Add more detailed information
        details = {
            **token,
            "description": f"{token['name']} is a cryptocurrency with a current market cap of ${token['market_cap']:,.0f}. It's one of the leading tokens in the blockchain ecosystem.",
            "contract_address": "0x" + ''.join(random.choices('0123456789abcdef', k=40)),
            "launch_date": (datetime.now() - timedelta(days=random.randint(30, 1000))).strftime("%Y-%m-%d"),
            "website": f"https://{token['name'].lower()}.io",
            "twitter": f"https://twitter.com/{token['name']}",
            "holders": random.randint(1000, 1000000)
        }
        return jsonify(details)
    return jsonify({"error": "Token not found"}), 404


@app.route('/api/toggle-favorite/<int:token_id>', methods=['POST'])
def toggle_favorite(token_id):
    """Toggle favorite status of a token"""
    for token in tokens_data:
        if token["id"] == token_id:
            token["is_favorite"] = not token["is_favorite"]
            return jsonify({"success": True, "is_favorite": token["is_favorite"]})
    return jsonify({"error": "Token not found"}), 404


@app.route('/api/ws-mock')
def ws_mock():
    """Mock WebSocket endpoint for real-time updates"""
    updated_tokens = []
    for token in tokens_data[:3]:  # Update only first 3 tokens
        change = round(random.uniform(-1, 1), 2)
        new_price = token["price"] * (1 + change / 100)
        new_price = round(new_price, 2)

        updated_tokens.append({
            "id": token["id"],
            "price": new_price,
            "change": change
        })

    return jsonify(updated_tokens)


# ==================== START APPLICATION ====================
if __name__ == '__main__':
    print("=" * 70)
    print("Axiom Trade Token Discovery Table - FIXED SEARCH BEHAVIOR")
