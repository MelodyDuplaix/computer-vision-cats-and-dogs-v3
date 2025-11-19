
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_fastapi_instrumentator import Instrumentator
import os
database_status = Gauge(
    'cv_database_connected',
    'Database connection status (1=connected, 0=disconnected)'
)
def setup_prometheus(app):
    """
    Configure Prometheus pour FastAPI
    Compatible avec l'API existante V2
    
    🎯 INSTRUMENTATION AUTOMATIQUE
    Le Instrumentator ajoute automatiquement :
    - http_request_duration_seconds : latence par endpoint
    - http_requests_total : nombre de requêtes par status code
    - http_requests_in_progress : requêtes concurrentes
    
    💡 ENDPOINT /metrics
    Exposé automatiquement au format Prometheus :
    # HELP cv_predictions_total Total number of predictions
    # TYPE cv_predictions_total counter
    cv_predictions_total{result="cat"} 42.0
    cv_predictions_total{result="dog"} 38.0
    
    Args:
        app: Instance FastAPI
    """
    if os.getenv('ENABLE_PROMETHEUS', 'false').lower() == 'true':
        Instrumentator().instrument(app).expose(app, endpoint="/metrics")
        print("✅ Prometheus metrics enabled at /metrics")
    else:
        print("ℹ️  Prometheus metrics disabled")
        # Utile en dev si on veut alléger le monitoring

# ═══════════════════════════════════════════════════════════════════════════
# 📝 HELPERS - Fonctions de tracking appelées par l'API
# ═══════════════════════════════════════════════════════════════════════════

def update_db_status(is_connected: bool):
    """
    Met à jour le statut de la base de données
    
    🔗 APPELÉ PAR : healthcheck ou retry logic de connexion DB
    
    Args:
        is_connected: True si connexion PostgreSQL active
    
    💡 EXEMPLE D'INTÉGRATION
    try:
        db.execute("SELECT 1")
        update_db_status(True)
    except Exception:
        update_db_status(False)
        # Alerte Grafana se déclenche automatiquement
    """
    database_status.set(1 if is_connected else 0)


inference_time_histogram = Histogram(
    'cv_inference_time_seconds',
    'Temps d\'inférence en secondes'
)

def track_inference_time(inference_time_ms: float):
    """Enregistre le temps d'inférence"""
    inference_time_histogram.observe(inference_time_ms / 1000)



feedback_counter = Counter(
    'cv_user_feedback_total',
    'Nombre de feedbacks utilisateurs',
    ['feedback_type']  # 'positive' ou 'negative'
)
    
def track_feedback(feedback_type: str):
    """Enregistre un feedback utilisateur"""
    feedback_counter.labels(feedback_type=feedback_type).inc()
    
    
low_confidence_predictions_counter = Counter(
    'cv_low_confidence_predictions_total',
    'Nombre de prédictions faibles de confiance',
    ['prediction_result'],  # 'cat' ou 'dog'
)
    
def track_low_confidence_prediction(prediction_result: str):
    """Enregistre une prédiction faible de confiance"""
    low_confidence_predictions_counter.labels(prediction_result=prediction_result).inc()
    
    
abnormal_image_size_counter = Counter(
    'cv_abnormal_image_size_total',
    'Compteur d\'images avec une taille anormale',
    ['type']  # 'small' or 'large' or 'normal'
)

IMAGE_SIZE_LOWER_THRESHOLD = 64 * 64

IMAGE_SIZE_UPPER_THRESHOLD = 5000 * 5000
    
def track_image_size(width: int, height: int):
    """
    Incrémente un compteur si la taille de l'image est considérée comme anormale.
    """
    size = width * height

    if size < IMAGE_SIZE_LOWER_THRESHOLD:
        abnormal_image_size_counter.labels(type='small').inc()
    elif size > IMAGE_SIZE_UPPER_THRESHOLD:
        abnormal_image_size_counter.labels(type='large').inc()
    else:
        abnormal_image_size_counter.labels(type='normal').inc()
    