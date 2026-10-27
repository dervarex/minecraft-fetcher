import pkgutil

import features

# loads all feature module (commands basically)
def all_feature_modules():
    for module in pkgutil.walk_packages(features.__path__, prefix="features."):
        if not module.ispkg:
            yield module.name
