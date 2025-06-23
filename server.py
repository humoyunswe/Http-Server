import socket
import os

HOST = "localhost"
PORT = 4221
files_directory = ""


def create_response(status, content="", content_type="text/plain"):
    """
    Creates HTTP response from parts:
        - handle_home()
        - handle_echo()
        - handle_user_agent()
        - read_file()
        - write_file()
        - handle_files()
        - route_request()
        - handle_client()


        HTTP/1.1 200 OK             
        Content-Type: text/plain   
        Content-Length: 11          
                             
        Hello World  


        Like that will response from function.
    """
    if content:
        response = f"{status}Content-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n{content}"
    else:
        response = f"{status}\r\n"
    return response.encode()

    
def parse_request(request_text):
    """
    Parses HTTP request and returns comfy data
    """
    lines = request_text.split('\r\n')

    first_line = lines[0].split(' ')
    method = first_line[0]
    path = first_line[1]

    headers = {}
    for line in lines[1:]:
        if line == "":
            break
        if ":" in line:
            key, value = line.split(': ', 1)
            headers[key.lower()] = value
    body = ""
    
    try: 
        empty_line_index = lines.index("")
        if empty_line_index + 1 < len(lines):
            body = lines[empty_line_index + 1]
    except ValueError:
        pass

    return {
        'mehtod': method,
        'path': path,
        'headers': headers,
        'body': body
    }


def handle_home():
    """Main page /"""
    return create_response("HTTP/1.1 200 OK\r\n")


def handle_echo(path):
    """
    Echo function /echo/text
    """
    text = path.replace('/echo/', '')
    return create_response("HTTP/1.1 200 OK\r\n",text)


def handle_user_agent(headers):
    """
    Returns User-Agent header
    """
    user_agent = headers.get('user-agent', 'Unknown')
    return create_response("HTTP/1.1 200 OK\r\n", user_agent)


def read_file(filename):
    try:
        filepath = os.path.join(files_directory, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        return create_response("HTTP/1.1 200 OK\r\n", content, "application/octet-stream")
    except FileNotFoundError:
        return create_response("HTTP/1.1 404 Not Found\r\n",)
    

def write_file(filename, content):
    """
    Writes file into files_directory
    """
    try:
        if files_directory and not os.path.exists(files_directory):
            os.makedirs(files_directory)

        filepath = os.path.join(files_directory, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return create_response("HTTP/1.1 201 Created\r\n", content)
    except Exception as e:
        print(f"Error while writing file: {e}")
        return create_response("HTTP/1.1 250 Internal Server Error\r\n",)


def handle_files(method, path, body):
    """
    Processes requests into files /files/filename
    """
    filename = path.replace('/files/','')

    if method == 'GET':
        return read_file(filename)
    elif method == 'POST':
        return write_file(filename, body)
    else:
        return create_response("HTTP/1.1 405 Method Not Allowed\r\n")

def main():
    pass

if __name__ == "__main__":
    main()