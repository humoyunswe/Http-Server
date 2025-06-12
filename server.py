import socket

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



def main():
    pass

if __name__ == "__main__":
    main()