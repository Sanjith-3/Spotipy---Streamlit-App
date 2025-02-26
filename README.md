# 🎵 AI-Driven Music Recommendation System 🎵

## 📖 Overview

The AI-Driven Music Recommendation System is an innovative application that combines emotion detection technology with Spotify's extensive music library to provide personalized music recommendations based on your emotional state and musical preferences.

> ⚠️ **Note:** This project is currently affected by changes in the Spotify API due to depreciation of the Get Recommendation Function


## ✨ Features

### 😀 Facial Emotion Analysis
- Real-time emotion detection using your webcam
- Upload images for emotion analysis
- Detects emotions including: happy, sad, angry, surprise, neutral, and more
- Powered by DeepFace AI technology

### 🎧 Spotify Music Search
- Search Spotify's vast music library for your favorite tracks
- Preview songs directly in the application
- View detailed track information including artist and album details

### 🎹 Customizable Audio Features
- Fine-tune music recommendations with adjustable audio parameters
- Customize:
  - 🔊 Acousticness (acoustic vs. electronic sound)
  - 💃 Danceability (how suitable a track is for dancing)
  - ⚡ Energy (intensity and activity level)
  - 🎸 Instrumentalness (presence of vocals vs. instruments)
  - 🎤 Liveness (studio recording vs. live performance feel)
  - 🗣️ Speechiness (spoken words vs. musical content)
  - 😊 Valence (musical positivity/mood)
  - 
## 🚀 How It Works

1. **Emotion Detection**:
   - The system uses your webcam to analyze your facial expressions in real-time
   - The AI detects your current emotional state (happy, sad, angry, etc.)
   - Initial music genre recommendations are provided based on your emotion

2. **Music Selection**:
   - Search for a track that matches your current mood or preference
   - The system connects to Spotify to fetch results from their extensive library
   - Select a track from the search results to use as a reference point
   - Preview the selected track with an audio sample

3. **Personalization**:
   - Adjust audio feature sliders to fine-tune your musical preferences
   - Each parameter influences different aspects of the music recommendations
   - The emotion detection automatically influences the valence parameter

4. **Recommendation Generation**:
   - The system uses your selected track, detected emotion, and adjusted parameters
   - It generates a curated list of similar tracks that match your current emotional state and preferences
   - Each recommendation includes track details and preview options

## 💻 Technical Stack

- **Frontend & Interface**: Streamlit
- **Emotion Analysis**: OpenCV, DeepFace
- **Music API**: Spotify API through Spotipy library
- **Programming Language**: Python

## 🔧 Technical Details

### Emotion Detection Pipeline

1. **Face Detection**:
   - Uses OpenCV's Haar Cascade classifier to detect faces in images/video frames
   - Each detected face is extracted as a Region of Interest (ROI)

2. **Emotion Analysis**:
   - The DeepFace library processes the extracted face ROI
   - DeepFace employs a pre-trained CNN (Convolutional Neural Network) that was trained on facial emotion datasets
   - Returns the dominant emotion from categories: happy, sad, angry, surprise, fear, disgust, neutral

3. **Emotion-to-Genre Mapping**:
   - Detected emotions are mapped to music genres through a predefined dictionary
   - Example mappings:
     - Happy → Pop
     - Sad → Blues
     - Angry → Metal
     - Neutral → Instrumental

### Spotify Integration

1. **Authentication**:
   - Uses Spotipy library to handle OAuth2 authentication with Spotify API
   - Implements Client Credentials Flow for application-level access

2. **Search Functionality**:
   - Leverages Spotify's search endpoint to query tracks by name
   - Results are limited to 10 tracks per search for better UX
   - Track data includes name, artist, album, preview URL, and album artwork

3. **Audio Features Extraction**:
   - Each track in Spotify has audio features quantified on a 0.0-1.0 scale
   - These features describe the track's acoustic characteristics and are used to find similar music

### Recommendation System

1. **Multi-source Input Processing**:
   - Facial emotion → influences valence parameter
   - User selected track → provides seed track ID for recommendations
   - User adjusted sliders → provides target audio features

2. **Fallback Strategy**:
   - Primary: Seed track-based recommendations
   - Secondary: Artist-based recommendations (if track-based fails)
   - Tertiary: Genre-based recommendations (if artist-based fails)

3. **Response Handling**:
   - Processes recommendation results from Spotify API
   - Formats and displays track information in a grid layout
   - Handles potential API errors with graceful degradation

### Streamlit Interface

1. **Interactive Components**:
   - Real-time webcam feed with OpenCV integration
   - File uploader for image analysis
   - Search box for querying Spotify
   - Interactive sliders for audio feature adjustment

2. **State Management**:
   - Uses Streamlit's session state to persist selected track details
   - Maintains context between different sections of the application

## 🔮 Future Enhancements

- **Playlist Creation**: Save your recommended tracks as Spotify playlists
- **Mood Tracking**: Track your emotional states over time with visual reports
- **Group Recommendations**: Generate recommendations for multiple users/emotions
- **Voice Commands**: Control the application using voice instructions
- **Mobile App**: Dedicated mobile application for on-the-go recommendations

## 📋 Requirements

- Python 3.7+
- Webcam for real-time emotion detection
- Spotify account (free account works)
- Internet connection for API access
