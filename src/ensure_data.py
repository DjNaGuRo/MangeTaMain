import os, pathlib, zipfile, io, sys
import streamlit as st

DATA_DIR = pathlib.Path("data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


def _log(msg: str):
    print(f"[ensure_data] {msg}", file=sys.stderr, flush=True)


def _extract_zip(src):
    if isinstance(src, (bytes, bytearray)):
        zf = zipfile.ZipFile(io.BytesIO(src))
    else:
        zf = zipfile.ZipFile(str(src))
    zf.extractall(DATA_DIR)


def ensure_data():
    mode = os.getenv("APP_MODE", "dev")
    remote_url = os.getenv("DATA_REMOTE_URL")

    DATA_DIR.mkdir(exist_ok=True)
    RAW_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)

    has_raw = any(RAW_DIR.iterdir())
    has_processed = any(PROCESSED_DIR.iterdir())
    _log(
        f"Mode={mode} url={'SET' if remote_url else 'MISSING'} raw={has_raw} processed={has_processed}"
    )

    if has_raw and has_processed:
        _log("Données présentes → skip.")
        return


    if not remote_url:
        _log("Aucune URL de données fournie et les dossiers de données sont absents.")
        st.error("Aucune donnée trouvée et DATA_REMOTE_URL n'est pas défini. Veuillez configurer la variable d'environnement DATA_REMOTE_URL avec le lien de téléchargement des données (zip).")
        raise RuntimeError("Aucune donnée trouvée et DATA_REMOTE_URL n'est pas défini. Veuillez configurer la variable d'environnement DATA_REMOTE_URL.")

    _log(f"Téléchargement: {remote_url}")
    try:
        if "drive.google.com" in remote_url:
            try:
                import gdown
            except ImportError:
                raise RuntimeError("gdown non installé (ajoute-le dans pyproject).")
            tmp_zip = DATA_DIR / "data.zip"
            gdown.download(remote_url, str(tmp_zip), quiet=False)
            if not tmp_zip.exists():
                raise RuntimeError("Téléchargement Drive échoué (fichier absent).")
            _log("Extraction zip...")
            _extract_zip(tmp_zip)
            tmp_zip.unlink(missing_ok=True)
        else:
            import requests

            resp = requests.get(remote_url, timeout=300)
            resp.raise_for_status()
            _log(f"Reçu {len(resp.content)} octets. Extraction...")
            _extract_zip(resp.content)
    except Exception as e:
        _log(f"Erreur téléchargement: {e}")
        raise

    has_raw = any(RAW_DIR.iterdir())
    has_processed = any(PROCESSED_DIR.iterdir())
    _log(f"Après extraction raw={has_raw} processed={has_processed}")
    if not has_raw or not has_processed:
        raise RuntimeError("Extraction incomplète.")
