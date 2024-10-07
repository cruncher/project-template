import os
import pytest

@pytest.fixture
def context():
    return {
    "project_name": "Test Cruncher Project",
    "project_slug": "test_project_name",
    "description": "Test Project generated by project-template & cookiecutter",
    "author_name": "Cruncher",
    "domain_name": "test.cruncher.ch",
    "email": "test@cruncher.ch",
    "debug": True,
    "cms": "DjangoCMS",
    "multilanguage": True,
    "use_parler": True,
    "add_submodule_bolt": True,
    "add_submodule_fn": True,
    "add_submodule_dom": True,
    "add_submodule_slideshow": True,
    "include_news_app": True,
  }

SUPPORTED_COMBINATIONS = [
    {"project_name": "Test Cruncher Project"},
    {"project_slug": "test_project_name"},
    {"description": "Test Project generated by project-template & cookiecutter"},
    {"author_name": "Cruncher"},
    {"domain_name": "test.cruncher.ch"},
    {"email": "test@cruncher.ch"},
    {"debug": True},
    {"debug": False},
    {"cms": "DjangoCMS"},
    {"cms": "Wagtail"},
    {"cms": "None"},
    {"multilanguage": True},
    {"multilanguage": False},
    {"use_parler": True},
    {"use_parler": False},
    {"add_submodule_bolt": True},
    {"add_submodule_bolt": False},
    {"add_submodule_fn": True},
    {"add_submodule_fn": False},
    {"add_submodule_dom": True},
    {"add_submodule_dom": False},
    {"add_submodule_slideshow": True},
    {"add_submodule_slideshow": False},
    {"include_news_app": True},
    {"include_news_app": False},
]

@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS)
def test_default_project_generation(cookies, context, context_override):
    submodule_options = {
        "add_submodule_bolt": False,
        "add_submodule_fn": False,
        "add_submodule_dom": False,
        "add_submodule_slideshow": False
    }
    context.update(submodule_options)
    result = cookies.bake(extra_context={**context, **context_override})
    assert result.exit_code == 0
    assert result.exception is None

    if context_override.get("add_submodule_bolt"):
        assert os.path.isdir(os.path.join(result.project_path,result.project_path.name, "static", "bolt"))
    if context_override.get("add_submodule_fn"):
        assert os.path.isdir(os.path.join(result.project_path,result.project_path.name, "static", "fn"))
    if context_override.get("add_submodule_dom"):
        assert os.path.isdir(os.path.join(result.project_path, result.project_path.name,"static", "dom"))
    if context_override.get("add_submodule_slideshow"):
        assert os.path.isdir(os.path.join(result.project_path, result.project_path.name, "static", "slide-show"))
    if context_override.get("include_news_app"):
        assert os.path.isdir(os.path.join(result.project_path, result.project_path.name, "apps", "news"))
    if context_override.get("cms") == "None":
        assert not os.path.isdir(os.path.join(result.project_path,result.project_path.name , "apps", "news"))
    

    assert result.project_path.name == "test_project_name"
    assert result.project_path.is_dir()
