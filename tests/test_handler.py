"""
Tests for Alexa FV Monitor Lambda handler.
"""
import json
import os
import pytest

# Mock environment variables before import
os.environ['FV_USER'] = 'test@example.com'
os.environ['FV_PASS'] = 'testpass'
os.environ['FV_STATION_ID'] = '1234'
os.environ['FV_CUSTOMER_ID'] = '9999'

# Mock the API module before importing handler
import sys
from unittest.mock import patch, MagicMock

# Create mock module
mock_api = MagicMock()
mock_api.get_all_data.return_value = {
    'pv_power': 1500,
    'grid_power': -200,
    'load_power': 1200,
    'battery_power': 100,
    'status': 'Normal',
    'weather': 'Sunny 20-30C',
    'day_energy': 8.5,
    'total_energy': 12345.0,
    'day_consumption': 6.2,
    'revenue': 1.25,
}
sys.modules['wisesolar_api'] = mock_api

from fv_handler import lambda_handler, build_response


def make_alexa_request(intent_name, slots=None):
    return {
        'version': '1.0',
        'session': {'new': True, 'sessionId': 'test'},
        'request': {
            'type': 'IntentRequest',
            'intent': {
                'name': intent_name,
                'slots': slots or {},
            },
        },
    }


def test_launch_request():
    event = {'request': {'type': 'LaunchRequest'}}
    result = lambda_handler(event, None)
    assert result['response']['shouldEndSession'] is False
    assert 'outputSpeech' in result['response']


def test_get_production():
    event = make_alexa_request('GetProduction')
    result = lambda_handler(event, None)
    speech = result['response']['outputSpeech']['text']
    assert '1500' in speech
    assert '8.5' in speech
    assert result['response']['shouldEndSession'] is True


def test_get_consumption():
    event = make_alexa_request('GetConsumption')
    result = lambda_handler(event, None)
    speech = result['response']['outputSpeech']['text']
    assert '1200' in speech
    assert '6.2' in speech


def test_get_status():
    event = make_alexa_request('GetStatus')
    result = lambda_handler(event, None)
    speech = result['response']['outputSpeech']['text']
    assert '1500' in speech
    assert '1200' in speech
    assert 'Normal' in speech


def test_get_revenue():
    event = make_alexa_request('GetRevenue')
    result = lambda_handler(event, None)
    speech = result['response']['outputSpeech']['text']
    assert '1.25' in speech


def test_get_battery():
    event = make_alexa_request('GetBattery')
    result = lambda_handler(event, None)
    speech = result['response']['outputSpeech']['text']
    assert '100' in speech
    assert 'caricando' in speech


def test_help():
    event = make_alexa_request('AMAZON.HelpIntent')
    result = lambda_handler(event, None)
    assert result['response']['shouldEndSession'] is False


def test_unknown_intent():
    event = make_alexa_request('SomeUnknownIntent')
    result = lambda_handler(event, None)
    speech = result['response']['outputSpeech']['text']
    assert 'Non ho capito' in speech


def test_session_ended():
    event = {'request': {'type': 'SessionEndedRequest'}}
    result = lambda_handler(event, None)
    assert result['response']['shouldEndSession'] is True


def test_api_error():
    mock_api.get_all_data.side_effect = RuntimeError('Connection failed')
    event = make_alexa_request('GetProduction')
    result = lambda_handler(event, None)
    speech = result['response']['outputSpeech']['text']
    assert 'Errore' in speech
    mock_api.get_all_data.side_effect = None
