"""
Alexa FV Monitor - Lambda Handler
=================================
AWS Lambda handler for Alexa Custom Skill.
"""
import json
from wisesolar_api import get_all_data

# Alexa intent handlers

def on_launch():
    return build_response('Benvenuto! Chiedi lo stato del fotovoltaico. '
                         'Prova: produzione, consumo, stato, o guadagno.', should_end_session=False)

def on_session_ended():
    return build_response('Arrivederci!', should_end_session=True)

def on_help():
    return build_response(
        'Puoi chiedermi: produzione, consumo, stato, o guadagno. '
        'Prova a dire: Alexa, chiedi a FV Monitor la produzione.',
        should_end_session=False
    )

def on_get_production():
    try:
        data = get_all_data()
        pw = data['pv_power']
        day = data['day_energy']
        total = data['total_energy']

        if pw > 0:
            speech = f'L impianto sta producendo {pw} watt. Oggi hai generato {day:.1f} kilowattora.'
        else:
            speech = f'L impianto non sta producendo. Oggi hai generato {day:.1f} kilowattora in totale.'

        return build_response(speech, should_end_session=True)
    except Exception as e:
        return build_response(f'Errore nel leggere i dati: {str(e)}', should_end_session=True)

def on_get_consumption():
    try:
        data = get_all_data()
        load = data['load_power']
        day_cons = data['day_consumption']

        speech = f'Casa sta consumando {load} watt. Oggi hai consumato {day_cons:.1f} kilowattora.'
        return build_response(speech, should_end_session=True)
    except Exception as e:
        return build_response(f'Errore nel leggere i dati: {str(e)}', should_end_session=True)

def on_get_status():
    try:
        data = get_all_data()
        pw = data['pv_power']
        load = data['load_power']
        gw = data['grid_power']
        status = data['status']
        weather = data['weather']

        grid_text = 'immettendo in rete' if gw > 0 else 'prelevando dalla rete' if gw < 0 else 'scambio nullo con la rete'
        abs_gw = abs(gw)

        speech = (f'Stato impianto: {status}. '
                 f'Produzione: {pw} watt. Consumo casa: {load} watt. '
                 f'Rete: {abs_gw} watt, {grid_text}.')
        if weather.strip():
            speech += f' Meteo: {weather.strip()}.'

        return build_response(speech, should_end_session=True)
    except Exception as e:
        return build_response(f'Errore nel leggere i dati: {str(e)}', should_end_session=True)

def on_get_revenue():
    try:
        data = get_all_data()
        revenue = data['revenue']
        day = data['day_energy']

        if revenue > 0:
            speech = f'Oggi hai guadagnato {revenue:.2f} euro. Produzione totale: {day:.1f} kilowattora.'
        else:
            speech = f'Non ho dati sul guadagno di oggi. Produzione totale: {day:.1f} kilowattora.'
        return build_response(speech, should_end_session=True)
    except Exception as e:
        return build_response(f'Errore nel leggere i dati: {str(e)}', should_end_session=True)

def on_get_battery():
    try:
        data = get_all_data()
        bt = data['battery_power']

        if bt > 0:
            speech = f'La batteria si sta caricando a {bt} watt.'
        elif bt < 0:
            speech = f'La batteria si sta scaricando a {abs(bt)} watt.'
        else:
            speech = 'La batteria e ferma.'
        return build_response(speech, should_end_session=True)
    except Exception as e:
        return build_response(f'Errore nel leggere i dati: {str(e)}', should_end_session=True)

# Alexa response builders

def build_response(speech_text, should_end_session=True):
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': speech_text,
            },
            'shouldEndSession': should_end_session,
        },
    }

# Main handler

INTENT_HANDLERS = {
    'GetProduction': on_get_production,
    'GetConsumption': on_get_consumption,
    'GetStatus': on_get_status,
    'GetRevenue': on_get_revenue,
    'GetBattery': on_get_battery,
    'AMAZON.HelpIntent': on_help,
    'AMAZON.CancelIntent': lambda: build_response('Ok, annullato.', should_end_session=True),
    'AMAZON.StopIntent': lambda: build_response('Arrivederci!', should_end_session=True),
}

def lambda_handler(event, context):
    request_type = event.get('request', {}).get('type')

    if request_type == 'LaunchRequest':
        return on_launch()
    elif request_type == 'SessionEndedRequest':
        return on_session_ended()
    elif request_type == 'IntentRequest':
        intent_name = event['request']['intent']['name']
        handler = INTENT_HANDLERS.get(intent_name)
        if handler:
            return handler()
        else:
            return build_response(f'Non ho capito l intenzione: {intent_name}. '
                                 'Prova a chiedere produzione, consumo, stato, o guadagno.',
                                 should_end_session=False)

    return build_response('Richiesta non riconosciuta.', should_end_session=True)
