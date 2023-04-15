import edge_tts
import asyncio

# from edge_tts import VoicesManager
#
# voices = asyncio.run(VoicesManager.create())
# voice = voices.find(Gender="Male", Language="zh")
# # Also supports Locales
# # voice = voices.find(Gender="Female", Locale="es-AR")
#
# communicate = edge_tts.Communicate('阳阳加油做作业', voice[2]['Name'])
# asyncio.run(communicate.save('temp/222.mp3'))
import pack.tool

pack.tool.speak("开水开了",is_OverWrite=True)