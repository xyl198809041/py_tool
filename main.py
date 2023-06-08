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

pack.tool.speak("根据搜索结果，你可以使用edge_tts库的rate和volume参数来调整声音响度12。例如，你可以使用以下代码来生成一个语音文件，其中文本是从1.txt文件中读取的，语音是zh-CN-YunxiNeural，速度是-4%，音量是+0%",is_OverWrite=True,spd=4)