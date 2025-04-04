from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configure Excel file path
EXCEL_FILE = 'guests.xlsx'

# Create Excel file if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['room', 'name', 'check_in', 'check_out'])
    df.to_excel(EXCEL_FILE, index=False)

def read_guests():
    try:
        logger.debug(f"Reading Excel file from {os.path.abspath(EXCEL_FILE)}")
        df = pd.read_excel(EXCEL_FILE)
        logger.debug(f"Successfully read {len(df)} rows from Excel")
        return df
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        return pd.DataFrame(columns=['room', 'name', 'check_in', 'check_out'])

def write_guests(df):
    try:
        logger.debug(f"Writing {len(df)} rows to Excel file")
        df.to_excel(EXCEL_FILE, index=False)
        logger.debug("Successfully wrote to Excel file")
        return True
    except Exception as e:
        logger.error(f"Error writing to Excel file: {e}")
        return False

@app.route('/api/guests', methods=['GET'])
def get_guests():
    logger.debug("GET /api/guests called")
    df = read_guests()
    # Replace NaN values with empty strings
    df = df.fillna('')
    # Sort by room number
    df['room'] = df['room'].astype(str)
    df = df.sort_values('room')
    result = df.to_dict('records')
    logger.debug(f"Returning {len(result)} guests")
    return jsonify(result)

@app.route('/api/guest/<room>', methods=['GET'])
def get_guest(room):
    df = read_guests()
    # Replace NaN values with empty strings
    df = df.fillna('')
    df['room'] = df['room'].astype(str)
    guest = df[df['room'] == str(room)]
    if len(guest) == 0:
        return jsonify({'error': 'Guest not found'}), 404
    return jsonify(guest.iloc[0].to_dict())

@app.route('/api/guest', methods=['POST'])
def add_guest():
    logger.debug("POST /api/guest called")
    data = request.json
    logger.debug(f"Received data: {data}")
    df = read_guests()
    
    # Check if room is already occupied
    if len(df[df['room'].astype(str) == str(data['room'])]) > 0:
        logger.debug(f"Room {data['room']} is already occupied")
        return jsonify({'error': 'Room already occupied'}), 400
    
    # Add new guest
    new_guest = pd.DataFrame([{
        'room': data['room'],
        'name': data['name'],
        'check_in': data['check_in'],
        'check_out': data['check_out']
    }])
    
    df = pd.concat([df, new_guest], ignore_index=True)
    
    if write_guests(df):
        logger.debug("Successfully added new guest")
        return jsonify({'message': 'Guest added successfully'})
    logger.error("Failed to add guest")
    return jsonify({'error': 'Failed to add guest'}), 500

@app.route('/api/guest/<room>', methods=['PUT'])
def update_guest(room):
    data = request.json
    df = read_guests()
    
    # Update guest information
    mask = df['room'].astype(str) == str(room)
    if not any(mask):
        return jsonify({'error': 'Guest not found'}), 404
    
    df.loc[mask, 'name'] = data['name']
    df.loc[mask, 'check_in'] = data['check_in']
    df.loc[mask, 'check_out'] = data['check_out']
    
    if write_guests(df):
        return jsonify({'message': 'Guest updated successfully'})
    return jsonify({'error': 'Failed to update guest'}), 500

@app.route('/api/guest/<room>', methods=['DELETE'])
def delete_guest(room):
    df = read_guests()
    
    # Delete guest
    mask = df['room'].astype(str) == str(room)
    if not any(mask):
        return jsonify({'error': 'Guest not found'}), 404
    
    df = df[~mask]
    
    if write_guests(df):
        return jsonify({'message': 'Guest deleted successfully'})
    return jsonify({'error': 'Failed to delete guest'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 