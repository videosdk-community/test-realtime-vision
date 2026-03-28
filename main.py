from videosdk.agents import AgentSession, WorkerJob, RoomOptions, JobContext, Agent, Pipeline
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler()])
class VisionAgent(Agent):  
    def __init__(self):  
        super().__init__(  
            instructions="You are a vision-enabled AI agent. Describe what you see in the video feed and respond to questions about visual content."  
        )  
  
    async def on_enter(self) -> None:  
        """Called when the agent session starts"""  
        await self.session.say("Hi! I'm your vision agent. Show me something and I'll describe what I see!")  
  
    async def on_exit(self) -> None:  
        """Called when the agent session ends"""  
        await self.session.say("Goodbye! Thanks for testing vision functionality with me.")  
  
async def start_session(context: JobContext):  
    # Initialize Gemini with vision capabilities  
    model = GeminiRealtime(  
        model="gemini-3.1-flash-live-preview",  
        config=GeminiLiveConfig(  
            voice="Leda",  
            response_modalities=["AUDIO"]  
        )  
    )  
  
    # Create real-time pipeline with vision support  
    pipeline = Pipeline(llm=model)  
      
    # Create agent session  
    session = AgentSession(  
        agent=VisionAgent(),  
        pipeline=pipeline  
    )  
  
    await session.start(wait_for_participant=True, run_until_shutdown=True)
  
def make_context() -> JobContext:  
    room_options = RoomOptions(  
        room_id="<room_id>",  
        name="Vision Test Agent",  
        playground=True,  
        vision=True,  
        recording=False  
    )  
      
    return JobContext(room_options=room_options)  
  
if __name__ == "__main__":  
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)  
    job.start()