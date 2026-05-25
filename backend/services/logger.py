from database.supabase_client import supabase

def log_gesture(gesture):

    data = {
        "gesture": gesture
    }

    supabase.table("gesture_logs").insert(data).execute()


def log_speech(text):

    data = {
        "speech_text": text
    }

    supabase.table("audio_logs").insert(data).execute()


def log_translation(input_text, output_text):

    data = {
        "input_text": input_text,
        "output_text": output_text
    }

    supabase.table("translation_logs").insert(data).execute()