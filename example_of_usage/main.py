from versions.version import Version, parse_from_str, in_allowed_format
from versions.converters.registry import main_converter_registry
from versions.converters.service import load_converters

from example_of_usage.custom_versions import Semver, Hash, BuildVersion

load_converters("example_of_usage.custom_converters")

# Any ancentor of Version is immutable.
source = Semver(version="11.5.7+25.3")
target = Hash(version="bh35ag56")

print("## Сценарий 1: Выяснить, какой формат у переданной (str) версии.")
unknown_version_format = "18.1.5+26.1"
parsed_version = parse_from_str(unknown_version_format)
assert type(parsed_version) == Semver
assert parsed_version.version == "18.1.5+26.1"

print("## Сценарий 2: Запретить ввод версии в формате Build.")
yes = in_allowed_format(BuildVersion.EXAMPLE, Hash|Semver)
print(f"{BuildVersion.EXAMPLE=} in a Hash or Semver format? ", end="")
print("YES") if yes else print("NO")
# OR by raising a error.
# assert in_allowed_format(BuildVersion.EXAMPLE, Hash|Semver, raise_an_error=True)
# TypeError: Version 'X70-26.2-ahbhge25' is not in allowed formats. Allowed formats: Hash: 'bh35ag56'; Semver: '11.5.7+25.3'; 

print("# Сценарий 3: Посмотреть все доступные форматы версий.")
print(Version.formats())

print("# Сценарий 4: Проверить, что версия (str) соответствует формату Semver.")
...

# Можно удалить этот метод?
print(Semver.matches("11.5.7+25.3"))

print("# Сценарий 5: Посмотреть все доступные конверторы версий.")
print("Available converters:", main_converter_registry.get_all())

print("# Сценарий 6: Сконвертировать Semver в Build")
print(f"Converted semver to build version:", source.convert_to(BuildVersion))
