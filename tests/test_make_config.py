from unittest import mock

from log_enricher import make_config, configure_loggers


def test_make_config_uses_default_enrichers():
    with mock.patch("log_enricher.default_enrichers") as default_enrichers:
        default_enrichers.return_value = ["a", "b"]
        config = make_config()
        assert default_enrichers.called
        assert config["filters"]["context"]["enrichers"] == ["a", "b"]


def test_make_config_combines_default_enrichers_with_given_enrichers():
    with mock.patch("log_enricher.default_enrichers") as default_enrichers:
        default_enrichers.return_value = ["a", "b"]
        config = make_config(enrichers=["c", "d"])
        assert default_enrichers.called
        assert config["filters"]["context"]["enrichers"] == ["a", "b", "c", "d"]


def test_configure_loggers():
    loggers = [
        "simple_logger",
        {
            "name": "complex_logger",
            "log_level": "DEBUG"
        }
    ]
    loggers_config = configure_loggers(loggers, "structured", "INFO")
    assert loggers_config["simple_logger"]["level"] == "INFO"
    assert loggers_config["complex_logger"]["level"] == "DEBUG"
