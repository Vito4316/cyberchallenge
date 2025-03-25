import requests
from bs4 import BeautifulSoup
import re

def fetch_maze(session, url):
    """Fetch the maze HTML from the provided URL using the session and return the maze text."""
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    maze_pre = soup.find('pre')
    if not maze_pre:
        return None, "Maze not found in the response"
    maze_html = str(maze_pre).replace('<pre>', '').replace('</pre>', '')
    return maze_html, response.text

def parse_maze(maze_html):
    """Parse the ASCII maze from HTML and convert it to a graph representation."""
    lines = [line for line in maze_html.split('<br/>')]

    # Convert string to list
    line = list(lines[len(lines)-2])
    # Modify the character
    line[-1] = 'y'
    # Update the string in the list
    lines[len(lines)-2] = ''.join(line)

    for i in lines:
        print(i)

    # Adjusting the end position if necessary (specific to the server's maze format)
    if lines:
        last_line = list(lines[-1])
        if last_line[-1] == '#':
            last_line[-1] = 'y'
            lines[-1] = ''.join(last_line)

    # Find starting point (marked with 'x')
    start_pos = None
    for row_idx, line in enumerate(lines):
        col_idx = line.find('x')
        if col_idx != -1:
            start_pos = (row_idx, col_idx)
            break

    end_pos = None
    for row_idx, line in enumerate(lines):
        col_idx = line.find('y')
        if col_idx != -1:
            end_pos = (row_idx, col_idx)
            break

    # Create a 2D grid representation of the maze, replacing wall characters with '#'
    wall_chars = '╞═╦╠╩╬╣╗╝╚╔╡║╨╥┃┗┛┓┏━┻┳┣┫'
    grid = []
    for line in lines:
        row = []
        for char in line:
            row.append('#' if char in wall_chars else ' ')
        grid.append(row)

    # Build the graph
    graph = {}
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == ' ' or (row, col) == start_pos:
                neighbors = []
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < len(grid) and
                        0 <= new_col < len(grid[new_row]) and
                        (grid[new_row][new_col] == ' ' or (new_row, new_col) == start_pos)):
                        neighbors.append((new_row, new_col))
                graph[(row, col)] = neighbors

    return graph, start_pos, end_pos

def dijkstra(graph, start, end):
    """Implement Dijkstra's algorithm to find the shortest path from start to end."""
    import heapq
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    previous = {node: None for node in graph}

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_node == end:
            break
        if current_distance > distances[current_node]:
            continue
        for neighbor in graph[current_node]:
            distance = current_distance + 1
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous.get(current, None)

    path.reverse()
    return path if path and path[0] == start else []

def print_directions(path):
    """Convert the path to a sequence of directions (U, R, D, L)."""
    directions = []
    for i in range(1, len(path)):
        prev_row, prev_col = path[i-1]
        curr_row, curr_col = path[i]
        if curr_row < prev_row:
            directions.append('U')
        elif curr_row > prev_row:
            directions.append('D')
        elif curr_col < prev_col:
            directions.append('L')
        else:
            directions.append('R')
    return directions

def submit_move(session, url, direction):
    """Submit a move (U, R, D, L) to the server using the session and get the updated maze."""
    direction_map = {'U': 'Up', 'R': 'Right', 'D': 'Down', 'L': 'Left'}
    if direction not in direction_map:
        return None, "Invalid direction"
    data = {direction: direction_map[direction]}
    response = session.post(url, data=data, allow_redirects=True)
    soup = BeautifulSoup(response.text, 'html.parser')
    maze_pre = soup.find('pre')
    if not maze_pre:
        return None, "Maze not found in the response"
    maze_html = str(maze_pre).replace('<pre>', '').replace('</pre>', '')
    return maze_html, response.text

def solve_maze(url):
    """Main function to solve the maze."""
    session = requests.Session()
    print("Fetching initial maze...")
    maze_html, html = fetch_maze(session, url)
    if not maze_html:
        return "Failed to fetch maze"

    graph, start_pos, end_pos = parse_maze(maze_html)
    if not start_pos:
        return "Could not find start position in the maze."
    if not end_pos:
        return "Could not find a valid end position."

    # Check if end_pos is in the graph
    if end_pos not in graph:
        return f"End position {end_pos} is not a valid node in the graph."

    print("Calculating shortest path...")
    path = dijkstra(graph, start_pos, end_pos)
    if not path:
        return "No path found from start to end."

    directions = print_directions(path)
    return {
        "path": path,
        "directions": directions,
        "direction_sequence": ''.join(directions),
        "steps": len(directions),
        "start_pos": start_pos,
        "end_pos": end_pos
    }

if __name__ == "__main__":
    url = "http://130.192.5.212:8421/"

    with requests.Session() as session:  # Single session for all requests
        print("Starting maze solution...")
        responses = []

        # Initial request
        print("Fetching initial maze...")
        maze_html, initial_response = fetch_maze(session, url)
        responses.append(initial_response)

        # Solve based on initial state
        graph, start, end = parse_maze(maze_html)
        path = dijkstra(graph, start, end)
        directions = print_directions(path)

        # Submit each move using the same session
        for i, direction in enumerate(directions, 1):
            print(f"\nSubmitting move {i}/{len(directions)}: {direction}")
            _, response_text = submit_move(session, url, direction)
            responses.append(response_text)

            # Check for early success
            if 'ptm{' in response_text:
                print("Flag found in intermediate response!")
                break

        # Print all responses with numbering
        print("\n\n=== All Server Responses ===")
        for idx, resp in enumerate(responses):
            print(f"\nResponse {idx + 1}:\n{resp}")
            print("-" * 40)

        # Final flag check
        flag_match = re.search(r'ptm{.*?}', responses[-1])
        print("\nFinal result:", f"Flag: {flag_match.group()}" if flag_match else "No flag found")
