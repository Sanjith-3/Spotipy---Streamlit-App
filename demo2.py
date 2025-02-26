import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize face cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to perform real-time emotion detection
def detect_emotion(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        return "No face detected"  # No face detected

    # Take the first detected face for simplicity
    (x, y, w, h) = faces[0]
    
    # Extract face ROI for DeepFace
    face_roi = frame[y:y+h, x:x+w]
    
    try:
        # Use DeepFace.analyze instead of the model.predict approach
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
        
        # Extract the dominant emotion
        if isinstance(result, list):
            detected_emotion = result[0]['dominant_emotion']
        else:
            detected_emotion = result['dominant_emotion']
            
        return detected_emotion
    except Exception as e:
        return f"Error: {str(e)}"

# Function to recommend music based on emotion
def recommend_music(emotion):
    music_genres = {
        'angry': 'Metal',
        'disgust': 'Classical',
        'fear': 'Ambient',
        'happy': 'Pop',
        'sad': 'Blues',
        'surprise': 'EDM',
        'neutral': 'Instrumental',
        'pain': 'Rock'
    }
    return music_genres.get(emotion, 'Unknown')

# Initialize Spotipy client
client_id = 'adc3e6adf62847d1898ea6e6f0a35f3f'
client_secret = 'a32154e6a5084ca5a49f162643602954'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Streamlit app
st.set_page_config(page_title='AI Driven Music System', layout="wide")
st.title('AI Driven Music System')
st.title("1. Emotion Analysis")

# Open the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    st.error("Error: Unable to open the webcam.")
    st.stop()

# Checkbox to start and stop face detection
start_detection = st.checkbox("Start Face Detection")

if start_detection:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Perform real-time emotion detection
        detected_emotion = detect_emotion(frame)

        # Update valence based on detected emotion
        if detected_emotion in ['happy', 'surprise']:
            valence = 0.6
        elif detected_emotion in ['angry', 'sad']:
            valence = 0.4
        else:
            valence = 0.5

        # Display the webcam feed with emotion information
        st.image(frame, channels="BGR")
        st.text(f"Detected Emotion: {detected_emotion}")
        st.text(f"Updated Valence: {valence:.2f}")
        
        # Recommend music based on detected emotion
        genre = recommend_music(detected_emotion)
        st.write(f"Recommended Genre: {genre}")
    else:
        st.error("Failed to capture frame from webcam")

else:
    # Option to upload an image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        # Read the uploaded image
        file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)

        # Perform emotion detection
        detected_emotion = detect_emotion(image)
        
        # Display the uploaded image
        st.image(image, caption='Uploaded Image', width=500)

        # Highlight the detected emotion message
        st.info(f"Detected Emotion: **{detected_emotion}**")

        # Recommend music based on detected emotion
        genre = recommend_music(detected_emotion)
        st.info(f"Recommended Genre: {genre}")

# Release the video capture object when the app stops
if 'cap' in locals() and cap.isOpened():
    cap.release()

# Streamlit app for music recommendation
st.title('2. Suggesting Tracks From Spotify')

# Spotify API credentials
client_id = '1138a66b81e2490593ab49b4573a0c5f'
client_secret = 'c7d18d1f37c44bd891128790a2f1b982'

# Initialize Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Initialize session state for storing selected track details
if 'selected_track_details' not in st.session_state:
    st.session_state.selected_track_details = None

# Search for a track
search_query = st.text_input('Search For a Track')

if search_query:
    results = sp.search(q=search_query, type='track', limit=10)

    if results and results['tracks']['items']:
        st.subheader('Search Results')
        track_options = [f"{track['name']} by {track['artists'][0]['name']}" for track in results['tracks']['items']]
        selected_track = st.selectbox('Select a track', track_options)

        if selected_track:
            # Find the index of the selected track in the results
            track_index = track_options.index(selected_track)
            # Save the selected track details in session state
            st.session_state.selected_track_details = results['tracks']['items'][track_index]
            
            # Display selected track details
            st.subheader('Selected Track Details')
            st.write(f"Track: {st.session_state.selected_track_details['name']}")
            st.write(f"Artist: {st.session_state.selected_track_details['artists'][0]['name']}")
            st.write(f"Album: {st.session_state.selected_track_details['album']['name']}")
            st.image(st.session_state.selected_track_details['album']['images'][0]['url'], width=200)
            
            # Check if preview URL exists before playing
            if st.session_state.selected_track_details['preview_url']:
                st.audio(st.session_state.selected_track_details['preview_url'], format="audio/mp3")
            else:
                st.warning("No audio preview available for this track")

# Slider for adjusting audio features
st.title('3. Music Recommendation Based on Custom Audio Features')
st.header('Adjust Audio Features')

# Slider for Acousticness
st.subheader("Acousticness")
st.info("Acousticness measures the amount of acoustic sound in the track. Decreasing it may lead to more electronic or non-acoustic recommendations, while increasing it may result in more acoustic recommendations.")
acousticness = st.slider('Acousticness', 0.0, 1.0, 0.5, 0.01)

# Slider for Danceability
st.subheader("Danceability")
st.info("Danceability quantifies how suitable the track is for dancing. Higher values represent tracks that are more danceable.")
danceability = st.slider('Danceability', 0.0, 1.0, 0.5, 0.01)

