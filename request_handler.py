from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from login.request import login_auth, register_user
from categories import create_category, get_categories
from models import Login
from posts import get_posts_by_id, get_post_details, get_all_posts, create_post


class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
        '''
        parses URL
        '''
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:

            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]

            return (resource, key, value)
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

            return (resource, id)

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
                                        status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_POST(self):
        """Handles POST requests to the server
        """
        # Set response code to 'Created'
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, _) = self.parse_url(
            self.path)  # pylint: disable=unbalanced-tuple-unpacking

        new_user = None
        new_category = None

        if resource == "login":
            user_login = login_auth(post_body['email'], post_body['password'])
            self.wfile.write(f"{user_login}".encode())

        if resource == "register":
            new_user = register_user(post_body)
            self.wfile.write(f"{new_user}".encode())

        if resource == "categories":
            new_category = create_category(post_body)
            self.wfile.write(f"{new_category}".encode())
        if resource == "posts":
            create_post(post_body)

    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "posts":
                if id is not None:
                    response = f"{get_post_details(id)}"
                else:
                    response = f"{get_all_posts()}"

            if resource == "categories":
                response = f"{get_categories()}"

            if resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            (resource, key, value) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "user" and resource == "posts":
                response = f"{get_posts_by_id(value)}"

        self.wfile.write(response.encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
