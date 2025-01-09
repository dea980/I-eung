from django.apps import AppConfig
"""
Articles 애플리케이션의 설정 클래스입니다.

이 클래스는 Django의 애플리케이션 설정을 정의하며, 'articles' 앱의 메타데이터와 관련된 정보를 제공합니다.

Attributes:
    default_auto_field: 모델에서 기본적으로 사용되는 자동 증가 필드 타입을 정의합니다.
    name: 애플리케이션의 이름을 정의합니다. 여기서는 'articles'로 설정되어 있습니다.
"""

class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'
