# 📊 Backtest de Stratégies Quantitatives

> Projet d'analyse quantitative comparant différentes stratégies d'investissement sur un univers d'actions américaines (2015-2026)

## 🎯 Objectif du Projet

Ce projet compare trois stratégies d'investissement à partir de données réelles du marché :
- **Buy & Hold** sur le S&P 500 (baseline)
- **Equal-Weighted** : allocation équipondérée mensuelle
- **Momentum 12-1** : sélection des 5 meilleures actions selon leur momentum

L'analyse complète génère automatiquement un rapport HTML interactif avec visualisations et statistiques de performance.

## 📁 Structure du Projet

```
backtest-strategies/
│
├── backtest_step_by_step.ipynb          # Notebook Jupyter détaillé (exploration)
├── backtest_with_html_output_fr.py      # Script Python (rapport français)
├── backtest_with_html_output_eng.py     # Script Python (rapport anglais)
├── backtest_report.html                 # Rapport généré (FR)
├── backtest_report_en.html              # Rapport généré (EN)
└── README.md                            # Ce fichier
```

## 🚀 Installation & Utilisation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/backtest-strategies.git
cd backtest-strategies
```

### 2. Installer les dépendances

```bash
pip install yfinance pandas numpy matplotlib
```

### 3. Exécuter le backtest

**Option A : Jupyter Notebook (exploration détaillée)**
```bash
jupyter notebook backtest_step_by_step.ipynb
```
→ Idéal pour comprendre chaque étape du processus

**Option B : Script Python (rapport automatique)**
```bash
# Version française
python backtest_with_html_output_fr.py

# Version anglaise
python backtest_with_html_output_eng.py
```
→ Génère directement le rapport HTML

### 4. Consulter les résultats

Ouvrez `backtest_report.html` dans votre navigateur pour voir :
- Courbes de performance cumulées
- Analyse des drawdowns
- Distribution des rendements
- Tableau comparatif des métriques (CAGR, Sharpe, volatilité, max DD)

## 📊 Méthodologie

### Univers d'Investissement
19 actions américaines large-cap :
```
AAPL, MSFT, AMZN, GOOGL, META, NVDA, BRK-B, JPM, JNJ, V, 
PG, UNH, MA, HD, XOM, BAC, KO, DIS, PEP
```

### Stratégies Testées

**1. Buy & Hold Benchmark (S&P 500)**
- Stratégie passive de référence
- Benchmark : `^GSPC`

**2. Equal-Weighted Portfolio**
- Rééquilibrage mensuel
- Poids identique pour chaque action (1/N)
- Évite la concentration sur les mega-caps

**3. Momentum 12-1 (Top 5)**
- Signal : rendement sur 12 mois, skip 1 mois
- Sélection : 5 meilleures actions chaque mois
- Stratégie quantitative trend-following

### Métriques Calculées

| Métrique | Description |
|----------|-------------|
| **CAGR** | Taux de croissance annuel composé |
| **Volatilité** | Écart-type annualisé des rendements |
| **Sharpe Ratio** | Rendement ajusté au risque (RF = 4.25%) |
| **Max Drawdown** | Perte maximale depuis le plus haut |

## 🛠️ Stack Technique

- **Data** : `yfinance` (Yahoo Finance API)
- **Calculs** : `pandas`, `numpy`
- **Visualisation** : `matplotlib`
- **Output** : HTML/CSS (design custom minimaliste)

## 📈 Résultats Attendus

Le rapport HTML présente :
- ✅ Comparaison visuelle des performances
- ✅ Analyse risk/return de chaque stratégie
- ✅ Identification des périodes de surperformance
- ✅ Évaluation du risque (drawdown, volatilité)

## 💡 Améliorations Possibles

- [ ] Ajouter d'autres facteurs (value, quality, low-vol)
- [ ] Implémenter le rebalancing avec coûts de transaction
- [ ] Backtester sur différentes périodes (rolling windows)
- [ ] Ajouter des tests statistiques (t-test, bootstrap)
- [ ] Intégrer une analyse de corrélation

## 📝 Notes Importantes

- **Données** : Prix ajustés des dividendes et splits
- **Fréquence** : Rebalancing mensuel (fin de mois)
- **Survivorship Bias** : L'univers actuel peut créer un biais (actions survivantes)
- **Disclaimer** : Projet académique - performances passées ne préjugent pas des résultats futurs

## 🎓 Contexte Académique

Projet réalisé dans le cadre de mes études en finance quantitative. 

**Compétences démontrées :**
- Conception et implémentation de backtests rigoureux
- Manipulation de données financières (time series)
- Calcul de métriques de performance risk-adjusted
- Automatisation de rapports d'analyse
- Documentation et présentation de résultats

## 📧 Contact

Pour toute question ou suggestion :
- **Email** : votre.email@example.com
- **LinkedIn** : [Votre Profil](https://linkedin.com/in/votre-profil)
- **GitHub** : [@votre-username](https://github.com/votre-username)

---

⭐ Si ce projet vous a été utile, n'hésitez pas à mettre une étoile !
