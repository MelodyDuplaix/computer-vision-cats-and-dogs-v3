.PHONY: help install test run docker-up docker-down monitor deploy

help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


install: ## Installe les dépendances
	python -m venv venv
	pip install -r requirements/monitoring.txt
	venv\Scripts\activate

test: ## Lance les tests
	pytest tests/ -v

run: ## Lance l'API localement
	python scripts/run_api.py
docker-up: ## Démarre tous les services Docker
	docker-compose -f docker/docker-compose.yml up -d

docker-down: ## Arrête tous les services Docker
	docker-compose -f docker/docker-compose.yml down

docker-logs: ## Affiche les logs des containers
	docker-compose -f docker/docker-compose.yml logs -f

docker-restart: ## Redémarre tous les services
	docker-compose -f docker/docker-compose.yml restart

monitor: ## Ouvre le dashboard Grafana
	@echo "🌐 Grafana: http://localhost:3000"
	@echo "📊 Prometheus: http://localhost:9090"
	@echo "🚀 API: http://localhost:8000"
	@echo "📈 Dashboard Plotly (V2): http://localhost:8000/monitoring"

setup-monitoring: ## Configure le monitoring initial
	@bash scripts/setup_monitoring.sh

deploy: ## Déploie sur le serveur de test
	@bash scripts/deploy.sh