# 🎓 Configuration Étudiant - Atelier MLOps

## Votre Identifiant

Vous avez été assigné : **STUDENT08** (remplacer XX par votre numéro)

## URLs d'Accès

Après déploiement, vos services seront accessibles sur :

- 🔧 **API FastAPI** : http://51.91.251.234:80XX
- 📊 **Grafana** : http://51.91.251.234:30XX  
- 📈 **Prometheus** : http://51.91.251.234:90XX

*Exemple pour student01 : http://51.91.251.234:8001*

## Tableau des Ports Assignés

| Prénom | Étudiant | STUDENT_ID | API | Grafana | Prometheus | PostgreSQL |
|--------|----------|------------|-----|---------|------------|------------|
| Rémi | 1 | student01 | 8001 | 3001 | 9091 | 5434 |
| Arnaud | 2 | student02 | 8002 | 3002 | 9092 | 5435 |
| Cyril | 3 | student03 | 8003 | 3003 | 9093 | 5436 |
| Dylan | 4 | student04 | 8004 | 3004 | 9094 | 5437 |
| Jonathan | 5 | student05 | 8005 | 3005 | 9095 | 5438 |
| Fabien | 6 | student06 | 8006 | 3006 | 9096 | 5439 |
| Maximilien | 7 | student07 | 8007 | 3007 | 9097 | 5440 |
| Melody | 8 | student08 | 8008 | 3008 | 9098 | 5441 |
| Patricia | 9 | student09 | 8009 | 3009 | 9099 | 5442 |
| Promise | 10 | student10 | 8010 | 3010 | 9100 | 5443 |
| Steve | 11 | student11 | 8011 | 3011 | 9101 | 5444 |

## Configuration GitHub

### Étape 1 : Créer votre Personal Access Token

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Note : `MLOps Workshop Token`
4. Expiration : 90 days
5. **Scope** : Cocher uniquement `repo`
6. Generate token
7. **Copier le token** (commence par `ghp_...`)

### Étape 2 : Configurer les Secrets GitHub

Dans **votre repository** forké :
1. Settings → Secrets and variables → Actions
2. New repository secret

Créer **8 secrets** :

| Secret Name | Votre Valeur |
|-------------|--------------|
| `STUDENT_ID` | `studentXX` (votre numéro) |
| `STUDENT_PORT_API` | `80XX` |
| `STUDENT_PORT_GRAFANA` | `30XX` |
| `STUDENT_PORT_PROMETHEUS` | `90XX` |
| `VPS_HOST` | `51.91.251.234` |
| `VPS_USER` | `ubuntu` |
| `SSH_PRIVATE_KEY` | *Fourni par le formateur* |
| `GH_TOKEN` | *Votre token créé à l'étape 1* |

### Étape 3 : Premier Déploiement
```bash
git add .
git commit -m "Initial setup for studentXX"
git push origin main
```

GitHub Actions se lance automatiquement → Vérifier dans l'onglet **Actions**

## Accès SSH au VPS (Debug)
```bash
ssh -i .\.ssh_key ubuntu@51.91.251.234
cd ~/apps/VOTRE-REPO-NAME-studentXX/docker
docker compose -p cv-studentXX ps
docker compose -p cv-studentXX logs
```

⚠️ **Règle** : Ne toucher qu'à vos propres containers (`cv-studentXX`)

## Aide

- Erreur de déploiement : Vérifier GitHub Actions → onglet Actions
- Containers ne démarrent pas : `docker compose -p cv-studentXX logs`
- Ports non accessibles : Vérifier les secrets GitHub