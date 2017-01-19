
import os
import json
import sys, traceback

from porper.models.connection import mysql_connection
from porper.controllers.token_controller import TokenController
from porper.controllers.role_controller import RoleController
from porper.controllers.user_controller import UserController
from porper.controllers.invited_user_controller import InvitedUserController
from porper.controllers.github_auth_controller import GithubAuthController
from porper.controllers.google_auth_controller import GoogleAuthController
from porper.controllers.permission_controller import PermissionController

ALLOWED_RESOURCES = (
    'role',
    'user',
    'invited_user',
    'permission'
)

def handler(event, context):

    paths = event['path'].split('/')
    path = paths[len(paths)-1]
    method = event['httpMethod']
    headers = event.get('headers')
    query_params = event.get('queryStringParameters')
    if query_params is None:
        query_params = {}
    post_data = {}
    if event.get('body'):
        post_data = json.loads(event.get('body'))

    connection = None
    try:
        connection = mysql_connection()
        print connection

        if path == 'auth' and method == 'POST':
            ret = authenticate(post_data, connection)
            print ret
            if not ret:
                return send_failure_response({'error': 'unauthorized'}, 401)
            if not ret.get('access_token'):
                return send_failure_response({'error': 'unauthorized'}, 401)
            else:
                connection.commit()
                return send_success_response(ret)

        # validate the given access_token, first
        ret = validate(headers.get('access_token'), connection)
        print ret
        if not ret:
            return send_failure_response({'error': 'not permitted'}, 403)
        access_token = ret.get('access_token')
        if not access_token:
            return send_failure_response({'error': 'not permitted'}, 403)

        controller = globals()['%sController' % path.title().replace('_', '')](connection)
        if method == 'GET':
            ret = controller.find_all(access_token, query_params)
        elif method == 'POST':
            ret = controller.create(access_token, post_data)
        elif method == 'PUT':
            ret = controller.update(access_token, post_data)
        elif method == 'DELETE':
            ret = controller.delete(access_token, post_data)
        else:
            return send_failure_response({'error': 'not permitted'}, 403)
        print ret
        connection.commit()
        return send_success_response(ret)
    except Exception, ex:
        traceback.print_exc(file=sys.stdout)
        if connection:  connection.rollback()
        return send_failure_response({'error': '%s' % ex}, 500)
    finally:
        if connection:  connection.close()


def authenticate(post_data, connection):
    try:
        id_token = post_data.get('id_token')
        code = post_data.get('code')
        state = post_data.get('state')
        redirect_uri = post_data.get('redirect_uri')
        provider = post_data['provider']
        print 'AuthController : post_data = %s' % post_data
        controller = globals()['%sAuthController' % provider.title().replace('_', '')](connection)
        if provider == 'google':
            return controller.authenticate(id_token)
        elif provider == 'github':
            return controller.authenticate(code, state, redirect_uri)
        raise Exception("Not supported provider, %s" % provider)
    except Exception, ex:
        return None


def validate(access_token, connection):
    try:
        print 'access_token = %s' % access_token
        token_controller = TokenController(connection)
        return token_controller.find(access_token)[0]
    except Exception, ex:
        return None


def send_not_permitted_method_response(path, method):
  response_body = {"error": "not permitted method %s in %s" % (method, path)}
  status_code = 404
  return send_response(response_body, status_code)


def sendNotFoundResponse(path, method):
  response_body = {error: "invalid path " + path}
  status_code = 404
  return send_response(response_body, status_code)


def send_success_response(ret_vaule):
  response_body = ret_vaule
  status_code = 200
  return send_response(response_body, status_code)


def send_failure_response(err, status_code):
  response_body = err
  return send_response(response_body, status_code)


def send_response(response_body, status_code):
  response = {
      'statusCode': status_code,
      'headers': { "Access-Control-Allow-Origin": "*" },
      'body': json.dumps(response_body)
  }
  print "response: %s" % response
  return response
