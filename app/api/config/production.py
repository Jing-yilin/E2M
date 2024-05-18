from api.config.default import DefaultConfig


class ProductionConfig(DefaultConfig):
    DEBUG = False
    # 生产环境的其他配置
