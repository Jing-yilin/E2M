from .default import DefaultConfig


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    # 开发环境的其他配置
