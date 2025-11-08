"""
Logging configuration for MangeTaMain project.

This module provides centralized logging configuration with:
- Base level: DEBUG
- Separate handlers for different log levels
- Logs stored in project root logs/ directory
"""

import logging
import logging.config
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    current = Path(__file__).resolve()
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    return Path.cwd()


def setup_logging():
    """
    Configure logging for the MangeTaMain project.
    
    Creates the following log files:
    - logs/debug.log: All debug and higher level messages
    - logs/error.log: Only ERROR and CRITICAL messages
    - logs/app.log: Application-specific messages (INFO and higher)
    """
    project_root = get_project_root()
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(asctime)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'console': {
                'format': '%(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'console',
                'stream': 'ext://sys.stdout'
            },
            'debug_file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': str(logs_dir / 'debug.log'),
                'mode': 'a',
                'encoding': 'utf-8'
            },
            'error_file': {
                'class': 'logging.FileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': str(logs_dir / 'error.log'),
                'mode': 'a',
                'encoding': 'utf-8'
            },
            'app_file': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'filename': str(logs_dir / 'app.log'),
                'mode': 'a',
                'encoding': 'utf-8'
            }
        },
        'loggers': {
            'mangetamain': {
                'level': 'DEBUG',
                'handlers': ['console', 'debug_file', 'error_file', 'app_file'],
                'propagate': False
            },
            'mangetamain.data_loader': {
                'level': 'DEBUG',
                'handlers': ['console', 'debug_file', 'error_file', 'app_file'],
                'propagate': False
            },
            'mangetamain.data_management_with_psql': {
                'level': 'DEBUG',
                'handlers': ['console', 'debug_file', 'error_file', 'app_file'],
                'propagate': False
            },
            'mangetamain.preprocessing': {
                'level': 'DEBUG',
                'handlers': ['console', 'debug_file', 'error_file', 'app_file'],
                'propagate': False
            },
            'mangetamain.visualization': {
                'level': 'DEBUG',
                'handlers': ['console', 'debug_file', 'error_file', 'app_file'],
                'propagate': False
            },
            'mangetamain.streamlit': {
                'level': 'DEBUG',
                'handlers': ['console', 'debug_file', 'error_file', 'app_file'],
                'propagate': False
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'debug_file', 'error_file']
        }
    }
    
    logging.config.dictConfig(logging_config)
    
    # Log the initialization
    logger = logging.getLogger('mangetamain')
    logger.info("Logging configuration initialized successfully")
    logger.debug(f"Logs directory: {logs_dir}")
    
    return logger


def get_logger(name: str = None):
    """
    Get a logger instance for the given name.
    
    Args:
        name: Logger name. If None, returns the main mangetamain logger.
        
    Returns:
        logging.Logger: Configured logger instance
    """
    if name is None:
        return logging.getLogger('mangetamain')
    
    # Ensure the name starts with mangetamain for proper configuration
    if not name.startswith('mangetamain'):
        name = f'mangetamain.{name}'
    
    return logging.getLogger(name)


# Initialize logging when module is imported
setup_logging()