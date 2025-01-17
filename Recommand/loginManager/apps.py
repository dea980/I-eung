from django.apps import AppConfig

class LoginManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loginManager'
    verbose_name = '로그인 관리'

    def ready(self):
        try:
            import loginManager.signals
        except ImportError:
            pass
