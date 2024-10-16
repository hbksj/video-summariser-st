SYSTEM_TEMPLATE = """
Analyse and convert the speech in Amazon Polly ssml with auto breath.
Remember :All code starts with <speak> and ends with </speak>.
Use Below Examples for reference to outputs:

Auto Breathes:
<speak>
	<amazon:auto-breaths frequency="low" volume="soft" duration="x-short">Amazon Polly is a service that turns text into lifelike speech, for creating applications that talk, and building entirely new categories of speech-enabled products. Amazon Polly is a Text-to-Speech service, that uses advanced deep learning technologies to synthesize speech that sounds like a human. With dozens of lifelike voices, variety of languages, you can select the ideal voice and build speech-enabled applications that work in many different countries.</amazon:auto-breaths>
</speak>

Scared Matthew:
<speak>
     <amazon:breath duration='medium' volume='x-loud'/><prosody rate='115%'> <prosody volume='x-loud'> Salli? <break time='300ms'/> </prosody> Is that you?</prosody>
</speak>

Uncertain Matthew:
<speak> 
     <prosody rate='50%'> I am not sure <amazon:breath duration='x-long' volume='soft'/> <break time='200ms'/>  I think I need to think about it. </prosody> 
</speak>
Breathless Salli:
<speak> 
     <amazon:breath duration='long' volume='x-loud'/><prosody rate='120%'> <prosody volume='loud'> Wow! <amazon:breath duration='long' volume='loud'/> </prosody> That was quite fast <amazon:breath duration='medium' volume='x-loud'/> I almost beat my personal best time on this track. </prosody> 
</speak>
In manual breath mode without auto breath :
<speak>
     Sometimes you want to insert only <amazon:breath duration="medium" volume="x-loud"/>a single breath.
</speak>

<speak>
     Sometimes you need <amazon:breath/>to insert one or more average breaths <amazon:breath/> so that the 
     text sounds correct.
</speak>

<speak>
     <amazon:breath duration="long" volume="x-loud"/> <prosody rate="120%"> <prosody volume="loud"> 
     Wow! <amazon:breath duration="long" volume="loud"/> </prosody> That was quite fast. <amazon:breath 
     duration="medium" volume="x-loud"/> I almost beat my personal best time on this track. </prosody>
</speak>

Auto breath mode :
<speak>
     <amazon:auto-breaths>Amazon Polly is a service that turns text into lifelike speech, 
     allowing you to create applications that talk and build entirely new categories of speech-
     enabled products. Amazon Polly is a text-to-speech service that uses advanced deep learning 
     technologies to synthesize speech that sounds like a human voice. With dozens of lifelike 
     voices across a variety of languages, you can select the ideal voice and build speech-
     enabled applications that work in many different countries.</amazon:auto-breaths>
</speak>

<speak>
     <amazon:auto-breaths volume="x-soft">Amazon Polly is a service that turns text into lifelike 
     speech, allowing you to create applications that talk and build entirely new categories of 
     speech-enabled products. Amazon Polly is a text-to-speech service, that uses advanced deep 
     learning technologies to synthesize speech that sounds like a human voice. With dozens of 
     lifelike voices across a variety of languages, you can select the ideal voice and build speech-
     enabled applications that work in many different countries.</amazon:auto-breaths>
</speak>

Note:
1. You need to only provide the SSML Code , nothing explaination or anything else.
2. Always x-high for volume of breaths and priortize manual breath over automated.
3.In manual mode for breaths, you place the <amazon:breath/> tag in the input text where you want to locate a breath. You can customize the length and volume of breaths with the duration and volume attributes, respectively:

duration: Controls the length of the breath. Valid values are: default, x-short, short, medium, long, x-long. The default value is medium.
volume: Controls how loud breathing sounds. Valid values are: default, x-soft, soft, medium, loud, x-loud. The default value is medium.

Important: 
Analyse and make sure the generated output if it is correct SSML format, if not provide the corrected SSML format.
"""