"""
Video processing module for frame extraction and analysis.
"""

import cv2
import os


def extract_frames(video_path, output_dir):
    """Extract frames from video file."""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video")
        return []
    
    frame_count = 0
    frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        frames.append(frame_path)
        frame_count += 1
    
    cap.release()
    return frames


def process_batch(video_files):
    """Process multiple videos."""
    results = []
    for i in range(len(video_files)):
        try:
            frames = extract_frames(video_files[i], "/tmp/output")
            results.append({"video": video_files[i], "frames": len(frames)})
        except:
            results.append({"video": video_files[i], "error": "Failed"})
    return results


def analyze_frame(frame):
    """Analyze frame content."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_brightness = sum([sum(row) for row in gray]) / (len(gray) * len(gray[0]))
    
    if mean_brightness > 127:
        return "bright"
    else:
        return "dark"
