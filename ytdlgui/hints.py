"""Erreurs courantes de yt-dlp : reconnaît une ligne d'erreur pour expliquer à l'utilisateur
ce qui s'est passé et ce qu'il peut y faire (fenêtre de conseil, cf. openHint dans
web/app.js). Motifs relevés dans le code de yt-dlp 2026.10.26.
"""
import re

# (clé, motif) : le premier motif trouvé l'emporte, d'où l'ordre. Une restriction
# géographique ou une limite de YouTube passe ainsi avant le conseil générique sur les
# cookies, et « please report this issue » (ajouté à toute erreur imprévue) vient en dernier.
_HINTS = [(key, re.compile(pattern, re.I)) for key, pattern in (
    ("cookies_locked", r"Could not copy Chrome cookie database"),
    ("ffmpeg", r"ffmpeg is not installed|ffmpeg not found|ffprobe and ffmpeg not found"),
    ("disk_full", r"No space left on device|Disk quota exceeded|\[Errno 28\]"),
    ("drm", r"DRM protected"),
    ("geo", r"not available from your location|not made this video available in your country"),
    ("rate_limit", r"try again later|HTTP Error 429"),
    ("js_runtime", r"supported JavaScript runtime"),
    # Le conseil de connexion de yt-dlp cite toujours --cookies (Reddit, Instagram, YouTube
    # « not a bot », limite d'âge, vidéo privée...) ; YouTube peut aussi exiger un captcha.
    ("login", r"--cookies|captcha challenge"),
    ("format", r"Requested format is not available"),
    ("unsupported", r"Unsupported URL"),
    ("network", r"getaddrinfo failed|Name or service not known|Temporary failure in name resolution"
                r"|timed out|Unable to connect to proxy|ProxyError|Connection refused"
                r"|Network is unreachable|No route to host"),
    ("unavailable", r"Video unavailable|This video is unavailable|has been removed"
                    r"|no longer available|has been terminated"),
    ("outdated", r"HTTP Error 403|please report this issue"),
)]


def classify(text):
    """Clé de la première erreur reconnue dans le texte (sortie de yt-dlp), ou None.
    Seules les lignes « ERROR: » comptent : les avertissements ne font pas échouer."""
    for line in str(text or "").splitlines():
        line = line.strip()
        if line.startswith("ERROR:"):
            for key, pattern in _HINTS:
                if pattern.search(line):
                    return key
    return None
