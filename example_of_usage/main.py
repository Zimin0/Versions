from pydantic import ValidationError

from versions import Version, parse_from_str, in_allowed_format
from versions.converters import load_converters, main_converter_registry

from custom_versions import Semver, Hash, BuildVersion

load_converters("custom_converters")


# Any subclass of Version is immutable.
source = Semver(version="11.5.7+25.3")
target = Hash(version="bh35ag56")


print("## Scenario 1: Detect the format of a version string.")

unknown_version = "18.1.5+26.1"

parsed_version = parse_from_str(unknown_version)

assert type(parsed_version) is Semver
assert parsed_version.version == unknown_version


print("## Scenario 2: Restrict input to specific version formats.")

is_allowed = in_allowed_format(
    BuildVersion.EXAMPLE,
    Hash | Semver,
)

print(
    f"Is {BuildVersion.EXAMPLE!r} in Hash or Semver format? ",
    end="",
)
print("YES" if is_allowed else "NO")

# Alternatively, raise an error if the format is not allowed.
#
# in_allowed_format(
#     BuildVersion.EXAMPLE,
#     Hash | Semver,
#     raise_an_error=True,
# )
#
# TypeError:
# Version 'XYZ70-26.2-ahbhge25' is not in allowed formats.
# Allowed formats:
# Hash: 'bh35ag56';
# Semver: '11.5.7+25.3';


print("## Scenario 3: Show all available version formats.")

print("Available version formats:", Version.formats())


print("## Scenario 4: Validate a string against the Semver format.")

input_version = "invalid-version"

# Method 1: validate using Version.matches().
if Semver.matches(input_version):
    print("Method 1: VALID")
else:
    print("Method 1: INVALID")


# Method 2: validate by creating a Version instance.
try:
    Semver(version=input_version)
except ValidationError:
    print("Method 2: INVALID")
else:
    print("Method 2: VALID")


print("## Scenario 5: Show all available version converters.")

print("Available converters:", main_converter_registry.get_all())


print("## Scenario 6: Convert Semver to BuildVersion.")

converted_version = source.convert_to(BuildVersion)

print("Converted Semver to BuildVersion:", converted_version)
