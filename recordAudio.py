import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav



class audioRecorder():
    def __init__(self):
        # Initialize the sample rate
        self.fs = 44100  # Sample rate in Hz
        self.recording = False

    def record_audio(self):
        # Import the necessary modules
        import sounddevice as sd  # For audio input/output
        import numpy as np  # For numerical computations
        from scipy.io.wavfile import write as wav_write  # For writing WAV files

        # Initialize an empty buffer to store the recorded audio
        buffer = []

        # Define a function to convert amplitude to decibels
        def amp_to_db(amp):
            return 20 * np.log10(amp)

        # Define a function to convert decibels to amplitude
        def db_to_amp(db):
            return 10 ** (db / 20)

        # Set the desired threshold in decibels
        desired_db = 30
        # Convert the desired threshold to amplitude
        threshold = db_to_amp(desired_db)

        # Define a callback function to process the audio data
        def callback(indata, frames, time, status):
            # Calculate the volume of the current audio frame
            volume_norm = np.linalg.norm(indata) * 100

            # If the volume is below the threshold and the buffer has at least 100 frames, stop the recording
            if volume_norm < threshold and len(buffer) > 100:
                print("Threshold reached, stopping recording")
                raise sd.CallbackAbort  # Abort the callback to stop the recording

            # Append the current audio frame to the buffer
            buffer.append(indata.copy())

        # Set the chunk size for the audio input stream
        chunksize = 1024

        # Open an input stream with the specified callback function and parameters
        with sd.InputStream(callback=callback, channels=2, samplerate=self.fs, blocksize=chunksize) as stream:
            self.recording = True
            while self.recording:
                # Sleep for 100 milliseconds to allow other threads to run
                sd.sleep(100)

        # After the recording has stopped, save the audio to a WAV file
        print("Saving Audio")
        # Concatenate the audio frames in the buffer into a single array
        buffer = np.concatenate(buffer, axis=0)
        # Write the audio array to a WAV file
        wav_write('output.wav', self.fs, buffer)

        # Return the recorded audio
        return buffer

    def stop_recording(self):
        self.recording = False




"""import numpy as np

def amplitude_to_db(amplitude):
    
    #Converts amplitude to decibel (dB) level.

    #Args:
    #    amplitude (float): The amplitude of the soundwave.

    #Returns:
    #    float: Decibel level.
   
    reference_intensity = 10**(-12)  # Threshold of human hearing (W/m^2)
    intensity = (amplitude**2) / 2  # Convert amplitude to intensity
    db = 10 * np.log10(intensity / reference_intensity)
    return db

# Example usage:
recorded_amplitude = 0.1  # Replace with your recorded amplitude
decibel_level = amplitude_to_db(recorded_amplitude)
print(f"Decibel level: {decibel_level:.2f} dB")"""






'''

        # Set the desired threshold in decibels (a measure of sound intensity)
        desired_db = 30
        # Convert the desired threshold from decibels to amplitude (linear scale)
        threshold = db_to_amp(desired_db)

        # Define a callback function to process incoming audio data
        def callback(indata, frames, time, status):
            # Calculate the root mean square (RMS) volume of the current audio frame 
            volume_norm = np.linalg.norm(indata) * 100

            # If the volume falls below the threshold and enough audio has been captured, stop recording
            if volume_norm < threshold and len(buffer) > 100:
                print("Threshold reached, stopping recording")
                raise sd.CallbackAbort  # Signal to the audio stream to stop

            # Add the current audio frame to the buffer for later saving
            buffer.append(indata.copy())
'''






'''
class audioRecorder():
    def __init__(self):
        self.fs = 44100
        #self.duration = 15  # seconds

    def record_audio(self):
        import sounddevice as sd
        import numpy as np
        from scipy.io import wavfile

        buffer = []

        def amp_to_db(amp):
            return 20 * np.log10(amp)

        def db_to_amp(db):
            return 10 ** (db / 20)

        desired_db = 0.9
        threshold = db_to_amp(desired_db)

        def callback(indata, frames, time, status):
            volume_norm = np.linalg.norm(indata) * 100
            if volume_norm < threshold and len(buffer) > 100:
                print("Threshold reached, stopping recording")
                raise sd.CallbackAbort
            buffer.append(indata.copy())

        chunksize = 1024
        with sd.InputStream(callback=callback, channels=2, samplerate=self.fs, blocksize=chunksize) as stream:
            while True:
                sd.sleep(100)

        print("Saving Audio")
        buffer = np.concatenate(buffer, axis=0)
        wavfile.write('output.wav', self.fs, buffer)
        return buffer
        '''






































'''
class audioRecorder():
    def __init__(self):
        super().__init__()
        self.fs=44100
        self.duration = 15 # seconds

    def record_audio(self):
        #print("record_audio() started")
        #fs = 44100
        #duration = 10  # seconds
        #print("duration set")

        buffer = []

        def amp_to_db(amp):
            return 20 * np.log10(amp)

        def db_to_amp(db):
            return 10 ** (db / 20)

        desired_db = 0.9
        threshold = db_to_amp(desired_db)
        #print(threshold)

        def callback(indata, frames, time, status):
            volume_norm = np.linalg.norm(indata) * 100
            #print(volume_norm)
            #print(desired_db)
            # print("| " + "-" + str(volume_norm)) #+ "#" * int(volume_norm)
            #self.duration += 1

            #while volume_norm > desired_db and len(buffer) > 50:
            #    pass
            #else:
            #    print("Threshhold reached, stopping recording")
            #    raise sd.CallbackAbort

            if volume_norm < desired_db and len(buffer) > 100:
                print("Threshhold reached, stopping recording")
                #update_ui()
                raise sd.CallbackAbort
            elif volume_norm > desired_db:
                #Continue recording
                pass

            buffer.append(indata.copy())

        chunksize = 1024
        with sd.InputStream(callback=callback, channels=2, samplerate=self.fs, blocksize=chunksize) as stream:
            sd.sleep(int(self.duration * 1000))
            print(int(self.duration * 1000))

           

        print("Saving Audio")
        buffer = np.concatenate(buffer, axis=0)
        wav.write('output.wav', self.fs, buffer)
        return buffer
        '''


'''
           for i in range(0, int(fs/chunksize * duration)):
               buffer[i*stream.chunksize:(i+1)*stream.chunksize] = data
           #sd.sleep(int(duration * 1000))
           '''






'''
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    print("Recording Audio...")
    sd.wait()
    print("Audio recording complete, Play Audio")
    sd.play(myrecording, fs)
    sd.wait()
    print("Play Audio Complete")
    print("Saving Audio")
    # Save as WAV file
    wav.write('output.wav', fs, myrecording)
    return myrecording'''