# Slider for Energy
st.subheader("Energy")
st.info("Energy measures the intensity and activity in the music. Higher values indicate more energetic tracks, while lower values represent calmer tracks.")
energy = st.slider('Energy', 0.0, 1.0, 0.5, 0.01)

# Slider for Instrumentalness
st.subheader("Instrumentalness")
st.info("Instrumentalness assesses the presence of vocals in the track. Lower values suggest the presence of vocals, while higher values indicate instrumental tracks.")
instrumentalness = st.slider('Instrumentalness', 0.0, 1.0, 0.5, 0.01)

# Slider for Liveness
st.subheader("Liveness")
st.info("Liveness indicates the likelihood of a live audience in the track. Higher values suggest a live performance, while lower values imply a studio recording.")
liveness = st.slider('Liveness', 0.0, 1.0, 0.5, 0.01)

# Slider for Speechiness
st.subheader("Speechiness")
st.info("Speechiness quantifies the presence of spoken words in the track. Higher values indicate more speech-like audio, while lower values are more musical and instrumental.")
speechiness = st.slider('Speechiness', 0.0, 1.0, 0.5, 0.01)

# Slider for Valence
st.subheader("Valence")
st.info("Valence measures the overall positivity of the track. Higher values represent happier and more positive tracks, while lower values indicate sadder or more negative tracks.")
valence = st.slider('Valence', 0.0, 1.0, 0.5, 0.01)
# Button to generate recommendations
if st.button('Generate Similar Tracks'):
    # Make sure we have a selected track before generating recommendations
    if st.session_state.selected_track_details is None:
        st.warning("Please search and select a track first!")
    else:
        show_recommendations = True  # Flag to control whether to show recommendations
        try:
            # Use only widely recognized genres and a more focused approach
            target_audio_features = {
                'target_acousticness': acousticness,
                'target_danceability': danceability,
                'target_energy': energy,
                'target_instrumentalness': instrumentalness,
                'target_liveness': liveness,
                'target_speechiness': speechiness,
                'target_valence': valence
            }
            
            # Option 1: Try with track only (most specific)
            st.write("Attempting to find recommendations based on track...")
            try:
                recommended_tracks = sp.recommendations(
                    seed_tracks=[st.session_state.selected_track_details['id']], 
                    limit=5, 
                    **target_audio_features
                )
                if not recommended_tracks['tracks']:
                    raise Exception("No tracks returned")
            except Exception as e1:
                st.warning(f"Track-based recommendation failed: {str(e1)}")
                
                # Option 2: Try with artist only
                st.write("Attempting to find recommendations based on artist...")
                try:
                    artist_id = st.session_state.selected_track_details['artists'][0]['id']
                    recommended_tracks = sp.recommendations(
                        seed_artists=[artist_id],
                        limit=5, 
                        **target_audio_features
                    )
                    if not recommended_tracks['tracks']:
                        raise Exception("No tracks returned")
                except Exception as e2:
                    st.warning(f"Artist-based recommendation failed: {str(e2)}")
                    
                    # Option 3: Try with a general popular genre
                    st.write("Attempting to find recommendations based on general genres...")
                    try:
                        # Use popular genres that are likely to work
                        recommended_tracks = sp.recommendations(
                            seed_genres=['pop'],
                            limit=5, 
                            **target_audio_features
                        )
                        if not recommended_tracks['tracks']:
                            raise Exception("No tracks returned")
                    except Exception as e3:
                        st.error(f"All recommendation methods failed.")
                        st.info("Try searching for a more popular track or adjust the audio feature settings.")
                        show_recommendations = False  # Set flag to skip showing recommendations
            
            # Display recommendations if any method succeeded
            if show_recommendations:
                st.subheader('Recommended Tracks:')
                
                num_columns = 2  # Number of tracks per row
                num_tracks = len(recommended_tracks['tracks'])
                
                if num_tracks == 0:
                    st.warning("No recommendations found. Try adjusting the audio features or selecting a different track.")
                else:
                    num_rows = (num_tracks + num_columns - 1) // num_columns
                    
                    for row in range(num_rows):
                        cols = st.columns(num_columns)
                        for col in range(num_columns):
                            idx = row * num_columns + col
                            if idx < num_tracks:
                                rec_track = recommended_tracks['tracks'][idx]
                                with cols[col]:
                                    st.write(f"Track: {rec_track['name']}")
                                    st.write(f"Artist: {rec_track['artists'][0]['name']}")
                                    st.write(f"Album: {rec_track['album']['name']}")
                                    st.image(rec_track['album']['images'][0]['url'], width=200)
                                    st.write(f"Original URL: [Listen on Spotify]({rec_track['external_urls']['spotify']})")
                                    # Check if preview URL exists before playing
                                    if rec_track['preview_url']:
                                        st.audio(rec_track['preview_url'], format="audio/mp3")
                                    else:
                                        st.warning("No audio preview available for this track")
        
        except Exception as e:
            st.error(f"Error getting recommendations: {str(e)}")
            st.info("Try searching for a different track or adjusting your audio feature settings.")