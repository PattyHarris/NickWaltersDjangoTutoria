# Uncomment when testing
# from django.http import HttpResponse

from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

# I changed this fron "translate" to this function name
# so as not to be confused with the request page name.


def handleSubmit(request):

    # print(request.GET['about'])

    if 'about' in request.GET:
        return render(request, "about.html")

    original = request.GET["originalText"].lower()
    translation = ""

    for word in original.split():
        if word[0] in ['a', 'e', 'i', 'o', 'u']:
            # The first letter is a vowel
            translation += word
            translation += "yay "
        else:
            # Handle consonants - here you're supposed to place all letters
            # before the initial vowel to the end of the word sequence
            # followed by 'ay' - Nick uses the first letter only.
            lastBit = word[0]
            newWord = word[1:]

            newWordIndex = 0
            while newWordIndex < len(newWord):

                if newWord[newWordIndex] in ['a', 'e', 'i', 'o', 'u']:
                    # Take the rest of the word beginning at index and add it
                    translation += newWord[newWordIndex:]

                    # Add on the constonants string
                    translation += lastBit

                    # Add on "ay"
                    translation += "ay "
                    break
                else:
                    lastBit += newWord[newWordIndex]
                    newWordIndex += 1

    # For testing - uncomment the import above as well.
    # return HttpResponse(translation)

    # We can pass a dictionary here with the data that will be
    # received by the translate page.
    return render(request, 'translate.html', {'original': original, 'translation': translation})
