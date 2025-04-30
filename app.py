from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# FIFO Algorithm
def fifo_algorithm(pages, frame_count):
    frames = []
    faults = []
    page_faults = 0
    page_hits = 0
    current_frames = []

    for i, page in enumerate(pages):
        if page not in current_frames:
            page_faults += 1
            faults.append(i)

            if len(current_frames) < frame_count:
                current_frames.append(page)
            else:
                current_frames.pop(0)
                current_frames.append(page)
        else:
            page_hits += 1

        frames.append(current_frames.copy())

    return {
        "frames": frames,
        "faults": faults,
        "page_faults": page_faults,
        "page_hits": page_hits
    }

# Optimal Algorithm
def optimal_algorithm(pages, frame_count):
    frames = []
    faults = []
    page_faults = 0
    page_hits = 0
    current_frames = []

    for i, page in enumerate(pages):
        if page not in current_frames:
            page_faults += 1
            faults.append(i)

            if len(current_frames) < frame_count:
                current_frames.append(page)
            else:
                farthest_use = -1
                to_replace = -1

                for j, frame_page in enumerate(current_frames):
                    try:
                        next_use = pages[i+1:].index(frame_page) + i + 1
                    except ValueError:
                        to_replace = j
                        break

                    if next_use > farthest_use:
                        farthest_use = next_use
                        to_replace = j

                current_frames[to_replace] = page
        else:
            page_hits += 1

        frames.append(current_frames.copy())

    return {
        "frames": frames,
        "faults": faults,
        "page_faults": page_faults,
        "page_hits": page_hits
    }

# LRU Algorithm
def lru_algorithm(pages, frame_count):
    frames = []
    faults = []
    page_faults = 0
    page_hits = 0
    current_frames = []
    last_used = {}

    for i, page in enumerate(pages):
        last_used[page] = i

        if page not in current_frames:
            page_faults += 1
            faults.append(i)

            if len(current_frames) < frame_count:
                current_frames.append(page)
            else:
                lru_page = min(current_frames, key=lambda p: last_used[p])
                current_frames.remove(lru_page)
                current_frames.append(page)
        else:
            page_hits += 1

        frames.append(current_frames.copy())

    return {
        "frames": frames,
        "faults": faults,
        "page_faults": page_faults,
        "page_hits": page_hits
    }

@app.route('/')
def index():
    return render_template('index.html')  # You must create index.html in the templates folder

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    reference_string = data['reference_string']
    algorithm_type = data.get('algorithm_type', 'all')

    # Support both comma and space separated input
    pages = [int(x.strip()) for x in reference_string.replace(',', ' ').split() if x.strip()]
    frame_count = int(data['frame_count'])

    results = {}

    if algorithm_type == 'fifo' or algorithm_type == 'all':
        results['fifo'] = fifo_algorithm(pages, frame_count)
    if algorithm_type == 'optimal' or algorithm_type == 'all':
        results['optimal'] = optimal_algorithm(pages, frame_count)
    if algorithm_type == 'lru' or algorithm_type == 'all':
        results['lru'] = lru_algorithm(pages, frame_count)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
