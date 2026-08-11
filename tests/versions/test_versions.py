import pytest
from pydantic import ValidationError

from versions.custom_models import Semver 

@pytest.fixture()
def semver() -> Semver:
    return Semver(version="18.1.5+26.1")



def test_regex_and_example_is_not_changable(semver: Semver):
    with pytest.raises(ValidationError) as error:
        semver.FORMAT = '123'
    
    with pytest.raises(ValidationError) as error:
        semver.EXAMPLE = '123'


# # print with repr()
# str1 = "hell"
# raise ValueError(f"Error: {str1!r}")