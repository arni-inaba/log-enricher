from unittest import mock

from log_enricher import make_config


def test_make_config_uses_default_enrichers():
    with mock.patch('log_enricher.default_enrichers') as default_enrichers:
        default_enrichers.return_value = ['a', 'b']
        config = make_config(app_version='a', release_stage='b')
        assert default_enrichers.called
        print(config)
        assert config['filters']['context']['enrichers'] == ['a', 'b']


def test_make_config_combines_default_enrichers_with_given_enrichers():
    with mock.patch('log_enricher.default_enrichers') as default_enrichers:
        default_enrichers.return_value = ['a', 'b']
        config = make_config(app_version='a', release_stage='b', enrichers=['c', 'd'])
        assert default_enrichers.called
        assert config['filters']['context']['enrichers'] == ['a', 'b', 'c', 'd']
