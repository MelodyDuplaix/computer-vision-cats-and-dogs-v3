
import os
import requests
from datetime import datetime
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent.parent

load_dotenv(ROOT_DIR / '.env')
class DiscordNotifier:
    """
    Envoie des notifications Discord pour événements critiques
    """
    
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        self.enabled = bool(self.webhook_url)
        
    def send_alert(self, 
                   title: str, 
                   message: str, 
                   level: str = "info",
                   metrics: Optional[dict] = None):
        """
        Envoie une alerte Discord enrichie (embed)
        """
        if not self.enabled:
            return 
        colors = {
            "info": 3447003,      # Bleu (#3498db) - informations générales
            "warning": 16776960,  # Jaune (#ffff00) - attention requise
            "error": 15158332,    # Rouge (#e74c3c) - dysfonctionnement
            "critical": 10038562  # Rouge foncé (#992d22) - incident majeur
        }
        embed = {
            "title": f"🚨 {title}",
            
            "description": message,
            
            "color": colors.get(level, 3447003),
            
            "timestamp": datetime.utcnow().isoformat(),
            
            "footer": {
                "text": "CV Cats & Dogs Monitoring"
            }
            # 📌 Signature en bas de l'embed (branding)
        }
        if metrics:
            embed["fields"] = [
                {
                    "name": key,           # Nom de la métrique
                    "value": str(value),   # Valeur (converti en string)
                    "inline": True         # Affichage côte à côte (max 3 par ligne)
                }
                for key, value in metrics.items()
            ]
        payload = {
            "username": "MLOps Bot",
            
            "embeds": [embed]
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            
            response.raise_for_status()
            
        except Exception as e:
            print(f"❌ Failed to send Discord alert: {e}")

notifier = DiscordNotifier()

def alert_model_degradation(accuracy: float, threshold: float = 0.85):
    """
    Alerte si l'accuracy du modèle baisse sous le seuil
    """
    if accuracy < threshold:
        notifier.send_alert(
            title="Model Performance Degradation",
            message=f"Model accuracy ({accuracy:.2%}) dropped below threshold ({threshold:.2%})",
            level="warning",  # Warning car dégradation progressive (pas incident immédiat)
            metrics={
                "Current Accuracy": f"{accuracy:.2%}",
                "Threshold": f"{threshold:.2%}",
                "Gap": f"{(accuracy - threshold):.2%}"  # Négatif = problème
            }
        )

def alert_high_latency(latency_ms: float, threshold: float = 2000):
    """
    Alerte si la latence d'inférence est trop élevée
    """
    if latency_ms > threshold:
        notifier.send_alert(
            title="High Inference Latency",
            message=f"Inference taking {latency_ms}ms (threshold: {threshold}ms)",
            level="error",  # Error car impact direct sur UX
            metrics={
                "Latency": f"{latency_ms:.0f}ms",
                "Threshold": f"{threshold:.0f}ms",
                "Slowdown": f"x{(latency_ms / threshold):.1f}"  # Ex: x2.5 = 2.5x plus lent
            }
        )

def alert_database_disconnected():
    """
    Alerte si la base de données PostgreSQL est déconnectée
    """
    notifier.send_alert(
        title="Database Connection Lost",
        message="PostgreSQL database is unreachable. All feedback storage is currently disabled.",
        level="critical",  # Critical car perte de fonctionnalité majeure
        metrics={
            "Service": "PostgreSQL",
            "Impact": "❌ Feedback storage offline",
            "Action": "Check docker logs cv_postgres"
        }
    )

def alert_deployment_success(version: str):
    """
    Notification de déploiement réussi (non-blocking, informatif)
    """
    notifier.send_alert(
        title="Deployment Successful",
        message=f"Version {version} deployed successfully to production",
        level="info",  # Info car événement positif (pas un problème)
        metrics={
            "Version": version,
            "Status": "✅ Running",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
