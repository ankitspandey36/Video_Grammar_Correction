import speech_recognition as sr
from gtts import gTTS
from parse import parse_silence_log
from get_duration import get_audio_duration
from speeed import change_audio_speed
from final import mute_video_and_add_audio
import os
from dotenv import load_dotenv
import streamlit as st
import tempfile
load_dotenv()


st.title("Video Grammar Improver")

# Upload video file
uploaded_file = st.file_uploader("Upload a video", type=["mp4"])

if uploaded_file is not None:
    # Save the uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_file.read())
        temp_video_path = temp_video.name

    # Display uploaded video
    st.video(temp_video_path)

    # Button to start the grammar improvement process
    if st.button("Improve Grammar"):
        st.write("Processing...")


        input_video = temp_video_path
        os.system(f"ffmpeg -i {input_video} -q:a 0 -map a extracted_audio.wav")
        os.system("ffmpeg -i extracted_audio.wav -af silencedetect=n=-30dB:d=0.5 -f null - 2> silence_log.txt")
        parsed_silences=parse_silence_log("silence_log.txt")
        parsed_speak=[]
        # parsed_speak.append((0,parsed_silences[0]["start"]))
        duration=get_audio_duration("extracted_audio.wav")
        for i in range(len(parsed_silences)-1):
            parsed_speak.append((parsed_silences[i]["end"],parsed_silences[i+1]["start"]))

        # parsed_speak.append((parsed_silences[-1]["end"],duration))  # try duration -0.1
        print("aparsed_speak : ",parsed_speak)
        texts=[]
        for i in parsed_speak:
            # extract_audio_part("extracted_audio.wav",str(i[0]),str(i[1]),"extracted_audio_part.wav")

            os.system(f"ffmpeg -i extracted_audio.wav -ss {i[0]} -to {i[1]} -c copy output_part.wav")
            try:
                r = sr.Recognizer()
                with sr.AudioFile('output_part.wav') as source:
                    audio = r.record(source)
                    text = r.recognize_google(audio)
                    texts.append(text)
                os.remove("output_part.wav")

            except:
                texts.append("")
                if os.path.exists("output_part.wav"):
                    os.remove("output_part.wav")
                continue
        os.remove("extracted_audio.wav")



        print(texts)
        import  google.generativeai as genai
        API_KEY = os.getenv("API_KEY")
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([ str(texts),"You are a english trainer. Please resolve gramatical errors for each element of the list. correct each element by understanding the overall context of what the person wants to say. don't do anything for empty strings and return the empty string as it is. If you feel any sentence is incomplete, complete it by adding few words. 'strictly don't keep multiple options for words or new words in parenthesis', instead add most relevant word. dont add so many words else it would be difficult to sync. The total number of items in the list should remain same. return the corrected python list. Only return the list "])
        # Get the response data from Gemini
        gemini_response = response.text
        pt=gemini_response[9:-4]
        print(pt)
        got_speaks=[]
        idx=0
        for i in eval(pt):
            print(i)
            if i!="":
                tts = gTTS(i, lang='en',tld='co.in')
                tts.save(f'new_audio{idx}.mp3')
                got_speaks.append(idx)
            idx+=1

        final_audios=[]
        for i in range(len(parsed_speak)):
            if i in got_speaks:
                # try:
                    print("duration :",float(parsed_speak[i][1])-float(parsed_speak[i][0]))
                    change_audio_speed(f'new_audio{i}.mp3',f'speeded_audio{i}.mp3',float(parsed_speak[i][1])-float(parsed_speak[i][0]))
                    os.remove(f'new_audio{i}.mp3')
                    final_audios.append((f'speeded_audio{i}.mp3',parsed_speak[i][0]))
                # except:
                #     final_audios.append((f'new_audio{i}.mp3',parsed_speak[i][0]))
            # else:
            #     os.remove(f'new_audio{i}.mp3')

        mute_video_and_add_audio(input_video,"output.mp4",final_audios)
        st.write("Corrected Video")
        st.video("output.mp4")
        for i in final_audios:
            os.remove(i[0])

        
    



