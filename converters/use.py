


if __name__ == "__main__":
    # Какие требования?
    # 1) Могут добавляться новые способы конвертации для уже существующих пар
    # 2) Могу добавляться новые переходы между версиями.
    # 3) Должен поддерживаться новый переход с использованием уже существующих классов конверторов. 
    # 4) Должа быть возможность добавлять дублер-конвертер - второй запасной способ конвертации.
    # 5) Должа быть возможность выдавать приоритет конверторам.

    from versions.converters.base import Convertor
    from versions.custom_models import Semver, BuildVersion
    from versions.converters.custom_converters import SemverToBuildConverter
    from versions.converters.registry import main_convertor_registry
    
    print("Available converters:", main_convertor_registry.formats())
    
    source_semver = Semver(version="26.6.3+26.1")
    
    converter_to_build = source_semver.convert_to(BuildVersion)
    print(converter_to_build)
    
    # c1 = SemverToBuildConverter()
    # print(c1.convert(source_semver))

    
    # Use case 1
    # smv = Semver(version="26.6.3+26.1")
    # build = smv.convertTo(to=BuildVersion) # raise a error if convertor does not exist.
    # assert isinstance(build, BuildVersion)
