# 🏗️ Exercices Atelier MLOps

## Objectif

Ajouter progressivement des métriques de monitoring à l'application de classification d'images.

---

## 📊 Exercice 1 : Métrique Latence d'Inférence (Jour 1-2)

### Objectif
Monitorer le temps de réponse des prédictions.

### Fichiers à Modifier

#### 1. `src/monitoring/prometheus_metrics.py`

**Ajouter** :
```python
# DONE: Créer métrique histogram pour latence
inference_time_histogram = Histogram(
    'cv_inference_time_seconds',
    'Temps d\'inférence en secondes'
)

def track_inference_time(inference_time_ms: float):
    """Enregistre le temps d'inférence"""
    inference_time_histogram.observe(inference_time_ms / 1000)
```

#### 2. `src/routes.py`

Dans la fonction `predict()`, **ajouter** :
```python
# DONE: Mesurer et tracker le temps d'inférence
start_time = time.time()
# ... code de prédiction ...
inference_time_ms = (time.time() - start_time) * 1000
track_inference_time(inference_time_ms)
```

#### 3. `monitoring/prometheus/rules/alerts.yml`

**Ajouter** :
```yaml
  - alert: alert_high_latency
    expr: rate(cv_inference_time_seconds_sum[5m]) / rate(cv_inference_time_seconds_count[5m]) > 2
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "Latence élevée détectée"
      description: "Latence moyenne > 2s pendant 2 minutes"
```

#### 4. `monitoring/grafana/provisioning/alerting/cv-alerts.yml`

**Ajouter l'alerte** (voir exemple dans le dashboard actuel)

### Déployer
```bash
git add .
git commit -m "feat: Add inference_time metric"
git push origin main
```

### Vérifier

1. Grafana → Explorer → Requête : `cv_inference_time_seconds`
2. Faire 10 prédictions sur l'API
3. Vérifier que la métrique s'affiche
4. Créer un panel Grafana pour afficher la latence moyenne

---

## 📝 Exercice 2 : Métrique Feedback Utilisateur (Jour 3)

### Objectif
Tracker les retours utilisateurs (positifs/négatifs).

### À Implémenter

1. **Métrique Prometheus** :
```python
# DONE: Créer métrique counter pour feedback
feedback_counter = Counter(
    'cv_user_feedback_total',
    'Nombre de feedbacks utilisateurs',
    ['feedback_type']  # 'positive' ou 'negative'
)
```

- [x] : modifier feedback
2. **Route** : Modifier `/feedback` pour appeler `track_feedback()`

- [x] : ajouter alerte feedback
1. **Alerte** : Si taux de feedback négatif > 50% pendant 10min

- [x] : ajouter panel piechart
4. **Dashboard Grafana** : Panel pie chart pour répartition positive/negative

---

## 🎨 Exercice 3 : Métriques Custom (Jour 3-4)

Choisir **2 métriques** parmi :

- Distribution des prédictions (cats vs dogs)
- Nombre d'utilisateurs uniques
- [x] Taux de prédictions avec faible confiance (< 60%)
- Nombre de requêtes par heure
- Taille moyenne des images uploadées

### Livrables

1. Code Python (métriques + routes)
2. Alertes Prometheus
3. Alertes Grafana provisionnées
4. Dashboard Grafana complet

---

## 🏆 Bonus (Jour 4)

### Tests Automatisés dans CI/CD

Ajouter dans `.github/workflows/deploy.yml` **AVANT** le déploiement :
```yaml
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements/base.txt -r requirements/dev.txt
      - run: pytest tests/ -v
```

### Dashboard Grafana Stylé

- Utiliser des variables
- Ajouter des liens entre panels
- Organiser en rows
- Utiliser des thresholds colorés
- Ajouter des descriptions

---

## ✅ Checkpoints de Validation

- [x] Métrique inference_time visible dans Prometheus
- [x] Alerte high_latency configurée
- [x] Dashboard Grafana affiche la latence
- [x] Notification Discord reçue en cas d'alerte
- [x] Métrique feedback_counter fonctionnelle
- [x] 2 métriques custom implémentées
- [-] Tests automatisés dans CI/CD
- [ ] Dashboard final complet et stylé