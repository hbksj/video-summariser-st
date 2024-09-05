
SUMMARIZER_PROMPT="""
Summarize the below content input on the below guidelines:
- The minimum word count of the summary should strictly be {min_word_length} words. 
- The maximum word count of the summary should strictly be {max_word_length} words.
- Show the number of words at the end of summary.

Input :  {input}

Also detect the language of the transcript and let the user know the language.

Also provide summary in below language if language is not empty else provide in english.

Language : {language}

Note: 
- Dont let the user know what input content you are using.
- Only the summary part should be in the selected language , the other information should remain in english.
"""