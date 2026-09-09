import discord
import edge_tts
import asyncio
import os

class VoiceManager:
    def __init__(self):
        self.voice_client = None
        self.output_file = "response.mp3"

    async def join_channel(self, channel):
        """Joins a voice channel."""
        if self.voice_client and self.voice_client.is_connected():
            if self.voice_client.channel.id != channel.id:
                await self.voice_client.move_to(channel)
        else:
            self.voice_client = await channel.connect()

    async def leave_channel(self):
        """Leaves the current voice channel."""
        if self.voice_client and self.voice_client.is_connected():
            await self.voice_client.disconnect()
            self.voice_client = None

    async def speak(self, text):
        """Converts text to speech and plays it in the voice channel."""
        if not self.voice_client or not self.voice_client.is_connected():
            return False

        try:
            # Generate TTS file
            communicate = edge_tts.Communicate(text, "en-US-AndrewNeural")
            await communicate.save(self.output_file)

            # Play the audio
            if self.voice_client.is_playing():
                self.voice_client.stop()

            source = discord.FFmpegPCMAudio(self.output_file)
            self.voice_client.play(source)

            # Wait for audio to finish playing
            while self.voice_client.is_playing():
                await asyncio.sleep(1)
            
            return True
        except Exception as e:
            print(f"Voice error: {e}")
            return False
        finally:
            # Clean up the file if it exists
            if os.path.exists(self.output_file):
                try:
                    os.remove(self.output_file)
                except:
                    pass
