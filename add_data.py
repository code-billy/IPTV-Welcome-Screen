import pandas as pd

# Create the data for all rooms
rooms = [str(num).zfill(3) for num in range(101, 105)] + \
        [str(num).zfill(3) for num in range(201, 209)] + \
        [str(num).zfill(3) for num in range(301, 309)] + \
        [str(num).zfill(3) for num in range(401, 409)]

# Current guest data
guest_data = {
    '101': {'name': 'John Doe', 'check_in': '2025-02-18', 'check_out': '2025-02-18'},
    '102': {'name': 'Alice Smith', 'check_in': '2025-02-19', 'check_out': '2025-02-19'},
    '103': {'name': 'Billy Brightson', 'check_in': '2025-03-26', 'check_out': '2025-03-28'},
    '104': {'name': 'Alan Gard', 'check_in': '2025-03-14', 'check_out': '2025-03-22'}
}

# Create the full data list
data = []
for room in rooms:
    if room in guest_data:
        guest = guest_data[room]
        data.append({
            'room': room,
            'name': guest['name'],
            'check_in': guest['check_in'],
            'check_out': guest['check_out']
        })
    else:
        data.append({
            'room': room,
            'name': '',
            'check_in': '',
            'check_out': ''
        })

# Create DataFrame and save to Excel
df = pd.DataFrame(data)
df.to_excel('guests.xlsx', index=False)
print("Data added successfully") 