from deepface import DeepFace

def detect_expression(frame):
    try:
        result = DeepFace.analyze(
            frame,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="skip"
        )

        if isinstance(result, list):
            result = result[0]

        emotion = result["dominant_emotion"]
        confidence = result["emotion"][emotion]

        return emotion.capitalize(), confidence

    except Exception:
        return "Unknown", 0