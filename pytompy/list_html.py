import os
import socket
# import uasyncio as asyncio
import json

def get_first_match_in_second_column(file_path, target_value):
    data=[]
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) < 2:
                    continue  # Skip invalid lines (less than 2 columns)
                
                name = parts[0].strip()
                second_column_value = parts[1].strip()  # Second column value
                
                # Check if the second column matches the target value
                if second_column_value == str(target_value):  # Convert to string for comparison
                    values = [value.strip() for value in parts[1:]]
                    data.append({'name': name, 'values': values})
                    return data
                
        return None  # Return None if no match is found
    except OSError as e:
        print(f"Error reading file: {e}")
        return None



def get_data_from_file(file_path, n=10):
    data = []
    try:
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                if i >= n:
                    break  # Stop after n entries
                
                parts = line.strip().split(',')
                if len(parts) < 2:
                    continue  # Skip invalid lines
                
                name = parts[0].strip()
                values = [value.strip() for value in parts[1:]]
                data.append({
                    'name': name,
                    'values': values
                })
        return data
    except OSError as e:
        print(f"Error reading file: {e}")
        return None

def send_response(client, payload, status_code=200):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    client.sendall("Content-Length: {}\r\n".format(len(payload)))
    client.sendall("\r\n")
    
    if len(payload) > 0:
        client.sendall(payload)



def handle_root(client):
    data = get_data_from_file('configs/listnames.txt')  # Assuming the text file is placed at /textfile.txt
    data2 = get_first_match_in_second_column('configs/listnames.txt', 2)
    data = data+data2
    if data is None:
        return "<h1>Error reading data</h1>"    
    response_header = """
    <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px 12px; text-align: left; border: 1px solid #ddd; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        button { margin: 10px 0; padding: 10px; font-size: 16px; }
    </style>    
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Value 1</th>
                    <th>Value 2</th>
                    <th>Value 3</th>
                    <th>Value 4</th>
                    <th>Value 5</th>
                </tr>
            </thead>
            <tbody>
    """
    response_variable = ""

    for row in data:
        response_variable += f"<tr><td>{row['name']}</td>"
        for value in row['values']:
            response_variable += f"<td>{value}</td>"
        response_variable += "</tr>\n"
    
    response_footer = """
                    </tbody>
        </table>
    """
    send_response(client, response_header + response_variable + response_footer)

def start(port=80):
    import network
    import ure  
    addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]
    global server_socket
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)
    print('listening on', addr)
    while True:
        client, addr = server_socket.accept()
        client.settimeout(5.0)
        print('client connected from', addr)
        request = b""
        try:
            while not "\r\n\r\n" in request:
                request += client.recv(512)
        except OSError:
            pass
        print("Request is: {}".format(request))
        if "HTTP" not in request:
            # skip invalid requests
            client.close()
            continue
        url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request.decode('ascii')).group(1).rstrip("/")
        print("URL is {}".format(url))

        if url == "":
            handle_root(client)
        


start()




        