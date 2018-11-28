import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

teams_table = boto3.resource('dynamodb').Table('Teams')

""" build different responses for lex """
def close(session_attributes, fulfillment_state, message):
    close_response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': {
                'contentType': 'PlainText',
                'content': message
            }
        }
    }
    return close_response

def delegate(session_attributes, slots):
    delegate_response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }
    return delegate_response

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    elicit_slot_response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'message': {
                'contentType': 'PlainText',
                'content': message
            },
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit
        }
    }
    return elicit_slot_response

""" Helpers """
def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

""" Intents """ 
def dispatch_lex_intent(intent_request):
    intent_name = intent_request['currentIntent']['name']
    # dispatch to intent handler
    if intent_name == 'GetTeamMembers':
        return get_team_members(intent_request)
    elif intent_name == 'GiveFeedback':
        return give_feedback(intent_request)
    raise Exception('Sorry intent with name ' + intent_name + ' not supported by this bot.')

def get_team_members(intent_request):
    slots = get_slots(intent_request)
    team_name = slots['teamName']

    if team_name is not None:
        # check if team name is in db
        try:
            members = teams_table.get_item(Key={'Name': team_name})['Item']['Members']
            msg = 'Members of ' + team_name + ': '
            for member in enumerate(members):
                msg += '{}, '.format(member[1]['Name'])
            return close(intent_request['sessionAttributes'], 'Fulfilled', msg)
        except KeyError as e:
            msg = 'Member {} is not part of any team yet.'.format(team_name)       
            return close(intent_request['sessionAttributes'], 'Failed', msg)
            
    else:
        message = 'What is the name of the team?'
        return elicit_slot(
            intent_request['sessionAttributes'],
            intent_request['currentIntent']['name'],
            slots,
            'teamName',
            message
        )

def give_feedback(intent_request):
    source = intent_request['invocationSource']
    slots = get_slots(intent_request)
    team_name = slots['teamName']
    member = slots['member']
    feedback = slots['feedback']
    if source == 'DialogCodeHook': 
        if member is None:
            elicit_msg = 'Can you repeat the name please?'
            return elicit_slot(
                intent_request['sessionAttributes'],
                intent_request['currentIntent']['name'],
                slots,
                'member',
                elicit_msg
            )
        elif team_name is None:
            elicit_msg = 'What is the team name?'
            return elicit_slot(
                intent_request['sessionAttributes'],
                intent_request['currentIntent']['name'],
                slots,
                'teamName',
                elicit_msg
            )
        elif feedback is None:
            t = teams_table.query(KeyConditionExpression=Key('Name').eq(team_name))['Items']
            members = t[0]['Members'] if t else []
            m = []
            for mem in members:
                if member in mem.values():
                    m.append(1)
                    break
            if t and m:
                elicit_msg = 'What is your feedback for {}?'.format(member)
                return elicit_slot(
                    intent_request['sessionAttributes'],
                    intent_request['currentIntent']['name'],
                    slots,
                    'feedback',
                    elicit_msg
                )
            else:
                msg = 'Either team or member could not be found.'
                return close(intent_request['sessionAttributes'], 'Failed', msg)
        return delegate(intent_request['sessionAttributes'], slots)
    # Update db with new feedback for team member
    table = teams_table.query(
        KeyConditionExpression=Key('Name').eq(team_name),
        ProjectionExpression='Members'
    )
    members = table['Items'][0]['Members']
    wanted_member = {}
    for m in members:
        if member in m.values():
            wanted_member = m
            members.remove(m)
    if 'Feedback' in wanted_member:
        wanted_member['Feedback'].append(feedback)
    else:
        wanted_member['Feedback']=feedback
    members.append(wanted_member)
    try:
        teams_table.update_item(
            Key={'Name': team_name},
            UpdateExpression="set Members = :val1",
            ExpressionAttributeValues={
                ':val1': members
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        err_msg = 'Update feedback failed: {} not found in DB.'.format(member)
        return close(intent_request['sessionAttributes'], 'Failed', err_msg)
    else:
        fulfillment_response = 'Your feedback for {} has been saved.'.format(member)
        return close(intent_request['sessionAttributes'], 'Fulfilled', fulfillment_response)



""" Main entry point where events are coming in and invoking the lambda function """
def lambda_handler(event, context):
    return dispatch_lex_intent(event)